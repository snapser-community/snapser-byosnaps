# Gotchas
What to Watch Out For When Working in This Repo

## Endpoints
- The Snapend Id is NOT part of the URL. This allows you to use the same BYOSnap in multiple Snapends.
```go
// swagger:operation GET /v1/byosnap-basic/users/{user_id}/game apiOne (👈 No Snapend Id in the URL)
```
- All externally accessible APIs need to start with /$prefix/$byosnapId/remaining_path. where $prefix = v1, $byosnapId = byosnap-python-basic and remaining_path = /users/<user_id>.
```go
// swagger:operation GET /v1/byosnap-basic/users/{user_id}/game apiOne (👈 Check the URL format)
```
- Notice the `x-snapser-auth-types` tags in the endpoint annotations and swagger.json. They tell Snapser if it should expose this API in the SDK and the API Explorer. Note: but you should still validate the auth type in the code.
```go
// ApiOneHandler handles the GET request for an API endpoint
// swagger:operation GET /v1/byosnap-basic/users/{user_id}/game apiOne
// ---
// summary: Retrieves game data for a specified user
// description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
// operationId: apiOneHandler
// x-snapser-auth-types: ["user", "api-key", "internal"] (👈 This controls the x-snapser-auth-types tags in the swagger)
```

IMPORTANT: But you also have to pass those auth types to the middleware so that you get Authorization checks for free. Just adding those tags for swagger, are not going to do the authorization check for you.
```go
apiOneHandler := http.HandlerFunc(ApiOneHandler)
r.Handle("/v1/byosnap-basic/users/{user_id}/game", validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(apiOneHandler)).Methods("GET") // (👈 This tells the middleware that user auth, app auth and internal auth are allowed)
```
- Snapser tech automatically adds the correct header to the SDK and API Explorer for your API. So you do not need to add the headers here against your API. Eg: For APIs exposed over User Auth, both the SDK and API Explorer will expose the Token header for you to fill in. For Api-Key Auth, the API Explorer will expose the Api-Key header for you to fill in. For internal APIs, the SDK and API Explorer will expose the Gateway header.
```go
// ApiOneHandler handles the GET request for an API endpoint
// swagger:operation GET /v1/byosnap-basic/users/{user_id}/game apiOne
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
- We use go-swagger to convert annotations to swagger.json. But go-swagger only supports 2.X. Snapser is built on the swagger 3.x platform, so we use openApi to convert the 2.x swagger to 3.x. Swagger generation also has some gotchas. Please see the section below.

## Swagger generation
- This repo uses ApiSpec and MarshmallowPlugin to convert flask controller annotations to a Swagger. There are a few gotchas that you need to be aware of.
- In order to keep the API and Swagger generation code separate, you have a `generate_swagger.py` file that handles the generation of the swagger.
- If you add a new API, register them in `generate_swagger.py`. You have to do this at two places
```python
# Register your endpoints
app.add_url_rule('/v1/byosnap-basic/users/<user_id>/game',
                 view_func=api_one, methods=['GET']) # (👈 #1 Add the rule)

# Generate paths using the FlaskPlugin
with app.test_request_context():
    spec.path(view=api_one) # (👈 #1 Add the path)
```
- If you add any new Schemas make sure you register them here
```python
spec.components.schema("UserIdParameterSchema", schema=UserIdParameterSchema)
```

- Then, in your main code, every API needs to have an annotation like this. Check all the gotcha callouts below
```python
"""API that is accessible by User, Api-Key and Internal auth (👈 This is just for you. The ApiSpec does not use this)
    ---
    get:
      summary: 'API One' (👈 [Required] Give any short name)
      description: This API will work with User and Api-Key auth. With a valid user token and api-key,you can access this API. (👈 [Required] Give any verbose description)
      operationId: 'API One' (👈 [Required] Powers the API Name in the SDK and the Api Explorer)
      x-snapser-auth-types: (👈 [Required] So Snapser shows or hides this API in the SDK and API Explorer)
        - user
        - api-key
        - internal
      parameters: (👈 [Required] No need to add any Token or Api-Key headers. Snapser handles this)
      - in: path
        schema: UserIdParameterSchema
      responses:
        200:
          content:
            application/json:
              schema: SuccessResponseSchema
          description: 'A successful response'
        400:
          content:
            application/json:
              schema: ErrorResponseSchema
          description: 'Unauthorized'
        401:
          content:
            application/json:
               schema: ErrorResponseSchema
          description: 'Unauthorized'
    """
```

-