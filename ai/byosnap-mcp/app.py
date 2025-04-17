import logging
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from functools import wraps

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

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

# Decorators


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


# --------------------
# Health
# --------------------


@app.route("/healthz", methods=["GET"])
def health():
    '''
    Health check endpoint
    '''
    return "OK"

# --------------------
# Resources
# --------------------


@app.route("/v1/byosnap-mcp/mcp/resources/player-profile", methods=["GET"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def get_player_profile():
    """
    Get Player Profile
    ---
    get:
      summary: 'Resources'
      operationId: GetPlayerProfile
      description: 'Fetch a player profile and current game state'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      responses:
        200:
          description: Player profile returned
          content:
            application/json:
              schema: PlayerProfileSchema
              example:
                user_id: "user_12345"
                username: "DragonSlayer_77"
                level: 19
                inventory: ["sword", "potion", "map"]
                xp: 1320
    """
    return jsonify({
        "user_id": "user_12345",
        "username": "DragonSlayer_77",
        "level": 19,
        "inventory": ["sword", "potion", "map"],
        "xp": 1320
    })

# --------------------
# Tools
# --------------------


@app.route("/v1/byosnap-mcp/mcp/tools/give-xp", methods=["POST"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def give_xp():
    """
    Give XP Tool
    ---
    post:
      summary: Tools
      operationId: GiveXP
      description: Award XP to a user
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      requestBody:
        required: true
        content:
          application/json:
            schema: GiveXPInputSchema
      responses:
        200:
          description: XP awarded
          content:
            application/json:
              schema: GiveXPResponseSchema
              example:
                message: "Given 100 XP to user user_12345"
                status: "success"
    """
    data = request.get_json()
    user_id = data.get("user_id")
    amount = data.get("amount")
    return jsonify({
        "message": f"Given {amount} XP to user {user_id}",
        "status": "success"
    })

# --------------------
# Prompts
# --------------------


@app.route("/v1/byosnap-mcp/mcp/prompts/quest-helper", methods=["GET"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def quest_helper_prompt():
    """
    Quest Helper Prompt Template
    ---
    get:
      summary: Prompts
      operationId: QuestHelperPrompt
      description: A reusable prompt template for quest guidance
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      responses:
        200:
          description: Prompt template
          content:
            application/json:
              schema: PromptTemplateSchema
              example:
                template: "You are a helpful NPC..."
                input_variables: ["quest_name", "current_step"]
    """
    return jsonify({
        "template": (
            "You are a helpful NPC. The player is currently on the '{quest_name}' quest. "
            "They are at step {current_step}. Guide them in an immersive fantasy tone."
        ),
        "input_variables": ["quest_name", "current_step"]
    })

# --------------------
# Schemas
# --------------------


@app.route("/v1/byosnap-mcp/mcp/schema/player-profile", methods=["GET"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def schema_player_profile():
    """
    Player Profile Schema
    ---
    get:
      summary: Schema of player profile object
      operationId: PlayerProfileSchema
      description: JSON schema for player profile
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      responses:
        200:
          description: JSON schema
          content:
            application/json:
              schema: PlayerProfileJSONSchema
              example:
                type: object
                properties:
                  user_id: {type: string}
                  username: {type: string}
                  level: {type: integer}
                  inventory: {type: array, items: {type: string}}
                  xp: {type: integer}
                required: ["user_id", "username", "level"]
    """
    return jsonify({
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "username": {"type": "string"},
            "level": {"type": "integer"},
            "inventory": {"type": "array", "items": {"type": "string"}},
            "xp": {"type": "integer"}
        },
        "required": ["user_id", "username", "level"]
    })

# --------------------
# Manifest
# --------------------


@app.route("/v1/byosnap-mcp/mcp/manifest.json", methods=["GET"])
@cross_origin()
@validate_authorization(AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)
def manifest():
    """
    MCP Manifest
    ---
    get:
      summary: MCP manifest
      operationId: GetMCPManifest
      description: MCP manifest for agent compatibility
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      responses:
        200:
          description: MCP manifest for agent compatibility
          content:
            application/json:
              schema: MCPManifestSchema
    """
    return jsonify({
        "schema_version": "v0",
        "description": "Snapser MCP Snap — expose player data and game tools to LLMs.",
        "auth": {
            "type": "header",
            "name": "Api-Key",
            "required": True,
            "description": "Include your Snapser API key in the `Api-Key` header."
        },
        "resources": {
            "player_profile": {
                "name": "player_profile",
                "description": "Fetch a player's profile and current game state",
                "method": "GET",
                "path": "/v1/byosnap-mcp/mcp/resources/player-profile",
                "schema": "/v1/byosnap-mcp/mcp/schema/player-profile"
            }
        },
        "tools": {
            "give_xp": {
                "name": "give_xp",
                "description": "Award XP to a user",
                "method": "POST",
                "path": "/v1/byosnap-mcp/mcp/tools/give-xp",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "amount": {"type": "integer"}
                    },
                    "required": ["user_id", "amount"]
                }
            }
        },
        "prompts": {
            "quest_helper": {
                "name": "quest_helper",
                "description": "A reusable prompt template for quest guidance",
                "path": "/v1/byosnap-mcp/mcp/prompts/quest-helper"
            }
        }
    })


if __name__ == "__main__":
    app.run(port=5003, debug=True)
