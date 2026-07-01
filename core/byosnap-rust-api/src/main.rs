// Core Rust BYOSnap Example — minimal starter scaffold.
//
// This is the recommended starting point for a new Rust BYOSnap. Every endpoint
// Snapser expects is present, but each handler body is a STUB: it returns a
// simple placeholder and carries a `// TODO` describing what you would implement
// here.
//
// Fill in the stubs with your own logic. When you need to persist data, call
// other Snaps, or wire up the configuration/import-export tooling, look at the
// matching handler in `advanced/byosnap-rust-api` for a complete, working
// reference.
//
// The boilerplate that is already wired up for you (and should usually stay
// as-is):
//   - The `BYOSNAP_ID` constant that builds every route prefix
//   - The `validate_authorization` helper (User / Api-Key / Internal auth checks)
//   - The `/healthz` readiness endpoint
//   - The permissive CORS layer
//
// The five example endpoints at the bottom show how to expose an API over each
// Snapser auth type (User, Api-Key, Internal), an endpoint that accepts all
// three together (you do NOT need a separate route per auth type), and one
// endpoint that surfaces in the special Admin SDK. Use them as templates for
// your own logic.

use actix_cors::Cors;
use actix_web::{web, App, HttpRequest, HttpResponse, HttpServer, middleware::Logger};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

// --- Constants ---

const AUTH_TYPE_HEADER_KEY: &str = "Auth-Type";
const GATEWAY_HEADER_KEY: &str = "Gateway";
const USER_ID_HEADER_KEY: &str = "User-Id";

const AUTH_TYPE_USER: &str = "user";
const AUTH_TYPE_API_KEY: &str = "api-key";
const GATEWAY_INTERNAL: &str = "internal";

// BYOSNAP_ID is the URL segment Snapser uses to route to this Snap. Every
// externally reachable route is prefixed with `/v1/{BYOSNAP_ID}`. Change it in
// one place instead of editing every route string.
const BYOSNAP_ID: &str = "byosnap-core";

// --- Models ---

#[derive(Serialize, Deserialize)]
struct SuccessMessage {
    message: String,
}

#[derive(Serialize, Deserialize)]
struct ErrorResponse {
    error_message: String,
}

#[derive(Serialize, Deserialize, Clone)]
struct SettingsComponent {
    id: String,
    #[serde(rename = "type")]
    component_type: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    value: Option<serde_json::Value>,
}

#[derive(Serialize, Deserialize, Clone)]
struct SettingsSection {
    id: String,
    components: Vec<SettingsComponent>,
}

#[derive(Serialize, Deserialize, Clone)]
struct SettingsSchema {
    sections: Vec<SettingsSection>,
}

#[derive(Serialize, Deserialize)]
struct ExportSettingsSchema {
    version: String,
    exported_at: i64,
    data: HashMap<String, HashMap<String, SettingsSchema>>,
}

#[derive(Serialize, Deserialize)]
struct CustomSettingsPayload {
    payload: serde_json::Value,
}

// --- Authorization ---

enum AuthType {
    User,
    ApiKey,
    Internal,
}

fn validate_authorization(
    req: &HttpRequest,
    allowed: &[AuthType],
    path_user_id: Option<&str>,
) -> bool {
    let gateway = req
        .headers()
        .get(GATEWAY_HEADER_KEY)
        .and_then(|v| v.to_str().ok())
        .unwrap_or("");
    let is_internal = gateway.eq_ignore_ascii_case(GATEWAY_INTERNAL);

    let auth_type = req
        .headers()
        .get(AUTH_TYPE_HEADER_KEY)
        .and_then(|v| v.to_str().ok())
        .unwrap_or("");
    let is_api_key = auth_type.eq_ignore_ascii_case(AUTH_TYPE_API_KEY);

    let user_id_header = req
        .headers()
        .get(USER_ID_HEADER_KEY)
        .and_then(|v| v.to_str().ok())
        .unwrap_or("");

    let target_user = path_user_id.unwrap_or(user_id_header);
    let is_target_user = !user_id_header.is_empty() && user_id_header == target_user;

    for auth in allowed {
        match auth {
            AuthType::Internal => {
                if is_internal {
                    return true;
                }
            }
            AuthType::ApiKey => {
                if is_api_key || is_internal {
                    return true;
                }
            }
            AuthType::User => {
                if is_internal || is_api_key || is_target_user {
                    return true;
                }
            }
        }
    }
    false
}

fn unauthorized() -> HttpResponse {
    HttpResponse::Unauthorized().json(ErrorResponse {
        error_message: "Unauthorized".to_string(),
    })
}

// --- Default settings helper ---

fn default_settings() -> SettingsSchema {
    SettingsSchema {
        sections: vec![SettingsSection {
            id: "registration".to_string(),
            components: vec![SettingsComponent {
                id: "characters".to_string(),
                component_type: "textarea".to_string(),
                value: Some(serde_json::Value::String(String::new())),
            }],
        }],
    }
}

fn default_characters_payload() -> HashMap<String, SettingsSchema> {
    let mut m = HashMap::new();
    m.insert("characters".to_string(), default_settings());
    m
}

// ===========================================================================
// Health Check
// ===========================================================================

async fn healthz() -> HttpResponse {
    HttpResponse::Ok().body("Ok")
}

// ===========================================================================
// A i]: Configuration Tool: Built using the Snapser UI Builder
// ===========================================================================

async fn get_settings(req: HttpRequest) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // Snapser sends `tool_id` and `environment` query params so you can scope the
    // settings blob per environment. This stub returns the default shape the
    // Configuration Tool expects.
    // TODO: Fetch the saved settings (e.g. from the Storage Snap) and return them.
    //       See advanced/byosnap-rust-api for the full implementation.
    HttpResponse::Ok().json(default_settings())
}

async fn update_settings(req: HttpRequest, _body: web::Json<serde_json::Value>) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: Validate the incoming settings and persist them (e.g. via the Storage
    //       Snap). See advanced/byosnap-rust-api for the full implementation.
    HttpResponse::Ok().json(SuccessMessage {
        message: "Success".to_string(),
    })
}

// ===========================================================================
// A ii]: Custom HTML Snap Configuration Tool
// ===========================================================================

async fn get_settings_custom(req: HttpRequest) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // The custom HTML tool expects the settings wrapped in a `payload` key.
    // TODO: Fetch the saved settings and return them wrapped as {"payload": ...}.
    //       See advanced/byosnap-rust-api for the full implementation.
    HttpResponse::Ok().json(CustomSettingsPayload {
        payload: serde_json::Value::String(String::new()),
    })
}

async fn update_settings_custom(
    req: HttpRequest,
    _body: web::Json<serde_json::Value>,
) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: Validate the incoming settings and persist them. See
    //       advanced/byosnap-rust-api for the full implementation.
    HttpResponse::Ok().json(SuccessMessage {
        message: "Success".to_string(),
    })
}

// ===========================================================================
// A iii]: User Manager Tool: Custom HTML User Manager Tool
// ===========================================================================

async fn get_user_data_custom(req: HttpRequest, _path: web::Path<String>) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: Look up this user's data and return it wrapped as {"payload": ...}.
    //       See advanced/byosnap-rust-api for the full implementation.
    HttpResponse::Ok().json(CustomSettingsPayload {
        payload: serde_json::Value::String(String::new()),
    })
}

async fn update_user_data_custom(
    req: HttpRequest,
    _path: web::Path<String>,
    _body: web::Json<serde_json::Value>,
) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: Validate the incoming data and persist it for this user_id. See
    //       advanced/byosnap-rust-api for the full implementation.
    HttpResponse::Ok().json(SuccessMessage {
        message: "Success".to_string(),
    })
}

// ===========================================================================
// B: Snapend Sync|Clone: Import/Export
// ===========================================================================

async fn export_settings(req: HttpRequest) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // Snapser calls this when cloning/syncing a Snapend. Return your settings for
    // every environment so they can be re-imported elsewhere. The key inside each
    // environment ("characters" here) is the Tool ID whose payload you export.
    let version = std::env::var("BYOSNAP_VERSION").unwrap_or_else(|_| "v1.0.0".to_string());

    let mut data = HashMap::new();
    data.insert("dev".to_string(), default_characters_payload());
    data.insert("stage".to_string(), default_characters_payload());
    data.insert("prod".to_string(), default_characters_payload());

    // TODO: Load the real saved settings per environment (e.g. batch-get from the
    //       Storage Snap) and merge them in. See advanced/byosnap-rust-api.
    HttpResponse::Ok().json(ExportSettingsSchema {
        version,
        exported_at: 0,
        data,
    })
}

async fn import_settings(
    req: HttpRequest,
    _body: web::Json<serde_json::Value>,
) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: Validate the incoming export payload and persist each environment's
    //       settings (e.g. batch-replace on the Storage Snap). See
    //       advanced/byosnap-rust-api for validation + Storage writes.
    HttpResponse::Ok().json(SuccessMessage {
        message: "Success".to_string(),
    })
}

async fn validate_import_settings(
    req: HttpRequest,
    body: web::Json<serde_json::Value>,
) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // Snapser sends the settings it is about to import. Decide whether you can
    // accept them: return 200 with the payload if so, or 500 with an error if not.
    // TODO: Add your own validation here. See advanced/byosnap-rust-api for an
    //       example that checks the dev/stage/prod structure.
    HttpResponse::Ok().json(body.into_inner())
}

// ===========================================================================
// C: User Tool: GDPR Endpoints
// ===========================================================================

async fn get_user_data(req: HttpRequest, _path: web::Path<String>) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: Fetch and return everything you store for this user_id. See
    //       advanced/byosnap-rust-api for the Storage read.
    HttpResponse::Ok().json(serde_json::json!({}))
}

async fn update_user_data(req: HttpRequest, _path: web::Path<String>) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: Persist the incoming data for this user_id. See
    //       advanced/byosnap-rust-api for the Storage write.
    HttpResponse::Ok().json(serde_json::json!({}))
}

async fn delete_user_data(req: HttpRequest, _path: web::Path<String>) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: Delete everything you store for this user_id. See
    //       advanced/byosnap-rust-api for the Storage delete.
    HttpResponse::Ok().json(serde_json::json!({}))
}

// ===========================================================================
// Regular API Endpoints — your Snap's business logic lives here.
//
// The stubs below demonstrate each Snapser auth exposure. The auth type you
// pass to `validate_authorization(...)` enforces it at runtime. Add, rename, or
// remove these to fit your Snap.
//
// A single endpoint can accept MULTIPLE auth types at once (see the last
// example) — you do not need a separate route per auth type.
// ===========================================================================

// Example endpoint exposed over User auth. Accessible by a logged-in user,
// validated against the User-Id in their token. Surfaces in the client/game SDK.
async fn example_user_endpoint(req: HttpRequest, path: web::Path<String>) -> HttpResponse {
    let user_id = path.into_inner();
    if !validate_authorization(&req, &[AuthType::User], Some(&user_id)) {
        return unauthorized();
    }
    // TODO: add your business logic here
    HttpResponse::Ok().json(SuccessMessage {
        message: format!("Hello user {}", user_id),
    })
}

// Example endpoint exposed over Api-Key auth. Accessible with a valid API key;
// use for trusted server-to-server calls.
async fn example_api_key_endpoint(req: HttpRequest) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::ApiKey], None) {
        return unauthorized();
    }
    // TODO: add your business logic here
    HttpResponse::Ok().json(SuccessMessage {
        message: "Hello api-key caller".to_string(),
    })
}

// Example endpoint exposed over Internal auth. Callable only by other Snaps
// within the same Snapend (internal gateway). Surfaces in the internal SDK.
async fn example_internal_endpoint(req: HttpRequest) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: add your business logic here
    HttpResponse::Ok().json(SuccessMessage {
        message: "Hello internal caller".to_string(),
    })
}

// Example endpoint surfaced in the special Admin SDK.
//
// Note: `admin` is NOT an auth type. In the other language examples an `admin`
// swagger tag surfaces the API in the Admin SDK; there is no swagger for Rust,
// so here we simply guard via the INTERNAL check. Admin-SDK calls reach the Snap
// through the internal gateway.
async fn example_admin_endpoint(req: HttpRequest) -> HttpResponse {
    if !validate_authorization(&req, &[AuthType::Internal], None) {
        return unauthorized();
    }
    // TODO: add your business logic here
    HttpResponse::Ok().json(SuccessMessage {
        message: "Hello admin caller".to_string(),
    })
}

// Example endpoint that accepts MULTIPLE auth types on ONE route. Reachable by a
// logged-in user, a valid API key, or an internal Snap. List every auth type you
// want to allow — no need for a separate route per type.
async fn example_multi_auth_endpoint(req: HttpRequest, path: web::Path<String>) -> HttpResponse {
    let user_id = path.into_inner();
    if !validate_authorization(
        &req,
        &[AuthType::User, AuthType::ApiKey, AuthType::Internal],
        Some(&user_id),
    ) {
        return unauthorized();
    }
    // TODO: add your business logic here
    HttpResponse::Ok().json(SuccessMessage {
        message: format!("Hello, request for user {} passed multi-auth", user_id),
    })
}

// ===========================================================================
// Main
// ===========================================================================

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();
    log::info!("Starting {} server on :5003", BYOSNAP_ID);

    HttpServer::new(|| {
        let cors = Cors::permissive();

        let prefix = format!("/v1/{}", BYOSNAP_ID);

        App::new()
            .wrap(Logger::default())
            .wrap(cors)
            // Health check (no prefix)
            .route("/healthz", web::get().to(healthz))
            // Configuration Tool (Snapser UI Builder)
            .route(
                &format!("{}/settings", prefix),
                web::get().to(get_settings),
            )
            .route(
                &format!("{}/settings", prefix),
                web::put().to(update_settings),
            )
            // Custom HTML Configuration Tool
            .route(
                &format!("{}/settings/custom", prefix),
                web::get().to(get_settings_custom),
            )
            .route(
                &format!("{}/settings/custom", prefix),
                web::put().to(update_settings_custom),
            )
            // User Manager Tool
            .route(
                &format!("{}/settings/users/{{user_id}}/custom", prefix),
                web::get().to(get_user_data_custom),
            )
            .route(
                &format!("{}/settings/users/{{user_id}}/custom", prefix),
                web::post().to(update_user_data_custom),
            )
            // Import/Export (Snapend Sync/Clone)
            .route(
                &format!("{}/settings/export", prefix),
                web::get().to(export_settings),
            )
            .route(
                &format!("{}/settings/import", prefix),
                web::post().to(import_settings),
            )
            .route(
                &format!("{}/settings/validate-import", prefix),
                web::post().to(validate_import_settings),
            )
            // GDPR User Data
            .route(
                &format!("{}/settings/users/{{user_id}}/data", prefix),
                web::get().to(get_user_data),
            )
            .route(
                &format!("{}/settings/users/{{user_id}}/data", prefix),
                web::put().to(update_user_data),
            )
            .route(
                &format!("{}/settings/users/{{user_id}}/data", prefix),
                web::delete().to(delete_user_data),
            )
            // Regular API Endpoints (example handlers, one per auth exposure)
            // a. User auth
            .route(
                &format!("{}/users/{{user_id}}/example", prefix),
                web::get().to(example_user_endpoint),
            )
            // b. Api-Key auth
            .route(
                &format!("{}/example/api-key", prefix),
                web::get().to(example_api_key_endpoint),
            )
            // c. Internal auth
            .route(
                &format!("{}/example/internal", prefix),
                web::get().to(example_internal_endpoint),
            )
            // d. Admin SDK (guarded via internal; requests arrive via the
            //    internal gateway)
            .route(
                &format!("{}/example/admin", prefix),
                web::get().to(example_admin_endpoint),
            )
            // e. Multiple auth types on one route (User + Api-Key + Internal)
            .route(
                &format!("{}/users/{{user_id}}/example/multi-auth", prefix),
                web::get().to(example_multi_auth_endpoint),
            )
    })
    .bind("0.0.0.0:5003")?
    .run()
    .await
}
