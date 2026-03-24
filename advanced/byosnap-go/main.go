// Package main BYOSnap Advanced Go Example
//
// BYOSnap Advanced Go Example
// with restful endpoints demonstrating configuration tools, import/export, GDPR user data, and Storage API integration.
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

// TODO: Uncomment when snapser_internal SDK is generated
// import snapser_internal "snapser_internal"
// var storageClient *snapser_internal.APIClient

func main() {
	r := mux.NewRouter()

	// Configure CORS
	corsOpts := handlers.AllowedOrigins([]string{"*"}) // Allows all origins
	corsHeaders := handlers.AllowedHeaders([]string{"Content-Type", "Token", "Api-Key", "App-Key", "Gateway", "User-Id"})
	corsMethods := handlers.AllowedMethods([]string{"GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"})

	// Health Check Endpoint
	r.HandleFunc("/healthz", HealthCheckHandler).Methods("GET")

	// --- A i]: Configuration Tool: Built using the Snapser UI Builder ---
	getSettingsHandler := http.HandlerFunc(GetSettings)
	r.Handle("/v1/byosnap-advanced/settings",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(getSettingsHandler)).Methods("GET")

	updateSettingsHandler := http.HandlerFunc(UpdateSettings)
	r.Handle("/v1/byosnap-advanced/settings",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(updateSettingsHandler)).Methods("PUT")

	// --- A ii]: New Configuration Tool: Custom HTML Snap Configuration Tool ---
	getSettingsCustomHandler := http.HandlerFunc(GetSettingsCustom)
	r.Handle("/v1/byosnap-advanced/settings/custom",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(getSettingsCustomHandler)).Methods("GET")

	updateSettingsCustomHandler := http.HandlerFunc(UpdateSettingsCustom)
	r.Handle("/v1/byosnap-advanced/settings/custom",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(updateSettingsCustomHandler)).Methods("PUT")

	// --- B: Snapend Sync|Clone: Import/Export ---
	exportSettingsHandler := http.HandlerFunc(ExportSettings)
	r.Handle("/v1/byosnap-advanced/settings/export",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(exportSettingsHandler)).Methods("GET")

	importSettingsHandler := http.HandlerFunc(ImportSettings)
	r.Handle("/v1/byosnap-advanced/settings/import",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(importSettingsHandler)).Methods("POST")

	validateImportHandler := http.HandlerFunc(ValidateImportSettings)
	r.Handle("/v1/byosnap-advanced/settings/validate-import",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(validateImportHandler)).Methods("POST")

	// --- A iii]: User Manager Tool: Custom HTML User Manager Tool ---
	getUserDataCustomHandler := http.HandlerFunc(GetUserDataCustom)
	r.Handle("/v1/byosnap-advanced/settings/users/{user_id}/custom",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(getUserDataCustomHandler)).Methods("GET")

	updateUserDataCustomHandler := http.HandlerFunc(UpdateUserDataCustom)
	r.Handle("/v1/byosnap-advanced/settings/users/{user_id}/custom",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(updateUserDataCustomHandler)).Methods("POST")

	// --- C: User Tool: GDPR Endpoints ---
	getUserDataHandler := http.HandlerFunc(GetUserData)
	r.Handle("/v1/byosnap-advanced/settings/users/{user_id}/data",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(getUserDataHandler)).Methods("GET")

	updateUserDataHandler := http.HandlerFunc(UpdateUserData)
	r.Handle("/v1/byosnap-advanced/settings/users/{user_id}/data",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(updateUserDataHandler)).Methods("PUT")

	deleteUserDataHandler := http.HandlerFunc(DeleteUserData)
	r.Handle("/v1/byosnap-advanced/settings/users/{user_id}/data",
		validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(deleteUserDataHandler)).Methods("DELETE")

	// --- Test Auth Methods ---
	testUserAuthHandler := http.HandlerFunc(TestUserAuth)
	r.Handle("/v1/byosnap-advanced/user-auth/{user_id}",
		validateAuthorization([]string{AuthTypeHeaderValueUserAuth}, "user_id")(testUserAuthHandler)).Methods("GET")

	testApiKeyAuthHandler := http.HandlerFunc(TestApiKeyAuth)
	r.Handle("/v1/byosnap-advanced/api-key-auth",
		validateAuthorization([]string{AuthTypeHeaderValueApiKeyAuth}, "")(testApiKeyAuthHandler)).Methods("GET")

	// --- Regular API Endpoints exposed by the Snap ---
	getActiveCharactersHandler := http.HandlerFunc(GetActiveCharacters)
	r.Handle("/v1/byosnap-advanced/users/{user_id}/characters/active",
		validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(getActiveCharactersHandler)).Methods("GET")

	// TODO: Uncomment when snapser_internal SDK is generated
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

// ===========================================================================
// A i]: Configuration Tool: Built using the Snapser UI Builder
// ===========================================================================

// GetSettings returns the settings for the characters microservice
// swagger:operation GET /v1/byosnap-advanced/settings getSettings
// ---
// summary: Configuration Tool
// description: Get the settings for the characters microservice. This endpoint is called by the Snapser Configuration Tool.
// operationId: GetSettings
// x-snapser-auth-types: ["internal"]
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
	_ = blobOwnerKey // Used when Storage SDK is connected

	// TODO: Uncomment when snapser_internal SDK is generated
	// config := snapser_internal.NewConfiguration()
	// config.Servers[0].URL = os.Getenv(StorageHTTPURLEnvKey)
	// client := snapser_internal.NewAPIClient(config)
	// req := client.StorageServiceAPI.StorageGetBlob(r.Context()).
	//   AccessType(PrivateAccessType).
	//   BlobKey(CharacterSettingsBlobKey).
	//   OwnerId(blobOwnerKey).
	//   Gateway(getEnv(InternalHeaderEnvKey, DefaultInternalHeaderValue))
	// apiResponse, _, err := req.Execute()
	// if err == nil && apiResponse != nil {
	//   var parsed interface{}
	//   json.Unmarshal([]byte(apiResponse.GetValue()), &parsed)
	//   writeJSON(w, http.StatusOK, parsed)
	//   return
	// }

	writeJSON(w, http.StatusOK, defaultSettings)
}

// UpdateSettings updates the settings for the characters microservice
// swagger:operation PUT /v1/byosnap-advanced/settings updateSettings
// ---
// summary: Configuration Tool
// description: Update the settings for the characters microservice. This endpoint is called by the Snapser Configuration Tool.
// operationId: UpdateSettings
// x-snapser-auth-types: ["internal"]
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
	_ = blobOwnerKey // Used when Storage SDK is connected

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

	// TODO: Add any custom validation here and on error return:
	// writeError(w, http.StatusBadRequest, "Duplicate characters found")

	// TODO: Uncomment when snapser_internal SDK is generated
	// 1. StorageGetBlob to get current CAS
	// 2. StorageReplaceBlob with the new data and CAS
	// (see Python example for full flow)

	writeJSON(w, http.StatusOK, blobData)
}

// ===========================================================================
// A ii]: New Configuration Tool: Custom HTML Snap Configuration Tool
// ===========================================================================

// GetSettingsCustom returns the settings for the custom HTML configuration tool
// swagger:operation GET /v1/byosnap-advanced/settings/custom getSettingsCustom
// ---
// summary: Custom Configuration Tool
// description: Get the settings for the custom HTML configuration tool.
// operationId: GetSettingsCustom
// x-snapser-auth-types: ["internal"]
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
	_ = blobOwnerKey // Used when Storage SDK is connected

	// TODO: Uncomment when snapser_internal SDK is generated
	// StorageGetBlob with PrivateAccessType, CharacterSettingsBlobKey, blobOwnerKey
	// If found, wrap in CustomSettingsPayload{Payload: parsed}

	writeJSON(w, http.StatusOK, defaultSettings)
}

// UpdateSettingsCustom updates the settings from the custom HTML configuration tool
// swagger:operation PUT /v1/byosnap-advanced/settings/custom updateSettingsCustom
// ---
// summary: Custom Configuration Tool
// description: Update the settings from the custom HTML configuration tool.
// operationId: UpdateSettingsCustom
// x-snapser-auth-types: ["internal"]
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
	_ = blobOwnerKey // Used when Storage SDK is connected

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

	// TODO: Uncomment when snapser_internal SDK is generated
	// 1. StorageGetBlob to get current CAS
	// 2. StorageReplaceBlob with the new data and CAS

	writeJSON(w, http.StatusOK, blobData)
}

// ===========================================================================
// A iii]: User Manager Tool: Custom HTML User Manager Tool
// ===========================================================================

// GetUserDataCustom gets the user data for the custom HTML User Manager tool
// swagger:operation GET /v1/byosnap-advanced/settings/users/{user_id}/custom getUserDataCustom
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

	// TODO: Uncomment when snapser_internal SDK is generated
	// StorageGetBlob with ProtectedAccessType, CharactersBlobKey, userID
	// If found, wrap in CustomSettingsPayload{Payload: parsed}

	writeJSON(w, http.StatusOK, defaultPayload)
}

// UpdateUserDataCustom updates the user data for the custom HTML User Manager tool
// swagger:operation POST /v1/byosnap-advanced/settings/users/{user_id}/custom updateUserDataCustom
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

	// TODO: Uncomment when snapser_internal SDK is generated
	// 1. StorageGetBlob with ProtectedAccessType, CharactersBlobKey, userID to get CAS
	// 2. StorageReplaceBlob with the new data and CAS

	writeJSON(w, http.StatusOK, blobData)
}

// ===========================================================================
// B: Snapend Sync|Clone: Used by Snapser's built-in configuration import export system
// ===========================================================================

// ExportSettings exports all settings across environments
// swagger:operation GET /v1/byosnap-advanced/settings/export exportSettings
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
			"dev":   getDefaultCharactersPayload(),
			"stage": getDefaultCharactersPayload(),
			"prod":  getDefaultCharactersPayload(),
		},
	}

	// Remember when storing these blobs we are storing them with
	// `characters_dev`, `characters_stage` and `characters_prod` as the owner_id
	// blobKeyIDs := []string{
	// 	CharactersToolID + "_dev",
	// 	CharactersToolID + "_stage",
	// 	CharactersToolID + "_prod",
	// }

	// TODO: Uncomment when snapser_internal SDK is generated
	// StorageBatchGetBlobs with PrivateAccessType, CharacterSettingsBlobKey, blobKeyIDs
	// For each result, parse the value and update response.Data[env][CharactersToolID]

	writeJSON(w, http.StatusOK, response)
}

// ImportSettings imports settings across environments
// swagger:operation POST /v1/byosnap-advanced/settings/import importSettings
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

	// Validate the incoming structure
	if !validateExportStructure(&settingsData) {
		writeError(w, http.StatusInternalServerError, "Invalid JSON")
		return
	}

	// TODO: Uncomment when snapser_internal SDK is generated
	// Build blob payloads for dev, stage, prod with cas="0" (force replace)
	// StorageBatchReplaceBlob with all three blob payloads

	writeJSON(w, http.StatusOK, SuccessMessageSchema{Message: "Success"})
}

// ValidateImportSettings validates settings before importing
// swagger:operation POST /v1/byosnap-advanced/settings/validate-import validateImportSettings
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

	// Perform basic validation. You can add more validation by fetching the
	// settings from storage and comparing with the incoming settings.
	if !validateExportStructure(&settingsData) {
		writeError(w, http.StatusInternalServerError, "Invalid JSON")
		return
	}

	writeJSON(w, http.StatusOK, settingsData)
}

// validateExportStructure checks that the export data has the required structure
func validateExportStructure(data *ExportSettingsSchema) bool {
	if data.Data == nil {
		return false
	}
	for _, env := range []string{"dev", "stage", "prod"} {
		envData, ok := data.Data[env]
		if !ok {
			return false
		}
		if _, ok := envData[CharactersToolID]; !ok {
			return false
		}
	}
	return true
}

// ===========================================================================
// C: User Tool: Get, Update and Delete User data: GDPR
// ===========================================================================

// GetUserData gets user data (GDPR)
// swagger:operation GET /v1/byosnap-advanced/settings/users/{user_id}/data getUserData
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
	gateway := r.Header.Get(GatewayHeaderKey)
	if gateway == "" || gateway != GatewayHeaderValueInternalOrigin {
		writeError(w, http.StatusUnauthorized, "Unauthorized")
		return
	}

	// vars := mux.Vars(r)
	// userID := vars["user_id"]

	// TODO: Uncomment when snapser_internal SDK is generated
	// StorageGetBlob with PrivateAccessType, CharactersBlobKey, userID
	// If found, parse and return the value
	// If not found, return BadRequest with "No data"

	writeJSON(w, http.StatusOK, map[string]interface{}{})
}

// UpdateUserData updates user data (GDPR)
// swagger:operation PUT /v1/byosnap-advanced/settings/users/{user_id}/data updateUserData
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
	gateway := r.Header.Get(GatewayHeaderKey)
	if gateway == "" || gateway != GatewayHeaderValueInternalOrigin {
		writeError(w, http.StatusUnauthorized, "Unauthorized")
		return
	}

	// TODO: Implement user data update using Storage API
	writeJSON(w, http.StatusOK, map[string]interface{}{})
}

// DeleteUserData deletes user data (GDPR right-to-be-forgotten)
// swagger:operation DELETE /v1/byosnap-advanced/settings/users/{user_id}/data deleteUserData
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
	gateway := r.Header.Get(GatewayHeaderKey)
	if gateway == "" || gateway != GatewayHeaderValueInternalOrigin {
		writeError(w, http.StatusUnauthorized, "Unauthorized")
		return
	}

	// vars := mux.Vars(r)
	// userID := vars["user_id"]

	// TODO: Uncomment when snapser_internal SDK is generated
	// StorageDeleteBlob with PrivateAccessType, CharactersBlobKey, userID
	// If response is nil, return BadRequest with "No blob"

	writeJSON(w, http.StatusOK, map[string]interface{}{})
}

// ===========================================================================
// Regular API Endpoints exposed by the Snap
// ===========================================================================

// GetActiveCharacters returns active characters for a user
// swagger:operation GET /v1/byosnap-advanced/users/{user_id}/characters/active getActiveCharacters
// ---
// summary: Character APIs
// description: Get active characters for a user. This API supports User, API-Key, and Internal auth types.
// operationId: GetActiveCharacters
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
//     description: Characters retrieved successfully
//     schema:
//       $ref: '#/definitions/CharactersResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func GetActiveCharacters(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, CharactersResponseSchema{
		Characters: []string{},
	})
}

// ===========================================================================
// Test Auth Methods
// ===========================================================================

// TestUserAuth tests user authentication
// swagger:operation GET /v1/byosnap-advanced/user-auth/{user_id} testUserAuth
// ---
// summary: Test User Auth
// description: Test user authentication. This API supports User auth type only.
// operationId: TestUserAuth
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
//     description: User auth validation passed
//     schema:
//       $ref: '#/definitions/SuccessMessageSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func TestUserAuth(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	userID := vars["user_id"]

	writeJSON(w, http.StatusOK, SuccessMessageSchema{
		Message: fmt.Sprintf("Hello User %s, you have passed the User Auth validation", userID),
	})
}

// TestApiKeyAuth tests API key authentication
// swagger:operation GET /v1/byosnap-advanced/api-key-auth testApiKeyAuth
// ---
// summary: Test API Key Auth
// description: Test API key authentication. This API supports API-Key auth type only.
// operationId: TestApiKeyAuth
// x-snapser-auth-types: ["api-key"]
//
// responses:
//   200:
//     description: API key auth validation passed
//     schema:
//       $ref: '#/definitions/SuccessMessageSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func TestApiKeyAuth(w http.ResponseWriter, r *http.Request) {
	apiKeyName := r.Header.Get("Api-Key-Name")

	writeJSON(w, http.StatusOK, SuccessMessageSchema{
		Message: fmt.Sprintf("You have passed the API Key Auth validation using the key %s", apiKeyName),
	})
}
