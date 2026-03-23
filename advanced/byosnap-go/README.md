# BYOSnap Advanced Go Example

An advanced BYOSnap example built with Go 1.21 and Gorilla Mux, demonstrating configuration tools, import/export, GDPR user data, and Storage API integration.

## Features

This example demonstrates the following Snapser BYOSnap capabilities:

- **Configuration Tool (UI Builder)**: GET/PUT settings endpoints for the Snapser-managed configuration UI
- **Custom HTML Configuration Tool**: GET/PUT endpoints for a custom HTML-based configuration interface
- **Custom HTML User Manager Tool**: GET/POST endpoints for per-user data via a custom HTML interface
- **Snapend Sync/Clone (Import/Export)**: Export and import settings across environments (dev, stage, prod)
- **GDPR User Data**: Get, update, and delete user data (right-to-be-forgotten)
- **Public Character APIs**: Externally accessible API for retrieving active characters
- **Multi-Environment Support**: dev, stage, prod environment isolation
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
docker build -t byosnap-advanced-go .
docker run -p 5003:5003 byosnap-advanced-go
```

## Project Structure

```
byosnap-go/
├── main.go               # Entry point with all route handlers
├── models.go             # Swagger model definitions
├── middleware.go          # Authorization middleware
├── constants.go          # Constants for headers, auth types, storage
├── go.mod / go.sum       # Go module dependencies
├── Dockerfile            # Multi-stage Docker build (Go 1.21, Alpine ARM64)
├── generate_swagger.sh   # Swagger generation script
├── snapser_internal/     # Auto-generated SDK (generate separately)
├── snapser-resources/    # Snapser configuration files
├── README.md             # This file
└── GOTCHAS.md            # Important development notes
```

## API Endpoints

### Configuration Tool (Internal Auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/byosnap-advanced/settings` | Get configuration settings |
| PUT | `/v1/byosnap-advanced/settings` | Update configuration settings |
| GET | `/v1/byosnap-advanced/settings/custom` | Get custom HTML config |
| PUT | `/v1/byosnap-advanced/settings/custom` | Update custom HTML config |

### Export/Import (Internal Auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/byosnap-advanced/settings/export` | Export all env settings |
| POST | `/v1/byosnap-advanced/settings/import` | Import settings |
| POST | `/v1/byosnap-advanced/settings/validate-import` | Validate before import |

### User Manager (Internal Auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/byosnap-advanced/settings/users/{user_id}/custom` | Get user data (custom) |
| POST | `/v1/byosnap-advanced/settings/users/{user_id}/custom` | Update user data (custom) |
| GET | `/v1/byosnap-advanced/settings/users/{user_id}/data` | Get user data (GDPR) |
| PUT | `/v1/byosnap-advanced/settings/users/{user_id}/data` | Update user data |
| DELETE | `/v1/byosnap-advanced/settings/users/{user_id}/data` | Delete user data (GDPR) |

### Public APIs (User + API-Key + Internal Auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/byosnap-advanced/users/{user_id}/characters/active` | Get active characters |

### System
| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Health check |

## Storage Integration

The Storage API calls are stubbed with TODO comments. To enable them:

1. Generate the `snapser_internal` SDK from the Storage service OpenAPI spec
2. Place the generated code in the `snapser_internal/` directory
3. Uncomment the `snapser_internal` import and `storageClient` variable in `main.go`
4. Uncomment the Storage API call blocks in each handler

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SNAPEND_STORAGE_HTTP_URL` | Storage service endpoint URL |
| `SNAPEND_INTERNAL_HEADER` | Gateway header value for internal calls (default: "internal") |
| `BYOSNAP_VERSION` | Version string for export responses (default: "v1.0.0") |
| `SNAPSER_ENVIRONMENT` | Current environment (DEVELOPMENT, STAGING, PRODUCTION) |
