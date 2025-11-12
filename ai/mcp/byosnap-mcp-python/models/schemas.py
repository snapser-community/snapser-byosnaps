# from marshmallow import Schema, fields


# class MCPRequestSchema(Schema):
#     """
#     Schema for the MCP JSON-RPC 2.0 request payload.
#     """
#     method = fields.Str(required=True, description="JSON-RPC method name")
#     id = fields.Raw(
#         required=False, description="JSON-RPC request id (string or number)")
#     params = fields.Dict(required=False, description="JSON-RPC params object")


# class SuccessResponseSchema(Schema):
#     """
#     Schema for a successful JSON-RPC 2.0 response envelope.
#     This is what your MCP endpoint returns on success via jsonrpc_result_response().
#     """
#     jsonrpc = fields.Str(
#         required=True,
#         description="JSON-RPC version, always '2.0'.",
#         example="2.0",
#     )
#     id = fields.Raw(
#         required=False,
#         description="Echoed JSON-RPC request id.",
#     )
#     result = fields.Dict(
#         required=False,
#         description="JSON-RPC result object containing MCP tool/resource output.",
#     )


# class ErrorResponseSchema(Schema):
#     """
#     Schema for a JSON-RPC 2.0 error envelope.
#     This is what your MCP endpoint returns on error via jsonrpc_error_response().
#     """
#     jsonrpc = fields.Str(
#         required=True,
#         description="JSON-RPC version, always '2.0'.",
#         example="2.0",
#     )
#     id = fields.Raw(
#         required=False,
#         allow_none=True,
#         description="Echoed request id; null/omitted for parse errors.",
#     )
#     error = fields.Dict(
#         required=True,
#         description="JSON-RPC error object (code, message, optional data).",
#         example={"code": -32600, "message": "Invalid Request"},
#     )
from marshmallow import Schema, fields


class MCPRequestSchema(Schema):
    """
    Schema for the MCP JSON-RPC 2.0 request payload.
    """
    method = fields.Str(required=True, description="JSON-RPC method name")

    id = fields.Raw(
        required=False,
        description="JSON-RPC request id (string or number)",
        metadata={
            "oneOf": [
                {"type": "string"},
                {"type": "integer"},
            ]
        },
    )

    params = fields.Dict(
        required=False,
        description="JSON-RPC params object",
    )


class SuccessResponseSchema(Schema):
    """
    Schema for a successful JSON-RPC 2.0 response envelope.
    """
    jsonrpc = fields.Str(
        required=True,
        description="JSON-RPC version, always '2.0'.",
        example="2.0",
    )

    id = fields.Raw(
        required=False,
        description="Echoed JSON-RPC request id.",
        metadata={
            "oneOf": [
                {"type": "string"},
                {"type": "integer"},
            ]
        },
    )

    result = fields.Dict(
        required=False,
        description=(
            "JSON-RPC result object containing MCP tool/resource output."
        ),
    )


class ErrorResponseSchema(Schema):
    """
    Schema for a JSON-RPC 2.0 error envelope.
    """
    jsonrpc = fields.Str(
        required=True,
        description="JSON-RPC version, always '2.0'.",
        example="2.0",
    )

    id = fields.Raw(
        required=False,
        allow_none=True,
        description="Echoed request id; null/omitted for parse errors.",
        metadata={
            "oneOf": [
                {"type": "string"},
                {"type": "integer"},
            ]
            # nullable comes from allow_none=True in OpenAPI 3.0
        },
    )

    error = fields.Dict(
        required=True,
        description="JSON-RPC error object (code, message, optional data).",
        example={"code": -32600, "message": "Invalid Request"},
    )
