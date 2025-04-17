package main

import (
	"encoding/json"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
)

// validateAuthorization dynamically checks the allowed authentication methods
func validateAuthorization(allowedAuthTypes []string, userIDResourceKey string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			gatewayHeaderValue := r.Header.Get(GatewayHeaderKey)
			isInternalCall := strings.ToLower(gatewayHeaderValue) == GatewayHeaderValueInternalOrigin
			authTypeHeaderValue := r.Header.Get(AuthTypeHeaderKey)
			isApiKeyAuth := strings.ToLower(authTypeHeaderValue) == AuthTypeHeaderValueApiKeyAuth
			userIDHeaderValue := r.Header.Get(UserIDHeaderKey)
			// If the API has a URL parameter for user_id, then use that
      // Otherwise, use the User-Id header value as the default
			targetUser := mux.Vars(r)[userIDResourceKey]
			if targetUser == "" {
				targetUser = userIDHeaderValue
			}
			isTargetUser := userIDHeaderValue == targetUser && userIDHeaderValue != ""

			validationPassed := false
			for _, authType := range allowedAuthTypes {
				switch authType {
				case GatewayHeaderValueInternalOrigin:
					if isInternalCall {
						validationPassed = true
					}
				case AuthTypeHeaderValueApiKeyAuth:
					if !isInternalCall && isApiKeyAuth {
						validationPassed = true
					}
				case AuthTypeHeaderValueUserAuth:
					if !isInternalCall && !isApiKeyAuth && isTargetUser {
						validationPassed = true
					}
				}

				if validationPassed {
					break
				}
			}

			if !validationPassed {
				w.WriteHeader(http.StatusUnauthorized)
				errorResponse := ErrorResponseSchema{
					ErrorMessage: "Unauthorized",
				}
				json.NewEncoder(w).Encode(errorResponse)
				return
			}

			next.ServeHTTP(w, r)
		})
	}
}
