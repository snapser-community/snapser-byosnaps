'''
This script generates a Swagger specification for the BYOSnap Basic Python Example.
'''
import os
import json
from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from models.schemas import PlayerProfileSchema, GiveXPInputSchema, GiveXPResponseSchema, \
    PromptTemplateSchema, PlayerProfileJSONSchema, MCPResourceSchema, MCPToolSchema, \
    MCPPromptSchema, MCPManifestAuthSchema, MCPManifestSchema
from app import get_player_profile, give_xp, quest_helper_prompt, schema_player_profile, manifest

# Constants
RESOURCES_DIR = 'snapser-resources'
API_SPEC_FILENAME = 'swagger.json'

# Initialize Flask App
app = Flask(__name__)

# Register your endpoints
app.add_url_rule('/v1/byosnap-mcp/mcp/resources/player-profile',
                 view_func=get_player_profile, methods=['GET'])
app.add_url_rule('/v1/byosnap-mcp/mcp/tools/give-xp',
                 view_func=give_xp, methods=['POST'])
app.add_url_rule('/v1/byosnap-mcp/mcp/prompts/quest-helper',
                 view_func=quest_helper_prompt, methods=['GET'])
app.add_url_rule('/v1/byosnap-mcp/mcp/schema/player-profile',
                 view_func=schema_player_profile, methods=['GET'])
app.add_url_rule('/v1/byosnap-mcp/mcp/manifest.json',
                 view_func=manifest, methods=['GET'])
# Initialize APISpec
spec = APISpec(
    title="BYOSnap Gemini API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
spec.components.schema("PlayerProfileSchema", schema=PlayerProfileSchema)
spec.components.schema("ErrorResponseSchema", schema=GiveXPInputSchema)
spec.components.schema("SuccessResponseSchema", schema=GiveXPResponseSchema)
spec.components.schema("PromptTemplateSchema", schema=PromptTemplateSchema)
spec.components.schema("PlayerProfileJSONSchema",
                       schema=PlayerProfileJSONSchema)
spec.components.schema("MCPResourceSchema", schema=MCPResourceSchema)
spec.components.schema("MCPToolSchema", schema=MCPToolSchema)
spec.components.schema("MCPPromptSchema", schema=MCPPromptSchema)
spec.components.schema("MCPManifestAuthSchema", schema=MCPManifestAuthSchema)
spec.components.schema("MCPManifestSchema", schema=MCPManifestSchema)


# Generate paths using the FlaskPlugin
with app.test_request_context():
    spec.path(view=get_player_profile)
    spec.path(view=give_xp)
    spec.path(view=quest_helper_prompt)
    spec.path(view=schema_player_profile)
    spec.path(view=manifest)

# Save to JSON
if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)
with open(os.path.join(RESOURCES_DIR, API_SPEC_FILENAME), 'w') as f:
    json.dump(spec.to_dict(), f, indent=4)

print(
    f"Swagger specification generated at {os.path.join(RESOURCES_DIR, API_SPEC_FILENAME)}")
