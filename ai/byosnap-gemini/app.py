'''
Gemini Wrapper - Snapser BYOSnap
'''
import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response, Response, stream_with_context
from flask_cors import CORS, cross_origin
from functools import wraps
import google.generativeai as genai

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

# Environment
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Flask App
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


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


# @app.route('/v1/byosnap-gemini/chat', methods=['OPTIONS'])
# @app.route('/v1/byosnap-gemini/chat-stream', methods=['OPTIONS'])
# @cross_origin()
# def cors_overrides(path=None):
#     '''
#     CORS preflight request handler
#     '''
#     return f'{path} Ok'


@app.route("/healthz", methods=["GET"])
def health():
    '''
    Health check endpoint
    '''
    return "Ok"


# Helpers


def build_text_prompt(messages):
    '''
    Build a text prompt from messages
    '''
    return [{"role": m["role"], "parts": [m["content"]]} for m in messages]


@app.route("/v1/byosnap-gemini/chat", methods=["POST"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def chat():
    """Gemini chat completion
    ---
    post:
      summary: 'Chat APIs'
      description: This API is a wrapper around Gemini's non-streaming text and multimodal chat.
      operationId: 'GeminiChat'
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
                  example: gemini-pro
                messages:
                  type: array
                  description: Text-only chat messages
                  items:
                    type: object
                    properties:
                      role:
                        type: string
                        enum: [user, model]
                      content:
                        type: string
                parts:
                  type: array
                  description: Optional multimodal input (e.g., base64 image + text)
                  items:
                    oneOf:
                      - type: object
                        properties:
                          text:
                            type: string
                      - type: object
                        properties:
                          inline_data:
                            type: object
                            properties:
                              mime_type:
                                type: string
                                example: image/png
                              data:
                                type: string
                                format: byte
                temperature:
                  type: number
                  format: float
                  default: 0.7
                max_tokens:
                  type: integer
                  example: 1024
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
        model_name = data.get("model", "models/gemini-2.0-flash")
        if not model_name.startswith("models/"):
            model_name = f"models/{model_name}"
        model = genai.GenerativeModel(model_name)

        if "parts" in data:
            response = model.generate_content(
                contents=data["parts"],
                generation_config={
                    "temperature": data.get("temperature", 0.7),
                    "max_output_tokens": data.get("max_tokens", 1024)
                }
            )
        else:
            prompt = build_text_prompt(data["messages"])
            response = model.generate_content(
                contents=prompt,
                generation_config={
                    "temperature": data.get("temperature", 0.7),
                    "max_output_tokens": data.get("max_tokens", 1024)
                }
            )

        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error_message": str(e)}), 500


@app.route("/v1/byosnap-gemini/chat-stream", methods=["POST"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def chat_stream():
    """Gemini chat stream completion
    ---
    post:
      summary: 'Chat APIs'
      description: Gemini streaming chat with SSE response.
      operationId: 'GeminiChatStream'
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
                  example: gemini-pro
                messages:
                  type: array
                  description: Text-only chat messages
                  items:
                    type: object
                    properties:
                      role:
                        type: string
                        enum: [user, model]
                      content:
                        type: string
                parts:
                  type: array
                  description: Optional multimodal input (e.g., base64 image + text)
                  items:
                    oneOf:
                      - type: object
                        properties:
                          text:
                            type: string
                      - type: object
                        properties:
                          inline_data:
                            type: object
                            properties:
                              mime_type:
                                type: string
                                example: image/jpeg
                              data:
                                type: string
                                format: byte
                temperature:
                  type: number
                  format: float
                  default: 0.7
                max_tokens:
                  type: integer
                  example: 1024
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
    model_name = data.get("model", "models/gemini-2.0-flash")
    if not model_name.startswith("models/"):
        model_name = f"models/{model_name}"
    model = genai.GenerativeModel(model_name)

    def generate():
        try:
            if "parts" in data:
                stream = model.generate_content(
                    contents=data["parts"],
                    stream=True,
                    generation_config={
                        "temperature": data.get("temperature", 0.7),
                        "max_output_tokens": data.get("max_tokens", 1024)
                    }
                )
            else:
                prompt = build_text_prompt(data["messages"])
                stream = model.generate_content(
                    contents=prompt,
                    stream=True,
                    generation_config={
                        "temperature": data.get("temperature", 0.7),
                        "max_output_tokens": data.get("max_tokens", 1024)
                    }
                )

            for chunk in stream:
                yield f"data: {chunk.text}\n\n"
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
