// Package main BYOSnap Core Go Example
//
// BYOSnap Core Go Example — minimal starter scaffold.
//
// This is the recommended starting point for a new Go BYOSnap. Every endpoint
// Snapser expects is present, but each handler body is a STUB: it returns a
// simple placeholder and carries a `// TODO` describing what you would
// implement here. Fill in the stubs with your own logic. When you need to
// persist data, call other Snaps, or wire up the configuration/import-export
// tooling, look at the matching handler in advanced/byosnap-go for a complete,
// working reference.
//
//		Schemes: https
//	  Host: localhost:5003
//		Version: 1.0.0
//		License: Apache 2.0 http://www.apache.org/licenses/LICENSE-2.0.html
//		Contact:
//		  Name: Snapser Admin
//		  URL: https://snapser.com
//		  Email: admin@snapser.com
//
//		Consumes:
//		- application/json
//
//		Produces:
//		- application/json
//
// swagger:meta
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
)

// The generated Snapser server SDK ships in this project for internal
// Snap-to-Snap calls (e.g. reading/writing the Storage Snap). It is left
// commented out because the stubs below don't use it yet — uncomment when you
// start implementing real logic. See advanced/byosnap-go for usage.
// import snapser_internal "snapser_internal"
// var storageClient *snapser_internal.APIClient

func main() {
	r := mux.NewRouter()

	// Configure CORS
	// @GOTCHAS 👋 - CORS
	//   1. The Snapser API Explorer runs in the browser. Enabling CORS lets you
	//      call these APIs from the API Explorer.
	corsOpts := handlers.AllowedOrigins([]string{"*"}) // Allows all origins
	corsHeaders := handlers.AllowedHeaders([]string{"Content-Type", "Token", "Api-Key", "App-Key", "Gateway", "User-Id"})
	corsMethods := handlers.AllowedMethods([]string{"GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"})

	// Health Check Endpoint
	// @GOTCHAS 👋 - Health Check Endpoint
	//   1. The health URL does not take any URL prefix like the other APIs.
	r.HandleFunc("/healthz", HealthCheckHandler).Methods("GET")

	// CORS pre-flight override for the example route. gorilla/handlers already
	// handles CORS globally; registering an explicit OPTIONS handler keeps the
	// example path reachable from the browser-based API Explorer.
	r.HandleFunc(fmt.Sprintf("%s/users/{user_id}/example", APIPrefix), CorsOverridesHandler).Methods("OPTIONS")

	// --- A i]: Configuration Tool: Built using the Snapser UI Builder ---
	getSettingsHandler := http.HandlerFunc(GetSettings)
	r.Handle(fmt.Sprintf("%s/settings", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(getSettingsHandler)).Methods("GET")

	updateSettingsHandler := http.HandlerFunc(UpdateSettings)
	r.Handle(fmt.Sprintf("%s/settings", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(updateSettingsHandler)).Methods("PUT")

	// --- A ii]: New Configuration Tool: Custom HTML Snap Configuration Tool ---
	getSettingsCustomHandler := http.HandlerFunc(GetSettingsCustom)
	r.Handle(fmt.Sprintf("%s/settings/custom", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(getSettingsCustomHandler)).Methods("GET")

	updateSettingsCustomHandler := http.HandlerFunc(UpdateSettingsCustom)
	r.Handle(fmt.Sprintf("%s/settings/custom", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(updateSettingsCustomHandler)).Methods("PUT")

	// --- B: Snapend Sync|Clone: Import/Export ---
	exportSettingsHandler := http.HandlerFunc(ExportSettings)
	r.Handle(fmt.Sprintf("%s/settings/export", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(exportSettingsHandler)).Methods("GET")

	importSettingsHandler := http.HandlerFunc(ImportSettings)
	r.Handle(fmt.Sprintf("%s/settings/import", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(importSettingsHandler)).Methods("POST")

	validateImportHandler := http.HandlerFunc(ValidateImportSettings)
	r.Handle(fmt.Sprintf("%s/settings/validate-import", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(validateImportHandler)).Methods("POST")

	// --- A iii]: User Manager Tool: Custom HTML User Manager Tool ---
	getUserDataCustomHandler := http.HandlerFunc(GetUserDataCustom)
	r.Handle(fmt.Sprintf("%s/settings/users/{user_id}/custom", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(getUserDataCustomHandler)).Methods("GET")

	updateUserDataCustomHandler := http.HandlerFunc(UpdateUserDataCustom)
	r.Handle(fmt.Sprintf("%s/settings/users/{user_id}/custom", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(updateUserDataCustomHandler)).Methods("POST")

	// --- C: User Tool: GDPR Endpoints ---
	getUserDataHandler := http.HandlerFunc(GetUserData)
	r.Handle(fmt.Sprintf("%s/settings/users/{user_id}/data", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(getUserDataHandler)).Methods("GET")

	updateUserDataHandler := http.HandlerFunc(UpdateUserData)
	r.Handle(fmt.Sprintf("%s/settings/users/{user_id}/data", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(updateUserDataHandler)).Methods("PUT")

	deleteUserDataHandler := http.HandlerFunc(DeleteUserData)
	r.Handle(fmt.Sprintf("%s/settings/users/{user_id}/data", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(deleteUserDataHandler)).Methods("DELETE")

	// --- Example business API endpoints ---
	//
	// The stubs below demonstrate each Snapser auth exposure. The
	// `x-snapser-auth-types` tag in the swagger block controls which SDK / tool
	// the API surfaces in, and the matching validateAuthorization(...) enforces
	// it at runtime. Add, rename, or remove these to fit your Snap.
	//
	// A single endpoint can accept MULTIPLE auth types at once (see the
	// multi-auth example) — you do NOT need a separate route per auth type.

	// a. User auth
	exampleUserHandler := http.HandlerFunc(ExampleUserAuth)
	r.Handle(fmt.Sprintf("%s/users/{user_id}/example", APIPrefix),
		validateAuthorization([]string{AuthTypeHeaderValueUserAuth}, "user_id")(exampleUserHandler)).Methods("GET")

	// b. Api-Key auth
	exampleApiKeyHandler := http.HandlerFunc(ExampleApiKeyAuth)
	r.Handle(fmt.Sprintf("%s/example/api-key", APIPrefix),
		validateAuthorization([]string{AuthTypeHeaderValueApiKeyAuth}, "")(exampleApiKeyHandler)).Methods("GET")

	// c. Internal auth
	exampleInternalHandler := http.HandlerFunc(ExampleInternalAuth)
	r.Handle(fmt.Sprintf("%s/example/internal", APIPrefix),
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "")(exampleInternalHandler)).Methods("GET")

	// d. Admin SDK. `admin` is NOT an auth type; the endpoint is exposed over
	//    real auth types (api-key + internal) and the `x-snapser-sdk-categories:
	//    admin` tag is what surfaces it in the Admin SDK. Guard it with those
	//    same auth types.
	exampleAdminHandler := http.HandlerFunc(ExampleAdminSdk)
	r.Handle(fmt.Sprintf("%s/example/admin", APIPrefix),
		validateAuthorization([]string{AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "")(exampleAdminHandler)).Methods("GET")

	// e. Multi-auth. One endpoint can accept multiple auth types; no separate
	//    route per type is needed.
	exampleMultiAuthHandler := http.HandlerFunc(ExampleMultiAuth)
	r.Handle(fmt.Sprintf("%s/users/{user_id}/example/multi-auth", APIPrefix),
		validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(exampleMultiAuthHandler)).Methods("GET")

	// The Snapser internal SDK / storage client would be initialized here once
	// you start implementing real logic. See advanced/byosnap-go.
	// config := snapser_internal.NewConfiguration()
	// config.Servers[0].URL = os.Getenv(StorageHTTPURLEnvKey)
	// storageClient = snapser_internal.NewAPIClient(config)

	// Start server
	log.Println("Starting server on :5003")
	log.Fatal(http.ListenAndServe(":5003", handlers.CORS(corsOpts, corsHeaders, corsMethods)(r)))
}

// Helper to get env variable with default
func getEnv(key, defaultValue string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return defaultValue
}

// Helper to write JSON response
func writeJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

// Helper to write JSON error response
func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, ErrorResponseSchema{ErrorMessage: message})
}

// Returns the default settings structure
func getDefaultSettings() *SettingsSchema {
	return &SettingsSchema{
		Sections: []SettingsSectionSchema{
			{
				ID: "registration",
				Components: []SettingsComponentSchema{
					{
						ID:    "characters",
						Type:  "textarea",
						Value: "",
					},
				},
			},
		},
	}
}

// Returns the default characters payload for an environment
func getDefaultCharactersPayload() map[string]*SettingsSchema {
	return map[string]*SettingsSchema{
		CharactersToolID: getDefaultSettings(),
	}
}

// HealthCheckHandler returns ok for health checks
func HealthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Ok"))
}

// CorsOverridesHandler answers CORS pre-flight (OPTIONS) requests for the
// example route so the browser-based API Explorer can call it.
func CorsOverridesHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(fmt.Sprintf("%s Ok", vars["user_id"])))
}

// ===========================================================================
// A i]: Configuration Tool: Built using the Snapser UI Builder
// ===========================================================================

// GetSettings returns the settings for this Snap's Configuration Tool
// swagger:operation GET /v1/byosnap-core/settings getSettings
// ---
// summary: Configuration Tool
// description: Get the settings for this Snap's Configuration Tool. This endpoint is called by the Snapser Configuration Tool.
// operationId: GetSettings
// x-snapser-auth-types: ["internal"]
// x-snapser-sdk-categories: [admin]
// parameters:
//   - name: tool_id
//     in: query
//     required: false
//     type: string
//   - name: environment
//     in: query
//     required: false
//     type: string
//
// responses:
//   200:
//     description: Settings retrieved successfully
//     schema:
//       $ref: '#/definitions/SettingsSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func GetSettings(w http.ResponseWriter, r *http.Request) {
	defaultSettings := getDefaultSettings()
	toolID := r.URL.Query().Get("tool_id")
	environment := r.URL.Query().Get("environment")
	if environment == "" {
		environment = DefaultEnvironment
	}
	blobOwnerKey := fmt.Sprintf("%s_%s", toolID, environment)
	_ = blobOwnerKey // Used when the Storage SDK is connected

	// TODO: Fetch the saved settings for blobOwnerKey (e.g. from the Storage Snap
	//       via snapser_internal) and return them. For now we return the default.
	//       See advanced/byosnap-go for the full Storage read.
	writeJSON(w, http.StatusOK, defaultSettings)
}

// UpdateSettings updates the settings for this Snap's Configuration Tool
// swagger:operation PUT /v1/byosnap-core/settings updateSettings
// ---
// summary: Configuration Tool
// description: Update the settings for this Snap's Configuration Tool. This endpoint is called by the Snapser Configuration Tool.
// operationId: UpdateSettings
// x-snapser-auth-types: ["internal"]
// x-snapser-sdk-categories: [admin]
// parameters:
//   - name: tool_id
//     in: query
//     required: false
//     type: string
//   - name: environment
//     in: query
//     required: false
//     type: string
//   - name: body
//     in: body
//     required: true
//     schema:
//       $ref: '#/definitions/SettingsSchema'
//
// responses:
//   200:
//     description: Settings updated successfully
//     schema:
//       $ref: '#/definitions/SettingsSchema'
//   400:
//     description: Bad request
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
//   500:
//     description: Server error
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func UpdateSettings(w http.ResponseWriter, r *http.Request) {
	toolID := r.URL.Query().Get("tool_id")
	environment := r.URL.Query().Get("environment")
	if environment == "" {
		environment = DefaultEnvironment
	}
	blobOwnerKey := fmt.Sprintf("%s_%s", toolID, environment)
	_ = blobOwnerKey // Used when the Storage SDK is connected

	var blobData map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&blobData); err != nil {
		writeError(w, http.StatusInternalServerError, "Invalid JSON "+err.Error())
		return
	}

	// Extract payload if wrapped
	if payload, ok := blobData["payload"]; ok {
		if payloadMap, ok := payload.(map[string]interface{}); ok {
			blobData = payloadMap
		}
	}

	// TODO: Validate blobData and persist it for blobOwnerKey (e.g. via the
	//       Storage Snap). On a validation failure return
	//       writeError(w, http.StatusBadRequest, "..."). See advanced/byosnap-go
	//       for the full implementation.
	writeJSON(w, http.StatusOK, blobData)
}

// ===========================================================================
// A ii]: New Configuration Tool: Custom HTML Snap Configuration Tool
// ===========================================================================

// GetSettingsCustom returns the settings for the custom HTML configuration tool
// swagger:operation GET /v1/byosnap-core/settings/custom getSettingsCustom
// ---
// summary: Custom Configuration Tool
// description: Get the settings for the custom HTML configuration tool.
// operationId: GetSettingsCustom
// x-snapser-auth-types: ["internal"]
// x-snapser-sdk-categories: [admin]
// parameters:
//   - name: tool_id
//     in: query
//     required: false
//     type: string
//   - name: environment
//     in: query
//     required: false
//     type: string
//
// responses:
//   200:
//     description: Custom settings retrieved successfully
//     schema:
//       $ref: '#/definitions/CustomSettingsPayload'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func GetSettingsCustom(w http.ResponseWriter, r *http.Request) {
	defaultSettings := CustomSettingsPayload{Payload: ""}
	toolID := r.URL.Query().Get("tool_id")
	environment := r.URL.Query().Get("environment")
	if environment == "" {
		environment = DefaultEnvironment
	}
	blobOwnerKey := fmt.Sprintf("%s_%s", toolID, environment)
	_ = blobOwnerKey // Used when the Storage SDK is connected

	// TODO: Fetch the saved settings for blobOwnerKey and return them wrapped as
	//       CustomSettingsPayload{Payload: <settings>}. See advanced/byosnap-go.
	writeJSON(w, http.StatusOK, defaultSettings)
}

// UpdateSettingsCustom updates the settings from the custom HTML configuration tool
// swagger:operation PUT /v1/byosnap-core/settings/custom updateSettingsCustom
// ---
// summary: Custom Configuration Tool
// description: Update the settings from the custom HTML configuration tool.
// operationId: UpdateSettingsCustom
// x-snapser-auth-types: ["internal"]
// x-snapser-sdk-categories: [admin]
// parameters:
//   - name: tool_id
//     in: query
//     required: false
//     type: string
//   - name: environment
//     in: query
//     required: false
//     type: string
//   - name: body
//     in: body
//     required: true
//     schema:
//       $ref: '#/definitions/CustomSettingsPayload'
//
// responses:
//   200:
//     description: Custom settings updated successfully
//   500:
//     description: Server error
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func UpdateSettingsCustom(w http.ResponseWriter, r *http.Request) {
	toolID := r.URL.Query().Get("tool_id")
	environment := r.URL.Query().Get("environment")
	if environment == "" {
		environment = DefaultEnvironment
	}
	blobOwnerKey := fmt.Sprintf("%s_%s", toolID, environment)
	_ = blobOwnerKey // Used when the Storage SDK is connected

	var blobData map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&blobData); err != nil {
		writeError(w, http.StatusInternalServerError, "Invalid JSON "+err.Error())
		return
	}

	// Extract payload if wrapped
	if payload, ok := blobData["payload"]; ok {
		if payloadMap, ok := payload.(map[string]interface{}); ok {
			blobData = payloadMap
		}
	}

	// TODO: Validate blobData and persist it for blobOwnerKey. On a validation
	//       failure return a 400 with an error_message. See advanced/byosnap-go.
	writeJSON(w, http.StatusOK, blobData)
}

// ===========================================================================
// A iii]: User Manager Tool: Custom HTML User Manager Tool
// ===========================================================================

// GetUserDataCustom gets the user data for the custom HTML User Manager tool
// swagger:operation GET /v1/byosnap-core/settings/users/{user_id}/custom getUserDataCustom
// ---
// summary: User Manager Tool
// description: Get the user data for the custom HTML User Manager tool.
// operationId: GetUserDataCustom
// x-snapser-auth-types: ["internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     type: string
//
// responses:
//   200:
//     description: User data retrieved successfully
//     schema:
//       $ref: '#/definitions/CustomSettingsPayload'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func GetUserDataCustom(w http.ResponseWriter, r *http.Request) {
	// vars := mux.Vars(r)
	// userID := vars["user_id"]
	defaultPayload := CustomSettingsPayload{Payload: ""}

	// TODO: Look up this user's data (e.g. from the Storage Snap) and return it
	//       wrapped as CustomSettingsPayload{Payload: <data>}. See
	//       advanced/byosnap-go.
	writeJSON(w, http.StatusOK, defaultPayload)
}

// UpdateUserDataCustom updates the user data for the custom HTML User Manager tool
// swagger:operation POST /v1/byosnap-core/settings/users/{user_id}/custom updateUserDataCustom
// ---
// summary: User Manager Tool
// description: Update the user data for the custom HTML User Manager tool.
// operationId: UpdateUserDataCustom
// x-snapser-auth-types: ["internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     type: string
//   - name: body
//     in: body
//     required: true
//     schema:
//       $ref: '#/definitions/CustomSettingsPayload'
//
// responses:
//   200:
//     description: User data updated successfully
//   500:
//     description: Server error
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func UpdateUserDataCustom(w http.ResponseWriter, r *http.Request) {
	// vars := mux.Vars(r)
	// userID := vars["user_id"]

	var blobData map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&blobData); err != nil {
		writeError(w, http.StatusInternalServerError, "Invalid JSON "+err.Error())
		return
	}

	// Extract payload if wrapped
	if payload, ok := blobData["payload"]; ok {
		if payloadMap, ok := payload.(map[string]interface{}); ok {
			blobData = payloadMap
		}
	}

	// TODO: Validate blobData and persist it for this user_id. See
	//       advanced/byosnap-go for the Storage write.
	writeJSON(w, http.StatusOK, blobData)
}

// ===========================================================================
// B: Snapend Sync|Clone: Used by Snapser's built-in configuration import export system
// ===========================================================================

// ExportSettings exports all settings across environments
// swagger:operation GET /v1/byosnap-core/settings/export exportSettings
// ---
// summary: Export Settings
// description: Export all settings across environments (dev, stage, prod) for Snapend Sync/Clone.
// operationId: ExportSettings
// x-snapser-auth-types: ["internal"]
// responses:
//   200:
//     description: Settings exported successfully
//     schema:
//       $ref: '#/definitions/ExportSettingsSchema'
//   500:
//     description: Server error
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ExportSettings(w http.ResponseWriter, r *http.Request) {
	response := ExportSettingsSchema{
		Version:    getEnv(ByoSnapVersionEnvKey, DefaultByoSnapVersion),
		ExportedAt: time.Now().Unix(),
		Data: map[string]map[string]*SettingsSchema{
			// The key here (CharactersToolID) is the Tool ID whose payload you export.
			"dev":   getDefaultCharactersPayload(),
			"stage": getDefaultCharactersPayload(),
			"prod":  getDefaultCharactersPayload(),
		},
	}

	// TODO: Load the real saved settings per environment (e.g. batch-get from the
	//       Storage Snap) and merge them into response.Data[env]. See
	//       advanced/byosnap-go for the full implementation.
	writeJSON(w, http.StatusOK, response)
}

// ImportSettings imports settings across environments
// swagger:operation POST /v1/byosnap-core/settings/import importSettings
// ---
// summary: Import Settings
// description: Import settings across environments (dev, stage, prod) for Snapend Sync/Clone.
// operationId: ImportSettings
// x-snapser-auth-types: ["internal"]
// parameters:
//   - name: body
//     in: body
//     required: true
//     schema:
//       $ref: '#/definitions/ExportSettingsSchema'
//
// responses:
//   200:
//     description: Settings imported successfully
//     schema:
//       $ref: '#/definitions/SuccessMessageSchema'
//   400:
//     description: Bad request
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
//   500:
//     description: Server error
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ImportSettings(w http.ResponseWriter, r *http.Request) {
	var settingsData ExportSettingsSchema
	if err := json.NewDecoder(r.Body).Decode(&settingsData); err != nil {
		writeError(w, http.StatusInternalServerError, "Server Exception: "+err.Error())
		return
	}

	// TODO: Validate the incoming export payload and persist each environment's
	//       settings (e.g. batch-replace on the Storage Snap with cas="0" to
	//       force replace). See advanced/byosnap-go for validation + Storage
	//       writes.
	writeJSON(w, http.StatusOK, SuccessMessageSchema{Message: "Success"})
}

// ValidateImportSettings validates settings before importing
// swagger:operation POST /v1/byosnap-core/settings/validate-import validateImportSettings
// ---
// summary: Validate Import Settings
// description: Validate settings before importing. Snapser sends the settings that are about to be imported - validate if you can accept them.
// operationId: ValidateImportSettings
// x-snapser-auth-types: ["internal"]
// parameters:
//   - name: body
//     in: body
//     required: true
//     schema:
//       $ref: '#/definitions/ExportSettingsSchema'
//
// responses:
//   200:
//     description: Settings are valid
//     schema:
//       $ref: '#/definitions/ExportSettingsSchema'
//   500:
//     description: Invalid settings
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ValidateImportSettings(w http.ResponseWriter, r *http.Request) {
	var settingsData ExportSettingsSchema
	if err := json.NewDecoder(r.Body).Decode(&settingsData); err != nil {
		writeError(w, http.StatusInternalServerError, "Invalid JSON")
		return
	}

	// TODO: Add your own validation here. Return 200 with the payload if you can
	//       accept it, or 500 with an error_message if not. See advanced/byosnap-go
	//       for an example that checks the dev/stage/prod structure.
	writeJSON(w, http.StatusOK, settingsData)
}

// ===========================================================================
// C: User Tool: Get, Update and Delete User data: GDPR
// ===========================================================================

// GetUserData gets user data (GDPR)
// swagger:operation GET /v1/byosnap-core/settings/users/{user_id}/data getUserData
// ---
// summary: User Data (GDPR)
// description: Get user data. Used by the GDPR tool and the User Manager tool.
// operationId: GetUserData
// x-snapser-auth-types: ["internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     type: string
//
// responses:
//   200:
//     description: User data retrieved successfully
//   400:
//     description: No data found
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func GetUserData(w http.ResponseWriter, r *http.Request) {
	// vars := mux.Vars(r)
	// userID := vars["user_id"]

	// TODO: Fetch and return everything you store for this user_id. See
	//       advanced/byosnap-go for the Storage read.
	writeJSON(w, http.StatusOK, map[string]interface{}{})
}

// UpdateUserData updates user data (GDPR)
// swagger:operation PUT /v1/byosnap-core/settings/users/{user_id}/data updateUserData
// ---
// summary: User Data (GDPR)
// description: Update user data. Used by the GDPR tool and the User Manager tool.
// operationId: UpdateUserData
// x-snapser-auth-types: ["internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     type: string
//
// responses:
//   200:
//     description: User data updated successfully
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func UpdateUserData(w http.ResponseWriter, r *http.Request) {
	// vars := mux.Vars(r)
	// userID := vars["user_id"]

	// TODO: Persist the incoming data for this user_id. See advanced/byosnap-go.
	writeJSON(w, http.StatusOK, map[string]interface{}{})
}

// DeleteUserData deletes user data (GDPR right-to-be-forgotten)
// swagger:operation DELETE /v1/byosnap-core/settings/users/{user_id}/data deleteUserData
// ---
// summary: User Data (GDPR)
// description: Delete user data. Implements the GDPR right-to-be-forgotten.
// operationId: DeleteUserData
// x-snapser-auth-types: ["internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     type: string
//
// responses:
//   200:
//     description: User data deleted successfully
//   400:
//     description: No blob found
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func DeleteUserData(w http.ResponseWriter, r *http.Request) {
	// vars := mux.Vars(r)
	// userID := vars["user_id"]

	// TODO: Delete everything you store for this user_id. See advanced/byosnap-go
	//       for the Storage delete.
	writeJSON(w, http.StatusOK, map[string]interface{}{})
}

// ===========================================================================
// Example API Endpoints — your Snap's business logic lives here.
//
// The stubs below demonstrate each Snapser auth exposure. The
// `x-snapser-auth-types` tag in the swagger block controls which SDK / tool the
// API surfaces in, and the matching validateAuthorization(...) enforces it at
// runtime. Add, rename, or remove these to fit your Snap.
// ===========================================================================

// ExampleUserAuth is an example endpoint exposed over User auth
// swagger:operation GET /v1/byosnap-core/users/{user_id}/example exampleUserAuth
// ---
// summary: 'Example: User Auth'
// description: Accessible by a logged-in user, validated against the User-Id in their token. Surfaces in the client/game SDK.
// operationId: ExampleUserAuth
// x-snapser-auth-types: ["user"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
//
// responses:
//   200:
//     description: Success
//     schema:
//       $ref: '#/definitions/SuccessMessageSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ExampleUserAuth(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	userID := vars["user_id"]

	// TODO: add your business logic here (user-scoped).
	writeJSON(w, http.StatusOK, SuccessMessageSchema{
		Message: fmt.Sprintf("Hello user %s", userID),
	})
}

// ExampleApiKeyAuth is an example endpoint exposed over Api-Key auth
// swagger:operation GET /v1/byosnap-core/example/api-key exampleApiKeyAuth
// ---
// summary: 'Example: Api-Key Auth'
// description: Accessible with a valid API key. Use for trusted server-to-server calls.
// operationId: ExampleApiKeyAuth
// x-snapser-auth-types: ["api-key"]
// responses:
//   200:
//     description: Success
//     schema:
//       $ref: '#/definitions/SuccessMessageSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ExampleApiKeyAuth(w http.ResponseWriter, r *http.Request) {
	// TODO: add your business logic here (api-key-scoped).
	writeJSON(w, http.StatusOK, SuccessMessageSchema{
		Message: "Hello api-key caller",
	})
}

// ExampleInternalAuth is an example endpoint exposed over Internal auth
// swagger:operation GET /v1/byosnap-core/example/internal exampleInternalAuth
// ---
// summary: 'Example: Internal Auth'
// description: Callable only by other Snaps within the same Snapend (internal gateway). Surfaces in the internal SDK.
// operationId: ExampleInternalAuth
// x-snapser-auth-types: ["internal"]
// responses:
//   200:
//     description: Success
//     schema:
//       $ref: '#/definitions/SuccessMessageSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ExampleInternalAuth(w http.ResponseWriter, r *http.Request) {
	// TODO: add your business logic here (internal-only).
	writeJSON(w, http.StatusOK, SuccessMessageSchema{
		Message: "Hello internal caller",
	})
}

// ExampleAdminSdk is an example endpoint surfaced in the special Admin SDK.
//
// Note: `admin` is NOT an auth type. The endpoint is exposed over normal auth
// types (here api-key + internal); the `x-snapser-sdk-categories: [admin]` tag is
// what places it in the Admin SDK (used by admin tooling / the Snapser
// dashboard).
// swagger:operation GET /v1/byosnap-core/example/admin exampleAdminSdk
// ---
// summary: 'Example: Admin SDK'
// description: Exposed over api-key + internal auth and surfaced in the Admin SDK via x-snapser-sdk-categories.
// operationId: ExampleAdminSdk
// x-snapser-auth-types: ["api-key", "internal"]
// x-snapser-sdk-categories: [admin]
// responses:
//   200:
//     description: Success
//     schema:
//       $ref: '#/definitions/SuccessMessageSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ExampleAdminSdk(w http.ResponseWriter, r *http.Request) {
	// This endpoint is reachable via api-key or internal auth (enforced by the
	// router). The `x-snapser-sdk-categories: [admin]` tag is what surfaces it in
	// the Admin SDK. `admin` is NOT an auth type.
	// TODO: add your business logic here (admin-only).
	writeJSON(w, http.StatusOK, SuccessMessageSchema{
		Message: "Hello admin caller",
	})
}

// ExampleMultiAuth is an example endpoint that accepts multiple auth types on ONE route.
//
// One endpoint can accept multiple auth types; you do NOT need a separate route
// per type. Pass every accepted auth type to both the swagger tag (for SDK
// exposure) and the validateAuthorization(...) call (for runtime enforcement).
// swagger:operation GET /v1/byosnap-core/users/{user_id}/example/multi-auth exampleMultiAuth
// ---
// summary: 'Example: Multi Auth'
// description: One endpoint reachable by a logged-in user, a valid API key, or an internal Snap. List every auth type you want to allow - no need for a separate route per type.
// operationId: ExampleMultiAuth
// x-snapser-auth-types: ["user", "api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
//
// responses:
//   200:
//     description: Success
//     schema:
//       $ref: '#/definitions/SuccessMessageSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func ExampleMultiAuth(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	userID := vars["user_id"]

	// TODO: add your business logic here.
	writeJSON(w, http.StatusOK, SuccessMessageSchema{
		Message: fmt.Sprintf("Hello, request for user %s passed multi-auth", userID),
	})
}
