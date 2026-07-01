'''
This script generates a Swagger specification for the BYOSnap Core Python Example.

Only endpoints that carry an x-snapser-auth-types tag (i.e. the ones Snapser
should surface in an SDK / API Explorer) are registered below.
'''
import os
import json
from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from models.schemas import UserIdParameterSchema, ExportSettingsSchema, ErrorResponseSchema, \
    CharactersResponseSchema, SuccessMessageSchema, SettingsEnvironmentDataSchema, SettingsSchema, \
    ByoToolPayloadSectionSchema, SectionComponentSchema, GroupComponentItemSchema, \
    GroupComponentItemSchema, BaseComponentSchema, GroupComponentSchema
from app import API_PREFIX, settings_export, settings_import, update_settings, \
    example_user_endpoint, example_api_key_endpoint, example_internal_endpoint, \
    example_admin_endpoint, example_multi_auth_endpoint

# Constants
RESOURCES_DIR = 'snapser-resources'
API_SPEC_FILENAME = 'swagger.json'

# Initialize Flask App
app = Flask(__name__)

# Register your endpoints. Routes reuse API_PREFIX from app.py so the Snap id
# only ever lives in one place.
app.add_url_rule(f"{API_PREFIX}/settings/export",
                 view_func=settings_export, methods=['GET'])
app.add_url_rule(f"{API_PREFIX}/settings/import",
                 view_func=settings_import, methods=['POST'])
app.add_url_rule(f"{API_PREFIX}/settings",
                 view_func=update_settings, methods=['PUT'])
app.add_url_rule(f"{API_PREFIX}/users/<user_id>/example",
                 view_func=example_user_endpoint, methods=['GET'])
app.add_url_rule(f"{API_PREFIX}/example/api-key",
                 view_func=example_api_key_endpoint, methods=['GET'])
app.add_url_rule(f"{API_PREFIX}/example/internal",
                 view_func=example_internal_endpoint, methods=['GET'])
app.add_url_rule(f"{API_PREFIX}/example/admin",
                 view_func=example_admin_endpoint, methods=['GET'])
app.add_url_rule(f"{API_PREFIX}/users/<user_id>/example/multi-auth",
                 view_func=example_multi_auth_endpoint, methods=['GET'])

# Initialize APISpec
spec = APISpec(
    title="BYOSnap Core Python Example",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
spec.components.schema("UserIdParameterSchema", schema=UserIdParameterSchema)
spec.components.schema("CharactersResponseSchema",
                       schema=CharactersResponseSchema)
spec.components.schema("SuccessMessageSchema",
                       schema=SuccessMessageSchema)
spec.components.schema("ErrorResponseSchema",
                       schema=ErrorResponseSchema)
spec.components.schema("SettingsSchema",
                       schema=SettingsSchema)
spec.components.schema("ExportSettingsSchema",
                       schema=ExportSettingsSchema)

# Generate paths using the FlaskPlugin
with app.test_request_context():
    spec.path(view=settings_export)
    spec.path(view=settings_import)
    spec.path(view=update_settings)
    spec.path(view=example_user_endpoint)
    spec.path(view=example_api_key_endpoint)
    spec.path(view=example_internal_endpoint)
    spec.path(view=example_admin_endpoint)
    spec.path(view=example_multi_auth_endpoint)

# Save to JSON
if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)
with open(os.path.join(RESOURCES_DIR, API_SPEC_FILENAME), 'w') as f:
    json.dump(spec.to_dict(), f, indent=4)

print(
    f"Swagger specification generated at {os.path.join(RESOURCES_DIR, API_SPEC_FILENAME)}")
