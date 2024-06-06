import os
import json

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from flask import Flask, abort, request, make_response, jsonify, send_file
from pprint import pprint
from flask_cors import CORS, cross_origin

class TokenHeaderSchema(Schema):
  Token = fields.Str(required=True)


class CustomServiceParameter(Schema):
  req_id = fields.Int()


class CustomServiceSchema(Schema):
  id = fields.Int()
  content = fields.Str()


spec = APISpec(
  title="Custom Python Service",
  version="1.0.0",
  openapi_version="3.0.2",
  info=dict(
    description="Custom Python Service API",
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
      name="Custom Python Service",
      description="Endpoints for the Custom Python Service"
    )
  ],
  plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("CustomService", schema=CustomServiceSchema)

API_SPEC_FILENAME = 'swagger.json'
MARKDOWN_FILENAME = 'README.md'

# Extensions initialization
# =========================
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/v1/byosnap-jinks-flask/openapispec', methods=["GET"])
def api_spec():
  try:
    directory = os.getcwd()
    return send_file(directory + '/' + API_SPEC_FILENAME)
  except Exception as e:
     return str(e)

@app.route('/v1/byosnap-jinks-flask/markdown', methods=["GET"])
def markdown_docs():
  try:
    directory = os.getcwd()
    return send_file(directory + '/' + MARKDOWN_FILENAME)
  except Exception as e:
     return str(e)

@app.route('/v1/byosnap-jinks-flask/health', methods=["GET"])
def health():
  return "Ok Health Check"

@app.route('/v1/byosnap-jinks-flask/openapispec', methods=["OPTIONS"])
@app.route('/v1/byosnap-jinks-flask/markdown', methods=["OPTIONS"])
@app.route('/v1/byosnap-jinks-flask/health', methods=["OPTIONS"])
@app.route('/v1/byosnap-jinks-flask/resource-one/<req_id>', methods=['OPTIONS'])
@app.route('/v1/byosnap-jinks-flask/resource-two/<req_id>', methods=['OPTIONS'])
@cross_origin()
def cors_overrides(path):
  return f'{path} Ok'

#https://gateway.snapser.com/$clusterId/v1/byosnap-jinks-flask
@app.route("/v1/byosnap-jinks-flask/resource-one/<req_id>", methods=["GET"])
def resource_one(req_id):
  """Custom API Resource One.
  ---
  get:
    summary: 'resource_one'
    description: Custom Call Resource One
    operationId: Get Resource One
    parameters:
    - in: path
      schema: CustomServiceParameter
    - in: header
      schema: TokenHeaderSchema
    responses:
      200:
        content:
          application/json:
            schema: CustomServiceSchema
        description: 'A successful response'
      201:
        content:
          application/json:
            schema: CustomServiceSchema
        description: 'A successful creation'
  """
  # (...)
  return jsonify({
     'id': req_id,
     'content': 'test'
  })

@app.route("/v1/byosnap-jinks-flask/resource-two/<req_id>", methods=["GET"])
def resource_two(req_id):
  """Custom API Resource Two.
  ---
  get:
    summary: 'resource_two'
    description: Custom Call Resource Two
    operationId: Get Resource Two
    security:
      - Authorization: []
    parameters:
    - in: header
      schema: TokenHeaderSchema
    - in: path
      schema: CustomServiceParameter
    responses:
      200:
        content:
          application/json:
            schema: CustomServiceSchema
        description: 'A successful response'
      201:
        content:
          application/json:
            schema: CustomServiceSchema
        description: 'A successful creation'
  """
  # (...)
  return jsonify({
     'id': req_id,
     'content': 'test'
  })


# Since path inspects the view and its route,
# we need to be in a Flask request context
with app.test_request_context():
  spec.path(view=resource_one)
  spec.path(view=resource_two)
# We're good to go! Save this to a file for now.
with open(API_SPEC_FILENAME, 'w') as f:
    json.dump(spec.to_dict(), f)

# pprint(spec.to_dict())
# print(spec.to_yaml())