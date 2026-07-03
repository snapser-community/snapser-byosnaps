package main

// swagger:model UserIdParameterSchema
type UserIdParameterSchema struct {
	UserID string `json:"user_id"`
}

// swagger:model SuccessResponseSchema
type SuccessResponseSchema struct {
	API          string `json:"api"`
	AuthType     string `json:"auth_type"`
	HeaderUserID string `json:"header_user_id"`
	PathUserID   string `json:"path_user_id"`
	Message      string `json:"message"`
}

// swagger:model SuccessMessageSchema
type SuccessMessageSchema struct {
	Message string `json:"message"`
}

// swagger:model ErrorResponseSchema
type ErrorResponseSchema struct {
	ErrorMessage string `json:"error_message"`
}

// swagger:model CharactersResponseSchema
type CharactersResponseSchema struct {
	Characters []string `json:"characters"`
}

// swagger:model SettingsComponentSchema
type SettingsComponentSchema struct {
	ID         string                   `json:"id"`
	Type       string                   `json:"type"`
	Value      interface{}              `json:"value,omitempty"`
	Components []GroupComponentItemSchema `json:"components,omitempty"`
}

// swagger:model GroupComponentItemSchema
type GroupComponentItemSchema struct {
	ComponentOne   *SettingsComponentSchema `json:"component_one,omitempty"`
	ComponentTwo   *SettingsComponentSchema `json:"component_two,omitempty"`
	ComponentThree *SettingsComponentSchema `json:"component_three,omitempty"`
	ComponentFour  *bool                    `json:"component_four,omitempty"`
}

// swagger:model SettingsSectionSchema
type SettingsSectionSchema struct {
	ID         string                    `json:"id"`
	Components []SettingsComponentSchema `json:"components"`
}

// swagger:model SettingsSchema
type SettingsSchema struct {
	Sections []SettingsSectionSchema `json:"sections"`
}

// swagger:model ExportSettingsSchema
type ExportSettingsSchema struct {
	Version    string                                `json:"version"`
	ExportedAt int64                                 `json:"exported_at"`
	Data       map[string]map[string]*SettingsSchema `json:"data"`
}

// swagger:model CustomSettingsPayload
type CustomSettingsPayload struct {
	Payload interface{} `json:"payload"`
}
