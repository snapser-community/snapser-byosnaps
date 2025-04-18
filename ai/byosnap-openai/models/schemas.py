from marshmallow import Schema, fields


# Shared for chat & stream
class ChatMessageSchema(Schema):
    '''
    Chat message schema for OpenAI API.
    '''
    role = fields.Str(required=True, validate=lambda x: x in [
                      "system", "user", "assistant"])
    content = fields.Str(required=True)


class OpenAIChatRequestSchema(Schema):
    '''
    OpenAI chat request schema.
    '''
    model = fields.Str(required=True, example="gpt-4")
    messages = fields.List(fields.Nested(ChatMessageSchema), required=True)
    temperature = fields.Float(missing=0.7)


class OpenAICompletionRequestSchema(Schema):
    '''
    OpenAI completion request schema.
    '''
    model = fields.Str(required=True, example="gpt-3.5-turbo-instruct")
    prompt = fields.Str(
        required=True, example="Write a short story about dragons.")
    max_tokens = fields.Int(missing=100)
    temperature = fields.Float(missing=0.7)


class OpenAIEmbeddingRequestSchema(Schema):
    '''
    OpenAI embedding request schema.
    '''
    model = fields.Str(required=True, example="text-embedding-ada-002")
    input = fields.Str(
        required=True, example="Turn this sentence into an embedding.")


class SuccessResponseSchema(Schema):
    '''
    Success response schema for OpenAI API.
    '''
    response = fields.Raw()


class SuccessEmbeddingResponseSchema(Schema):
    '''
    Success response schema for OpenAI embedding API.
    '''
    embedding = fields.List(fields.Float(), required=True)


class ErrorResponseSchema(Schema):
    '''
    Error response schema for OpenAI API.
    '''
    error_message = fields.Str(required=True)
