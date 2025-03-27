from marshmallow import Schema, fields


class TokenHeaderSchema(Schema):
    Token = fields.Str(required=True)


class UserIdParameterSchema(Schema):
    user_id = fields.Str()


class SuccessResponseSchema(Schema):
    api = fields.Str()
    auth_type = fields.Str()
    source_user_id = fields.Str()
    target_user_id = fields.Str()
    message = fields.Str()


class ErrorResponseSchema(Schema):
    error_message = fields.Str()
