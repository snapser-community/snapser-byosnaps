# GOTCHAS

Important things to keep in mind when developing this Spring Boot BYOSnap.

## URL Routing

1. **URL Prefix**: All externally accessible APIs must start with `/v1/byosnap-core/`. The Snapend ID is NOT part of the URL — this lets you use the same BYOSnap in multiple Snapends. This prefix is built from `AppConstants.API_PREFIX`, so change `BYOSNAP_ID` in one place instead of editing every route.
   ```java
   @GetMapping(AppConstants.API_PREFIX + "/users/{userId}/example")
   ```
   Spring lets you concatenate a `public static final String` constant into the mapping value because it is a compile-time constant. Do NOT try to build the path from a non-final field or a method call — annotation values must be constant expressions.
2. **Health Check**: The `/healthz` endpoint does NOT take any URL prefix. It is served at the root.
   ```java
   @GetMapping("/healthz") // no prefix, no BYOSnap id
   ```
3. **Settings Endpoints**: Settings endpoints use `/v1/byosnap-core/settings/...` and are internal-only.
4. **Path variable name**: The auth interceptor reads the target user id from the `{userId}` path variable (see `AuthorizationInterceptor#extractPathUserId`). If you rename the path variable in a route, pass the new name via `@ValidateAuthorization(userIdPathVariable = "...")` or the user-ownership check will silently fall back to the `User-Id` header.

## Authentication

1. **`@ValidateAuthorization` enforces auth at runtime**. Adding a `x-snapser-auth-types` tag to swagger.json alone does NOT perform any authorization — it only controls SDK/API-Explorer exposure. You must ALSO annotate the handler with `@ValidateAuthorization(...)` listing the same auth types so the `AuthorizationInterceptor` enforces them.
   ```java
   @GetMapping(AppConstants.API_PREFIX + "/users/{userId}/example/multi-auth")
   @ValidateAuthorization({ AppConstants.AUTH_TYPE_USER, AppConstants.AUTH_TYPE_API_KEY, AppConstants.GATEWAY_INTERNAL_ORIGIN })
   ```
2. **A single endpoint can accept multiple auth types** — list them all in the annotation. You do not need a separate route per auth type.
3. **`admin` is not an auth type.** Tagging an operation with `admin` in swagger.json only surfaces it in the Admin SDK. Admin calls still arrive through the internal gateway, so guard admin endpoints with `GATEWAY_INTERNAL_ORIGIN`.
4. **Failure response**: On an auth failure the interceptor returns HTTP **400** with body `{"error_message":"Unauthorized"}` (matching the other core examples). It does not return 401/403.
5. **Header injection**: Snapser automatically adds the correct headers (Token / Api-Key / Gateway) in the SDK and API Explorer based on the auth type. You do not need to declare those headers in swagger.json.
6. **Interceptor is a no-op without the annotation**. `AuthorizationInterceptor` is registered on `/**`, but it only runs when the matched handler method carries `@ValidateAuthorization`. That is why `/healthz` and CORS preflights pass through untouched.

## CORS

1. The Snapser API Explorer runs in the browser. CORS is enabled in `WebConfig#addCorsMappings` so you can exercise the APIs from the API Explorer.
2. Allowed headers include `Content-Type`, `Token`, `Api-Key`, `App-Key`, `Gateway`, and `User-Id`. Spring MVC answers `OPTIONS` preflight automatically once CORS mappings are registered, so there is no separate CORS controller.

## Swagger / OpenAPI

1. The **authoritative** spec is the hand-authored `snapser-resources/swagger.json` (OpenAPI 3.0.2). Snapser reads this file to generate the SDK and power the API Explorer.
2. springdoc is included for a local `/swagger` UI convenience only. Its generated spec is NOT what Snapser consumes and does not carry the `x-snapser-auth-types` extensions — do not rely on it for publishing.
3. When you add, rename, or remove an endpoint, update `snapser-resources/swagger.json` by hand: add the path, its `operationId`, and the correct `x-snapser-auth-types` array.
4. **Only SDK-exposed endpoints belong in swagger.json.** The internal settings/GDPR system endpoints are intentionally omitted (matching the other core examples) except the import/export operations that Snapser tooling calls.

## Docker / Build

1. The Dockerfile is multi-stage: it builds with `maven:3.9-eclipse-temurin-21` and runs on `eclipse-temurin:21-jre`.
2. `finalName=app` in `pom.xml` gives a stable jar name so `COPY --from=build /app/target/app.jar app.jar` always works. If you remove that, the copy will break.
3. Build for arm64 by default (`ARG PLATFORM=linux/arm64`). Override with `--build-arg PLATFORM=linux/amd64` if needed.
4. The container `EXPOSE`s 5003 and the app's `server.port=5003` must stay in sync with `snapser-byosnap-profile.json`'s `external_port`.
