package main

import "fmt"

// BYOSnap Identity
// BYOSNAP_ID is the URL segment Snapser uses to route to this Snap. Every
// externally reachable route is prefixed with APIPrefix. Change BYOSnapID in
// one place instead of editing every route string. Note: the
// `// swagger:operation ... /v1/byosnap-core/...` annotation comments are
// literal paths (they run at code-generation time, so they cannot use this
// const) and must be kept in sync manually.
const (
	BYOSnapID = "byosnap-core"
)

// APIPrefix is the common prefix for every externally reachable route.
var APIPrefix = fmt.Sprintf("/v1/%s", BYOSnapID)

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
	EventbusHTTPURLEnvKey  = "SNAPEND_EVENTBUS_HTTP_URL"
	InternalHeaderEnvKey   = "SNAPEND_INTERNAL_HEADER"
	ByoSnapVersionEnvKey   = "BYOSNAP_VERSION"

	// Default Values
	DefaultInternalHeaderValue = "internal"
	DefaultByoSnapVersion      = "v1.0.0"
	DefaultEnvironment         = "DEFAULT"
)
