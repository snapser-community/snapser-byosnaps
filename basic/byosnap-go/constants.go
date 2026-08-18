package main

const (
	AuthTypeHeaderKey                = "Auth-Type"
	AuthTypeHeaderValueUserAuth      = "user"
	AuthTypeHeaderValueApiKeyAuth    = "api-key"
	GatewayHeaderKey                 = "Gateway"
	GatewayHeaderValueInternalOrigin = "internal"
	UserIDHeaderKey                  = "User-Id"
	// RequestIDHeaderKey carries the Snapser request id on every inbound request
	// (gRPC metadata uses the lowercase `x-request-id`).
	RequestIDHeaderKey = "X-Request-Id"
)
