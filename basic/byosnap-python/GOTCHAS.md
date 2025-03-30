# Gotchas
What to Watch Out For When Working in This Repo

## Endpoints
- The Snapend Id is NOT part of the URL. This allows you to use the same BYOSnap in multiple Snapends.
```python
@app.route("/v1/byosnap-python-basic/users/<user_id>/game", methods=["GET"])
```
- All externally accessible APIs need to start with /$prefix/$byosnapId/remaining_path. where $prefix = v1, $byosnapId = byosnap-python-basic and remaining_path = /users/<user_id>.
```python
@app.route("/v1/byosnap-python-basic/users/<user_id>/game", methods=["GET"])
```
- Notice the `x-snapser-auth-types` tags in the endpoint annotations and swagger.json. They tell Snapser if it should expose this API in the SDK and the API Explorer. Note: but you should still validate the auth type in the code.
```python
@app.route("/v1/byosnap-python-basic/users/<user_id>/game", methods=["GET"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def api_one(user_id):
    """API that is accessible by User, Api-Key and Internal auth
    ---
    get:
      summary: 'API One'
      description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
      operationId: 'API One'
      x-snapser-auth-types: (👈 This)
        - user
        - api-key
        - internal
```
- Snapser tech automatically adds the correct header to the SDK and API Explorer for your API. So you do not need to add the headers here against your API. Eg: For APIs exposed over User Auth, both the SDK and API Explorer will expose the Token header for you to fill in. For Api-Key Auth, the API Explorer will expose the Api-Key header for you to fill in. For internal APIs, the SDK and API Explorer will expose the Gateway header.
```python
@app.route("/v1/byosnap-python-basic/users/<user_id>/game", methods=["GET"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def api_one(user_id):
    """API that is accessible by User, Api-Key and Internal auth
    ---
    get:
      summary: 'API One'
      description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
      operationId: 'API One'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      parameters: (👈 No headers added to params)
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
    # Note: Authorization checks are done in the decorator
    auth_type_header = request.headers.get(AUTH_TYPE_HEADER_KEY)
    user_id_header = request.headers.get(USER_ID_HEADER_KEY)
    # Success state
    return make_response(jsonify({
        'api': api_one.__name__,
        'auth-type': auth_type_header,
        'header-user-id': user_id_header if user_id_header else 'N/A',
        'path-user-id': user_id,
        'message': 'success',
    }), 200)
```
- The health endpoint does not have to contain the prefix. It should just be available at the root level.
```python
@app.route('/healthz', methods=["GET"]) # (👈 No prefix or BYOSnap Id)
def health():
    return "Ok"
```
- We use ApiSpec to convert annotations to swagger.json. The swagger.json is used by Snapser to generate the SDK and power the API Explorer. Swagger generation also has some gotchas. Please see the section below.

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