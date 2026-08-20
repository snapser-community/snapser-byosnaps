package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	"google.golang.org/grpc/metadata"
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
//  3. Forward the request id on outbound Snap-to-Snap calls: the X-Request-Id
//     header over HTTP, the `x-request-id` metadata key over gRPC (see
//     outgoingInternalContext). Startup calls have no request id, so the field
//     is omitted there.
// ===========================================================================

const (
	// RequestIDHeaderKey carries the Snapser request id on inbound HTTP requests
	// (the Eventbus webhook included).
	RequestIDHeaderKey = "X-Request-Id"
	// RequestIDMetadataKey is the same id on gRPC calls. gRPC metadata keys are
	// lowercase.
	RequestIDMetadataKey = "x-request-id"
)

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
func requestLogging(c *gin.Context) {
	requestID := c.GetHeader(RequestIDHeaderKey)
	if requestID == "" {
		// gRPC-gateway style callers send the id as metadata instead of a header.
		if md, ok := metadata.FromIncomingContext(c.Request.Context()); ok {
			if values := md.Get(RequestIDMetadataKey); len(values) > 0 {
				requestID = values[0]
			}
		}
	}
	requestID = sanitizeRequestID(requestID)

	requestScopedLogger := logger
	if requestID != "" {
		requestScopedLogger = logger.With(slog.String("request-id", requestID))
	}
	ctx := context.WithValue(c.Request.Context(), loggerContextKey, requestScopedLogger)
	ctx = context.WithValue(ctx, requestIDContextKey, requestID)
	c.Request = c.Request.WithContext(ctx)

	c.Next()
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

// outgoingInternalContext returns ctx with the metadata every internal gRPC
// call needs: the internal gateway marker, plus the request id when the call is
// made on behalf of a request so the downstream Snap's logs correlate.
func outgoingInternalContext(ctx context.Context) context.Context {
	pairs := []string{"gateway", "internal"}
	if requestID := sanitizeRequestID(requestIDFromContext(ctx)); requestID != "" {
		pairs = append(pairs, RequestIDMetadataKey, requestID)
	}
	return metadata.NewOutgoingContext(ctx, metadata.Pairs(pairs...))
}
