from marshmallow import Schema, fields, validate, ValidationError


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


class CharactersResponseSchema(Schema):
    '''
    Schema for the characters response.
    '''
    characters = fields.List(fields.Str(), required=True)


class SuccessResponseSchema(Schema):
    '''
    Schema for the success response.
    '''
    api = fields.Str()
    auth_type = fields.Str()
    header_user_id = fields.Str()
    path_user_id = fields.Str()
    message = fields.Str()


class SuccessMessageSchema(Schema):
    '''
    Schema for the success message.
    '''
    message = fields.Str()


class ErrorResponseSchema(Schema):
    '''
    Schema for the error response.
    '''
    error_message = fields.Str()


class BaseComponentSchema(Schema):
    '''
    Base schema for components.
    '''
    id = fields.String(required=True)
    type = fields.String(
        required=True,
        validate=validate.OneOf([
            'text', 'textarea', 'number', 'select', 'multi_select',
            'checkbox', 'radio', 'group'
        ])
    )
    value = fields.Raw(required=False)


class GroupComponentItemSchema(Schema):
    '''
    Schema for group component items.
    '''
    component_one = fields.Nested(BaseComponentSchema, required=False)
    component_two = fields.Nested(BaseComponentSchema, required=False)
    component_three = fields.Nested(BaseComponentSchema, required=False)
    component_four = fields.Boolean(required=False)


class GroupComponentSchema(Schema):
    '''
    Schema for group components.
    '''
    id = fields.String(required=True)
    type = fields.String(
        required=True,
        validate=validate.Equal('group')
    )
    components = fields.List(fields.Nested(
        GroupComponentItemSchema), required=True)


class SectionComponentSchema(Schema):
    '''
    Schema for section components.
    '''
    # Allow either a base component or a group component
    # This will be dynamically validated
    id = fields.String(required=True)
    type = fields.String(required=True)
    value = fields.Raw(required=False)
    components = fields.List(fields.Nested(
        GroupComponentItemSchema), required=False)

    def validate(self, data, **kwargs):
        '''
        Custom validation to ensure that either a base component or a group
        '''
        if data.get("type") == "group":
            if "components" not in data:
                raise ValidationError("Group type must include 'components'")
        else:
            if "value" not in data:
                raise ValidationError(
                    "Non-group component must include 'value'")


class ByoToolPayloadSectionSchema(Schema):
    '''
    Schema for the BYO tool payload section.
    '''
    id = fields.String(required=True)
    components = fields.List(fields.Nested(
        SectionComponentSchema), required=True)


class SettingsSchema(Schema):
    '''
    Schema for the BYO tool payload.
    '''
    sections = fields.List(fields.Nested(
        ByoToolPayloadSectionSchema), required=True)


class SettingsEnvironmentDataSchema(Schema):
    '''
    Schema for the environment data.
    '''
    # Mapping from tool_id (e.g. "characters") to tool payload schema
    characters = fields.Nested(SettingsSchema, required=True)

    # Optionally, allow dynamic keys instead of hardcoding "characters"
    # tool_id = fields.Dict(keys=fields.String(), values=fields.Nested(ByoToolPayloadSchema))


class ExportSettingsSchema(Schema):
    '''
    Schema for the export response.
    '''
    version = fields.String(required=True)
    exported_at = fields.Integer(required=True)
    data = fields.Dict(
        keys=fields.String(validate=validate.OneOf(["dev", "stage", "prod"])),
        values=fields.Nested(SettingsEnvironmentDataSchema),
        required=True
    )
