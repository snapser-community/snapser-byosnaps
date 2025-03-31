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
	apiOneHandler := http.HandlerFunc(ApiOneHandler)
	r.Handle("/v1/byosnap-basic/users/{user_id}/game", validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(apiOneHandler)).Methods("GET")

	apiTwoHandler := http.HandlerFunc(ApiTwoHandler)
	r.Handle("/v1/byosnap-basic/users/{user_id}/game", validateAuthorization([]string{AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(apiTwoHandler)).Methods("POST")

	apiThreeHandler := http.HandlerFunc(ApiThreeHandler)
	r.Handle("/v1/byosnap-basic/users/{user_id}", validateAuthorization([]string{GatewayHeaderValueInternalOrigin}, "user_id")(apiThreeHandler)).Methods("DELETE")

	apiFourHandler := http.HandlerFunc(ApiFourHandler)
	r.Handle("/v1/byosnap-basic/users/{user_id}/profile", validateAuthorization([]string{AuthTypeHeaderValueUserAuth, AuthTypeHeaderValueApiKeyAuth, GatewayHeaderValueInternalOrigin}, "user_id")(apiFourHandler)).Methods("PUT")

	// Start server
	log.Println("Starting server on :5003")
	log.Fatal(http.ListenAndServe(":5003", handlers.CORS(corsOpts, corsHeaders, corsMethods)(r)))
}

// HealthCheckHandler returns ok for health checks
func HealthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Ok"))
}

// ApiOneHandler handles the GET request for an API endpoint
// swagger:operation GET /v1/byosnap-basic/users/{user_id}/game apiOne
// ---
// summary: Retrieves game data for a specified user
// description: This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.
// operationId: apiOneHandler
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
func ApiOneHandler(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	response := SuccessResponseSchema{
		API:          "ApiOneHandler",
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

// ApiTwoHandler handles the POST request for an API endpoint
// swagger:operation POST /v1/byosnap-basic/users/{user_id}/game apiTwo
// ---
// summary: API Two
// description: This API will work only with Api-Key auth. You can access this API with a valid api-key.
// operationId: API Two
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
func ApiTwoHandler(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	if userIdHeader == "" {
		userIdHeader = "N/A"
	}
	response := SuccessResponseSchema{
		API:          "ApiTwoHandler",
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

// ApiThreeHandler handles the DELETE request for an API endpoint
// swagger:operation DELETE /v1/byosnap-basic/users/{user_id} apiThree
// ---
// summary: API Three
// description: This API will work only when the call is coming from within the Snapend.
// operationId: API Three
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
func ApiThreeHandler(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	if userIdHeader == "" {
		userIdHeader = "N/A"
	}
	response := SuccessResponseSchema{
		API:          "ApiThreeHandler",
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

// ApiFourHandler handles the PUT request for an API endpoint. TODO: For you to update
// swagger:operation PUT /v1/byosnap-basic/users/{user_id}/profile apiFour
// ---
// summary: API Four
// description: This API will work only when the call is coming from within the Snapend.
// operationId: API Four
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
func ApiFourHandler(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	if userIdHeader == "" {
		userIdHeader = "N/A"
	}
	response := SuccessResponseSchema{
		API:          "ApiFourHandler",
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
