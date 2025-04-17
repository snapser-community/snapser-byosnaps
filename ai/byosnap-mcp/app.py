from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

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
