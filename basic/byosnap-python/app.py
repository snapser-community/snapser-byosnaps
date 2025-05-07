'''
Basic Python BYOSnap Example.
'''
import logging

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from functools import wraps


# Constants
# Header Keys
AUTH_TYPE_HEADER_KEY = 'Auth-Type'
GATEWAY_HEADER_KEY = 'Gateway'
USER_ID_HEADER_KEY = 'User-Id'
# Header Values
AUTH_TYPE_HEADER_VALUE_USER_AUTH = 'user'
AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH = 'api-key'
GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE = 'internal'
# ALL Auth Types
ALL_AUTH_TYPES = [AUTH_TYPE_HEADER_VALUE_USER_AUTH,
                  AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE]


# Configure logging to display messages of level DEBUG and above
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# App Initialization
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Decorators


def validate_authorization(*allowed_auth_types, user_id_resource_key="user_id"):
    '''
    Decorator to validate authorization headers
    '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get Gateway Header
            gateway_header_value = request.headers.get(GATEWAY_HEADER_KEY, "")
            is_internal_call = \
                gateway_header_value.lower() == GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE
            # Get Auth Type Header
            auth_type_header_value = request.headers.get(
                AUTH_TYPE_HEADER_KEY, "")
            is_api_key_auth = \
                auth_type_header_value.lower() == AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH
            # Get User Id Header
            user_id_header_value = request.headers.get(USER_ID_HEADER_KEY, "")
            # If the API has a URL parameter for user_id, then use that
            # Otherwise, use the User-Id header value as the default
            target_user = kwargs.get(
                user_id_resource_key, user_id_header_value)
            is_target_user = \
                user_id_header_value == target_user and user_id_header_value != ""

            # Validate
            validation_passed = False
            for auth_type in allowed_auth_types:
                if auth_type == GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE:
                    # If `Auth-Type: Internal`, then the call must be internal
                    if not is_internal_call:
                        # Failed validation
                        continue
                    validation_passed = True
                elif auth_type == AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH:
                    # If `Auth-Type: Api-Key`, and the call is not internal, then the call must be pass the Api-Key validation
                    if not is_internal_call and not is_api_key_auth:
                        # Failed validation
                        continue
                    validation_passed = True
                elif auth_type == AUTH_TYPE_HEADER_VALUE_USER_AUTH:
                    # If `Auth-Type: User`, and the call is not internal or of type api-key auth, then the call must be pass the User validation
                    if not is_internal_call and not is_api_key_auth and not is_target_user:
                        # Failed validation
                        continue
                    validation_passed = True

            # Check if the provided auth_type is within the allowed types for this endpoint
            if not validation_passed:
                return make_response(jsonify({'error_message': 'Unauthorized'}), 400)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# CORS Overrides

# @GOTCHAS 👋 - CORS
#   1. Snapser API Explorer tool runs in the browser. Enabling CORS allows you to access the APIs via the API Explorer.
#


@app.route('/v1/byosnap-basic/users/<user_id>/game', methods=['OPTIONS'])
@app.route('/v1/byosnap-basic/users/<user_id>', methods=['OPTIONS'])
@app.route('/v1/byosnap-basic/users/<user_id>/profile', methods=['OPTIONS'])
@cross_origin()
def cors_overrides(path):
    return f'{path} Ok'

# APIs

# @GOTCHAS 👋 - Health Check Endpoint
#    1. The health URL does not take any URL prefix like other APIs
#


@app.route('/healthz', methods=["GET"])
def health():
    return "Ok"

# @GOTCHAS 👋 - Externally available APIs
#     1. The Snapend Id is NOT part of the URL. This allows you to use the same BYOSnap in multiple Snapends.
#     2. All externally accessible APIs need to start with /$prefix/$byosnapId/remaining_path. where $prefix = v1, $byosnapId = byosnap-basic and remaining_path = /users/<user_id>.
#     3. The YAML comment below is used to generate the swagger.json file.
#     4. Notice the x-snapser-auth-types tags in the swagger.json. They tell Snapser if it should expose this API in
#        the SDK and the API Explorer. Note: but you should still validate the auth type in the code.
#     5. Snapser tech automatically adds the correct header to the SDK and API Explorer. So you do not need to add
#       the headers here in the swagger generation. Eg: For APIs exposed over User Auth, both the SDK
#       and API Explorer will expose the Token header for you to fill in. For Api-Key Auth, the API Explorer will
#       expose the Api-Key header for you to fill in. For internal APIs, the SDK and API Explorer will expose
#       the Gateway header.


@app.route("/v1/byosnap-basic/users/<user_id>/game", methods=["GET"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def get_game(user_id):
    """API that is accessible by User, Api-Key and Internal auth
    ---
    get:
      summary: 'Game APIs'
      description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
      operationId: 'GetGame'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      parameters:
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
        'api': get_game.__name__,
        'auth-type': auth_type_header,
        'header-user-id': user_id_header if user_id_header else 'N/A',
        'path-user-id': user_id,
        'message': 'success',
    }), 200)


@app.route("/v1/byosnap-basic/users/<user_id>/game", methods=["POST"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def save_game(user_id):
    """API that is accessible by Api-Key and Internal auth. User auth will not be allowed. Code does this by checking the Auth-Type header.
    ---
    post:
      summary: 'Game APIs'
      description: This API will work only with Api-Key auth. You can access this API with a valid api-key.
      operationId: 'SaveGame'
      x-snapser-auth-types:
        - api-key
        - internal
      parameters:
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
    auth_type_header = request.headers.get(AUTH_TYPE_HEADER_KEY)
    user_id_header = request.headers.get(USER_ID_HEADER_KEY)
    return make_response(jsonify({
        'api': save_game.__name__,
        'auth-type': auth_type_header,
        'header-user-id': user_id_header if user_id_header else 'N/A',
        'path-user-id': user_id,
        'message': 'success',
    }), 200)


@app.route("/v1/byosnap-basic/users/<user_id>", methods=["DELETE"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def delete_user(user_id):
    """API that is only accessible via Internal auth. Both User Auth calls and Api-Key Auth calls will NOT work, as they are external calls. This is done by checking the Gateway header.
    ---
    delete:
      summary: 'User APIs'
      description: This API will work only when the call is coming from within the Snapend.
      operationId: 'DeleteUser'
      x-snapser-auth-types:
        - internal
      parameters:
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
    gateway_header = request.headers.get(GATEWAY_HEADER_KEY)
    user_id_header = request.headers.get(USER_ID_HEADER_KEY)
    return make_response(jsonify({
        'api': delete_user.__name__,
        'auth-type': gateway_header,
        'header-user-id': user_id_header if user_id_header else 'N/A',
        'path-user-id': user_id,
        'message': 'success',
    }), 200)


@app.route("/v1/byosnap-basic/users/<user_id>/profile", methods=["PUT"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def update_user_profile(user_id):
    """API that is accessible by User, Api-Key and Internal auth
    ---
    put:
      summary: 'User APIs'
      description: This API will work for all auth types.
      operationId: 'UpdateUserProfile'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      parameters:
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
    gateway_header = request.headers.get(GATEWAY_HEADER_KEY)
    user_id_header = request.headers.get(USER_ID_HEADER_KEY)
    return make_response(jsonify({
        'api': update_user_profile.__name__,
        'auth-type': gateway_header,
        'header-user-id': user_id_header if user_id_header else 'N/A',
        'path-user-id': user_id,
        # TODO: Add a message
        'message': 'TODO: Add a message',
    }), 200)

# Uncomment if developing locally
# if __name__ == "__main__":
    # Change debug to True if you are in development
    # app.run(host='0.0.0.0', port=5003, debug=False)
