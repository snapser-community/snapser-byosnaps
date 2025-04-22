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

// swagger:model ErrorResponseSchema
type ErrorResponseSchema struct {
	ErrorMessage string `json:"error_message"`
}

// swagger:model ProfilePayloadSchema
type ProfilePayloadSchema struct {
	Profile map[string]interface{} `json:"profile"`
}
