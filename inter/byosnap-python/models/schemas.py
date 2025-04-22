from marshmallow import Schema, fields


class TokenHeaderSchema(Schema):
    '''
    Schema for the token header.
    '''
    # NOTE: TokenHeaderSchema is not used any more. Snapser automatically adds
    # the right header in the SDK and API explorer.
    Token = fields.Str(required=True)


class UserIdParameterSchema(Schema):
    '''
    Schema for the user ID parameter.
    '''
    user_id = fields.Str()


class ProfilePayloadSchema(Schema):
    '''
    Schema for the profile payload.
    '''
    profile = fields.Dict(
        required=True, description="JSON representation of the profile being updated")


class SuccessResponseSchema(Schema):
    '''
    Schema for the success response.
    '''
    api = fields.Str()
    auth_type = fields.Str()
    header_user_id = fields.Str()
    path_user_id = fields.Str()
    message = fields.Str()


class ErrorResponseSchema(Schema):
    '''
    Schema for the error response.
    '''
    error_message = fields.Str()
