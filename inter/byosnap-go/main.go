// Package main BYOSnap Intermediate Go Example
//
// BYOSnap Intermediate Go Example
// with restful endpoints
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
	"log"
	"io"
	"net/http"
	"os"
	snapser_internal "snapser_internal"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
)

var profilesClient *snapser_internal.APIClient

func main() {
	r := mux.NewRouter()

	// Configure CORS
	corsOpts := handlers.AllowedOrigins([]string{"*"}) // Allows all origins
	corsHeaders := handlers.AllowedHeaders([]string{"Content-Type", "Token", "Api-Key", "App-Key", "Gateway", "User-Id"})
	corsMethods := handlers.AllowedMethods([]string{"GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"})


	// Health Check Endpoint
	r.HandleFunc("/healthz", HealthCheckHandler).Methods("GET")

	// API Endpoints
	getGameHandler := http.HandlerFunc(GetGame)
	r.Handle("/v1/byosnap-inter/users/{user_id}/game", validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(getGameHandler)).Methods("GET")

	saveGameHandler := http.HandlerFunc(SaveGame)
	r.Handle("/v1/byosnap-inter/users/{user_id}/game", validateAuthorization([]string{AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(saveGameHandler)).Methods("POST")

	deleteUserHandler := http.HandlerFunc(DeleteUser)
	r.Handle("/v1/byosnap-inter/users/{user_id}", validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(deleteUserHandler)).Methods("DELETE")

	updateUserProfileHandler := http.HandlerFunc(UpdateUserProfile)
	r.Handle("/v1/byosnap-inter/users/{user_id}/profile", validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(updateUserProfileHandler)).Methods("PUT")

	//Init the snapser client
	config := snapser_internal.NewConfiguration()
	config.Servers[0].URL = os.Getenv("SNAPEND_PROFILES_HTTP_URL")
	profilesClient = snapser_internal.NewAPIClient(config)
	// Start server
	log.Println("Starting server on :5003")
	log.Fatal(http.ListenAndServe(":5003", handlers.CORS(corsOpts, corsHeaders, corsMethods)(r)))

}

// HealthCheckHandler returns ok for health checks
func HealthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Ok"))
}

// PostGameHandler handles the GET request for an API endpoint
// swagger:operation GET /v1/byosnap-inter/users/{user_id}/game postGame
// ---
// summary: Game APIs
// description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
// operationId: GetGame
// x-snapser-auth-types: ["user", "api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
// responses:
//   200:
//     description: Successfully retrieved data
//     schema:
//       $ref: '#/definitions/SuccessResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func GetGame(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	response := SuccessResponseSchema{
		API:          "GetGame",
		AuthType:     authType,
		HeaderUserID: userIdHeader,
		PathUserID:   mux.Vars(r)["user_id"],
		Message:      "success",
	}

	// Marshal the struct to JSON
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		http.Error(w, "Error creating response", http.StatusInternalServerError)
		return
	}

	// Set the content type and write the response
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonResponse)
}

// SaveGameHandler handles the POST request for an API endpoint
// swagger:operation POST /v1/byosnap-inter/users/{user_id}/game saveGame
// ---
// summary: Game APIs
// description: This API will work only with Api-Key auth. You can access this API with a valid api-key.
// operationId: SaveGame
// x-snapser-auth-types: ["api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
// responses:
//   200:
//     description: Successfully retrieved data
//     schema:
//       $ref: '#/definitions/SuccessResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func SaveGame(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	if userIdHeader == "" {
		userIdHeader = "N/A"
	}
	response := SuccessResponseSchema{
		API:          "PostGame",
		AuthType:     authType,
		HeaderUserID: userIdHeader,
		PathUserID:   mux.Vars(r)["user_id"],
		Message:      "success",
	}

	// Marshal the struct to JSON
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		http.Error(w, "Error creating response", http.StatusInternalServerError)
		return
	}

	// Set the content type and write the response
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonResponse)
}

// DeleteUserHandler handles the DELETE request for an API endpoint
// swagger:operation DELETE /v1/byosnap-inter/users/{user_id} deleteUser
// ---
// summary: User APIs
// description: This API will work only when the call is coming from within the Snapend.
// operationId: DeleteUser
// x-snapser-auth-types: ["internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
// responses:
//   200:
//     description: Successfully retrieved data
//     schema:
//       $ref: '#/definitions/SuccessResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func DeleteUser(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	if userIdHeader == "" {
		userIdHeader = "N/A"
	}
	response := SuccessResponseSchema{
		API:          "DeleteUser",
		AuthType:     authType,
		HeaderUserID: userIdHeader,
		PathUserID:   mux.Vars(r)["user_id"],
		Message:      "success",
	}

	// Marshal the struct to JSON
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		http.Error(w, "Error creating response", http.StatusInternalServerError)
		return
	}

	// Set the content type and write the response
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonResponse)
}

// UpdateUserProfileHandler handles the PUT request for an API endpoint. TODO: For you to update
// swagger:operation PUT /v1/byosnap-inter/users/{user_id}/profile updateUserProfile
// ---
// summary: User APIs
// description: This API will work only when the call is coming from within the Snapend.
// operationId: UpdateUserProfile
// x-snapser-auth-types: ["user", "api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
//   - name: profile_payload
//     in: body
//     required: true
//     description: Payload containing profile fields
//     schema:
//       $ref: "#/definitions/ProfilePayloadSchema"
// responses:
//   200:
//     description: Successfully retrieved data
//     schema:
//       $ref: '#/definitions/SuccessResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func UpdateUserProfile(w http.ResponseWriter, r *http.Request) {
	// TODO: Uncomment the code below to enable the functionality
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	if userIdHeader == "" {
		userIdHeader = "N/A"
	}
	var profilePayload ProfilePayloadSchema
	bodyBytes, _ := io.ReadAll(r.Body)
	err := json.Unmarshal(bodyBytes, &profilePayload)
	if err != nil {
		w.Write([]byte(`{"error_message": "Error un-marshalling request body"}`))
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	if profilePayload.Profile == nil {
		w.Write([]byte(`{"error_message": "Profile is required"}`))
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	req := profilesClient.ProfilesServiceAPI.ProfilesInternalUpsertProfile(r.Context(), userIdHeader).Gateway("internal").Body(snapser_internal.UpsertProfileRequest{
		Profile: profilePayload.Profile,
	})
	snapserRes, httpResp, err := req.Execute()
	if httpResp == nil {
		w.Write([]byte(`{"error_message": "Error calling snapser"}`))
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	if err != nil {
		body := httpResp.Body
		bodyBytes, _ := io.ReadAll(body)
		body.Close()

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(httpResp.StatusCode)
		w.Write(bodyBytes)
		return
	}

	jsonResponse, err := json.Marshal(snapserRes)
	if err != nil {
		w.WriteHeader(httpResp.StatusCode)
		w.Write([]byte(`{"error_message": "Error creating response"}`))
		return
	}

	response := SuccessResponseSchema{
		API:          "UpdateUserProfile",
		AuthType:     authType,
		HeaderUserID: userIdHeader,
		PathUserID:   mux.Vars(r)["user_id"],
		Message:     string(jsonResponse),
	}

	// Marshal the struct to JSON
	jsonResponse, err = json.Marshal(response)
	if err != nil {
		http.Error(w, "Error creating response", http.StatusInternalServerError)
		return
	}

	// Set the content type and write the response
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonResponse)
}
