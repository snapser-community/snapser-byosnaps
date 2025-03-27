'''
Basic Python BYOSnap Example.
'''
import os
import json
import logging

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin

# Constants
USER_AUTH_HEADER = 'user'
API_KEY_AUTH_HEADER = 'api-key'
GATEWAY_ACCESS_HEADER = 'gateway'


# Configure logging to display messages of level DEBUG and above
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# App Initialization
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


# CORS
@app.route('/v1/byosnap-python-basic/health', methods=["OPTIONS"])
@app.route('/v1/byosnap-python-basic/resource-one/<req_id>', methods=['OPTIONS'])
@app.route('/v1/byosnap-python-basic/resource-two/<req_id>', methods=['OPTIONS'])
@cross_origin()
def cors_overrides(path):
    '''
    @method - CORS Overrides for all the APIs in the service

    @GOTCHA 👋 - Snapser API Explorer tool runs in the browser. Enabling CORS allows you to access the APIs via the API Explorer
    '''
    return f'{path} Ok'

# APIs


@app.route('/healthz', methods=["GET"])
def health():
    #
    # @method - Health Check. So Snapser knows when to start sending traffic to the service.
    #
    # @GOTCHAS 👋
    #    1. The health URL does not take any URL prefix like other APIs
    #
    return "Ok"


@app.route("/v1/byosnap-python-basic/users/<user_id>/game", methods=["GET"])
def api_one(user_id):
    #
    # @method - API One
    #
    # @GOTCHAS 👋
    #     1. All externally accessible APIs need to start with $prefix/$byosnapId/remaining_path. where $prefix = /v1, $byosnapId = byosnap-python-basic and remaining_path = /users/<user_id>
    #     2. The Snapend Id is NOT part of the URL. This allows you to the same BYOSnap to be used by multiple Snapends
    #     3. The YAML comment below is used to generate the swagger.json file.
    #
    """API that works with User and Api-Key auth
    ---
    get:
      summary: 'API One'
      description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
      operationId: 'API One'
      x-require-auth: user
      parameters:
      - in: path
        schema: UserIdParameterSchema
      - in: header
        schema: TokenHeaderSchema
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
    auth_type_header = request.headers.get('Auth-Type')
    user_id_header = request.headers.get('User-Id')
    # If the call is from a client to BYOSnap viz User Auth then you
    # want to confirm that the user_id in the header matches the user_id in the path
    # If not you may allow another logged in user to access the data of the user in the path
    if auth_type_header == USER_AUTH_HEADER:
        if user_id_header != user_id:
            return make_response(jsonify({'error_message': 'Not authorized'}), 401)
    # if auth_type_header == API_KEY_AUTH_HEADER:
    #     if not user_id_header or user_id_header == '':
    #         return make_response(jsonify({'error_message': 'API Needs the User-Id header'}), 400)
    # App Auth on the other hand is for the service to service communication
    # and so you allow the server to override the source user_id
    # Success state
    return make_response(jsonify({
        'api': 'api-one',
        'auth-type': auth_type_header,
        'source-user-id': user_id_header,
        'target-user-id': user_id,
        'message': 'success',
    }), 200)


@app.route("/v1/byosnap-python-basic/users/<user_id>/game", methods=["POST"])
def api_two(user_id):
    #
    # @method - API Two
    #
    # @GOTCHAS 👋
    #     1. All externally accessible APIs need to start with $prefix/$byosnapId/remaining_path. where $prefix = /v1, $byosnapId = byosnap-python-basic and remaining_path = /users/<user_id>
    #     2. The Snapend Id is NOT part of the URL. This allows you to the same BYOSnap to be used by multiple Snapends
    #     3. The YAML comment below is used to generate the swagger.json file.
    #
    """API that works only with Api-Key auth
    ---
    post:
      summary: 'API Two'
      description: This API will work only with Api-Key auth. You can access this API with a valid api-key.
      operationId: 'API Two'
      x-require-auth: api-key
      parameters:
      - in: path
        schema: UserIdParameterSchema
      - in: header
        schema: TokenHeaderSchema
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
    auth_type_header = request.headers.get('Auth-Type')
    user_id_header = request.headers.get('User-Id')
    # If the call is from a client to BYOSnap you want to error out
    if auth_type_header == USER_AUTH_HEADER:
        return make_response(jsonify({'error_message': 'Auth type not supported'}), 401)
    # In Api key auth mode, you may need the target user_id; which the sender needs to pass in the header
    if not user_id_header or user_id_header == '':
        return make_response(jsonify({'error_message': 'API Needs the User-Id header'}), 401)
    # Success state
    return make_response(jsonify({
        'api': 'api-two',
        'auth-type': auth_type_header,
        'source-user-id': user_id_header,
        'target-user-id': user_id,
        'message': 'success',
    }), 200)


@app.route("/v1/byosnap-python-basic/users/<user_id>", methods=["DELETE"])
def api_three(user_id):
    #
    # @method - API Three
    #
    # @GOTCHAS 👋
    #     1. All externally accessible APIs need to start with $prefix/$byosnapId/remaining_path. where $prefix = /v1, $byosnapId = byosnap-python-basic and remaining_path = /users/<user_id>
    #     2. The Snapend Id is NOT part of the URL. This allows you to the same BYOSnap to be used by multiple Snapends
    #     3. The YAML comment below is used to generate the swagger.json file.
    #
    """API that works only when calls are coming from within the Snapend
    ---
    get:
      summary: 'API Three'
      description: This API will work only when the call is coming from within the Snapend.
      operationId: 'API Three'
      x-require-auth: api-key
      parameters:
      - in: path
        schema: UserIdParameterSchema
      - in: header
        schema: TokenHeaderSchema
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
    gateway_header = request.headers.get('Gateway')
    user_id_header = request.headers.get('User-Id')
    if not gateway_header or gateway_header != GATEWAY_ACCESS_HEADER:
        return make_response(jsonify({'error_message': 'Unauthorized'}), 401)
    if not user_id_header or user_id_header == '':
        return make_response(jsonify({'error_message': 'API Needs the User-Id header'}), 401)
    return make_response(jsonify({
        'api': 'api-three',
        'auth-type': gateway_header,
        'source-user-id': user_id_header,
        'target-user-id': user_id,
        'message': 'success',
    }), 200)


# Uncomment if developing locally
# if __name__ == "__main__":
#     # Change debug to True if you are in development
#     app.run(host='0.0.0.0', port=5003, debug=False)
