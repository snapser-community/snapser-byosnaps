export type SuccessResponse = {
  api: string;
  authType: string;
  headerUserId?: string;
  pathUserId: string;
  message: string;
}

export type ErrorResponse = {
  error_message: string;
}

export type JsonRpcId = string | number | null;

export interface JsonRpcRequest {
  jsonrpc?: '2.0';
  id?: JsonRpcId;
  method?: string;
  params?: any; // will show up as "object" in Swagger
}

export interface JsonRpcError {
  code: number;
  message: string;
  data?: any;
}

export interface JsonRpcErrorResponse {
  jsonrpc: '2.0';
  id: JsonRpcId;
  error: JsonRpcError;
}

export interface JsonRpcSuccessResponse {
  jsonrpc: '2.0';
  id: JsonRpcId;
  result: any;
}
