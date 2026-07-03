# Snapser BYOSnap — Core Examples

Minimal starter scaffolds for a new BYOSnap, one per supported language. These are the **recommended starting point** for building your own custom microservice: every endpoint Snapser expects is already wired up (auth middleware, health check, CORS, the configuration / import-export / user-data hooks, and swagger/SDK generation), but each handler body is a **stub** that returns a simple placeholder and carries a `// TODO`.

Fill in the stubs with your own logic. For complete, working implementations of every hook, see the matching example under [`advanced/`](../advanced).

## What's in each example

- **Auth middleware** that enforces the Snapser auth types (User, Api-Key, Internal).
- **`GET /healthz`** readiness endpoint (no prefix).
- **Configuration Tool hooks** — `settings` and `settings/custom` (GET/PUT) stubs.
- **User Manager hooks** — `settings/users/{user_id}/custom` (GET/POST) stubs.
- **Snapend sync / clone hooks** — `settings/export`, `settings/import`, `settings/validate-import` stubs.
- **GDPR / user-data hooks** — `settings/users/{user_id}/data` (GET/PUT/DELETE) stubs.
- **Five example business endpoints**, one per auth exposure, to copy as templates:

  | Endpoint | Exposure |
  | --- | --- |
  | `GET /v1/byosnap-core/users/{user_id}/example` | User auth |
  | `GET /v1/byosnap-core/example/api-key` | Api-Key auth |
  | `GET /v1/byosnap-core/example/internal` | Internal auth |
  | `GET /v1/byosnap-core/example/admin` | Admin SDK (guarded via the internal gateway; `admin` is an SDK-exposure tag, **not** an auth type) |
  | `GET /v1/byosnap-core/users/{user_id}/example/multi-auth` | User + Api-Key + Internal on one route (you do **not** need a separate route per auth type) |

All externally reachable routes share the `/v1/byosnap-core` prefix, defined once via a single Snap-id constant so you can rename it in one place.

## Examples

1. **[Python](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-python)** — Flask
2. **[Go](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-go)** — Gorilla Mux
3. **[Node TypeScript](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-node-ts)** — Express + tsoa
4. **[C#](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/ByoSnapCSharp)** — ASP.NET Core
5. **[Rust](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-rust-api)** — actix-web
6. **[Java](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-java)** — Spring Boot
7. **[Kotlin](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-kotlin)** — Ktor

## Using a scaffold

1. Copy the folder for your language.
2. Rename the Snap id — change the single `byosnap-core` constant to your Snap's id (this updates every route prefix).
3. Implement the stubbed handlers. Each has a `// TODO` describing what to do and a pointer to the matching `advanced/` handler for a full reference.
4. Regenerate / update the OpenAPI spec. Python, Go, Node, and C# ship a `generate_swagger` script; Java and Kotlin keep a hand-maintained `snapser-resources/swagger.json` (Java also exposes springdoc at `/v3/api-docs` for local dev); Rust has no spec step.
