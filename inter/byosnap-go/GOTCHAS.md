# Gotchas
What to Watch Out For When Working in This Repo

## Endpoints
- The Snapend Id is NOT part of the URL. This allows you to use the same BYOSnap in multiple Snapends.
```go
// swagger:operation GET /v1/byosnap-inter/users/{user_id}/game apiOne (👈 No Snapend Id in the URL)
```
- All externally accessible APIs need to start with /$prefix/$byosnapId/remaining_path. where $prefix = v1, $byosnapId = byosnap-inter and remaining_path = /users/<user_id>.
```go
// swagger:operation GET /v1/byosnap-inter/users/{user_id}/game apiOne (👈 Check the URL format)
```
- Notice the `x-snapser-auth-types` tags in the endpoint annotations and swagger.json. They tell Snapser if it should expose this API in the SDK and the API Explorer. Note: but you should still validate the auth type in the code.
```go
// ApiOneHandler handles the GET request for an API endpoint
// swagger:operation GET /v1/byosnap-inter/users/{user_id}/game apiOne
// ---
// summary: Retrieves game data for a specified user
// description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
// operationId: apiOneHandler
// x-snapser-auth-types: ["user", "api-key", "internal"] (👈 This controls the x-snapser-auth-types tags in the swagger)
```

IMPORTANT: But you also have to pass those auth types to the middleware so that you get Authorization checks for free. Just adding those tags for swagger, are not going to do the authorization check for you.
```go
apiOneHandler := http.HandlerFunc(ApiOneHandler)
r.Handle("/v1/byosnap-inter/users/{user_id}/game", validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(apiOneHandler)).Methods("GET") // (👈 This tells the middleware that user auth, app auth and internal auth are allowed)
```
- Snapser tech automatically adds the correct header to the SDK and API Explorer for your API. So you do not need to add the headers here against your API. Eg: For APIs exposed over User Auth, both the SDK and API Explorer will expose the Token header for you to fill in. For Api-Key Auth, the API Explorer will expose the Api-Key header for you to fill in. For internal APIs, the SDK and API Explorer will expose the Gateway header.
```go
// ApiOneHandler handles the GET request for an API endpoint
// swagger:operation GET /v1/byosnap-inter/users/{user_id}/game apiOne
// ---
// summary: Retrieves game data for a specified user
// description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
// operationId: apiOneHandler
// x-snapser-auth-types: ["user", "api-key", "internal"]
// parameters: (👈 No headers added to params)
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
// responses:
//   200:
//     description: Successfully retrieved data
//     schema:
//       $ref: '#/definitions/SuccessResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ApiOneHandler(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	response := SuccessResponseSchema{
		API:          "ApiOneHandler",
		AuthType:     authType,
		HeaderUserID: userIdHeader,
		PathUserID:   mux.Vars(r)["user_id"],
		Message:      "success",
	}

	// Marshal the struct to JSON
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		http.Error(w, "Error creating response", http.StatusInternalServerError)
		return
	}

	// Set the content type and write the response
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonResponse)
}
```
- The health endpoint does not have to contain the prefix. It should just be available at the root level.
```go
// Health Check Endpoint
r.HandleFunc("/healthz", HealthCheckHandler).Methods("GET")
```
- We use go-swagger to convert annotations to swagger.json. But **go-swagger** only supports 2.X. Snapser is built on the swagger 3.x platform, so we use openApi to convert the 2.x swagger to 3.x. Swagger generation also has some gotchas. Please see the section below.

## Logging
- Write one JSON object per line to stdout with `level` (`debug`/`info`/`warn`/`error`), `message`
  and `timestamp`. Snapser reads `level` to color the line in the Logs tool. See `logging.go`.
- Every inbound request carries an `X-Request-Id` header. The `requestLogging` middleware binds it
  once per request, and handlers call `requestLogger(r)` so every line carries a `request-id` field.
```go
r.Use(requestLogging) // (👈 binds X-Request-Id once, in main.go)
requestLogger(r).Info("Get game", slog.String("user_id", userID)) // (👈 line carries request-id)
```
- The field name must be `request-id` (kebab-case). Snapser correlates the lines of one request
  across Snaps by this field and samples logs per request, not per line.
- Snap-to-Snap calls must forward `X-Request-Id` so downstream logs correlate. The generated
  `snapser_internal` client has no per-call header option, so `requestIDForwarder` (a
  `http.RoundTripper` set on `config.HTTPClient`) adds the header from the context you pass to the
  client. Pass `r.Context()` to every call.

## Swagger generation
- This repo uses **go-swagger** and method annotations to create a Swagger. There are a few gotchas that you need to be aware of.
- The comment at the top of the main.go file is what generates the **info** object in the swagger.
```go
// Package main BYOSnap Intermediate Go Example
//
// BYOSnap Intermediate Go Example
// with restful endpoints
//
//		Schemes: https
//	  Host: localhost:5003
//		Version: 1.0.0
//		License: Apache 2.0 http://www.apache.org/licenses/LICENSE-2.0.html
//		Contact:
//		  Name: Snapser Admin
//		  URL: https://snapser.com
//		  Email: admin@snapser.com
//
//		Consumes:
//		- application/json
//
//		Produces:
//		- application/json
//
// swagger:meta
package main

import (
	"encoding/json"
  ...
)
```
- Every API needs to have an annotation like this. Check all the gotcha callouts below
```go
// ApiOneHandler handles the GET request for an API endpoint
// swagger:operation GET /v1/byosnap-inter/users/{user_id}/game apiOne (👈 This is just for you. The ApiSpec does not use this)
// ---
// summary: Retrieves game data for a specified user (👈 required: Add a short summary about the API)
// description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API. (👈 required: Add a verbose description about the API)
// operationId: apiOneHandler (👈 required: This is what gets converted to the method name in the SDK and API Explorer)
// x-snapser-auth-types: ["user", "api-key", "internal"] (👈 required: Tells the SDK and API explorer if you want to see this API in the user, api-key and internal SDKs and API Explorer tabs)
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
// responses:
//   200:
//     description: Successfully retrieved data
//     schema:
//       $ref: '#/definitions/SuccessResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ApiOneHandler(w http.ResponseWriter, r *http.Request) {
  ...
}
```
