import os
import json
import time
import logging

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from flask import Flask, request, make_response, jsonify, send_file
from flask_cors import CORS, cross_origin
import snapser
from snapser.rest import ApiException


class TokenHeaderSchema(Schema):
    Token = fields.Str(required=True)


class UserIdParameter(Schema):
    user_id = fields.Str()


class CharacterIdParameter(Schema):
    character_id = fields.Str()


class SuccessResponseSchema(Schema):
    success_message = fields.Str()


class ErrorResponseSchema(Schema):
    error_message = fields.Str()


class CharacterSchema(Schema):
    id = fields.String(required=True)
    session_token = fields.String(required=True)
    refreshed_at = fields.String(required=True)
    token_validity_seconds = fields.String(required=True)


class CharactersResponseSchema(Schema):
    characters = fields.Dict(
        keys=fields.Str(), values=fields.Nested(CharacterSchema))


spec = APISpec(
    title="BYOSnap Characters API",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(
        description="Microservice to manage characters in a game",
        version="1.0.0-oas3",
        contact=dict(
          email="tech@snapser.com"
        ),
        license=dict(
            name="Apache 2.0",
            url='http://www.apache.org/licenses/LICENSE-2.0.html'
        )
    ),
    servers=[
        # dict(
        #     description="Test server",
        #     url="https://resources.donofden.com"
        #     )
    ],
    tags=[
        dict(
            name="BYOSnap Characters API",
            description="Microservice to manage characters in a game"
        )
    ],
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("ErrorResponseSchema", schema=ErrorResponseSchema)
spec.components.schema("CharactersResponseSchema",
                       schema=CharactersResponseSchema)

API_SPEC_FILENAME = 'swagger.json'
MARKDOWN_FILENAME = 'README.md'

# Configure logging to display messages of level DEBUG and above
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Extensions initialization
# =========================
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/v1/byosnap-characters/openapispec', methods=["OPTIONS"])
@app.route('/v1/byosnap-characters/markdown', methods=["OPTIONS"])
# @app.route('/v1/byosnap-characters/settings', methods=["OPTIONS"])
# @app.route("/v1/byosnap-characters/settings/export", methods=["OPTIONS"])
# @app.route("/v1/byosnap-characters/settings/import", methods=["OPTIONS"])
@app.route('/v1/byosnap-characters/health', methods=["OPTIONS"])
@app.route('/v1/byosnap-characters/users/<user_id>/characters', methods=['OPTIONS'])
@app.route('/v1/byosnap-characters/users/<user_id>/characters/<character_id>/activate', methods=['OPTIONS'])
@cross_origin()
def cors_overrides(path):
    return f'{path} Ok'

# https://gateway.snapser.com/$clusterId/v1/byosnap-characters

# SYSTEM: Used by Snapser's API Explorer and Configuration tool


@app.route('/v1/byosnap-characters/openapispec', methods=["GET"])
def api_spec():
    try:
        directory = os.getcwd()
        return send_file(directory + '/' + API_SPEC_FILENAME)
    except Exception as e:
        return str(e)


@app.route('/v1/byosnap-characters/markdown', methods=["GET"])
def markdown_docs():
    try:
        directory = os.getcwd()
        return send_file(directory + '/' + MARKDOWN_FILENAME)
    except Exception as e:
        return str(e)
# END: SYSTEM: Used by Snapser's API Explorer and Configuration tool


@app.route('/healthz', methods=["GET"])
def health():
    return "Ok Health Check"

# SYSTEM: Used by Snapser's built-in configuration import export system


@app.route("/v1/byosnap-characters/settings/export", methods=["GET"])
def settings_export():
    """Export Settings
    ---
    get:
      summary: 'Export Settings'
      description: Export Settings
      operationId: Export Settings
      parameters:
      - in: header
        schema: TokenHeaderSchema
      responses:
        200:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
        201:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
    """
    response = {
        "version": os.environ['BYOSNAP_VERSION'],
        "exported_at": int(time.time()),
        "data": {
            "character_settings": {
                "version": "v1.0.0",
                "id": "characters",
                "endpoint": "",
                "category": "flat_form",
                "env_support": "single",
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
    configuration = snapser.Configuration(
        host=os.environ['SNAPEND_STORAGE_HTTP_URL']
    )
    with snapser.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = snapser.StorageServiceApi(api_client)
        try:
            # Storage Settings
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if api_response is None:
                return make_response(jsonify(response), 200)
            response['data']['character_settings'] = json.loads(
                api_response.value)
            return make_response(jsonify(response), 200)
        except ApiException as e:
            pass
    return make_response(jsonify(response), 200)


@app.route("/v1/byosnap-characters/settings/import", methods=["POST"])
def settings_import():
    """Import Settings
    ---
    post:
      summary: 'Import Settings'
      description: Import Settings
      operationId: Import Settings
      parameters:
      - in: header
        schema: TokenHeaderSchema
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    character_settings:
                      type: object
                      properties:
                        version:
                          type: string
                        id:
                          type: string
                        endpoint:
                          type: string
                        category:
                          type: string
                        env_support:
                          type: string
                        sections:
                          type: array
                          items:
                            type: object
                            properties:
                              id:
                                type: string
                              components:
                                type: array
                                items:
                                  type: object
                                  properties:
                                    id:
                                      type: string
                                    type:
                                      type: string
                                    value:
                                      type: string
      responses:
        200:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
        201:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
    """
    try:
        settings_data = request.get_json()
        if not settings_data or 'data' not in settings_data:
            return make_response(jsonify({
                'error_message': 'Invalid JSON'
            }), 500)
        settings = settings_data['data']['character_settings']
        # Split the characters by comma but also trim the characters
        character_list = settings['sections'][0]['components'][0]['value'].split(
            ',')
        character_list = [character.strip() for character in character_list]
        # Check for duplicates
        if len(character_list) != len(set(character_list)):
            return make_response(jsonify({
                'error_message': 'Duplicate characters found'
            }), 400)
        # Save the characters to the storage
        configuration = snapser.Configuration(
            host=os.environ['SNAPEND_STORAGE_HTTP_URL']
        )
        with snapser.ApiClient(configuration=configuration) as api_client:
            cas = '12345'
            # Create an instance of the API class
            api_instance = snapser.StorageServiceApi(api_client)
            try:
                # Get Storage CAS
                api_response = api_instance.storage_internal_get_blob(
                    access_type='private',
                    blob_key='character_settings',
                    owner_id='byosnap_characters',
                    gateway=os.environ['SNAPEND_INTERNAL_HEADER']
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
                    owner_id='byosnap_characters',
                    gateway=os.environ['SNAPEND_INTERNAL_HEADER'],
                    body={
                        "value": json.dumps(settings),
                        "ttl": 0,
                        "create": True,
                        "cas": cas
                    }
                )
                if api_response is None:
                    return make_response(jsonify({
                        'error_message': 'Server Error'
                    }), 500)
                return make_response(jsonify(settings), 200)
            except ApiException as e:
                return make_response(jsonify({
                    'error_message': 'Server Exception: ' + str(e)
                }), 500)
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Server Exception' + str(e)
        }), 500)


@app.route("/v1/byosnap-characters/settings/validate-import", methods=["POST"])
def validate_settings():
    settings_data = request.get_json()
    if 'data' not in settings_data:
        return make_response(jsonify({
            'error_message': 'Invalid JSON'
        }), 500)
    settings = settings_data['data']['character_settings']
    # Split the characters by comma but also trim the characters
    character_list = settings['sections'][0]['components'][0]['value'].split(
        ',')
    character_list = [character.strip() for character in character_list]
    # Check for duplicates
    if len(character_list) != len(set(character_list)):
        return make_response(jsonify({
            'error_message': 'Duplicate characters found'
        }), 400)
    response = {
        'version': os.environ['BYOSNAP_VERSION'],
        'exported_at': int(time.time()),
        'data': {'character_settings':
                 # This part is generated by the BYOSnap Tool builder. We are storing it as is into storage
                 {
                     "version": "v1.0.0",
                     "id": "characters",
                     "endpoint": "",
                     "category": "flat_form",
                     "env_support": "single",
                     "sections": [
                         {
                             "id": "registration",
                             "components": [
                                 {
                                     "id": "characters",
                                     "type": "textarea",
                                     "value": settings['sections'][0]['components'][0]['value']
                                 }
                             ]
                         }
                     ]
                 }}
    }
    configuration = snapser.Configuration(
        host=os.environ['SNAPEND_STORAGE_HTTP_URL']
    )
    with snapser.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = snapser.StorageServiceApi(api_client)
        try:
            # Storage Settings
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if api_response is None:
                return make_response(jsonify(response), 200)
            # Load storage data
            response['data']['character_settings'] = json.loads(
                api_response.value)
            # Update the characters with the imported characters
            response['data']['character_settings']['sections'][0]['components'][0]['value'] = settings['sections'][0]['components'][0]['value']
            return make_response(jsonify(response), 200)
        except ApiException as e:
            pass
    return make_response(jsonify(response), 200)

# End: SYSTEM: Used by Snapser's built-in configuration import export system

# SYSTEM: User Tool: Delete and Reset User data


@app.route("/v1/byosnap-characters/settings/users/<user_id>/data", methods=["DELETE"])
def delete_user_data(user_id):
    gateway = request.headers.get('Gateway')
    if not gateway or gateway.lower() != 'internal':
        return make_response(jsonify({
            'error_message': 'Unauthorized'
        }), 401)
    # Delete the character blob from storage
    storage_configuration = snapser.Configuration(
        host=os.environ['SNAPEND_STORAGE_HTTP_URL']
    )
    with snapser.ApiClient(configuration=storage_configuration) as storage_api_client:
        storage_api_instance = snapser.StorageServiceApi(storage_api_client)
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

# End: SYSTEM: User Tool: Delete and Reset User data

# SYSTEM: Used by the Snap Configuration Tool


@app.route("/v1/byosnap-characters/settings", methods=["GET"])
def get_settings():
    '''
    Get the settings for the characters microservice
    '''
    default_settings = {
        'version': 'v1.0.0',
        'id': 'characters',
        'endpoint': '',
        'category': 'flat_form',
        'env_support': 'single',
        'sections': [
            {
                'id': 'registration',
                'components': [
                    {
                        'id': 'characters',
                        'type': 'textarea',
                        'value': ''
                    }
                ]
            }
        ]
    }
    configuration = snapser.Configuration(
        host=os.environ['SNAPEND_STORAGE_HTTP_URL']
    )
    with snapser.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = snapser.StorageServiceApi(api_client)
        try:
            # Anonymous Login
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if api_response is None:
                return make_response(jsonify(default_settings), 200)
            return make_response(jsonify(json.loads(api_response.value)), 200)
        except ApiException as e:
            pass
    return make_response(jsonify(default_settings), 200)

   # return make_response(jsonify(), 200)


@app.route("/v1/byosnap-characters/settings", methods=["PUT"])
def update_settings():
    '''
    Update the settings for the characters microservice
    '''
    try:
        blob_data = request.get_json()
        if 'payload' in blob_data:
            blob_data = blob_data['payload']
        character_string = blob_data['sections'][0]['components'][0]['value']
        # Split the characters by comma but also trim the characters
        character_list = character_string.split(',')
        character_list = [character.strip() for character in character_list]
        # Check for duplicates
        if len(character_list) != len(set(character_list)):
            return make_response(jsonify({
                'error_message': 'Duplicate characters found'
            }), 400)
        blob_data['sections'][0]['components'][0]['value'] = ','.join(
            character_list)
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Invalid JSON ' + str(e)
        }), 500)

    configuration = snapser.Configuration(
        host=os.environ['SNAPEND_STORAGE_HTTP_URL']
    )
    with snapser.ApiClient(configuration=configuration) as api_client:
        cas = '12345'
        # Create an instance of the API class
        api_instance = snapser.StorageServiceApi(api_client)
        try:
            # Anonymous Login
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
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
                owner_id='byosnap_characters',
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

# End: SYSTEM: Used by the Snap Configuration Tool


# Regular API Endpoints exposed by the Snap
@app.route("/v1/byosnap-characters/users/<user_id>/characters", methods=["GET"])
def get_characters(user_id):
    """Get Game Characters for a User.
    ---
    get:
      summary: 'Get Characters'
      description: Get Player Id and Tokens for Characters in a Game
      operationId: Get Characters
      parameters:
      - in: path
        schema: UserIdParameter
      - in: header
        schema: TokenHeaderSchema
      responses:
        200:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
        201:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
    """
    storage_configuration = snapser.Configuration(
        host=os.environ['SNAPEND_STORAGE_HTTP_URL']
    )
    auth_configuration = snapser.Configuration(
        host=os.environ['SNAPEND_AUTH_HTTP_URL']
    )
    with snapser.ApiClient(configuration=storage_configuration) as storage_api_client:
        # Create an instance of the API class
        storage_api_instance = snapser.StorageServiceApi(storage_api_client)
        try:
            # Get blob
            storage_api_response = storage_api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='characters',
                owner_id=user_id,
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if storage_api_response is None:
                return make_response(jsonify({'characters': {}}), 200)
            cas = storage_api_response.cas
            characters: CharactersResponseSchema = json.loads(
                storage_api_response.value)
            # What we want to do is go over every character and check if their token is near expiry
            # If it is, we want to refresh the token
            for character_id, character in characters['characters'].items():
                # Get last refresh time + token validity and compare with current time
                # If it is less than 24 hours, refresh the token
                # Call the Auth Anon Login API to refresh the token
                # Update the token in the characters dict
                refreshed_at = int(character['refreshed_at'])
                token_validity_seconds = int(
                    character['token_validity_seconds'])

                # Calculate expiry time
                expiry_time = refreshed_at + token_validity_seconds

                # Get current time in seconds since epoch
                current_time = int(time.time())

                # Check if the expiry is within the next 12 hours
                # 12 hours in seconds = 12 * 60 * 60 = 43200 seconds
                expires_in_24_hours = expiry_time - current_time <= 86400
                if expires_in_24_hours:
                    with snapser.ApiClient(configuration=auth_configuration) as auth_api_client:
                        # Create an instance of the API class
                        auth_api_instance = snapser.AuthServiceApi(
                            auth_api_client)
                        body = snapser.AuthAnonLoginRequest(
                            create_user=True,
                            username=f"{user_id}-{character_id}"
                        )

                        try:
                            # Anonymous Login
                            auth_api_response = auth_api_instance.auth_internal_anon_login(
                                body)
                            if auth_api_response is None:
                                return make_response(jsonify({
                                    'error_message': 'Server Error'
                                }), 500)

                            characters['characters'][character_id] = {
                                'id': auth_api_response.user.id,
                                'session_token': auth_api_response.user.session_token,
                                'refreshed_at': auth_api_response.user.refreshed_at,
                                'token_validity_seconds': auth_api_response.user.token_validity_seconds
                            }
                        except ApiException as e:
                            return make_response(jsonify({
                                'error_message': 'Server Exception: ' + str(e)
                            }), 500)

            # Now save the characters back to the storage
            try:
                storage_api_response = storage_api_instance.storage_internal_replace_blob(
                    access_type='private',
                    blob_key='characters',
                    owner_id=user_id,
                    gateway=os.environ['SNAPEND_INTERNAL_HEADER'],
                    body={
                        "value": json.dumps(characters),
                        "ttl": 0,
                        "create": True,
                        "cas": cas
                    }
                )
                if storage_api_response is None:
                    return make_response(jsonify({
                        'error_message': 'Server Error'
                    }), 500)
            except ApiException as e:
                return make_response(jsonify({
                    'error_message': 'Server Exception: ' + str(e)
                }), 500)
            return make_response(jsonify(characters), 200)

            # return make_response(jsonify(json.loads(api_response.value)), 200)
        except ApiException as e:
            pass
    return make_response(jsonify({'characters': {}}), 200)


@app.route("/v1/byosnap-characters/users/<user_id>/characters", methods=["DELETE"])
def reset_characters(user_id):
    """Resets characters for a user.
    ---
    delete:
      summary: 'Reset Characters (App Auth only)'
      description: Resets all characters for a user (App Auth only)
      operationId: Reset Characters
      parameters:
      - in: path
        schema: UserIdParameter
      - in: header
        schema: TokenHeaderSchema
      responses:
        200:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Reset successful'
    """
    auth_type = request.headers.get('Auth-Type')
    if not auth_type or (auth_type.lower() != 'app' and auth_type.lower() != 'api-key'):
        return make_response(jsonify({
            'error_message': 'Unauthorized'
        }), 401)
    # Delete the character blob from storage
    storage_configuration = snapser.Configuration(
        host=os.environ['SNAPEND_STORAGE_HTTP_URL']
    )
    with snapser.ApiClient(configuration=storage_configuration) as storage_api_client:
        storage_api_instance = snapser.StorageServiceApi(storage_api_client)
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
    return make_response(jsonify({'characters': {}}), 200)


@app.route("/v1/byosnap-characters/users/<user_id>/characters/<character_id>/register", methods=["PATCH"])
def activate_character(user_id, character_id):
    """Activate a Character.
    ---
    patch:
      summary: 'Activate Character'
      description: Activate a Character in a Game. This call is idempotent. The characters token is refreshed if it is near expiry.
      operationId: Activate Character
      parameters:
      - in: header
        schema: TokenHeaderSchema
      - in: path
        schema: UserIdParameter
      - in: path
        schema: CharacterIdParameter
      responses:
        200:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'A successful activation'
        201:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'A successful activation'
        400:
          content:
            application/json:
              schema: ErrorResponseSchema
          description: 'Bad request'
        500:
          content:
            application/json:
              schema: ErrorResponseSchema
          description: 'Server error'
    """
    storage_configuration = snapser.Configuration(
        host=os.environ['SNAPEND_STORAGE_HTTP_URL']
    )
    auth_configuration = snapser.Configuration(
        host=os.environ['SNAPEND_AUTH_HTTP_URL']
    )
    # Validate if the character is in the list of characters
    with snapser.ApiClient(configuration=storage_configuration) as storage_api_client:
        # Create an instance of the API class
        storage_api_instance = snapser.StorageServiceApi(storage_api_client)
        try:
            api_response = storage_api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if api_response is not None:
                characters = json.loads(api_response.value)
                if character_id not in characters['sections'][0]['components'][0]['value']:
                    return make_response(jsonify({
                        'error_message': 'Character not found'
                    }), 400)
        except ApiException:
            pass
    logging.debug("Went past settings validation")
    # Get the characters for the user
    characters: CharactersResponseSchema = {'characters': {}}
    cas = '12345'
    # Get the characters for the user
    with snapser.ApiClient(configuration=storage_configuration) as storage_api_client:
        storage_api_instance = snapser.StorageServiceApi(storage_api_client)
        try:
            # Get blob
            storage_api_response = storage_api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='characters',
                owner_id=user_id,
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if storage_api_response is None:
                return make_response(jsonify({
                    'error_message': 'No blob'
                }), 400)
            cas = storage_api_response.cas
            characters = json.loads(storage_api_response.value)
            # return make_response(jsonify(json.loads(api_response.value)), 200)
        except ApiException:
            # You come here when the doc is not even present
            pass

    # For the character, we want to renew the token
    with snapser.ApiClient(configuration=auth_configuration) as auth_api_client:
        # Create an instance of the API class
        auth_api_instance = snapser.AuthServiceApi(
            auth_api_client)
        body = snapser.AuthAnonLoginRequest(
            create_user=True,
            username=f"{user_id}-{character_id}"
        )

        try:
            # Anonymous Login
            auth_api_response = auth_api_instance.auth_internal_anon_login(
                body)
            if auth_api_response is None:
                return make_response(jsonify({
                    'error_message': 'Server Error'
                }), 500)
            if 'characters' not in characters:
                characters['characters'] = {}
            characters['characters'][character_id] = {
                'id': auth_api_response.user.id,
                'session_token': auth_api_response.user.session_token,
                'refreshed_at': auth_api_response.user.refreshed_at,
                'token_validity_seconds': auth_api_response.user.token_validity_seconds
            }
        except ApiException as e:
            return make_response(jsonify({
                'error_message': 'Server Exception: ' + str(e)
            }), 500)

    # Now save the characters back to the storage
    try:
        storage_api_response = storage_api_instance.storage_internal_replace_blob(
            access_type='private',
            blob_key='characters',
            owner_id=user_id,
            gateway=os.environ['SNAPEND_INTERNAL_HEADER'],
            body={
                "value": json.dumps(characters),
                "ttl": 0,
                "create": True,
                "cas": cas
            }
        )
        if storage_api_response is None:
            return make_response(jsonify({
                'error_message': 'Server Error'
            }), 500)
    except ApiException as e:
        return make_response(jsonify({
            'error_message': 'Server Exception: ' + str(e)
        }), 500)
    return make_response(jsonify(characters), 200)
# End: Regular API Endpoints exposed by the Snap


# TODO: Uncomment only when trying to generate the API Spec
# Since path inspects the view and its route,
# we need to be in a Flask request context
with app.test_request_context():
    spec.path(view=get_characters)
    spec.path(view=activate_character)
    spec.path(view=reset_characters)
# We're good to go! Save this to a file for now.
with open(API_SPEC_FILENAME, 'w') as f:
    json.dump(spec.to_dict(), f)

# # pprint(spec.to_dict())
# # print(spec.to_yaml())
# END: Uncomment only when trying to generate the API Spec

# TODO: Uncomment if developing locally
# if __name__ == "__main__":
#     # Change debug to True if you are in development
#     app.run(host='0.0.0.0', port=5003, debug=False)
