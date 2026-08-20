package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"strings"
)

// ===========================================================================
// Logging
//
// @GOTCHAS 👋 - Logging
//  1. Write ONE JSON object per line to stdout. Snapser reads `level`
//     (debug|info|warn|error) to color the line in the Logs tool, plus
//     `message` and `timestamp`.
//  2. Snapser correlates every log line of a request ACROSS Snaps by the
//     `request-id` field, and samples logs per request instead of per line.
//     Bind it ONCE per request (requestLogging) instead of passing it to each
//     log call.
//  3. Forward X-Request-Id on outbound Snap-to-Snap calls so the downstream
//     Snap logs the same request-id. Startup work has no request id, so the
//     field is omitted there.
// ===========================================================================

// logger writes the JSON line shape Snapser parses: `timestamp`, `level` and
// `message` instead of slog's default `time`, `LEVEL` and `msg`.
var logger = slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
	Level: slog.LevelDebug,
	ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
		switch a.Key {
		case slog.TimeKey:
			// Containers may set TZ; Snapser expects the Z form.
			a.Key = "timestamp"
			a.Value = slog.TimeValue(a.Value.Time().UTC())
		case slog.MessageKey:
			a.Key = "message"
		case slog.LevelKey:
			a.Value = slog.StringValue(strings.ToLower(a.Value.String()))
		}
		return a
	},
}))

type contextKey int

const (
	loggerContextKey contextKey = iota
	requestIDContextKey
)

// X-Request-Id is client-supplied: cap the length and allow only safe chars.
func sanitizeRequestID(v string) string {
	if len(v) > 128 {
		v = v[:128]
	}
	for _, r := range v {
		if !(r == '-' || r == '_' || r == '.' ||
			(r >= '0' && r <= '9') || (r >= 'a' && r <= 'z') || (r >= 'A' && r <= 'Z')) {
			return ""
		}
	}
	return v
}

// requestLogging binds the inbound request id to a request scoped logger, so
// every line a handler logs carries `request-id`.
func requestLogging(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		requestID := sanitizeRequestID(r.Header.Get(RequestIDHeaderKey))
		requestScopedLogger := logger
		if requestID != "" {
			requestScopedLogger = logger.With(slog.String("request-id", requestID))
		}
		ctx := context.WithValue(r.Context(), loggerContextKey, requestScopedLogger)
		ctx = context.WithValue(ctx, requestIDContextKey, requestID)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// requestLogger returns the logger bound by requestLogging. Use it in handlers.
func requestLogger(r *http.Request) *slog.Logger {
	return contextLogger(r.Context())
}

// contextLogger returns the logger bound to ctx, falling back to the base
// logger for work that runs outside a request (e.g. boot).
func contextLogger(ctx context.Context) *slog.Logger {
	if l, ok := ctx.Value(loggerContextKey).(*slog.Logger); ok {
		return l
	}
	return logger
}

// requestIDFromContext returns the request id bound to ctx. It is empty for
// work that runs outside a request.
func requestIDFromContext(ctx context.Context) string {
	requestID, _ := ctx.Value(requestIDContextKey).(string)
	return requestID
}

// forwardRequestID copies the request id onto an outbound Snap-to-Snap call so
// the downstream Snap logs correlate with this request.
func forwardRequestID(ctx context.Context, req *http.Request) {
	if requestID := sanitizeRequestID(requestIDFromContext(ctx)); requestID != "" {
		req.Header.Set(RequestIDHeaderKey, requestID)
	}
}
