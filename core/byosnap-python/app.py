'''
Core Python BYOSnap Example — minimal starter scaffold.

This is the recommended starting point for a new Python BYOSnap. Every endpoint
Snapser expects is present, but each handler body is a STUB: it returns a simple
placeholder and carries a `# TODO` describing what you would implement here.

Fill in the stubs with your own logic. When you need to persist data, call other
Snaps, or wire up the configuration/import-export tooling, look at the matching
handler in `advanced/byosnap-python/app.py` for a complete, working reference.

The boilerplate that is already wired up for you (and should usually stay as-is):
  - The `BYOSNAP_ID` / `API_PREFIX` constants that build every route prefix
  - The `validate_authorization` decorator (User / Api-Key / Internal auth checks)
  - The `/healthz` readiness endpoint
  - The CORS override route
  - The swagger `---` doc-comments that drive SDK + API Explorer generation

The five example endpoints at the bottom show how to expose an API over each
Snapser auth type (User, Api-Key, Internal), an endpoint that accepts all three
together (you do NOT need a separate route per auth type), and one endpoint that
surfaces in the special Admin SDK. Use them as templates for your own logic.
'''
import logging
import os
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from functools import wraps
# The generated Snapser server SDK ships in this project for internal
# Snap-to-Snap calls (e.g. reading/writing the Storage Snap). It is left
# commented out because the stubs below don't use it yet — uncomment when you
# start implementing real logic. See advanced/byosnap-python for usage.
# import snapser_internal
# from snapser_internal.rest import ApiException


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

# BYOSnap Identity
# BYOSNAP_ID is the URL segment Snapser uses to route to this Snap. Every
# externally reachable route is prefixed with API_PREFIX. Change BYOSNAP_ID in
# one place instead of editing every route string.
BYOSNAP_ID = "byosnap-core"
API_PREFIX = f"/v1/{BYOSNAP_ID}"


# Configure logging to display messages of level DEBUG and above
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# App Initialization
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Decorators


def validate_authorization(*allowed_auth_types, user_id_resource_key="user_id"):
    '''
    Decorator to validate authorization headers.

    Pass the auth types this endpoint should accept (any of
    AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH,
    GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE). Snapser injects the relevant headers;
    this decorator enforces them so you get authorization checks for free.

    Note on Admin-SDK APIs: `admin` is NOT an auth type. Guard admin endpoints
    with their real auth types (e.g. api-key + internal) and surface them in the
    Admin SDK by adding the `x-snapser-sdk-categories: [admin]` tag to the swagger
    operation.
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

@app.route(f"{API_PREFIX}/users/<user_id>/example", methods=['OPTIONS'])
@cross_origin()
def cors_overrides(user_id):
    '''
    CORS Overrides
    '''
    return f'{user_id} Ok'

# APIs

# @GOTCHAS 👋 - Health Check Endpoint
#    1. The health URL does not take any URL prefix like other APIs
#


@app.route('/healthz', methods=["GET"])
def health():
    '''
    Health Check Endpoint
    '''
    return "Ok"

# @GOTCHAS 👋 - Externally available APIs
#     1. The Snapend Id is NOT part of the URL. This allows you to use the same BYOSnap in multiple Snapends.
#     2. All externally accessible APIs need to start with /$prefix/$byosnapId/remaining_path. where $prefix = v1, $byosnapId = byosnap-core and remaining_path = /users/<user_id>. Here that prefix is built from API_PREFIX.
#     3. The YAML comment below is used to generate the swagger.json file.
#     4. Notice the x-snapser-auth-types tags in the swagger.json. They tell Snapser if it should expose this API in
#        the SDK and the API Explorer. Note: but you should still validate the auth type in the code.
#     5. Snapser tech automatically adds the correct header to the SDK and API Explorer. So you do not need to add
#       the headers here in the swagger generation. Eg: For APIs exposed over User Auth, both the SDK
#       and API Explorer will expose the Token header for you to fill in. For Api-Key Auth, the API Explorer will
#       expose the Api-Key header for you to fill in. For internal APIs, the SDK and API Explorer will expose
#       the Gateway header.

# A i]: Configuration Tool: Built using the Snapser UI Builder


@app.route(f"{API_PREFIX}/settings", methods=["GET"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def get_settings():
    """Get the settings for this Snap's Configuration Tool.

    Snapser always sends `tool_id` and `environment` as query params so you can
    scope the settings blob per environment (dev / stage / prod).
    ---
    get:
      summary: 'Configuration Tool'
      description: Get the settings for the Configuration Tool.
      operationId: Get Settings
      x-snapser-auth-types:
        - internal
      x-snapser-sdk-categories: [admin]
      responses:
        200:
          content:
            application/json:
              schema: SettingsSchema
          description: 'Settings retrieved successfully'
    """
    # This is the default payload shape the Configuration Tool expects.
    default_settings = {
        "sections": [
            {
                "id": "registration",
                "components": [
                    {
                        "id": "characters",
                        "type": "textarea",
                        "value": ""
                    }
                ]
            }
        ]
    }
    tool_id = request.args.get('tool_id')
    environment = request.args.get('environment', default='DEFAULT')
    _blob_owner_key = f"{tool_id}_{environment}"
    # TODO: Fetch the saved settings for `_blob_owner_key` (e.g. from the Storage
    #       Snap via snapser_internal) and return them. For now we return the
    #       default. See advanced/byosnap-python for the full Storage read.
    return make_response(jsonify(default_settings), 200)


@app.route(f"{API_PREFIX}/settings", methods=["PUT"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def update_settings():
    """Update the settings for this Snap's Configuration Tool.
    ---
    put:
      summary: 'Update Settings'
      description: Put
      operationId: Update Settings
      x-snapser-auth-types:
        - internal
      x-snapser-sdk-categories: [admin]
      requestBody:
        required: true
        content:
            application/json:
              schema: SettingsSchema
        description: 'Settings payload'
      responses:
        200:
          content:
            application/json:
              schema: SuccessMessageSchema
          description: 'Settings updated successfully'
        400:
            content:
                application/json:
                    schema: ErrorResponseSchema
            description: 'Error updating settings'
        500:
            content:
                application/json:
                    schema: ErrorResponseSchema
            description: 'Server Exception'
    """
    try:
        tool_id = request.args.get('tool_id')
        environment = request.args.get('environment', default='DEFAULT')
        _blob_owner_key = f"{tool_id}_{environment}"
        blob_data = request.get_json()
        if 'payload' in blob_data:
            blob_data = blob_data['payload']
        # TODO: Validate `blob_data` and persist it for `_blob_owner_key`
        #       (e.g. via the Storage Snap). On a validation failure return
        #       make_response(jsonify({'error_message': '...'}), 400).
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Invalid JSON ' + str(e)
        }), 500)

# End: Configuration Tool: Built using the Snapser UI Builder

# A ii]: New Configuration Tool: Custom HTML Snap Configuration Tool


@app.route(f"{API_PREFIX}/settings/custom", methods=["GET"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def get_settings_custom():
    """Get the settings for a custom HTML Configuration Tool.
    ---
    get:
      summary: 'Custom Configuration Tool'
      description: Get the settings for the custom HTML Configuration Tool.
      operationId: Get Settings Custom
      x-snapser-auth-types:
        - internal
      x-snapser-sdk-categories: [admin]
      responses:
        200:
          content:
            application/json:
              schema: SuccessMessageSchema
          description: 'Settings retrieved successfully'
    """
    # The custom HTML tool expects the settings wrapped in a `payload` key.
    default_settings = {"payload": ""}
    tool_id = request.args.get('tool_id')
    environment = request.args.get('environment', default='DEFAULT')
    _blob_owner_key = f"{tool_id}_{environment}"
    # TODO: Fetch the saved settings for `_blob_owner_key` and return them
    #       wrapped as {"payload": <settings>}. See advanced/byosnap-python.
    return make_response(jsonify(default_settings), 200)


@app.route(f"{API_PREFIX}/settings/custom", methods=["PUT"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def update_settings_custom():
    """Update the settings for a custom HTML Configuration Tool.
    ---
    put:
      summary: 'Custom Configuration Tool'
      description: Update the settings for the custom HTML Configuration Tool.
      operationId: Update Settings Custom
      x-snapser-auth-types:
        - internal
      x-snapser-sdk-categories: [admin]
      requestBody:
        required: true
        content:
            application/json:
              schema: SettingsSchema
        description: 'Settings payload'
      responses:
        200:
          content:
            application/json:
              schema: SuccessMessageSchema
          description: 'Settings updated successfully'
        500:
            content:
                application/json:
                    schema: ErrorResponseSchema
            description: 'Server Exception'
    """
    try:
        tool_id = request.args.get('tool_id')
        environment = request.args.get('environment', default='DEFAULT')
        _blob_owner_key = f"{tool_id}_{environment}"
        blob_data = request.get_json()
        if 'payload' in blob_data:
            blob_data = blob_data['payload']
        # TODO: Validate `blob_data` and persist it for `_blob_owner_key`.
        #       On a validation failure return a 400 with an error_message.
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Invalid JSON ' + str(e)
        }), 500)

# End: Configuration Tool: Custom HTML Snap Configuration Tool

# A iii]: User Manager Tool: Custom HTML User Manager Tool


@app.route(f"{API_PREFIX}/settings/users/<user_id>/custom", methods=["GET"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def get_user_data_custom(user_id):
    '''
    Get a user's data for the custom HTML User Manager Tool.
    '''
    # TODO: Look up this user's data (e.g. from the Storage Snap) and return it
    #       wrapped as {"payload": <data>}. See advanced/byosnap-python.
    return make_response(jsonify({"payload": ""}), 200)


@app.route(f"{API_PREFIX}/settings/users/<user_id>/custom", methods=["POST"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def update_user_data_custom(user_id):
    '''
    Update a user's data for the custom HTML User Manager Tool.
    '''
    try:
        blob_data = request.get_json()
        if 'payload' in blob_data:
            blob_data = blob_data['payload']
        # TODO: Validate `blob_data` and persist it for this user_id.
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Invalid JSON ' + str(e)
        }), 500)
    return make_response(jsonify({'success': True}), 200)

# End: User Manager Tool: Custom HTML User Manager Tool

# B: Snapend Sync|Clone: Used by Snapser's built-in configuration import export system


@app.route(f"{API_PREFIX}/settings/export", methods=["GET"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def settings_export():
    """Export Settings
    ---
    get:
      summary: 'Export Settings'
      description: Export Settings
      operationId: Export Settings
      x-snapser-auth-types:
        - internal
      responses:
        200:
          content:
            application/json:
              schema: ExportSettingsSchema
          description: 'Settings retrieved successfully'
    """
    # Snapser calls this when cloning/syncing a Snapend. Return your settings for
    # every environment so they can be re-imported elsewhere.
    empty_tool_payload = {
        "sections": [
            {
                "id": "registration",
                "components": [
                    {"id": "characters", "type": "textarea", "value": ""}
                ]
            }
        ]
    }
    response = {
        "version": os.environ.get('BYOSNAP_VERSION', "v1.0.0"),
        "exported_at": 0,
        "data": {
            # The key here ("characters") is the Tool ID whose payload you export.
            "dev": {"characters": empty_tool_payload},
            "stage": {"characters": empty_tool_payload},
            "prod": {"characters": empty_tool_payload},
        }
    }
    # TODO: Load the real saved settings per environment (e.g. batch-get from the
    #       Storage Snap) and merge them into `response['data']`. See
    #       advanced/byosnap-python for the full implementation.
    return make_response(jsonify(response), 200)


@app.route(f"{API_PREFIX}/settings/import", methods=["POST"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def settings_import():
    """Import Settings
    ---
    post:
      summary: 'Import Settings'
      description: Import Settings
      operationId: Import Settings
      x-snapser-auth-types:
        - internal
      requestBody:
        required: true
        content:
            application/json:
              schema: ExportSettingsSchema
        description: 'ExportSettingsSchema payload'
      responses:
        200:
          content:
            application/json:
              schema: SuccessMessageSchema
          description: 'SettingsSchema saved successfully'
        201:
          content:
            application/json:
              schema: SuccessMessageSchema
          description: 'SettingsSchema created successfully'
        400:
            content:
                application/json:
                    schema: ErrorResponseSchema
            description: 'Error saving settings'
        500:
            content:
                application/json:
                    schema: ErrorResponseSchema
            description: 'Server Exception'
    """
    try:
        settings_data = request.get_json()
        # TODO: Validate the incoming export payload and persist each
        #       environment's settings (e.g. batch-replace on the Storage Snap).
        #       See advanced/byosnap-python for validation + Storage writes.
        if not settings_data:
            return make_response(jsonify({'error_message': 'Invalid JSON'}), 500)
        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Server Exception' + str(e)
        }), 500)


@app.route(f"{API_PREFIX}/settings/validate-import", methods=["POST"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def validate_settings():
    '''
    Validate an incoming settings payload before an import.

    Snapser sends the settings it is about to import. Decide whether you can
    accept them: return 200 with the payload if so, or 500 with an error_message
    if not.
    '''
    settings_data = request.get_json()
    # TODO: Add your own validation here. See advanced/byosnap-python for an
    #       example that checks the dev/stage/prod structure.
    if not settings_data:
        return make_response(jsonify({'error_message': 'Invalid JSON'}), 500)
    return make_response(jsonify(settings_data), 200)


# End: Snapend Sync|Clone: Used by Snapser's built-in configuration import export system

# C: User Tool: Get, Update and Delete User data: Used by the GDPR tool and the User Manager tool

@app.route(f"{API_PREFIX}/settings/users/<user_id>/data", methods=["GET"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def get_user_data(user_id):
    '''
    Get a user's data. Used by the GDPR tool and the User Manager tool.
    '''
    # TODO: Fetch and return everything you store for this user_id. See
    #       advanced/byosnap-python for the Storage read.
    return make_response(jsonify({}), 200)


@app.route(f"{API_PREFIX}/settings/users/<user_id>/data", methods=["PUT"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def update_user_data(user_id):
    '''
    Update a user's data. Used by the User Manager tool.
    '''
    # TODO: Persist the incoming data for this user_id.
    return make_response(jsonify({}), 200)


@app.route(f"{API_PREFIX}/settings/users/<user_id>/data", methods=["DELETE"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def delete_user_data(user_id):
    '''
    Delete a user's data. Used by the GDPR tool to honor deletion requests.
    '''
    # TODO: Delete everything you store for this user_id. See
    #       advanced/byosnap-python for the Storage delete.
    return make_response(jsonify({}), 200)

# End: User Tool: Delete and Reset User data

# =========================================================================
# Regular API Endpoints — your Snap's business logic lives here.
#
# The stubs below demonstrate each Snapser auth exposure. The
# `x-snapser-auth-types` tag in the swagger block controls which SDK / tool the
# API surfaces in, and the matching `@validate_authorization(...)` enforces it
# at runtime. Add, rename, or remove these to fit your Snap.
#
# A single endpoint can accept MULTIPLE auth types at once (see the last
# example) — you do not need a separate route per auth type.
# =========================================================================


@app.route(f"{API_PREFIX}/users/<user_id>/example", methods=["GET"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, user_id_resource_key="user_id")
def example_user_endpoint(user_id):
    """Example endpoint exposed over User auth.
    ---
    get:
      summary: 'Example: User Auth'
      description: 'Accessible by a logged-in user, validated against the User-Id in their token. Surfaces in the client/game SDK.'
      operationId: ExampleUserAuth
      x-snapser-auth-types:
        - user
      parameters:
      - in: path
        schema: UserIdParameterSchema
      responses:
        200:
          content:
            application/json:
              schema: SuccessMessageSchema
          description: 'Success'
    """
    # TODO: Add your user-scoped business logic here.
    return make_response(jsonify({'message': f'Hello user {user_id}'}), 200)


@app.route(f"{API_PREFIX}/example/api-key", methods=["GET"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH)
def example_api_key_endpoint():
    """Example endpoint exposed over Api-Key auth.
    ---
    get:
      summary: 'Example: Api-Key Auth'
      description: 'Accessible with a valid API key. Use for trusted server-to-server calls.'
      operationId: ExampleApiKeyAuth
      x-snapser-auth-types:
        - api-key
      responses:
        200:
          content:
            application/json:
              schema: SuccessMessageSchema
          description: 'Success'
    """
    # TODO: Add your api-key-scoped business logic here.
    return make_response(jsonify({'message': 'Hello api-key caller'}), 200)


@app.route(f"{API_PREFIX}/example/internal", methods=["GET"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def example_internal_endpoint():
    """Example endpoint exposed over Internal auth.
    ---
    get:
      summary: 'Example: Internal Auth'
      description: 'Callable only by other Snaps within the same Snapend (internal gateway). Surfaces in the internal SDK.'
      operationId: ExampleInternalAuth
      x-snapser-auth-types:
        - internal
      responses:
        200:
          content:
            application/json:
              schema: SuccessMessageSchema
          description: 'Success'
    """
    # TODO: Add your internal-only business logic here.
    return make_response(jsonify({'message': 'Hello internal caller'}), 200)


@app.route(f"{API_PREFIX}/example/admin", methods=["GET"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def example_admin_endpoint():
    """Example endpoint surfaced in the special Admin SDK.

    Note: `admin` is NOT an auth type. The endpoint is exposed over normal auth
    types (here api-key + internal); the `x-snapser-sdk-categories: [admin]` tag is
    what places it in the Admin SDK (used by admin tooling / the Snapser
    dashboard).
    ---
    get:
      summary: 'Example: Admin SDK'
      description: 'Exposed over api-key + internal auth and surfaced in the Admin SDK via x-snapser-sdk-categories.'
      operationId: ExampleAdminSdk
      x-snapser-auth-types:
        - api-key
        - internal
      x-snapser-sdk-categories: [admin]
      responses:
        200:
          content:
            application/json:
              schema: SuccessMessageSchema
          description: 'Success'
    """
    # This endpoint is reachable via api-key or internal auth (enforced by the
    # decorator). The `x-snapser-sdk-categories: [admin]` tag above is what surfaces
    # it in the Admin SDK.
    # TODO: Add your admin business logic here.
    return make_response(jsonify({'message': 'Hello admin caller'}), 200)


@app.route(f"{API_PREFIX}/users/<user_id>/example/multi-auth", methods=["GET"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH,
                        GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def example_multi_auth_endpoint(user_id):
    """Example endpoint that accepts multiple auth types on ONE route.
    ---
    get:
      summary: 'Example: Multi Auth'
      description: 'One endpoint reachable by a logged-in user, a valid API key, or an internal Snap. List every auth type you want to allow — no need for a separate route per type.'
      operationId: ExampleMultiAuth
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
              schema: SuccessMessageSchema
          description: 'Success'
    """
    # Pass every accepted auth type to both the swagger tag (for SDK exposure)
    # and the @validate_authorization decorator (for runtime enforcement).
    # TODO: Add your business logic here.
    return make_response(jsonify({'message': f'Hello, request for user {user_id} passed multi-auth'}), 200)


# Uncomment if developing locally
# if __name__ == "__main__":
    # Change debug to True if you are in development
    # app.run(host='0.0.0.0', port=5003, debug=False)
