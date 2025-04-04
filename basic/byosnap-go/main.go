// Package main BYOSnap Basic Go Example
//
// BYOSnap Basic Go Example
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
	"net/http"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
)

func main() {
	r := mux.NewRouter()

	// Configure CORS
	corsOpts := handlers.AllowedOrigins([]string{"*"}) // Allows all origins
	corsHeaders := handlers.AllowedHeaders([]string{"X-Requested-With", "Content-Type", "Authorization"})
	corsMethods := handlers.AllowedMethods([]string{"GET", "POST", "PUT", "DELETE", "OPTIONS"})


	// Health Check Endpoint
	r.HandleFunc("/healthz", HealthCheckHandler).Methods("GET")

	// API Endpoints
	getGameHandler := http.HandlerFunc(GetGame)
	r.Handle("/v1/byosnap-basic/users/{user_id}/game", validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(getGameHandler)).Methods("GET")

	saveGameHandler := http.HandlerFunc(SaveGame)
	r.Handle("/v1/byosnap-basic/users/{user_id}/game", validateAuthorization([]string{AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(saveGameHandler)).Methods("POST")

	deleteUserHandler := http.HandlerFunc(DeleteUser)
	r.Handle("/v1/byosnap-basic/users/{user_id}", validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(deleteUserHandler)).Methods("DELETE")

	updateUserProfileHandler := http.HandlerFunc(UpdateUserProfile)
	r.Handle("/v1/byosnap-basic/users/{user_id}/profile", validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(updateUserProfileHandler)).Methods("PUT")

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
// swagger:operation GET /v1/byosnap-basic/users/{user_id}/game postGame
// ---
// summary: Game APIs
// description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
// operationId: Get Game
// x-snapser-auth-types: ["user", "api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
//   - name: Token
//     in: header
//     required: true
//     description: User Session Token
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
// swagger:operation POST /v1/byosnap-basic/users/{user_id}/game saveGame
// ---
// summary: Game APIs
// description: This API will work only with Api-Key auth. You can access this API with a valid api-key.
// operationId: Save Game
// x-snapser-auth-types: ["api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
//   - name: Token
//     in: header
//     required: true
//     description: User Session Token
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
// swagger:operation DELETE /v1/byosnap-basic/users/{user_id} deleteUser
// ---
// summary: User APIs
// description: This API will work only when the call is coming from within the Snapend.
// operationId: Delete User
// x-snapser-auth-types: ["internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
//   - name: Token
//     in: header
//     required: true
//     description: User Session Token
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
// swagger:operation PUT /v1/byosnap-basic/users/{user_id}/profile updateUserProfile
// ---
// summary: User APIs
// description: This API will work only when the call is coming from within the Snapend.
// operationId: Update User Profile
// x-snapser-auth-types: ["user", "api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
//   - name: Token
//     in: header
//     required: true
//     description: User Session Token
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
func UpdateUserProfile(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	if userIdHeader == "" {
		userIdHeader = "N/A"
	}
	response := SuccessResponseSchema{
		API:          "UpdateUserProfile",
		AuthType:     authType,
		HeaderUserID: userIdHeader,
		PathUserID:   mux.Vars(r)["user_id"],
		Message:      "TODO: Add your message here",
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
