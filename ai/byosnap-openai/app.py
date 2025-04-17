'''
Basic Python BYOSnap Example.
'''
from openai import OpenAI
import logging
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
# Header Values
AUTH_TYPE_HEADER_VALUE_USER_AUTH = 'user'
AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH = 'api-key'
GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE = 'internal'
# ALL Auth Types
ALL_AUTH_TYPES = [AUTH_TYPE_HEADER_VALUE_USER_AUTH,
                  AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE]


# Configure logging to display messages of level DEBUG and above
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# App Initialization
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Decorators


def validate_authorization(*allowed_auth_types, user_id_resource_key="user_id"):
    '''
    Decorator to validate the authorization type of the request.
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
            target_user = kwargs.get(user_id_resource_key, "")
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


@app.route('/v1/byosnap-openai/chat', methods=['OPTIONS'])
@app.route('/v1/byosnap-openai/chat-stream', methods=['OPTIONS'])
@app.route('/v1/byosnap-openai/completion', methods=['OPTIONS'])
@app.route('/v1/byosnap-openai/completion-stream', methods=['OPTIONS'])
@app.route('/v1/byosnap-openai/embedding', methods=['OPTIONS'])
@cross_origin()
def cors_overrides(path):
    '''
    CORS overrides for the API Explorer.
    '''
    return f'{path} Ok'

# APIs

# @GOTCHAS 👋 - Health Check Endpoint
#    1. The health URL does not take any URL prefix like other APIs
#


@app.route('/healthz', methods=["GET"])
def health():
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
