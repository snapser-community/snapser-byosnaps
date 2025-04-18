'''
This script generates a Swagger specification for the BYOSnap Basic Python Example.
'''
import os
import json
from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from models.schemas import ClaudeChatMessageSchema, ErrorResponseSchema, \
    ClaudeChatRequestSchema, SuccessResponseSchema
from app import chat, chat_stream

# Constants
RESOURCES_DIR = 'snapser-resources'
API_SPEC_FILENAME = 'swagger.json'

# Initialize Flask App
app = Flask(__name__)

# Register your endpoints
app.add_url_rule('/v1/byosnap-anthropic/chat',
                 view_func=chat, methods=['POST'])
app.add_url_rule('/v1/byosnap-anthropic/chat-stream',
                 view_func=chat_stream, methods=['POST'])

# Initialize APISpec
spec = APISpec(
    title="BYOSnap Anthropic API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
spec.components.schema("ClaudeChatMessageSchema",
                       schema=ClaudeChatMessageSchema)
spec.components.schema("ClaudeChatRequestSchema",
                       schema=ClaudeChatRequestSchema)
spec.components.schema("ErrorResponseSchema", schema=ErrorResponseSchema)
spec.components.schema("SuccessResponseSchema", schema=SuccessResponseSchema)


# Generate paths using the FlaskPlugin
with app.test_request_context():
    spec.path(view=chat)
    spec.path(view=chat_stream)

# Save to JSON
if not os.path.exists(RESOURCES_DIR):
    os.makedirs(RESOURCES_DIR)
with open(os.path.join(RESOURCES_DIR, API_SPEC_FILENAME), 'w') as f:
    json.dump(spec.to_dict(), f, indent=4)

print(
    f"Swagger specification generated at {os.path.join(RESOURCES_DIR, API_SPEC_FILENAME)}")
