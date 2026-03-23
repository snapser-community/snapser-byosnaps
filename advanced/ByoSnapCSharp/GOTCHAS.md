# GOTCHAS

Important things to keep in mind when developing this BYOSnap.

## URL Routing

1. **URL Prefix**: All externally accessible APIs need to start with `/v1/byosnap-advanced/`. The Snapend ID is NOT part of the URL - this allows you to use the same BYOSnap in multiple Snapends.
2. **Health Check**: The `/healthz` endpoint does NOT take any URL prefix.
3. **Settings Endpoints**: Settings endpoints use `/v1/byosnap-advanced/settings/...` and are internal-only.

## Authentication

1. **x-snapser-auth-types**: The `[SnapserAuth]` attribute generates `x-snapser-auth-types` in the Swagger JSON. This tells Snapser which auth types to expose in the SDK and API Explorer.
2. **Header Injection**: Snapser automatically adds the correct headers in the SDK and API Explorer based on the auth type. You do not need to add headers manually.
3. **Validation**: Always validate auth types in code using the `[ValidateAuthorization]` attribute, even though Snapser handles header injection.

## CORS

1. Snapser API Explorer runs in the browser. Enabling CORS allows you to test APIs via the API Explorer.
2. The `CorsController` handles OPTIONS preflight requests for all endpoints.

## Storage API

1. **CAS (Compare-And-Swap)**: All blob replacements use CAS for optimistic locking. Set `cas = "0"` to force replace.
2. **Blob Owner IDs**: The format matters. For configuration tools, use `{tool_id}_{environment}` (e.g., `characters_dev`). For user data, use the user ID directly.
3. **Access Types**: `private` blobs are internal-only. `protected` blobs are user-scoped.
4. **TTL**: Set to 0 for persistent blobs.

## Swagger Generation

1. Run `dotnet run generate-swagger` to regenerate `./snapser-resources/swagger.json`.
2. C# automatically adds `text/plain`, `application/json`, and `application/xml` to response content types. The `RemoveFormatParametersFilter` removes all but `application/json`.
3. The `SnapserAuthTypesOperationFilter` adds the `x-snapser-auth-types` extension to each operation.

## Configuration Tools

1. **UI Builder Tool**: Uses the `SettingsSchema` structure with sections and components. Snapser auto-generates the UI.
2. **Custom HTML Tool**: Uses a custom HTML file with the Snapser SDK for RPC calls. Supports dark/light theme.
3. **User Manager Tool**: Similar to custom HTML tool but scoped to individual users.

## Import/Export

1. **Export**: Returns settings for all environments (dev, stage, prod) with a version and timestamp.
2. **Import**: Validates the structure, then batch-replaces blobs with `cas = "0"` (force replace).
3. **Validate Import**: Pre-flight check - returns 200 if valid, 500 if invalid. No data is committed.

## SnapserInternal SDK

1. The `SnapserInternal/` directory contains auto-generated API client code.
2. Generate it from the Storage service OpenAPI spec.
3. Set the `BasePath` using the Snapser-provided environment variable (e.g., `SNAPEND_STORAGE_HTTP_URL`).
