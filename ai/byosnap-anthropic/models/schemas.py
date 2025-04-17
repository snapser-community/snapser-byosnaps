from marshmallow import Schema, fields


class ClaudeChatMessageSchema(Schema):
    role = fields.Str(required=True, validate=lambda r: r in [
                      "user", "assistant"])
    content = fields.Str(required=True)


class ClaudeChatRequestSchema(Schema):
    model = fields.Str(required=True, example="claude-3-sonnet-20240229")
    system = fields.Str(
        required=False, example="You are a helpful assistant who writes like Shakespeare.")
    messages = fields.List(fields.Nested(
        ClaudeChatMessageSchema), required=True)
    max_tokens = fields.Int(missing=1024)
    temperature = fields.Float(missing=0.7)


class SuccessResponseSchema(Schema):
    '''
    Schema for the success response.
    '''
    response = fields.Raw()


class ErrorResponseSchema(Schema):
    '''
    Schema for the error response.
    '''
    error_message = fields.Str()
