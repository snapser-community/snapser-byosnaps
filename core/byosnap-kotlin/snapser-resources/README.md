# BYOSnap Core Kotlin Example

This is the documentation for your BYOSnap. Update the section below to whatever you want. This file is rendered on the Snapser web app.

## Concept
When a Snapend has the Auth snap, you get authentication and authorization sorted out for you.

### Authorization
Snapser supports three kinds of authorization schemes:
1. **user auth**: (External Access) An external client accessing your endpoint. The client passes its session token as a header `Token: $sessionToken`, which your **gateway+auth** snap validates before forwarding the calling user id down as a `User-Id` header.
1. **api-key auth**: (External Access) In the Auth Snap's configuration tool you can add API keys and nominate the APIs each key may access. The caller passes the API key with each request; your gateway+auth snap validates it before the call reaches your BYOSnap.
1. **internal auth**: (Internal Access) Use this scheme when you do NOT want any external access. Only snaps within your Snapend (like other BYOSnaps) can call the endpoint.

**[IMPORTANT]**: All external calls (user or api-key auth) are validated for you by your Gateway+Auth snap. For internal calls, your API should check for the `Gateway: internal` header to confirm the call originated inside your Snapend. See the `validateAuthorization` helper in `src/main/kotlin/com/snapser/byosnap/Application.kt`.

## Endpoints
The five example endpoints demonstrate each exposure:
1. **ExampleUserAuth**: `GET /v1/byosnap-core/users/{user_id}/example` — exposed over user auth.
1. **ExampleApiKeyAuth**: `GET /v1/byosnap-core/example/api-key` — exposed over api-key auth.
1. **ExampleInternalAuth**: `GET /v1/byosnap-core/example/internal` — internal only.
1. **ExampleAdminSdk**: `GET /v1/byosnap-core/example/admin` — surfaces in the Admin SDK (arrives via the internal gateway).
1. **ExampleMultiAuth**: `GET /v1/byosnap-core/users/{user_id}/example/multi-auth` — one endpoint reachable over user, api-key, and internal auth.
