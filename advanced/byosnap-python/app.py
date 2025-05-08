'''
Intermediate Python BYOSnap Example.
'''
import logging
import os
import json
import time
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from functools import wraps
import snapser_internal
from snapser_internal.rest import ApiException


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

@app.route('/v1/byosnap-advanced/users/<user_id>/characters/<character_id>/active', methods=['OPTIONS'])
@cross_origin()
def cors_overrides(path):
    '''
    CORS Overrides
    '''
    return f'{path} Ok'

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
#     2. All externally accessible APIs need to start with /$prefix/$byosnapId/remaining_path. where $prefix = v1, $byosnapId = byosnap-inter and remaining_path = /users/<user_id>.
#     3. The YAML comment below is used to generate the swagger.json file.
#     4. Notice the x-snapser-auth-types tags in the swagger.json. They tell Snapser if it should expose this API in
#        the SDK and the API Explorer. Note: but you should still validate the auth type in the code.
#     5. Snapser tech automatically adds the correct header to the SDK and API Explorer. So you do not need to add
#       the headers here in the swagger generation. Eg: For APIs exposed over User Auth, both the SDK
#       and API Explorer will expose the Token header for you to fill in. For Api-Key Auth, the API Explorer will
#       expose the Api-Key header for you to fill in. For internal APIs, the SDK and API Explorer will expose
#       the Gateway header.

# A: Configuration Tool: Used by the Snap Configuration Tool


@app.route("/v1/byosnap-advanced/settings", methods=["GET"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def get_settings():
    '''
    Get the settings for the characters microservice
    '''
    # This is coming from the Payload we got in the Configuration tool
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
    # Get settings call always includes the tool_id and environment
    tool_id = request.args.get('tool_id')
    environment = request.args.get('environment', default='DEFAULT')
    blob_owner_key = f"{tool_id}_{environment}"
    # Make an internal call to Storage to get the settings
    configuration = snapser_internal.Configuration()
    with snapser_internal.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = snapser_internal.StorageServiceApi(api_client)
        try:
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id=blob_owner_key,
                gateway=os.environ.get('SNAPEND_INTERNAL_HEADER', 'internal')
            )
            if api_response is None:
                return make_response(jsonify(default_settings), 200)
            return make_response(jsonify(json.loads(api_response.value)), 200)
        except ApiException as e:
            pass
    return make_response(jsonify(default_settings), 200)

   # return make_response(jsonify(), 200)


@app.route("/v1/byosnap-advanced/settings", methods=["PUT"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def update_settings():
    '''
    Update the settings for the characters microservice
    '''
    try:
        # Update settings call always includes the tool_id and environment
        tool_id = request.args.get('tool_id')
        environment = request.args.get('environment', default='DEFAULT')
        blob_owner_key = f"{tool_id}_{environment}"
        blob_data = request.get_json()
        if 'payload' in blob_data:
            blob_data = blob_data['payload']
        # TODO: Add any custom validation here and on error send back `return make_response(jsonify({'error_message': 'Duplicate characters found'}), 400)``
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Invalid JSON ' + str(e)
        }), 500)

    configuration = snapser_internal.Configuration()
    with snapser_internal.ApiClient(configuration=configuration) as api_client:
        cas = '12345'
        # Create an instance of the API class
        api_instance = snapser_internal.StorageServiceApi(api_client)
        try:
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id=blob_owner_key,
                gateway=os.environ.get('SNAPEND_INTERNAL_HEADER', 'internal')
            )
            if api_response is not None:
                cas = api_response.cas
        except ApiException:
            # You come here when the doc is not even present
            pass
        try:
            api_response = api_instance.storage_internal_replace_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id=blob_owner_key,
                gateway=os.environ['SNAPEND_INTERNAL_HEADER'],
                body={
                    "value": json.dumps(blob_data),
                    "ttl": 0,
                    "create": True,
                    "cas": cas
                }
            )
            if api_response is None:
                return make_response(jsonify({
                    'error_message': 'Server Error'
                }), 500)
            return make_response(jsonify(blob_data), 200)
        except ApiException as e:
            return make_response(jsonify({
                'error_message': 'Server Exception: ' + str(e)
            }), 500)

# End: Configuration Tool: Used by the Snap Configuration Tool

# B: Snapend Sync|Clone: Used by Snapser's built-in configuration import export system


@app.route("/v1/byosnap-advanced/settings/export", methods=["GET"])
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
    response = {
        "version": os.environ.get('BYOSNAP_VERSION', "v1.0.0"),
        "exported_at": int(time.time()),
        "data": {
            "dev": {
                "characters": {  # This is the Tool ID which has the tool Payload inside
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
            },
            "stage": {
                "characters": {  # This is the Tool ID which has the tool Payload inside
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
            },
            "prod": {
                "characters": {  # This is the Tool ID which has the tool Payload inside
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
            }
        }
    }
    characters_tool_id = 'characters'
    # Remember when storing these blobs we are storing them with `characters_dev`, `characters_stage` and `characters_prod` as the blob_key
    blob_key_ids = [characters_tool_id + '_' +
                    environment for environment in ['dev', 'stage', 'prod']]
    configuration = snapser_internal.Configuration()
    with snapser_internal.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = snapser_internal.StorageServiceApi(api_client)
        try:
            # Storage Settings
            api_response = api_instance.storage_internal_batch_get_blobs(
                access_type='private',
                blob_key='character_settings',
                owner_id=blob_key_ids,
                gateway=os.environ.get(
                    'SNAPEND_INTERNAL_HEADER', 'internal')
            )
            if api_response is None:
                return make_response(jsonify(response), 200)
            for result in api_response.results:
                if result.success and result.response.owner_id == blob_key_ids[0] and \
                        result.response.value is not None and result.response.value != "":
                    # Load the dev data
                    response['data']['dev']['characters'] = json.loads(
                        result.response.value)
                elif result.success and result.response.owner_id == blob_key_ids[1] and \
                        result.response.value is not None and result.response.value != "":
                    # Load the stage data
                    response['data']['stage']['characters'] = json.loads(
                        result.response.value)
                elif result.success and result.response.owner_id == blob_key_ids[2] and \
                        result.response.value is not None and result.response.value != "":
                    # Load the prod data
                    response['data']['prod']['characters'] = json.loads(
                        result.response.value)
            return make_response(jsonify(response), 200)
        except ApiException as e:
            return make_response(jsonify({
                'error_message': 'API Exception' + str(e)
            }), 500)
    return make_response(jsonify(response), 200)


@app.route("/v1/byosnap-advanced/settings/import", methods=["POST"])
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
        # This is coming from the Settings Hook
        response = {
            "version": os.environ.get('BYOSNAP_VERSION', "v1.0.0"),
            "exported_at": int(time.time()),
            "data": {
                "dev": {
                    "characters": {  # This is the Tool ID which has the tool Payload inside
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
                },
                "stage": {
                    "characters": {  # This is the Tool ID which has the tool Payload inside
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
                },
                "prod": {
                    "characters": {  # This is the Tool ID which has the tool Payload inside
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
                }
            }
        }

        settings_data = request.get_json()
        if not settings_data or 'data' not in settings_data or 'dev' not in settings_data['data'] or \
            'stage' not in settings_data['data'] or 'prod' not in settings_data['data'] or \
                'characters' not in settings_data['data']['dev'] or \
            'characters' not in settings_data['data']['stage'] or \
                'characters' not in settings_data['data']['prod']:
            return make_response(jsonify({
                'error_message': 'Invalid JSON'
            }), 500)
        characters_tool_id = 'characters'
        blob_dev = {
            "value": json.dumps(settings_data['data']['dev']['characters']),
            "ttl": 0,
            "owner_id": f"{characters_tool_id}_dev",
            "create": True,
            "cas": "0",  # This forces a replace. Remember in settings we are replacing the blob; but its upto you if you want to merge
            "blob_key": "character_settings",
            "access_type": "private"
        }
        blob_stage = {
            "value": json.dumps(settings_data['data']['stage']['characters']),
            "ttl": 0,
            "owner_id": f"{characters_tool_id}_stage",
            "create": True,
            "cas": "0",  # This forces a replace. Remember in settings we are replacing the blob; but its upto you if you want to merge
            "blob_key": "character_settings",
            "access_type": "private"
        }
        blob_prod = {
            "value": json.dumps(settings_data['data']['prod']['characters']),
            "ttl": 0,
            "owner_id": f"{characters_tool_id}_prod",
            "create": True,
            "cas": "0",  # This forces a replace. Remember in settings we are replacing the blob; but its upto you if you want to merge
            "blob_key": "character_settings",
            "access_type": "private"
        }
        payload = {'blobs': [blob_dev, blob_stage, blob_prod]}
        # Save the characters to the storage
        configuration = snapser_internal.Configuration()
        with snapser_internal.ApiClient(configuration=configuration) as api_client:
            # Create an instance of the API class
            api_instance = snapser_internal.StorageServiceApi(api_client)
            try:
                api_response = api_instance.storage_internal_batch_replace_blob(
                    gateway=os.environ['SNAPEND_INTERNAL_HEADER'],
                    body=payload,
                )
                if api_response is None:
                    return make_response(jsonify({
                        'error_message': 'Server Error'
                    }), 500)
                return make_response({'message': 'Success'}, 200)
            except ApiException as e:
                return make_response(jsonify({
                    'error_message': 'Server Exception: ' + str(e)
                }), 500)
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Server Exception' + str(e)
        }), 500)


@app.route("/v1/byosnap-advanced/settings/validate-import", methods=["POST"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def validate_settings():
    '''
    Validate Settings - Think of this as, Snapser is sending you what the settings are going to be
    1. You need to validate if you are capable of accepting this settings
    2. If you are not, then return a 500 with the error message
    3. If you are, then return a 200 with the settings
    '''
    settings_data = request.get_json()
    # We are performing basic validation here. You can add more validation if you want by fetching the
    # settings from the storage and comparing it with the incoming settings
    if not settings_data or 'data' not in settings_data or 'dev' not in settings_data['data'] or \
        'stage' not in settings_data['data'] or 'prod' not in settings_data['data'] or \
            'characters' not in settings_data['data']['dev'] or \
        'characters' not in settings_data['data']['stage'] or \
            'characters' not in settings_data['data']['prod']:
        return make_response(jsonify({
            'error_message': 'Invalid JSON'
        }), 500)
    return make_response(jsonify(settings_data), 200)


# End: Snapend Sync|Clone: Used by Snapser's built-in configuration import export system

# C: User Tool: Delete and Reset User data


@app.route("/v1/byosnap-advanced/settings/users/<user_id>/data", methods=["DELETE"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def delete_user_data(user_id):
    '''
    Delete User Data
    '''
    gateway = request.headers.get('Gateway')
    if not gateway or gateway.lower() != 'internal':
        return make_response(jsonify({
            'error_message': 'Unauthorized'
        }), 401)
    # Delete the character blob from storage
    configuration = snapser_internal.Configuration()
    with snapser_internal.ApiClient(configuration=configuration) as storage_api_client:
        storage_api_instance = snapser_internal.StorageServiceApi(
            storage_api_client)
        try:
            # Get blob
            storage_api_response = storage_api_instance.storage_internal_delete_blob(
                access_type='private',
                blob_key='characters',
                owner_id=user_id,
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if storage_api_response is None:
                return make_response(jsonify({
                    'error_message': 'No blob'
                }), 400)
        except ApiException:
            pass
    return make_response(jsonify({}), 200)

# End: User Tool: Delete and Reset User data

# Regular API Endpoints exposed by the Snap


@app.route("/v1/byosnap-advanced/users/<user_id>/characters/active", methods=["GET"])
def check_active_characters(user_id):
    """Get Active Characters for a User.
    ---
    get:
      summary: 'Character APIs'
      description: Get
      operationId: Get Active Characters
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
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
    """
    return make_response(jsonify({'characters': []}), 200)


# End: SYSTEM: Used by the Snap Configuration Tool
# Uncomment if developing locally
# if __name__ == "__main__":
    # Change debug to True if you are in development
    # app.run(host='0.0.0.0', port=5003, debug=False)
