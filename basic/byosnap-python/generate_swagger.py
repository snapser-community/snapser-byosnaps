'''
This script generates a Swagger specification for the BYOSnap Basic Python Example.
'''
import os
import json
from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from models.schemas import UserIdParameterSchema, ErrorResponseSchema, SuccessResponseSchema, \
    TokenHeaderSchema
from app import get_game, save_game, delete_user, update_user_profile

# Constants
RESOURCES_DIR = 'snapser-resources'
API_SPEC_FILENAME = 'swagger.json'

# Initialize Flask App
app = Flask(__name__)

# Register your endpoints
app.add_url_rule('/v1/byosnap-basic/users/<user_id>/game',
                 view_func=get_game, methods=['GET'])
app.add_url_rule('/v1/byosnap-basic/users/<user_id>/game',
                 view_func=save_game, methods=['POST'])
app.add_url_rule('/v1/byosnap-basic/users/<user_id>',
                 view_func=delete_user, methods=['DELETE'])
app.add_url_rule('/v1/byosnap-basic/users/<user_id>/profile',
                 view_func=update_user_profile, methods=['PUT'])

# Initialize APISpec
spec = APISpec(
    title="BYOSnap Basic Python Example",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
spec.components.schema("TokenHeaderSchema", schema=TokenHeaderSchema)
spec.components.schema("UserIdParameterSchema", schema=UserIdParameterSchema)
spec.components.schema("ErrorResponseSchema", schema=ErrorResponseSchema)
spec.components.schema("SuccessResponseSchema", schema=SuccessResponseSchema)


# Generate paths using the FlaskPlugin
with app.test_request_context():
    spec.path(view=get_game)
    spec.path(view=save_game)
    spec.path(view=delete_user)
    spec.path(view=update_user_profile)

# Save to JSON
if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)
with open(os.path.join(RESOURCES_DIR, API_SPEC_FILENAME), 'w') as f:
    json.dump(spec.to_dict(), f, indent=4)

print(
    f"Swagger specification generated at {os.path.join(RESOURCES_DIR, API_SPEC_FILENAME)}")
