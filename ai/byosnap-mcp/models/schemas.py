from marshmallow import Schema, fields


class PlayerProfileSchema(Schema):
    user_id = fields.Str(required=True)
    username = fields.Str(required=True)
    level = fields.Int(required=True)
    inventory = fields.List(fields.Str(), required=True)
    xp = fields.Int(required=True)


class GiveXPInputSchema(Schema):
    user_id = fields.Str(required=True)
    amount = fields.Int(required=True)


class GiveXPResponseSchema(Schema):
    message = fields.Str(required=True)
    status = fields.Str(required=True)


class PromptTemplateSchema(Schema):
    template = fields.Str(required=True)
    input_variables = fields.List(fields.Str(), required=True)


class PlayerProfileJSONSchema(Schema):
    type = fields.Constant("object")
    properties = fields.Dict()
    required = fields.List(fields.Str())


class MCPResourceSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    method = fields.Str(required=True)
    path = fields.Str(required=True)
    schema = fields.Str(required=True)


class MCPToolSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    method = fields.Str(required=True)
    path = fields.Str(required=True)
    # You could use a nested schema if it's fixed
    input_schema = fields.Dict(required=True)


class MCPPromptSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    path = fields.Str(required=True)


class MCPManifestAuthSchema(Schema):
    type = fields.Str(required=True)
    name = fields.Str(required=True)
    required = fields.Bool(required=True)
    description = fields.Str(required=True)


class MCPManifestSchema(Schema):
    schema_version = fields.Str(required=True)
    description = fields.Str(required=True)
    auth = fields.Nested(MCPManifestAuthSchema, required=False)
    resources = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MCPResourceSchema))
    tools = fields.Dict(keys=fields.Str(), values=fields.Nested(MCPToolSchema))
    prompts = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MCPPromptSchema))
