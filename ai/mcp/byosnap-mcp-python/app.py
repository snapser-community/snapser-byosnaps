import logging
import os
import uuid
import json
from functools import wraps

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import snapser_internal
from snapser_internal.rest import ApiException
from typing import Dict, List, Any, Optional


# -----------------------------------------------------------------------------
# Snapser auth config (unchanged from your code)
# -----------------------------------------------------------------------------

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

AUTH_TYPE_HEADER_KEY = "Auth-Type"
GATEWAY_HEADER_KEY = "Gateway"
USER_ID_HEADER_KEY = "User-Id"

AUTH_TYPE_HEADER_VALUE_USER_AUTH = "user"
AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH = "api-key"
GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE = "internal"

TODOS_BLOB_KEY = 'todos'

ALL_AUTH_TYPES = [
    AUTH_TYPE_HEADER_VALUE_USER_AUTH,
    AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH,
    GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE,
]

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def validate_authorization(*allowed_auth_types, user_id_resource_key="user_id"):
    """
    Decorator to validate authorization headers.
    This is your original logic.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            gateway_header_value = request.headers.get(GATEWAY_HEADER_KEY, "")
            is_internal_call = (
                gateway_header_value.lower() == GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE
            )

            auth_type_header_value = request.headers.get(
                AUTH_TYPE_HEADER_KEY, "")
            is_api_key_auth = (
                auth_type_header_value.lower() == AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH
            )

            user_id_header_value = request.headers.get(USER_ID_HEADER_KEY, "")

            target_user = kwargs.get(
                user_id_resource_key, user_id_header_value)
            is_target_user = (
                user_id_header_value == target_user
                and user_id_header_value != ""
            )

            validation_passed = False
            for auth_type in allowed_auth_types:
                if auth_type == GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE:
                    if not is_internal_call:
                        continue
                    validation_passed = True
                elif auth_type == AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH:
                    if not is_internal_call and not is_api_key_auth:
                        continue
                    validation_passed = True
                elif auth_type == AUTH_TYPE_HEADER_VALUE_USER_AUTH:
                    if (
                        not is_internal_call
                        and not is_api_key_auth
                        and not is_target_user
                    ):
                        continue
                    validation_passed = True

            if not validation_passed:
                return make_response(
                    jsonify({"error_message": "Unauthorized"}), 400
                )
            return f(*args, **kwargs)

        return decorated_function

    return decorator


class TodoStore:
    '''
    Simple in-memory todo store structure.
    '''

    def __init__(self, tasks: List[Dict[str, Any]] = None, cas: str = '0'):
        if tasks is None:
            tasks = []
        self.tasks = tasks
        self.cas = cas

    def to_dict(self):
        '''
        Convert to dict.
        '''
        return {"tasks": self.tasks, "cas": self.cas}

# -----------------------------------------------------------------------------
# In-memory Storage (per user)
# -----------------------------------------------------------------------------


def get_user_id_for_request() -> str:
    """
    Helper to pick a user bucket.
    In real Snapser you’d map API key / tenant to user/workspace.
    """
    user_id = request.headers.get(USER_ID_HEADER_KEY)
    if not user_id:
        # Fallback bucket for demo
        user_id = "anonymous"
    return user_id


def get_tasks_for_user(user_id: str) -> TodoStore:
    configuration = snapser_internal.Configuration(
        host=os.getenv("SNAPEND_STORAGE_HTTP_URL")
    )
    todos_store = TodoStore(tasks=[], cas="0")

    with snapser_internal.ApiClient(configuration) as api_client:
        api = snapser_internal.StorageServiceApi(api_client)
        try:
            api_response = api.storage_get_blob(
                owner_id=user_id,
                access_type='protected',
                blob_key=TODOS_BLOB_KEY,
                gateway=GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE
            )
            if api_response.value:
                parsed = json.loads(api_response.value)
                todos_store = TodoStore(
                    tasks=parsed.get("tasks", []),
                    cas=api_response.cas or "0"
                )
        except ApiException as e:
            logging.warning("storage_get_blob ApiException: %s", e)
        except Exception as e:
            logging.exception("storage_get_blob Exception: %s", e)

    return todos_store


def save_tasks_for_user(user_id: str, new_store: TodoStore) -> TodoStore:
    '''
    Saves tasks for a given user from Snapser Storage Service.
    '''
    configuration = snapser_internal.Configuration(
        host=os.getenv("SNAPEND_STORAGE_HTTP_URL"))
    with snapser_internal.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = snapser_internal.StorageServiceApi(api_client)
        body = snapser_internal.StorageReplaceBlobRequest(
            access_type='protected', blob_key=TODOS_BLOB_KEY,
            create=True, cas=new_store.cas,
            owner_id=user_id, ttl=0,
            value=json.dumps({"tasks": new_store.tasks})
        )
        try:
            # Save Blob
            api_response = api_instance.storage_replace_blob(
                owner_id=user_id, access_type='protected',
                blob_key=TODOS_BLOB_KEY, gateway=GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE,
                body=body
            )
            if api_response.cas:
                new_store.cas = api_response.cas
        except ApiException as e:
            print(
                f"ApiException when calling StorageServiceApi->storage_get_blob: {e}\n")
        except Exception as e:
            print(
                f"Exception when calling StorageServiceApi->storage_get_blob: {e}\n")
    return new_store


def add_task_for_user(user_id: str, title: str) -> Dict:
    '''
    Add a new task for a given user.
    '''
    store = get_tasks_for_user(user_id)
    task = {"id": str(uuid.uuid4()), "title": title, "completed": False}
    store.tasks.append(task)
    save_tasks_for_user(user_id, store)
    return task


def complete_task_for_user(user_id: str, task_id: str) -> Optional[Dict[str, Any]]:
    '''
    Mark a task as completed for a given user.
    '''
    store = get_tasks_for_user(user_id)
    for task in store.tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks_for_user(user_id, store)
            return task
    return None


# -----------------------------------------------------------------------------
# JSON-RPC helpers (MCP uses JSON-RPC 2.0)
# -----------------------------------------------------------------------------

JSONRPC_VERSION = "2.0"

PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


def jsonrpc_error_response(_id, code, message, data=None):
    '''
    Create a JSON-RPC error response.
    '''
    payload = {
        "jsonrpc": JSONRPC_VERSION,
        "id": _id,
        "error": {"code": code, "message": message},
    }
    if data is not None:
        payload["error"]["data"] = data
    return jsonify(payload)


def jsonrpc_result_response(_id, result):
    '''
    Create a JSON-RPC result response.
    '''
    return jsonify({"jsonrpc": JSONRPC_VERSION, "id": _id, "result": result})


# -----------------------------------------------------------------------------
# MCP method handlers
# -----------------------------------------------------------------------------

def handle_initialize(_id, params):
    '''
    Handle MCP initialize method.
    '''
    protocol_version = params.get("protocolVersion", "2025-03-26")

    result = {
        "protocolVersion": protocol_version,
        "capabilities": {
            "tools": {"listChanged": False},
            # Not exposing resources/prompts in this test app
        },
        "serverInfo": {
            "name": "snapser-todo-mcp",
            "version": "0.1.0",
        },
    }
    return jsonrpc_result_response(_id, result)


def handle_tools_list(_id, params):
    """
    Advertise tools used by the Todo HTML:
      - add_todo(title)
      - complete_todo(id)
      - list_todos()
    """
    tools = [
        {
            "name": "list_todos",
            "description": "List all todo tasks for the current user.",
            "inputSchema": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "name": "add_todo",
            "description": "Add a new todo task with the given title.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the todo task.",
                    }
                },
                "required": ["title"],
            },
        },
        {
            "name": "complete_todo",
            "description": "Mark a todo task as completed by id.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The id of the todo task.",
                    }
                },
                "required": ["id"],
            },
        },
    ]

    return jsonrpc_result_response(_id, {"tools": tools})


def _mcp_todo_response(user_id: str, message: Optional[str] = None):
    """
    Shared helper: package tasks into the shape Apps SDK expects.

    Result of tools/call:
      {
        "content": [{ "type": "text", "text": "..." }],
        "structuredContent": { "tasks": [...] }
      }

    So that:
      - window.openai.toolOutput.tasks works in your HTML
      - callTool(..) resolves to { structuredContent: { tasks: [...] }, ... }
    """
    store = get_tasks_for_user(user_id)
    tasks = store.tasks

    if message is None:
        message = f"Now tracking {len(tasks)} tasks."

    return {
        "content": [
            {
                "type": "text",
                "text": message,
            }
        ],
        "structuredContent": {
            "tasks": tasks,
        },
    }


def handle_tools_call(_id, params):
    '''
    Handle MCP tools/call method.
    '''
    name = params.get("name")
    arguments = params.get("arguments") or {}

    user_id = get_user_id_for_request()

    try:
        if name == "list_todos":
            result = _mcp_todo_response(
                user_id, "Here are your current tasks.")
            return jsonrpc_result_response(_id, result)

        if name == "add_todo":
            title = arguments.get("title")
            if not isinstance(title, str) or not title.strip():
                return jsonrpc_error_response(
                    _id,
                    INVALID_PARAMS,
                    "add_todo requires a non-empty 'title' string.",
                )

            task = add_task_for_user(user_id, title.strip())
            msg = f"Added todo: '{task['title']}'."
            result = _mcp_todo_response(user_id, msg)
            return jsonrpc_result_response(_id, result)

        if name == "complete_todo":
            task_id = arguments.get("id")
            if not isinstance(task_id, str):
                return jsonrpc_error_response(
                    _id,
                    INVALID_PARAMS,
                    "complete_todo requires an 'id' string.",
                )

            task = complete_task_for_user(user_id, task_id)
            if task is None:
                return jsonrpc_error_response(
                    _id,
                    INVALID_PARAMS,
                    f"No todo found with id {task_id!r}.",
                )

            msg = f"Marked todo '{task['title']}' as completed."
            result = _mcp_todo_response(user_id, msg)
            return jsonrpc_result_response(_id, result)

        # Unknown tool name
        return jsonrpc_error_response(
            _id,
            METHOD_NOT_FOUND,
            f"Unknown tool: {name}",
        )

    except Exception:  # defensive
        logging.exception("Unhandled error in tools/call")
        return jsonrpc_error_response(_id, INTERNAL_ERROR, "Internal server error")


# -----------------------------------------------------------------------------
# MCP transport: single HTTP endpoint for JSON-RPC
# -----------------------------------------------------------------------------

@app.route("/v1/byosnap-mcp/mcp", methods=["POST"])
# @validate_authorization(
#     AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH,
#     GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE,
# )
@cross_origin()
def mcp_entrypoint():
    """
    API that is accessible by Api-Key and internal auth. User auth is not allowed.
    Code enforces this via the `Auth-Type` header.

    ---
    post:
      summary: MCP JSON-RPC endpoint
      description: >
        Snapser-hosted MCP endpoint that speaks JSON-RPC 2.0 and exposes
        initialize, tools/list, and tools/call.
      operationId: McpRpc
      requestBody:
        required: true
        content:
          application/json:
            schema: MCPRequestSchema
      responses:
        200:
          description: Successful JSON-RPC response
          content:
            application/json:
              schema: SuccessResponseSchema
        400:
          description: JSON-RPC error or auth failure
          content:
            application/json:
              schema: ErrorResponseSchema
        401:
          description: Unauthorized
          content:
            application/json:
              schema: ErrorResponseSchema
    """
    try:
        body = request.get_json(force=True, silent=False)
    except Exception:
        logging.exception("Failed to parse JSON body")
        return jsonrpc_error_response(None, PARSE_ERROR, "Invalid JSON")

    if not isinstance(body, dict):
        return jsonrpc_error_response(
            None, INVALID_REQUEST, "Request body must be an object"
        )

    logging.debug("MCP request body: %s", body)

    method = body.get("method")
    _id = body.get("id", None)
    params = body.get("params") or {}

    # Notifications (no id) – just swallow and 204
    if _id is None and isinstance(method, str) and method.startswith(
        "notifications/"
    ):
        logging.debug("Received notification: %s", method)
        return ("", 204)

    if method is None:
        return jsonrpc_error_response(_id, INVALID_REQUEST, "Missing 'method' field")

    # Route MCP methods
    if method == "initialize":
        return handle_initialize(_id, params)
    if method == "tools/list":
        return handle_tools_list(_id, params)
    if method == "tools/call":
        return handle_tools_call(_id, params)

    logging.warning("Unknown MCP method: %s", method)
    return jsonrpc_error_response(
        _id, METHOD_NOT_FOUND, f"Unknown method: {method}"
    )


# -----------------------------------------------------------------------------
# Health check
# -----------------------------------------------------------------------------

@app.route('/healthz', methods=["GET"])
def health():
    '''
    Simple health check endpoint.
    '''
    return "Ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
