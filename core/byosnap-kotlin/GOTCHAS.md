# GOTCHAS

Important things to keep in mind when developing this Ktor BYOSnap.

## URL Routing

1. **URL Prefix**: All externally accessible APIs start with `/v1/byosnap-core/`. The Snapend ID is NOT part of the URL — this lets you reuse the same BYOSnap across multiple Snapends. Every route is built from the `API_PREFIX` constant (`/v1/$BYOSNAP_ID`), so change `BYOSNAP_ID` in one place instead of editing every route string.
2. **Health Check**: The `/healthz` endpoint does NOT take any URL prefix. It is registered at the root in the `routing { }` block.
3. **Settings Endpoints**: Settings endpoints use `/v1/byosnap-core/settings/...` and are internal-only (guarded with `GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE`).
4. **Path parameters**: Ktor uses `{userId}` placeholders in the route string and `call.parameters["userId"]` to read them. The `swagger.json` uses `{user_id}` (snake_case) because that is the SDK-facing contract — the two are independent, and both are correct as shipped.

## Authentication

1. **validateAuthorization**: This is the Kotlin equivalent of the Python `validate_authorization` decorator. Ktor has no decorators, so call it as the first line of each handler: `if (!validateAuthorization(call, ...)) return@get`. It writes the 400 Unauthorized response and returns `false` on failure, so you must `return@<verb>` when it fails.
2. **Pass the same auth types to BOTH places**: the `x-snapser-auth-types` tag in `swagger.json` (which controls SDK / API Explorer exposure) AND the `validateAuthorization(...)` call (which enforces auth at runtime). Adding the swagger tag alone does NOT perform the authorization check.
3. **Header Injection**: Snapser automatically adds the correct headers in the SDK and API Explorer based on the auth type (Token for user, Api-Key for api-key, Gateway for internal). You do NOT add auth headers to the swagger yourself.
4. **`admin` is not an auth type**: Tagging an endpoint `admin` in `x-snapser-auth-types` only makes it surface in the Admin SDK. Admin-SDK requests still arrive through the internal gateway, so guard admin endpoints with `GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE`.
5. **Multiple auth types on one route**: An endpoint can accept several auth types at once (see the multi-auth example) — pass every accepted type to `validateAuthorization` and list them all in `x-snapser-auth-types`. You do NOT need a separate route per auth type.

## CORS

1. The Snapser API Explorer runs in the browser. The `install(CORS) { }` block enables cross-origin access so you can test APIs via the API Explorer.
2. CORS is configured with `anyHost()` plus the GET/POST/PUT/DELETE/OPTIONS methods and the headers Content-Type, Token, Api-Key, App-Key, Gateway, and User-Id. Ktor handles OPTIONS preflight automatically when the CORS plugin is installed — you do not need a separate preflight route.

## Swagger

1. `swagger.json` is hand-authored in `snapser-resources/`. Ktor does not auto-generate it, so when you add, rename, or remove an endpoint you must update `swagger.json` to match — include only the endpoints you want surfaced in the SDK / API Explorer.
2. Only SDK-exposed endpoints belong in `swagger.json`. The internal settings/import/export/user-data system endpoints that are guarded internal but not surfaced in the SDK are intentionally omitted (matching the other core examples).
3. Keep each operation's `x-snapser-auth-types` in sync with the `validateAuthorization` call in `Application.kt`.

## Build & Fat Jar

1. The Docker build produces a single runnable fat jar via the Ktor Gradle plugin's `buildFatJar` task (`io.ktor.plugin`). The jar lands at `build/libs/<rootProject.name>-all.jar` — here `byosnap-kotlin-all.jar`. The Dockerfile copies `build/libs/*-all.jar` to `app.jar` so the exact name does not matter.
2. **Main class**: `application { mainClass.set("com.snapser.byosnap.ApplicationKt") }`. Because `main()` lives at the top level of `Application.kt`, Kotlin compiles it into a class named `ApplicationKt` (file name + `Kt`). If you rename the file or move `main()`, update `mainClass` accordingly.
3. **Version alignment**: The `io.ktor.plugin` version in `build.gradle.kts` and `ktorVersion` in `gradle.properties` MUST match (both `2.3.12`). A mismatch can cause `buildFatJar` to behave unexpectedly.
4. **Port**: The server port (5003) is defined by `SERVER_PORT` in `Application.kt` and must match `EXPOSE` in the Dockerfile and `external_port` in `snapser-byosnap-profile.json`.

## Storage

1. When you implement the stubbed settings / user-data endpoints, persist data via the Snapser **Storage** snap, called over the internal gateway.
2. For configuration tools, use a blob owner key of the form `{tool_id}_{environment}` (e.g. `characters_dev`). For user data, use the user id directly.
