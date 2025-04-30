'''
This script generates a Swagger specification for the BYOSnap Intermediate Python Example.
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
from app import settings_export, settings_import, check_active_characters

# Constants
RESOURCES_DIR = 'snapser-resources'
API_SPEC_FILENAME = 'swagger.json'

# Initialize Flask App
app = Flask(__name__)

# Register your endpoints
app.add_url_rule("/v1/byosnap-advanced/settings/export",
                 view_func=settings_export, methods=['GET'])
app.add_url_rule("/v1/byosnap-advanced/settings/import",
                 view_func=settings_import, methods=['POST'])
app.add_url_rule("/v1/byosnap-advanced/users/<user_id>/characters/active",
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
spec.components.schema("SuccessMessageSchema",
                       schema=SuccessMessageSchema)
spec.components.schema("ErrorResponseSchema",
                       schema=ErrorResponseSchema)
spec.components.schema("ExportSettingsSchema",
                       schema=ExportSettingsSchema)
# spec.components.schema("SettingsEnvironmentDataSchema",
#                        schema=SettingsEnvironmentDataSchema)
# spec.components.schema("SettingsSchema",
#                        schema=SettingsSchema)
# spec.components.schema("ByoToolPayloadSectionSchema",
#                        schema=ByoToolPayloadSectionSchema)
# spec.components.schema("SectionComponentSchema",
#                        schema=SectionComponentSchema)
# spec.components.schema("GroupComponentSchema",
#                        schema=GroupComponentSchema)
# spec.components.schema("GroupComponentItemSchema",
#                        schema=GroupComponentItemSchema)
# spec.components.schema("BaseComponentSchema",
#                        schema=BaseComponentSchema)


# Generate paths using the FlaskPlugin
with app.test_request_context():
    spec.path(view=settings_export)
    spec.path(view=settings_import)
    spec.path(view=check_active_characters)

# Save to JSON
if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)
with open(os.path.join(RESOURCES_DIR, API_SPEC_FILENAME), 'w') as f:
    json.dump(spec.to_dict(), f, indent=4)

print(
    f"Swagger specification generated at {os.path.join(RESOURCES_DIR, API_SPEC_FILENAME)}")
