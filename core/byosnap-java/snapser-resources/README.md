# BYOSnap Java Core Example

This is the documentation for your BYOSnap. You can update the section below to whatever you want. It is rendered on the Snapser web app.

## Concept
When a Snapend has the Auth snap, you get authentication and authorization sorted out for you.

### Authorization
Snapser supports three kinds of authorization schemes:
1. **user auth**: (External Access) Used when an external client accesses your endpoint. The client passes its session token as a header viz **Token: $sessionToken$** which your **gateway+auth** snap validates, then forwards the calling user id down via the **User-Id** header on success.
1. **api-key auth**: (External Access) In the Auth Snap's configuration tool you can add API Keys and nominate the APIs a key can access. The caller passes the Api-Key with each request; your gateway+auth snap validates it and lets validated calls reach your BYOSnap.
1. **internal auth**: (Internal Access) Use this scheme if you do not want to allow any external access to your endpoint. Only snaps within your Snapend (like other BYOSnaps) will be able to call this endpoint.

**[IMPORTANT]**: All external calls (over user or api-key auth) are validated for you by your Gateway+Auth Snap. However, for internal calls your API should check for the **Gateway: internal** header to confirm the call is indeed coming from within your Snapend. See the `@ValidateAuthorization` annotation and `AuthorizationInterceptor` in this project to understand how this works.

## Endpoints
1. **Example: User Auth** — `GET /v1/byosnap-core/users/{user_id}/example`. Exposed over user auth (surfaces in the client/game SDK).
1. **Example: Api-Key Auth** — `GET /v1/byosnap-core/example/api-key`. Exposed over api-key auth (server-to-server calls).
1. **Example: Internal Auth** — `GET /v1/byosnap-core/example/internal`. Callable only by other Snaps in the same Snapend.
1. **Example: Admin SDK** — `GET /v1/byosnap-core/example/admin`. Surfaces in the Admin SDK. `admin` is not an auth type — the request still arrives via the internal gateway.
1. **Example: Multi Auth** — `GET /v1/byosnap-core/users/{user_id}/example/multi-auth`. One endpoint reachable by user, api-key, or internal auth.

## Files in this folder
- **snapser-byosnap-profile.json**: Tells Snapser about this BYOSnap's hardware, networking, and configuration requirements.
- **swagger.json**: The authoritative, hand-authored OpenAPI 3.0 spec. Snapser uses it to generate the SDK and power the API Explorer. Note the `x-snapser-auth-types` array on each operation — it controls SDK/API-Explorer exposure per auth type.
- **snapser-snapend-manifest.json**: A sample Snapend manifest (Auth + this BYOSnap + Storage) used to spin up a test cluster.
- **README.md**: This file.
