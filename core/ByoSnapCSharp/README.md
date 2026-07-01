# BYOSnap Core C# Example

A minimal starter scaffold for a C# BYOSnap, built with ASP.NET Core (.NET 9.0). Every endpoint Snapser expects is present, but each handler body is a STUB that returns a simple placeholder and carries a `// TODO` describing what you would implement here.

Fill in the stubs with your own logic. When you need to persist data, call other Snaps, or wire up the configuration/import-export tooling, look at the matching handler in `advanced/ByoSnapCSharp` for a complete, working reference.

## Features

This scaffold wires up the following Snapser BYOSnap capabilities (all stubbed):

- **Configuration Tool (UI Builder)**: GET/PUT settings endpoints for the Snapser-managed configuration UI
- **Custom HTML Configuration Tool**: GET/PUT endpoints for a custom HTML-based configuration interface
- **Custom HTML User Manager Tool**: GET/POST endpoints for per-user data via a custom HTML interface
- **Snapend Sync/Clone (Import/Export)**: Export and import settings across environments (dev, stage, prod)
- **GDPR User Data**: Get, update, and delete user data (right-to-be-forgotten)
- **Example Business APIs**: Five example endpoints demonstrating each Snapser auth exposure (User, Api-Key, Internal, Admin SDK, and a single multi-auth route)
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
docker build -t byosnap-core-csharp .
docker run -p 5003:5003 byosnap-core-csharp
```

## Project Structure

```
ByoSnapCSharp/
├── Attributes/           # Custom attributes for Swagger and auth
├── Controllers/          # API controllers
│   ├── SettingsController.cs       # Configuration tool endpoints (GET/PUT /settings, /settings/custom)
│   ├── ExportImportController.cs   # Export/Import/Validate endpoints
│   ├── UserManagerController.cs    # User manager + GDPR endpoints
│   ├── ExampleController.cs        # Example business APIs (one per auth type)
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
| GET | `/v1/byosnap-core/settings/users/{UserId}/custom` | Get user data (custom) |
| POST | `/v1/byosnap-core/settings/users/{UserId}/custom` | Update user data (custom) |
| GET | `/v1/byosnap-core/settings/users/{UserId}/data` | Get user data (GDPR) |
| PUT | `/v1/byosnap-core/settings/users/{UserId}/data` | Update user data |
| DELETE | `/v1/byosnap-core/settings/users/{UserId}/data` | Delete user data (GDPR) |

### Example Business APIs
These demonstrate each Snapser auth exposure. The `[SnapserAuth(...)]` attribute controls SDK/tool exposure (`x-snapser-auth-types`) and the matching `[ValidateAuthorization(...)]` enforces it at runtime.

| Method | Path | Auth Types | Description |
|--------|------|------------|-------------|
| GET | `/v1/byosnap-core/users/{UserId}/example` | user | Exposed over User auth; surfaces in the client/game SDK |
| GET | `/v1/byosnap-core/example/api-key` | api-key | Exposed over Api-Key auth; server-to-server calls |
| GET | `/v1/byosnap-core/example/internal` | internal | Callable only by other Snaps (internal gateway) |
| GET | `/v1/byosnap-core/example/admin` | admin | Surfaces in the Admin SDK. `admin` is a tag, NOT an auth type — the request still arrives via the internal gateway |
| GET | `/v1/byosnap-core/users/{UserId}/example/multi-auth` | user, api-key, internal | One endpoint accepting multiple auth types — no separate route per type |

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
