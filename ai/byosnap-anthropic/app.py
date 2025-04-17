'''
Anthropic Claude Wrapper - Snapser BYOSnap
'''
from anthropic import Anthropic
import logging
from dotenv import load_dotenv
import os

from flask import Flask, request, make_response, jsonify, Response, stream_with_context
from flask_cors import CORS, cross_origin
from functools import wraps

# Constants
AUTH_TYPE_HEADER_KEY = 'Auth-Type'
GATEWAY_HEADER_KEY = 'Gateway'
USER_ID_HEADER_KEY = 'User-Id'
AUTH_TYPE_HEADER_VALUE_USER_AUTH = 'user'
AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH = 'api-key'
GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE = 'internal'
ALL_AUTH_TYPES = [AUTH_TYPE_HEADER_VALUE_USER_AUTH,
                  AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE]

# Logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialization
load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

CLAUDE_MODELS = {
    "opus": "claude-3-opus-20240229",
    "sonnet": "claude-3-sonnet-20240229",
    "haiku": "claude-3-haiku-20240307"
}

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


def validate_authorization(*allowed_auth_types, user_id_resource_key="user_id"):
    '''
    Decorator to validate authorization headers
    '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            gateway_header_value = request.headers.get(GATEWAY_HEADER_KEY, "")
            is_internal_call = gateway_header_value.lower(
            ) == GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE
            auth_type_header_value = request.headers.get(
                AUTH_TYPE_HEADER_KEY, "")
            is_api_key_auth = auth_type_header_value.lower(
            ) == AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH
            user_id_header_value = request.headers.get(USER_ID_HEADER_KEY, "")
            target_user = kwargs.get(user_id_resource_key, "")
            is_target_user = user_id_header_value == target_user and user_id_header_value != ""

            validation_passed = False
            for auth_type in allowed_auth_types:
                if auth_type == GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE and is_internal_call:
                    validation_passed = True
                elif auth_type == AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH and (is_internal_call or is_api_key_auth):
                    validation_passed = True
                elif auth_type == AUTH_TYPE_HEADER_VALUE_USER_AUTH and not (is_internal_call or is_api_key_auth) and is_target_user:
                    validation_passed = True

            if not validation_passed:
                return make_response(jsonify({'error_message': 'Unauthorized'}), 400)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/v1/byosnap-anthropic/chat', methods=['OPTIONS'])
@app.route('/v1/byosnap-anthropic/chat-stream', methods=['OPTIONS'])
@cross_origin()
def cors_overrides(path=None):
    '''
    CORS preflight request handler
    '''
    return f'{path} Ok'


@app.route('/healthz', methods=["GET"])
def health():
    '''
    Health check endpoint
    '''
    return "Ok"


@app.route('/v1/byosnap-anthropic/chat', methods=['POST'])
def chat():
    """Claude chat completion
    ---
    post:
      summary: 'Anthropic Chat'
      description: This API is a wrapper around Claude's non-streaming chat.
      operationId: 'ClaudeChat'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                model:
                  type: string
                  example: claude-3-sonnet-20240229
                system:
                  type: string
                  example: You are a helpful assistant who writes like Shakespeare.
                messages:
                  type: array
                  items:
                    type: object
                    properties:
                      role:
                        type: string
                        enum: [user, assistant]
                      content:
                        type: string
                max_tokens:
                  type: integer
                  example: 1024
                temperature:
                  type: number
                  format: float
                  default: 0.7
      responses:
        200:
          content:
            application/json:
              schema: SuccessResponseSchema
          description: 'A successful response'
        500:
          content:
            application/json:
              schema: ErrorResponseSchema
          description: 'Server Error'
    """
    try:
        data = request.get_json()
        response = client.messages.create(
            model=CLAUDE_MODELS.get(data.get("tier"), data.get(
                "model", os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"))),
            system=data.get("system", "You are a helpful assistant."),
            messages=data["messages"],
            max_tokens=data.get("max_tokens", 1024),
            temperature=data.get("temperature", 0.7)
        )
        return jsonify({"response": response.content[0].text})
    except Exception as e:
        return jsonify({"error_message": str(e)}), 500


@app.route('/v1/byosnap-anthropic/chat-stream', methods=['POST'])
def chat_stream():
    """Claude chat stream completion
    ---
    post:
      summary: 'Anthropic Chat Stream'
      description: Claude streaming chat with SSE response.
      operationId: 'ClaudeChatStream'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                model:
                  type: string
                  example: claude-3-sonnet-20240229
                system:
                  type: string
                  example: You are a helpful assistant who writes like Shakespeare.
                messages:
                  type: array
                  items:
                    type: object
                    properties:
                      role:
                        type: string
                        enum: [user, assistant]
                      content:
                        type: string
                max_tokens:
                  type: integer
                  example: 1024
                temperature:
                  type: number
                  format: float
                  default: 0.7
      responses:
        200:
          description: Streaming response (text/event-stream)
          content:
            text/event-stream:
              schema:
                type: string
                example: |
                  data: Hello
                  data: world
                  data: [DONE]
        500:
          description: Server Error
          content:
            application/json:
              schema: ErrorResponseSchema
    """
    data = request.get_json()

    def generate():
        try:
            with client.messages.stream(
                model=data.get("model", os.getenv(
                    "ANTHROPIC_MODEL", "claude-3-sonnet-20240229")),
                system=data.get("system"),
                messages=data["messages"],
                max_tokens=data.get("max_tokens", 1024),
                temperature=data.get("temperature", 0.7)
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {text}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [Error] {str(e)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


if __name__ == "__main__":
    app.run(debug=True)
