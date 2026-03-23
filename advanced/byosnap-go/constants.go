package main

const (
	// Header Keys
	AuthTypeHeaderKey = "Auth-Type"
	GatewayHeaderKey  = "Gateway"
	UserIDHeaderKey   = "User-Id"

	// Auth Type Header Values
	AuthTypeHeaderValueUserAuth   = "user"
	AuthTypeHeaderValueApiKeyAuth = "api-key"
	GatewayHeaderValueInternalOrigin = "internal"

	// Storage Constants
	CharacterSettingsBlobKey = "character_settings"
	CharactersBlobKey        = "characters"
	PrivateAccessType        = "private"
	ProtectedAccessType      = "protected"
	CharactersToolID         = "characters"

	// Environment Variable Keys
	StorageHTTPURLEnvKey   = "SNAPEND_STORAGE_HTTP_URL"
	InternalHeaderEnvKey   = "SNAPEND_INTERNAL_HEADER"
	ByoSnapVersionEnvKey   = "BYOSNAP_VERSION"

	// Default Values
	DefaultInternalHeaderValue = "internal"
	DefaultByoSnapVersion      = "v1.0.0"
	DefaultEnvironment         = "DEFAULT"
)
