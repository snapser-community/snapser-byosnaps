'''
This script generates a Swagger specification for the BYOSnap Intermediate Python Example.
'''
import os
import json
from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from models.schemas import UserIdParameterSchema, ErrorResponseSchema, SuccessResponseSchema, \
    CharactersResponseSchema
from app import check_active_characters

# Constants
RESOURCES_DIR = 'snapser-resources'
API_SPEC_FILENAME = 'swagger.json'

# Initialize Flask App
app = Flask(__name__)

# Register your endpoints
app.add_url_rule('/v1/byosnap-advanced/users/<user_id>/characters/<character_id>/active',
                 view_func=check_active_characters, methods=['GET'])

# Initialize APISpec
spec = APISpec(
    title="BYOSnap Advanced Python Example",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
spec.components.schema("UserIdParameterSchema", schema=UserIdParameterSchema)
spec.components.schema("CharactersResponseSchema",
                       schema=CharactersResponseSchema)


# Generate paths using the FlaskPlugin
with app.test_request_context():
    spec.path(view=check_active_characters)

# Save to JSON
if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)
with open(os.path.join(RESOURCES_DIR, API_SPEC_FILENAME), 'w') as f:
    json.dump(spec.to_dict(), f, indent=4)

print(
    f"Swagger specification generated at {os.path.join(RESOURCES_DIR, API_SPEC_FILENAME)}")
