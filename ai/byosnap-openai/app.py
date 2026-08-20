'''
Basic Python BYOSnap Example.
'''
from openai import OpenAI
import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

from flask import Flask, request, make_response, jsonify, Response, stream_with_context
from flask_cors import CORS, cross_origin
from functools import wraps


# Constants
# Header Keys
AUTH_TYPE_HEADER_KEY = 'Auth-Type'
GATEWAY_HEADER_KEY = 'Gateway'
USER_ID_HEADER_KEY = 'User-Id'
REQUEST_ID_HEADER_KEY = 'X-Request-Id'
# Header Values
AUTH_TYPE_HEADER_VALUE_USER_AUTH = 'user'
AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH = 'api-key'
GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE = 'internal'
# ALL Auth Types
ALL_AUTH_TYPES = [AUTH_TYPE_HEADER_VALUE_USER_AUTH,
                  AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE]


# Logging

# @GOTCHAS 👋 - Logging
#   1. Log ONE JSON object per line to stdout. Snapser parses the `level` field
#      (debug/info/warn/error) to color the line in the Logs tool.
#   2. Snapser correlates all log lines of one request ACROSS snaps by the
#      `request-id` field (from the X-Request-Id header), and samples logs
#      per-request instead of per-line. Bind it once per request (see the
#      before_request hook) instead of passing it to every log call.
#   3. Forward X-Request-Id only on outbound snap-to-snap calls. Do NOT send it
#      to third-party APIs like OpenAI. This snap makes no snap-to-snap calls.

request_id_var = ContextVar('request_id', default='')


def _sanitize_request_id(value):
    '''X-Request-Id is client-supplied: cap the length and allow only safe chars.'''
    value = value[:128]
    if value and all(c.isalnum() or c in '-_.' for c in value):
        return value
    return ''


_LEVEL_MAP = {'DEBUG': 'debug', 'INFO': 'info', 'WARNING': 'warn',
              'ERROR': 'error', 'CRITICAL': 'error'}


class JsonLogFormatter(logging.Formatter):
    '''Formats logs as the JSON shape Snapser parses (level, message, timestamp, request-id).'''

    def format(self, record):
        entry = {
            'level': _LEVEL_MAP.get(record.levelname, 'info'),
            'message': record.getMessage(),
            'timestamp': datetime.fromtimestamp(
                record.created, timezone.utc).isoformat().replace('+00:00', 'Z'),
        }
        request_id = request_id_var.get()
        if request_id:
            entry['request-id'] = request_id
        if record.exc_info:
            entry['exception'] = self.formatException(record.exc_info)
        if record.stack_info:
            entry['stack'] = self.formatStack(record.stack_info)
        return json.dumps(entry)


_log_handler = logging.StreamHandler(sys.stdout)
_log_handler.setFormatter(JsonLogFormatter())
logging.basicConfig(level=logging.DEBUG, handlers=[_log_handler])
# Gunicorn configures these loggers with propagate=False, so point them at the JSON handler too
for _gunicorn_logger in ('gunicorn.error', 'gunicorn.access'):
    _gl = logging.getLogger(_gunicorn_logger)
    _gl.handlers = [_log_handler]
    _gl.propagate = False

# App Initialization
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.before_request
def bind_request_id():
    '''
    Bind X-Request-Id to a contextvar so every log line for this request carries it
    '''
    request_id_var.set(_sanitize_request_id(
        request.headers.get(REQUEST_ID_HEADER_KEY, '')))

# Decorators


def validate_authorization(*allowed_auth_types, user_id_resource_key="user_id"):
    '''
    Decorator to validate authorization headers
    '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get Gateway Header
            gateway_header_value = request.headers.get(GATEWAY_HEADER_KEY, "")
            is_internal_call = \
                gateway_header_value.lower() == GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE
            # Get Auth Type Header
            auth_type_header_value = request.headers.get(
                AUTH_TYPE_HEADER_KEY, "")
            is_api_key_auth = \
                auth_type_header_value.lower() == AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH
            # Get User Id Header
            user_id_header_value = request.headers.get(USER_ID_HEADER_KEY, "")
            # If the API has a URL parameter for user_id, then use that
            # Otherwise, use the User-Id header value as the default
            target_user = kwargs.get(
                user_id_resource_key, user_id_header_value)
            is_target_user = \
                user_id_header_value == target_user and user_id_header_value != ""

            # Validate
            validation_passed = False
            for auth_type in allowed_auth_types:
                if auth_type == GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE:
                    # If `Auth-Type: Internal`, then the call must be internal
                    if not is_internal_call:
                        # Failed validation
                        continue
                    validation_passed = True
                elif auth_type == AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH:
                    # If `Auth-Type: Api-Key`, and the call is not internal, then the call must be pass the Api-Key validation
                    if not is_internal_call and not is_api_key_auth:
                        # Failed validation
                        continue
                    validation_passed = True
                elif auth_type == AUTH_TYPE_HEADER_VALUE_USER_AUTH:
                    # If `Auth-Type: User`, and the call is not internal or of type api-key auth, then the call must be pass the User validation
                    if not is_internal_call and not is_api_key_auth and not is_target_user:
                        # Failed validation
                        continue
                    validation_passed = True

            # Check if the provided auth_type is within the allowed types for this endpoint
            if not validation_passed:
                return make_response(jsonify({'error_message': 'Unauthorized'}), 400)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# CORS Overrides

# @GOTCHAS 👋 - CORS
#   1. Snapser API Explorer tool runs in the browser. Enabling CORS allows you to access the APIs via the API Explorer.
#


# @app.route('/v1/byosnap-openai/chat', methods=['OPTIONS'])
# @app.route('/v1/byosnap-openai/chat-stream', methods=['OPTIONS'])
# @app.route('/v1/byosnap-openai/completion', methods=['OPTIONS'])
# @app.route('/v1/byosnap-openai/completion-stream', methods=['OPTIONS'])
# @app.route('/v1/byosnap-openai/embedding', methods=['OPTIONS'])
# @cross_origin()
# def cors_overrides(path):
#     '''
#     CORS overrides for the API Explorer.
#     '''
#     return f'{path} Ok'

# APIs

# @GOTCHAS 👋 - Health Check Endpoint
#    1. The health URL does not take any URL prefix like other APIs
#


@app.route('/healthz', methods=["GET"])
def health():
    '''
    Health check endpoint'''
    return "Ok"

# @GOTCHAS 👋 - Externally available APIs
#     1. The Snapend Id is NOT part of the URL. This allows you to use the same BYOSnap in multiple Snapends.
#     2. All externally accessible APIs need to start with /$prefix/$byosnapId/remaining_path. where $prefix = v1, $byosnapId = byosnap-openai and remaining_path = /users/<user_id>.
#     3. The YAML comment below is used to generate the swagger.json file.
#     4. Notice the x-snapser-auth-types tags in the swagger.json. They tell Snapser if it should expose this API in
#        the SDK and the API Explorer. Note: but you should still validate the auth type in the code.
#     5. Snapser tech automatically adds the correct header to the SDK and API Explorer. So you do not need to add
#       the headers here in the swagger generation. Eg: For APIs exposed over User Auth, both the SDK
#       and API Explorer will expose the Token header for you to fill in. For Api-Key Auth, the API Explorer will
#       expose the Api-Key header for you to fill in. For internal APIs, the SDK and API Explorer will expose
#       the Gateway header.


# --------- CHAT --------- #

@app.route("/v1/byosnap-openai/chat", methods=["POST"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def chat():
    """API to access OpenAI's chat completion
    ---
    post:
      summary: 'Chat APIs'
      description: This API is a wrapper around OpenAI's chat completion API.
      operationId: 'Chat'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      requestBody:
        required: true
        content:
          application/json:
            schema: OpenAIChatRequestSchema
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
        response = client.chat.completions.create(
            model=data.get("model", os.getenv("OPENAI_MODEL")),
            messages=data["messages"],
            temperature=data.get("temperature", 0.7)
        )
        return jsonify({
            "response": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({"error_message": str(e)}), 500


@app.route("/v1/byosnap-openai/chat-stream", methods=["POST"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def chat_stream():
    """API to access streaming with OpenAI
    ---
    post:
      summary: 'Chat APIs'
      description: >
        This API is a wrapper around OpenAI's chat streaming API.
        The response is streamed using Server-Sent Events (`text/event-stream`).
      operationId: ChatStream
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      requestBody:
        required: true
        content:
          application/json:
            schema: OpenAIChatRequestSchema
      responses:
        200:
          description: Streaming response (text/event-stream)
          content:
            text/event-stream:
              schema:
                type: string
                example: |
                  data: Hello\n\n
                  data: world\n\n
                  data: [DONE]\n\n
        500:
          description: Server Error
          content:
            application/json:
              schema: ErrorResponseSchema
    """
    data = request.get_json()

    def generate():
        try:
            response = client.chat.completions.create(
                model=data.get("model", os.getenv("OPENAI_MODEL")),
                messages=data["messages"],
                temperature=data.get("temperature", 0.7),
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield f"data: {chunk.choices[0].delta.content}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [Error] {str(e)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


# --------- COMPLETION --------- #

@app.route("/v1/byosnap-openai/completion", methods=["POST"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def completion():
    """API to access OpenAI's completion APIs
    ---
    post:
      summary: 'Completion APIs'
      description: This API is a wrapper around OpenAI's completion API.
      operationId: 'Completion'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      requestBody:
        required: true
        content:
          application/json:
            schema: OpenAICompletionRequestSchema
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
        response = client.completions.create(
            model=data.get("model", "gpt-3.5-turbo-instruct"),
            prompt=data["prompt"],
            max_tokens=data.get("max_tokens", 100),
            temperature=data.get("temperature", 0.7)
        )
        return jsonify({
            "response": response.choices[0].text.strip()
        })
    except Exception as e:
        return jsonify({"error_message": str(e)}), 500


@app.route("/v1/byosnap-openai/completion-stream", methods=["POST"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def completion_stream():
    """API to access completion streaming with OpenAI
    ---
    post:
      summary: 'Completion APIs'
      description: >
        This API is a wrapper around OpenAI's completion streaming API.
        The response is streamed using Server-Sent Events (`text/event-stream`).
      operationId: CompletionStream
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      requestBody:
        required: true
        content:
          application/json:
            schema: OpenAICompletionRequestSchema
      responses:
        200:
          description: Streaming response (text/event-stream)
          content:
            text/event-stream:
              schema:
                type: string
                example: |
                  data: Hello\n\n
                  data: world\n\n
                  data: [DONE]\n\n
        500:
          description: Server Error
          content:
            application/json:
              schema: ErrorResponseSchema
    """
    data = request.get_json()

    def generate():
        try:
            response = client.completions.create(
                model=data.get("model", "gpt-3.5-turbo-instruct"),
                prompt=data["prompt"],
                max_tokens=data.get("max_tokens", 100),
                temperature=data.get("temperature", 0.7),
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].text:
                    yield f"data: {chunk.choices[0].text}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [Error] {str(e)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


# --------- EMBEDDING --------- #

@app.route("/v1/byosnap-openai/embedding", methods=["POST"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def embedding():
    """API to access OpenAI's embedding APIs
    ---
    post:
      summary: 'Embedding APIs'
      description: This API is a wrapper around OpenAI's embedding API.
      operationId: 'Embedding'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      requestBody:
        required: true
        content:
          application/json:
            schema: OpenAIEmbeddingRequestSchema
      responses:
        200:
          content:
            application/json:
              schema: SuccessEmbeddingResponseSchema
          description: 'A successful response'
        500:
          content:
            application/json:
              schema: ErrorResponseSchema
          description: 'Server Error'
    """
    try:
        data = request.get_json()
        response = client.embeddings.create(
            model=data.get("model", "text-embedding-ada-002"),
            input=data["input"]
        )
        return jsonify({
            "embedding": response.data[0].embedding
        })
    except Exception as e:
        return jsonify({"error_message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

# Uncomment if developing locally
# if __name__ == "__main__":
#     # Change debug to True if you are in development
#     app.run(host='0.0.0.0', port=5003, debug=False)
