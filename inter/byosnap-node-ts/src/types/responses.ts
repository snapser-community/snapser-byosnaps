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
