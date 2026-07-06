# Snapser BYOSnap — Core Examples

Minimal starter scaffolds for a new BYOSnap, one per supported language. These are the **recommended starting point** for building your own custom microservice: everything Snapser expects is already wired up — auth middleware, a health check, CORS, the configuration / import-export / user-data hooks, eventbus integration, custom dashboard tools, and SDK generation — but each handler body is a **stub** that returns a simple placeholder and carries a `// TODO`.

Fill in the stubs with your own logic. For complete, working implementations of every hook, see the matching example under [`advanced/`](../advanced).

## Languages

| Language | Framework | Folder |
| --- | --- | --- |
| Python | Flask | [`byosnap-python`](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-python) |
| Go | Gorilla Mux | [`byosnap-go`](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-go) |
| Node (TypeScript) | Express + tsoa | [`byosnap-node-ts`](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-node-ts) |
| C# | ASP.NET Core | [`ByoSnapCSharp`](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/ByoSnapCSharp) |
| Rust | actix-web | [`byosnap-rust-api`](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-rust-api) |
| Java | Spring Boot | [`byosnap-java`](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-java) |
| Kotlin | Ktor | [`byosnap-kotlin`](https://github.com/snapser-community/snapser-byosnaps/tree/main/core/byosnap-kotlin) |

Every example is functionally identical across languages — same routes, same auth model, same tools — so pick the one that matches your stack.

## 1. Stubbed methods

Each example wires up every endpoint Snapser expects, with the body reduced to a stub (a placeholder return plus a `// TODO`). All externally reachable routes share the `/v1/byosnap-core` prefix, defined once via a single Snap-id constant so you can rename it in one place. The `GET /healthz` readiness endpoint sits at the root (no prefix).

**Platform hooks** (all guarded by Internal auth — they are called by Snapser, not by your clients):

- **Configuration Tool** — `GET/PUT /settings`
- **Custom Configuration Tool** — `GET/PUT /settings/custom`
- **User Manager Tool** — `GET/POST /settings/users/{user_id}/custom`
- **Snapend sync / clone** — `GET /settings/export`, `POST /settings/import`, `POST /settings/validate-import`
- **GDPR / user data** — `GET/PUT/DELETE /settings/users/{user_id}/data`

**Example business endpoints** — copy these as templates for your own APIs. Each shows one auth exposure; the swagger tag controls SDK visibility and the matching middleware enforces it at runtime:

| Endpoint | Exposure |
| --- | --- |
| `GET /v1/byosnap-core/users/{user_id}/example` | User auth |
| `GET /v1/byosnap-core/example/api-key` | Api-Key auth |
| `GET /v1/byosnap-core/example/internal` | Internal auth |
| `GET /v1/byosnap-core/example/admin` | Surfaced in the Admin SDK (`x-snapser-sdk-categories: ["admin"]`) and reached over api-key + internal auth. `admin` is an SDK *category*, not an auth type. |
| `GET /v1/byosnap-core/users/{user_id}/example/multi-auth` | User + Api-Key + Internal on one route — you do **not** need a separate route per auth type. |

## 2. Eventbus integration

Each example ships best-effort stubs for Snapser's Eventbus so you can emit and receive custom BYO events:

- **`registerEventTypes()`** runs **once on startup** and declares this Snap's custom event types with the Eventbus (`PUT /v1/eventbus/byo/event-types/byosnap-core`). It is best-effort — failures are logged and swallowed so they can never crash boot or block `/healthz`.
- **`publishEvent(subject, recipients, message)`** is a reusable helper that publishes an event (`POST /v1/eventbus/byo/events/byosnap-core/{subject}`). Call it from your business logic when you're ready to emit events.
- **`POST /internal/events`** is a reserved inbound receiver (root-level, no `/v1` prefix, like `/healthz`, and kept out of the SDK spec) that the Eventbus calls to deliver events to your Snap.

Outbound calls reach the Eventbus over the internal gateway using the `SNAPEND_EVENTBUS_HTTP_URL` environment variable plus a `Gateway: internal` header. If the Eventbus snap isn't part of your Snapend, the helpers log a notice and skip.

## 3. Custom Configuration (Admin) Tool

`snapser-resources/snapser-config-tool-characters-custom.html` is an example **custom admin/configuration tool** — an HTML page you upload with your BYOSnap that renders inside the Snapser dashboard. It reads and writes your Snap's settings through the injected `window.Snapser` SDK bridge, which calls your `GET/PUT /settings/custom` endpoints. Use it as a template for a bespoke settings UI.

## 4. Custom User Manager Tool

`snapser-resources/snapser-user-tool-characters-custom.html` is an example **custom user manager tool** — an HTML page for viewing and editing a specific user's data from the dashboard. It talks to your `GET/POST /settings/users/{user_id}/custom` endpoints via the `window.Snapser` bridge. Use it as a template for per-user admin screens.

## 5. The BYOSnap profile

`snapser-resources/snapser-byosnap-profile.json` tells Snapser how to build, run, and scale your Snap. Key fields:

- **`language` / `platform`** — how Snapser containerizes it (`linux/arm64` by default).
- **`ingress.external_port`** — the port your server listens on (`5003`).
- **`readiness_probe_config`** — the readiness path (`/healthz`) and startup grace (`initial_delay_seconds`, max 30). JVM examples use the full 30s.
- **`dev_template` / `stage_template` / `prod_template`** — cpu, memory, and replica counts per environment. Most examples use a small footprint (100m CPU / 128 MB); the JVM examples (Java, Kotlin) request more (0.5 CPU / 0.5–1 GB) because a JVM won't start in 128 MB.

## Using a scaffold

1. Copy the folder for your language.
2. Rename the Snap id — change the single `byosnap-core` constant to your Snap's id (this updates every route prefix).
3. Implement the stubbed handlers. Each has a `// TODO` and a pointer to the matching `advanced/` handler for a full reference.
4. Adjust `snapser-byosnap-profile.json` (resources, port) and the tool HTML files as needed, then publish with `snapctl byosnap publish`.
5. Regenerate / update the OpenAPI spec. Python, Go, Node, and C# ship a `generate_swagger` script; Java and Kotlin keep a hand-maintained `snapser-resources/swagger.json` (Java also exposes springdoc at `/v3/api-docs` for local dev); Rust has no spec step.

> Maintainer note: `publish-and-test-core.sh` publishes every example and brings it up in a test Snapend to verify all seven come online.
