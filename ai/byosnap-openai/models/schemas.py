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


class SuccessResponseSchema(Schema):
    '''
    Schema for the success response.
    '''
    response = fields.Raw()


class SuccessEmbeddingResponseSchema(Schema):
    '''
    Schema for the success embedding response.
    '''
    embedding = fields.List(fields.Float())


class ErrorResponseSchema(Schema):
    '''
    Schema for the error response.
    '''
    error_message = fields.Str()
