# BYOSnap Advanced C# Example

An advanced BYOSnap example built with ASP.NET Core (.NET 9.0), demonstrating configuration tools, import/export, GDPR user data, and Storage API integration.

## Features

This example demonstrates the following Snapser BYOSnap capabilities:

- **Configuration Tool (UI Builder)**: GET/PUT settings endpoints for the Snapser-managed configuration UI
- **Custom HTML Configuration Tool**: GET/PUT endpoints for a custom HTML-based configuration interface
- **Custom HTML User Manager Tool**: GET/POST endpoints for per-user data via a custom HTML interface
- **Snapend Sync/Clone (Import/Export)**: Export and import settings across environments (dev, stage, prod)
- **GDPR User Data**: Get, update, and delete user data (right-to-be-forgotten)
- **Public Character APIs**: Externally accessible API for retrieving active characters
- **Multi-Environment Support**: dev, stage, prod environment isolation
- **Swagger/OpenAPI**: Auto-generated API documentation with `x-snapser-auth-types` extensions

## Prerequisites

- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0)
- Docker (for building container images)

## Development

### Run Locally

```bash
dotnet run
```

The server starts on `http://localhost:5003`. Swagger UI is available at `http://localhost:5003/swagger`.

### Generate Swagger JSON

```bash
dotnet run generate-swagger
# or
./generate_swagger.sh
```

This generates `./snapser-resources/swagger.json`.

### Build Docker Image

```bash
docker build -t byosnap-advanced-csharp .
docker run -p 5003:5003 byosnap-advanced-csharp
```

## Project Structure

```
ByoSnapCSharp/
├── Attributes/           # Custom attributes for Swagger and auth
├── Controllers/          # API controllers
│   ├── SettingsController.cs       # Configuration tool endpoints (GET/PUT /settings, /settings/custom)
│   ├── ExportImportController.cs   # Export/Import/Validate endpoints
│   ├── UserManagerController.cs    # User manager + GDPR endpoints
│   ├── CharactersController.cs     # Public character APIs
│   ├── HealthController.cs         # Health check endpoint
│   └── CorsController.cs          # CORS preflight handlers
├── Filters/              # Swagger operation filters
├── Models/               # Request/response DTOs
├── Utilities/            # Constants and shared values
├── SnapserInternal/      # Auto-generated SDK (generate separately)
├── snapser-resources/    # Snapser configuration files
├── Program.cs            # Application entry point
├── Startup.cs            # Service and middleware configuration
├── Dockerfile            # Container build instructions
└── ByoSnapCSharp.csproj  # Project file
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
| GET | `/v1/byosnap-advanced/settings/users/{UserId}/custom` | Get user data (custom) |
| POST | `/v1/byosnap-advanced/settings/users/{UserId}/custom` | Update user data (custom) |
| GET | `/v1/byosnap-advanced/settings/users/{UserId}/data` | Get user data (GDPR) |
| PUT | `/v1/byosnap-advanced/settings/users/{UserId}/data` | Update user data |
| DELETE | `/v1/byosnap-advanced/settings/users/{UserId}/data` | Delete user data (GDPR) |

### Public APIs (User + API-Key + Internal Auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/byosnap-advanced/users/{UserId}/characters/active` | Get active characters |

### System
| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Health check |

## Storage Integration

The Storage API calls are stubbed with TODO comments. To enable them:

1. Generate the SnapserInternal SDK from the Storage service OpenAPI spec
2. Place the generated code in the `SnapserInternal/` directory
3. Uncomment the `using SnapserInternal.*` imports in the controllers
4. Uncomment the Storage API call blocks

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SNAPEND_STORAGE_HTTP_URL` | Storage service endpoint URL |
| `SNAPEND_INTERNAL_HEADER` | Gateway header value for internal calls (default: "internal") |
| `BYOSNAP_VERSION` | Version string for export responses (default: "v1.0.0") |
| `SNAPSER_ENVIRONMENT` | Current environment (DEVELOPMENT, STAGING, PRODUCTION) |
