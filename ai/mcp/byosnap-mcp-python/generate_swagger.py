"""
This script generates a Swagger (OpenAPI 3) specification
for the BYOSnap OpenAI Apps SDK Python MCP example.
"""

import os
import json

from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from models.schemas import (
    MCPRequestSchema,
    SuccessResponseSchema,
    ErrorResponseSchema,
)
from app import mcp_entrypoint

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RESOURCES_DIR = "snapser-resources"
API_SPEC_FILENAME = "swagger.json"

# ---------------------------------------------------------------------------
# Minimal Flask app for apispec to introspect
# ---------------------------------------------------------------------------

flask_app = Flask(__name__)

# Mount the MCP endpoint under your versioned path for the spec
flask_app.add_url_rule(
    "/v1/byosnap-mcp/mcp",
    view_func=mcp_entrypoint,
    methods=["POST"],
)

# ---------------------------------------------------------------------------
# APISpec configuration
# ---------------------------------------------------------------------------

spec = APISpec(
    title="BYOSnap OpenAI Apps SDK Python Example",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Register Marshmallow schemas as reusable components
spec.components.schema("MCPRequestSchema", schema=MCPRequestSchema)
spec.components.schema("SuccessResponseSchema", schema=SuccessResponseSchema)
spec.components.schema("ErrorResponseSchema", schema=ErrorResponseSchema)

# ---------------------------------------------------------------------------
# Generate paths using the FlaskPlugin
# ---------------------------------------------------------------------------

with flask_app.test_request_context():
    # This will inspect mcp_entrypoint and use the YAML docstring,
    # resolving MCPRequestSchema / SuccessResponseSchema / ErrorResponseSchema
    # into proper $ref components.
    spec.path(view=mcp_entrypoint)

# ---------------------------------------------------------------------------
# Write swagger.json
# ---------------------------------------------------------------------------

if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)

output_path = os.path.join(RESOURCES_DIR, API_SPEC_FILENAME)
with open(output_path, "w") as f:
    json.dump(spec.to_dict(), f, indent=4)

print(f"Swagger specification generated at {output_path}")
