# BYOSnap Core Go Example

A minimal BYOSnap starter scaffold built with Go 1.21 and Gorilla Mux. Every endpoint Snapser expects is present, but each handler body is a stub that returns a simple placeholder and carries a `// TODO`. Use this as the starting point for your own microservice, and see `advanced/byosnap-go` for complete, working implementations.

## What's included

This scaffold wires up the boilerplate so you can focus on your business logic:

- **Configuration Tool (UI Builder)**: GET/PUT settings endpoints for the Snapser-managed configuration UI (stubbed)
- **Custom HTML Configuration Tool**: GET/PUT endpoints for a custom HTML-based configuration interface (stubbed)
- **Custom HTML User Manager Tool**: GET/POST endpoints for per-user data via a custom HTML interface (stubbed)
- **Snapend Sync/Clone (Import/Export)**: Export/import/validate settings across environments (stubbed)
- **GDPR User Data**: Get, update, and delete user data (stubbed)
- **Example business endpoints**: Five example endpoints demonstrating each Snapser auth exposure (User, Api-Key, Internal, Admin SDK, and multi-auth)
- **Auth middleware, CORS, health check**: Ready to use
- **Swagger/OpenAPI**: go-swagger annotations with `x-snapser-auth-types` extensions

## Prerequisites

- [Go 1.21+](https://golang.org/dl/)
- [go-swagger](https://goswagger.io/) (for Swagger generation)
- Docker (for building container images and OpenAPI conversion)

## Development

### Run Locally

```bash
go run .
```

The server starts on `http://localhost:5003`.

### Generate Swagger JSON

```bash
./generate_swagger.sh
```

This generates `./snapser-resources/swagger2x.json` (Swagger 2.0) and then converts it to `./snapser-resources/swagger.json` (OpenAPI 3.0).

### Build Docker Image

```bash
docker build -t byosnap-core-go .
docker run -p 5003:5003 byosnap-core-go
```

## Project Structure

```
byosnap-go/
├── main.go               # Entry point with all route handlers (stubbed)
├── models.go             # Swagger model definitions
├── middleware.go         # Authorization middleware
├── constants.go          # BYOSnapID / APIPrefix, header keys, auth types
├── go.mod / go.sum       # Go module dependencies
├── Dockerfile            # Multi-stage Docker build (Go 1.21, Alpine ARM64)
├── generate_swagger.sh   # Swagger generation script
├── snapser-resources/    # Snapser configuration files
├── README.md             # This file
└── GOTCHAS.md            # Important development notes
```

## API Endpoints

The route prefix is built from `BYOSnapID` in `constants.go` (`/v1/byosnap-core`). Change it in one place instead of editing every route string.

### Configuration Tool (Internal Auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/byosnap-core/settings` | Get configuration settings |
| PUT | `/v1/byosnap-core/settings` | Update configuration settings |
| GET | `/v1/byosnap-core/settings/custom` | Get custom HTML config |
| PUT | `/v1/byosnap-core/settings/custom` | Update custom HTML config |

### Export/Import (Internal Auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/byosnap-core/settings/export` | Export all env settings |
| POST | `/v1/byosnap-core/settings/import` | Import settings |
| POST | `/v1/byosnap-core/settings/validate-import` | Validate before import |

### User Manager (Internal Auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/byosnap-core/settings/users/{user_id}/custom` | Get user data (custom) |
| POST | `/v1/byosnap-core/settings/users/{user_id}/custom` | Update user data (custom) |
| GET | `/v1/byosnap-core/settings/users/{user_id}/data` | Get user data (GDPR) |
| PUT | `/v1/byosnap-core/settings/users/{user_id}/data` | Update user data |
| DELETE | `/v1/byosnap-core/settings/users/{user_id}/data` | Delete user data (GDPR) |

### Example Business APIs
Each example shows how to expose an API over a Snapser auth type. `admin` is not an auth type — it only surfaces the API in the Admin SDK; requests still arrive via the internal gateway.

| Method | Path | Auth Types |
|--------|------|------------|
| GET | `/v1/byosnap-core/users/{user_id}/example` | user |
| GET | `/v1/byosnap-core/example/api-key` | api-key |
| GET | `/v1/byosnap-core/example/internal` | internal |
| GET | `/v1/byosnap-core/example/admin` | admin (surfaced in Admin SDK; internal gateway) |
| GET | `/v1/byosnap-core/users/{user_id}/example/multi-auth` | user, api-key, internal |

### System
| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Health check |

## Filling in the stubs

Each handler returns a placeholder and carries a `// TODO`. To implement real logic (persisting data, calling other Snaps):

1. Generate the `snapser_internal` SDK from the Storage service OpenAPI spec
2. Place the generated code in a `snapser_internal/` directory
3. Uncomment the `snapser_internal` import and `storageClient` variable in `main.go`
4. Replace each stub body with your logic — see the matching handler in `advanced/byosnap-go`

## Eventbus

The scaffold includes best-effort stubs for the Snapser Eventbus in `eventbus.go`. Internal calls target the Eventbus service at the URL in the `SNAPEND_EVENTBUS_HTTP_URL` env var and carry the `Gateway: internal` header (value from `SNAPEND_INTERNAL_HEADER`, default `internal`). If `SNAPEND_EVENTBUS_HTTP_URL` is not set, the outbound calls are logged and skipped. Three pieces:

- **`registerEventTypes()`** — called once from `main()` on startup. Best-effort: it logs success/failure and never blocks or crashes boot. Sends `PUT {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/event-types/byosnap-core` to declare the custom event types this Snap emits. Edit the `event_types` list (`// TODO`) for your Snap.
- **`publishEvent(subject, recipients, message)`** — a reusable helper that sends `POST {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/events/byosnap-core/{subject}` to publish an event. It is not wired into any endpoint — call it from your own business logic where an event should fire (see the doc comment in `eventbus.go` for example usage).
- **Inbound receiver `POST /internal/events`** — a reserved, root-level route (no `/v1` prefix, no BYOSnap id, like `/healthz`) the Eventbus POSTs to in order to deliver events. The `eventHandler` stub reads and logs the body and returns 200; add your parse + subject-switch logic (`// TODO`). It has no `swagger:operation` annotation, so it stays out of the generated SDK spec.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SNAPEND_STORAGE_HTTP_URL` | Storage service endpoint URL |
| `SNAPEND_EVENTBUS_HTTP_URL` | Eventbus service endpoint URL (used for registering event types and publishing events; if unset the Eventbus calls are skipped) |
| `SNAPEND_INTERNAL_HEADER` | Gateway header value for internal calls (default: "internal") |
| `BYOSNAP_VERSION` | Version string for export responses (default: "v1.0.0") |
| `SNAPSER_ENVIRONMENT` | Current environment (DEVELOPMENT, STAGING, PRODUCTION) |
