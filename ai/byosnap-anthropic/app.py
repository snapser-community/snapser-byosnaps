'''
Anthropic Claude Wrapper - Snapser BYOSnap
'''
from anthropic import Anthropic
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
AUTH_TYPE_HEADER_KEY = 'Auth-Type'
GATEWAY_HEADER_KEY = 'Gateway'
USER_ID_HEADER_KEY = 'User-Id'
REQUEST_ID_HEADER_KEY = 'X-Request-Id'
AUTH_TYPE_HEADER_VALUE_USER_AUTH = 'user'
AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH = 'api-key'
GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE = 'internal'
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
#      to third-party APIs like Anthropic. This snap makes no snap-to-snap calls.

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


@app.before_request
def bind_request_id():
    '''
    Bind X-Request-Id to a contextvar so every log line for this request carries it
    '''
    request_id_var.set(_sanitize_request_id(
        request.headers.get(REQUEST_ID_HEADER_KEY, '')))


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


# @app.route('/v1/byosnap-anthropic/chat', methods=['OPTIONS'])
# @app.route('/v1/byosnap-anthropic/chat-stream', methods=['OPTIONS'])
# @cross_origin()
# def cors_overrides(path=None):
#     '''
#     CORS preflight request handler
#     '''
#     return f'{path} Ok'


@app.route('/healthz', methods=["GET"])
def health():
    '''
    Health check endpoint
    '''
    return "Ok"


@app.route('/v1/byosnap-anthropic/chat', methods=['POST'])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def chat():
    """Claude chat completion
    ---
    post:
      summary: 'Chat APIs'
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
            schema: ClaudeChatRequestSchema
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
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def chat_stream():
    """Claude chat stream completion
    ---
    post:
      summary: 'Chat APIs'
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
            schema: ClaudeChatRequestSchema
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
