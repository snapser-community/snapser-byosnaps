import crypto from 'crypto';
import { ErrorResponse, SuccessResponse } from '../types/responses';
import { Request as ExpressRequest } from 'express';
import {
  Controller,
  Route,
  Post,
  Put,
  Delete,
  Extension,
  Body,
  Middlewares,
  TsoaResponse,
  Response,
  Res,
  Request,
  Path,
} from 'tsoa';
import { Todo } from '../types/app';
import { JsonRpcId, JsonRpcRequest, JsonRpcErrorResponse, JsonRpcSuccessResponse, JsonRpcError } from '../types/responses';
import { ReplaceBlobRequest, StorageGetBlobRequest, StorageGetBlobResponse, StorageReplaceBlobResponse, StorageServiceApi } from '../snapser-internal/api';

// # @GOTCHAS 👋 - Please read GOTCHAS.md


// MCP error codes
const PARSE_ERROR = -32700;
const INVALID_REQUEST = -32600;
const METHOD_NOT_FOUND = -32601;
const INVALID_PARAMS = -32602;
const INTERNAL_ERROR = -32603;

// -----------------------------------------------------------------------------
// In-memory TODO storage (per user)
// -----------------------------------------------------------------------------

const tasksByUserId: Record<string, Todo[]> = {};

type TodoStore = {
  todos: Todo[];
  cas: string;
}

function getUserIdForRequest(req: ExpressRequest, pathUserId?: string): string {
  // Prefer explicit header, fall back to path param, then to "anonymous"
  const headerUserId = req.header('User-Id');
  if (headerUserId && headerUserId.trim() !== '') {
    return headerUserId.trim();
  }
  if (pathUserId && pathUserId.trim() !== '') {
    return pathUserId.trim();
  }
  return 'anonymous';
}

async function getTasksForUser(userId: string): Promise<TodoStore> {
  const baseUrl = process.env.SNAPEND_STORAGE_HTTP_URL ?? 'http://storage-service:8090';
  const storageApi = new StorageServiceApi(baseUrl);

  let todos: Todo[] = [];
  let cas = '';

  try {
    const result = await storageApi.storageGetBlob(userId, 'protected', 'todos', 'internal');
    const body: StorageGetBlobResponse = result.body;

    cas = body.cas ?? ''; // IMPORTANT: keep the CAS from storage

    if (body.value) {
      const tasksObject = JSON.parse(body.value);
      todos = Array.isArray(tasksObject.todos) ? tasksObject.todos : [];
    }
  } catch (error: any) {
    // If the SDK exposes status code, handle 404 specially:
    const status = error?.status || error?.statusCode || error?.response?.status;

    if (status === 404) {
      // No blob yet -> start fresh, no CAS
      console.info(`No todo blob for user ${userId} yet, starting empty.`);
      return { todos: [], cas: '' };
    }

    console.error('Error fetching todos from storage blob:', error);
    // Let caller turn this into a JSON-RPC error instead of pretending it worked
    throw error;
  }

  return { todos, cas };
}

async function saveTasksForUser(userId: string, store: TodoStore): Promise<TodoStore> {
  const baseUrl = process.env.SNAPEND_STORAGE_HTTP_URL ?? 'http://storage-service:8090';
  const storageApi = new StorageServiceApi(baseUrl);

  const payload: ReplaceBlobRequest = {
    cas: store.cas,        // '' for create, actual CAS for updates
    create: true,
    ttl: 0,
    value: JSON.stringify({ todos: store.todos }),
  };

  const result = await storageApi.storageReplaceBlob(
    userId,
    'protected',
    'todos',
    'internal',
    payload,
  );

  const body: StorageReplaceBlobResponse = result.body;

  return {
    todos: store.todos,
    cas: body.cas ?? '',
  };
}


async function addTaskForUser(userId: string, title: string): Promise<Todo> {
  let currentStore: TodoStore = await getTasksForUser(userId);
  const id = crypto.randomUUID();
  const task: Todo = { id, title, completed: false };
  currentStore.todos.push(task);
  const updated = await saveTasksForUser(userId, currentStore);
  return task;
}

async function completeTaskForUser(userId: string, taskId: string): Promise<Todo | undefined> {
  let currentStore: TodoStore = await getTasksForUser(userId);
  const task = currentStore.todos.find((t) => t.id === taskId);
  if (task) {
    task.completed = true;
  }
  const updated = await saveTasksForUser(userId, currentStore);
  return task;
}

/**
 * Build a standard MCP tool result for the todo tools:
 *
 * {
 *   content: [{ type: "text", text: "..." }],
 *   structuredContent: { tasks: [...] }
 * }
 */
async function buildMcpTodoResult(userId: string, message?: string) {

  const currentStore: TodoStore = await getTasksForUser(userId);
  const todos = currentStore.todos;
  const text =
    message ?? (currentStore.todos.length === 0 ? 'You have no tasks.' : `You have ${currentStore.todos.length} tasks.`);
  return {
    content: [
      {
        type: 'text',
        text,
      },
    ],
    structuredContent: {
      tasks: todos,
    },
  };
}

// -----------------------------------------------------------------------------
// JSON-RPC helpers
// -----------------------------------------------------------------------------

function jsonRpcError(id: JsonRpcId, code: number, message: string, data?: any): JsonRpcErrorResponse {
  const error: JsonRpcError = { code, message };
  if (data !== undefined) {
    error.data = data;
  }
  return {
    jsonrpc: '2.0',
    id,
    error,
  };
}

function jsonRpcResult(id: JsonRpcId, result: any): JsonRpcSuccessResponse {
  return {
    jsonrpc: '2.0',
    id,
    result,
  };
}

// -----------------------------------------------------------------------------
// MCP handlers (initialize, tools/list, tools/call)
// -----------------------------------------------------------------------------

function handleInitialize(id: JsonRpcId, params: any): JsonRpcSuccessResponse {
  const protocolVersion = params?.protocolVersion ?? '2025-03-26';
  return jsonRpcResult(id, {
    protocolVersion,
    capabilities: {
      tools: { listChanged: false },
      // no resources or prompts in this test controller
    },
    serverInfo: {
      name: 'snapser-todo-mcp',
      version: '0.1.0',
    },
  });
}

function handleToolsList(id: JsonRpcId, params: any): JsonRpcSuccessResponse {
  const tools = [
    {
      name: 'list_todos',
      description: 'List all todo tasks for the current user.',
      inputSchema: {
        type: 'object',
        properties: {},
      },
    },
    {
      name: 'add_todo',
      description: 'Add a new todo task with the given title.',
      inputSchema: {
        type: 'object',
        properties: {
          title: {
            type: 'string',
            description: 'The title of the todo task.',
          },
        },
        required: ['title'],
      },
    },
    {
      name: 'complete_todo',
      description: 'Mark a todo task as completed by id.',
      inputSchema: {
        type: 'object',
        properties: {
          id: {
            type: 'string',
            description: 'The id of the todo task.',
          },
        },
        required: ['id'],
      },
    },
  ];

  return jsonRpcResult(id, { tools });
}

// async function handleToolsCall(
//   id: JsonRpcId,
//   params: any,
//   req: ExpressRequest,
//   pathUserId?: string,
// ): Promise<JsonRpcSuccessResponse | JsonRpcErrorResponse> {
//   const name: string | undefined = params?.name;
//   const args: any = params?.arguments ?? {};
//   const userId = getUserIdForRequest(req, pathUserId);

//   if (!name) {
//     return jsonRpcError(id, INVALID_PARAMS, "Missing 'name' in tools/call params.");
//   }

//   try {
//     if (name === 'list_todos') {
//       const result = await buildMcpTodoResult(userId, 'Here are your current tasks.');
//       return jsonRpcResult(id, result);
//     }
//     else if (name === 'add_todo') {
//       const title = args.title;
//       if (typeof title !== 'string' || !title.trim()) {
//         return jsonRpcError(id, INVALID_PARAMS, "add_todo requires a non-empty 'title' string.");
//       }
//       await addTaskForUser(userId, title.trim()).then((task) => {
//         const result = buildMcpTodoResult(userId, `Added todo: '${task.title}'.`);
//         return jsonRpcResult(id, result);
//       });
//     }
//     else if (name === 'complete_todo') {
//       const taskId = args.id;
//       if (typeof taskId !== 'string' || !taskId.trim()) {
//         return jsonRpcError(id, INVALID_PARAMS, "complete_todo requires an 'id' string.");
//       }
//       await completeTaskForUser(userId, taskId.trim()).then((task) => {
//         if (!task) {
//           return jsonRpcError(id, INVALID_PARAMS, `No todo found with id '${taskId}'.`);
//         }
//         const result = buildMcpTodoResult(userId, `Marked todo '${task.title}' as completed.`);
//         return jsonRpcResult(id, result);
//       });
//     } else {
//       return jsonRpcError(id, METHOD_NOT_FOUND, `Unknown tool: ${name}`);
//     }
//   } catch (err: any) {
//     console.error('Unhandled error in tools/call', err);
//     return jsonRpcError(id, INTERNAL_ERROR, 'Internal server error');
//   }
// }

// -----------------------------------------------------------------------------
// Controller
// -----------------------------------------------------------------------------

async function handleToolsCall(
  id: JsonRpcId,
  params: any,
  req: ExpressRequest,
  pathUserId?: string,
): Promise<JsonRpcSuccessResponse | JsonRpcErrorResponse> {
  const name: string | undefined = params?.name;
  const args: any = params?.arguments ?? {};
  const userId = getUserIdForRequest(req, pathUserId);

  if (!name) {
    return jsonRpcError(id, INVALID_PARAMS, "Missing 'name' in tools/call params.");
  }

  try {
    if (name === 'list_todos') {
      const result = await buildMcpTodoResult(userId, 'Here are your current tasks.');
      return jsonRpcResult(id, result);
    }

    if (name === 'add_todo') {
      const title = args.title;
      if (typeof title !== 'string' || !title.trim()) {
        return jsonRpcError(id, INVALID_PARAMS, "add_todo requires a non-empty 'title' string.");
      }

      const task = await addTaskForUser(userId, title.trim());
      const result = await buildMcpTodoResult(userId, `Added todo: '${task.title}'.`);
      return jsonRpcResult(id, result);
    }

    if (name === 'complete_todo') {
      const taskId = args.id;
      if (typeof taskId !== 'string' || !taskId.trim()) {
        return jsonRpcError(id, INVALID_PARAMS, "complete_todo requires an 'id' string.");
      }

      const task = await completeTaskForUser(userId, taskId.trim());
      if (!task) {
        return jsonRpcError(id, INVALID_PARAMS, `No todo found with id '${taskId}'.`);
      }

      const result = await buildMcpTodoResult(userId, `Marked todo '${task.title}' as completed.`);
      return jsonRpcResult(id, result);
    }

    return jsonRpcError(id, METHOD_NOT_FOUND, `Unknown tool: ${name}`);
  } catch (err: any) {
    console.error('Unhandled error in tools/call', err);
    return jsonRpcError(id, INTERNAL_ERROR, 'Internal server error');
  }
}

@Route('/v1/byosnap-mcp')
export class McpController extends Controller {
  /**
   * @summary MCP Endpoint
   */
  @Post('mcp')
  @Extension('x-description', 'MCP Endpoint to demonstrate BYOSnap MCP functionality.')
  // @Extension("x-snapser-auth-types", ["api-key", "internal"])
  @Response<JsonRpcSuccessResponse | JsonRpcErrorResponse>(200, 'Successful Response')
  @Response<ErrorResponse>(401, 'Unauthorized')
  // @Middlewares([authMiddleware(["api-key", "internal"])])
  public async handleMcp(
    @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
    // Optional: if you decide to include {userId} in the route path later
    // @Path() userId: string,
    @Body() body: JsonRpcRequest,
    @Request() req: ExpressRequest,
  ): Promise<JsonRpcSuccessResponse | JsonRpcErrorResponse> {
    const expressReq = req as ExpressRequest;

    // If you want to enforce auth here via middleware, uncomment the @Middlewares above.
    // For now we just parse JSON-RPC and respond.

    // let body: JsonRpcRequest;
    // try {
    //   body = expressReq.body as JsonRpcRequest;
    // } catch (err) {
    //   console.error('Failed to parse JSON body', err);
    //   this.setStatus(400);
    //   return jsonRpcError(null, PARSE_ERROR, 'Invalid JSON');
    // }

    if (!body || typeof body !== 'object') {
      this.setStatus(400);
      return jsonRpcError(null, INVALID_REQUEST, 'Request body must be an object.');
    }

    const { method, id = null, params = {} } = body;

    // Notifications: no id, method "notifications/..." -> no response body
    if (id === null && typeof method === 'string' && method.startsWith('notifications/')) {
      this.setStatus(204);
      return {} as any;
    }

    if (!method) {
      this.setStatus(400);
      return jsonRpcError(id, INVALID_REQUEST, "Missing 'method' field");
    }

    // Route MCP methods
    if (method === 'initialize') {
      return handleInitialize(id, params);
    }

    if (method === 'tools/list') {
      return handleToolsList(id, params);
    }

    if (method === 'tools/call') {
      return await handleToolsCall(id, params, expressReq);
    }

    this.setStatus(400);
    return jsonRpcError(id, METHOD_NOT_FOUND, `Unknown method: ${method}`);
  }
}
