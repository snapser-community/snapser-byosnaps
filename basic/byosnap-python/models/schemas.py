from marshmallow import Schema, fields


class UserIdParameterSchema(Schema):
    user_id = fields.Str()


class UserNameParameterSchema(Schema):
    user_name = fields.Str()


class SuccessResponseSchema(Schema):
    api = fields.Str()
    auth_type = fields.Str()
    header_user_id = fields.Str()
    path_user_id = fields.Str()
    message = fields.Str()


class ErrorResponseSchema(Schema):
    error_message = fields.Str()
