package main

import (
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
)

// validateAuthorization dynamically checks the allowed authentication methods
func validateAuthorization(allowedAuthTypes []string, userIDResourceKey string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			gatewayHeader := r.Header.Get(GatewayHeaderKey)
			isInternalCall := gatewayHeader == GatewayHeaderValueInternalOrigin
			authTypeHeader := r.Header.Get(AuthTypeHeaderKey)
			isApiKeyAuth := authTypeHeader == AuthTypeHeaderValueApiKeyAuth
			userIDHeader := r.Header.Get(UserIDHeaderKey)
			targetUser := mux.Vars(r)[userIDResourceKey]
			isTargetUser := userIDHeader == targetUser

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
