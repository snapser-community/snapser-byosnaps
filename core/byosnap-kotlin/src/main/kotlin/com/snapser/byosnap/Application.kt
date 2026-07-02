/*
 * Core Kotlin BYOSnap Example — minimal starter scaffold.
 *
 * This is the recommended starting point for a new Kotlin BYOSnap, built with
 * Ktor (Netty engine). Every endpoint Snapser expects is present, but each
 * handler body is a STUB: it returns a simple placeholder and carries a
 * `// TODO` describing what you would implement here.
 *
 * Fill in the stubs with your own logic. When you need to persist data, call
 * other Snaps, or wire up the configuration/import-export tooling, use the
 * Snapser Storage snap (call it over the internal gateway).
 *
 * The boilerplate that is already wired up for you (and should usually stay
 * as-is):
 *   - The BYOSNAP_ID / API_PREFIX constants that build every route prefix
 *   - The validateAuthorization helper (User / Api-Key / Internal auth checks)
 *   - The /healthz readiness endpoint
 *   - The CORS install (so the Snapser API Explorer can reach you in-browser)
 *
 * The five example endpoints at the bottom show how to expose an API over each
 * Snapser auth type (User, Api-Key, Internal), an endpoint that accepts all
 * three together (you do NOT need a separate route per auth type), and one
 * endpoint that surfaces in the special Admin SDK. Use them as templates for
 * your own logic.
 */
package com.snapser.byosnap

import io.ktor.http.HttpHeaders
import io.ktor.http.HttpMethod
import io.ktor.http.HttpStatusCode
import io.ktor.serialization.kotlinx.json.json
import io.ktor.server.application.Application
import io.ktor.server.application.ApplicationCall
import io.ktor.server.application.call
import io.ktor.server.application.install
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation
import io.ktor.server.plugins.cors.routing.CORS
import io.ktor.server.request.receiveText
import io.ktor.server.response.respond
import io.ktor.server.response.respondText
import io.ktor.server.routing.delete
import io.ktor.server.routing.get
import io.ktor.server.routing.post
import io.ktor.server.routing.put
import io.ktor.server.routing.routing
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonArray
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put

// =========================================================================
// Constants
// =========================================================================

// Header Keys
const val AUTH_TYPE_HEADER_KEY = "Auth-Type"
const val GATEWAY_HEADER_KEY = "Gateway"
const val USER_ID_HEADER_KEY = "User-Id"

// Header Values
const val AUTH_TYPE_HEADER_VALUE_USER_AUTH = "user"
const val AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH = "api-key"
const val GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE = "internal"

// BYOSnap Identity
// BYOSNAP_ID is the URL segment Snapser uses to route to this Snap. Every
// externally reachable route is prefixed with API_PREFIX. Change BYOSNAP_ID in
// one place instead of editing every route string.
const val BYOSNAP_ID = "byosnap-core"
val API_PREFIX = "/v1/$BYOSNAP_ID"

// The port this server listens on. Must match the external_port in
// snapser-resources/snapser-byosnap-profile.json.
const val SERVER_PORT = 5003

// Shared JSON codec used for parsing request bodies below.
private val jsonCodec = Json { ignoreUnknownKeys = true }

// =========================================================================
// Response models (kotlinx.serialization)
// =========================================================================

@Serializable
data class MessageResponse(val message: String)

@Serializable
data class SuccessResponse(val success: Boolean)

@Serializable
data class ErrorResponse(val error_message: String)

// =========================================================================
// Authorization helper
//
// Kotlin equivalent of the Python `validate_authorization` decorator. Call it
// at the top of each route handler with the auth types the endpoint should
// accept and (optionally) the userId from the path. It returns `true` when the
// caller is authorized; on failure it writes the 400 Unauthorized response and
// returns `false`, so the handler should simply `return` when it gets `false`.
//
// Pass any of AUTH_TYPE_HEADER_VALUE_USER_AUTH,
// AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE.
// Snapser injects the relevant headers; this helper enforces them so you get
// authorization checks for free.
//
// Note on Admin-SDK APIs: `admin` is NOT an auth type. Guard admin endpoints
// with their real auth types (e.g. api-key + internal) and surface them in the
// Admin SDK by adding the `x-snapser-sdk-categories: [admin]` tag to the swagger
// operation (do NOT add `admin` to x-snapser-auth-types).
// =========================================================================

suspend fun validateAuthorization(
    call: ApplicationCall,
    vararg allowedAuthTypes: String,
    userId: String? = null,
): Boolean {
    // Get Gateway Header
    val gatewayHeaderValue = call.request.headers[GATEWAY_HEADER_KEY] ?: ""
    val isInternalCall = gatewayHeaderValue.lowercase() == GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE

    // Get Auth Type Header
    val authTypeHeaderValue = call.request.headers[AUTH_TYPE_HEADER_KEY] ?: ""
    val isApiKeyAuth = authTypeHeaderValue.lowercase() == AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH

    // Get User Id Header
    val userIdHeaderValue = call.request.headers[USER_ID_HEADER_KEY] ?: ""
    // If the API has a URL parameter for userId, then use that. Otherwise, use
    // the User-Id header value as the default.
    val targetUser = userId ?: userIdHeaderValue
    val isTargetUser = userIdHeaderValue == targetUser && userIdHeaderValue != ""

    // Validate
    var validationPassed = false
    for (authType in allowedAuthTypes) {
        when (authType) {
            GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE -> {
                // If `internal`, then the call must be internal.
                if (!isInternalCall) continue
                validationPassed = true
            }
            AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH -> {
                // If `api-key`, and the call is not internal, then it must pass
                // the Api-Key validation.
                if (!isInternalCall && !isApiKeyAuth) continue
                validationPassed = true
            }
            AUTH_TYPE_HEADER_VALUE_USER_AUTH -> {
                // If `user`, and the call is not internal or of type api-key
                // auth, then it must pass the User validation.
                if (!isInternalCall && !isApiKeyAuth && !isTargetUser) continue
                validationPassed = true
            }
        }
    }

    if (!validationPassed) {
        call.respond(HttpStatusCode.BadRequest, ErrorResponse("Unauthorized"))
        return false
    }
    return true
}

// =========================================================================
// Application entrypoint
// =========================================================================

fun main() {
    embeddedServer(Netty, port = SERVER_PORT, host = "0.0.0.0") {
        module()
    }.start(wait = true)
}

fun Application.module() {
    // CORS
    //
    // @GOTCHAS 👋 - CORS
    //   1. The Snapser API Explorer tool runs in the browser. Enabling CORS
    //      allows you to access the APIs via the API Explorer.
    install(CORS) {
        anyHost()
        allowMethod(HttpMethod.Get)
        allowMethod(HttpMethod.Post)
        allowMethod(HttpMethod.Put)
        allowMethod(HttpMethod.Delete)
        allowMethod(HttpMethod.Options)
        allowHeader(HttpHeaders.ContentType)
        allowHeader("Token")
        allowHeader("Api-Key")
        allowHeader("App-Key")
        allowHeader("Gateway")
        allowHeader("User-Id")
    }

    // JSON serialization
    install(ContentNegotiation) {
        json(Json { encodeDefaults = true })
    }

    routing {
        // -----------------------------------------------------------------
        // Health Check Endpoint
        //
        // @GOTCHAS 👋 - Health Check Endpoint
        //   1. The health URL does not take any URL prefix like other APIs.
        // -----------------------------------------------------------------
        get("/healthz") {
            call.respondText("Ok", status = HttpStatusCode.OK)
        }

        // -----------------------------------------------------------------
        // System endpoints Snapser expects.
        //
        // @GOTCHAS 👋 - Externally available APIs
        //   1. The Snapend Id is NOT part of the URL. This lets you reuse the
        //      same BYOSnap across multiple Snapends.
        //   2. All externally accessible APIs start with
        //      /$prefix/$byosnapId/remaining_path, where $prefix = v1,
        //      $byosnapId = byosnap-core. That prefix is built from API_PREFIX.
        //   3. The x-snapser-auth-types tag in snapser-resources/swagger.json
        //      tells Snapser whether to expose an API in the SDK and API
        //      Explorer. You should still validate the auth type in code.
        //   4. Snapser automatically adds the correct header to the SDK and API
        //      Explorer, so you do not add auth headers here.
        // -----------------------------------------------------------------

        // A i]: Configuration Tool: Built using the Snapser UI Builder
        get("$API_PREFIX/settings") {
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)) return@get
            // This is the default payload shape the Configuration Tool expects.
            val toolId = call.request.queryParameters["tool_id"]
            val environment = call.request.queryParameters["environment"] ?: "DEFAULT"
            @Suppress("UNUSED_VARIABLE")
            val blobOwnerKey = "${toolId}_$environment"
            // TODO: Fetch the saved settings for `blobOwnerKey` (e.g. from the
            //       Storage Snap over the internal gateway) and return them. For
            //       now we return the default shape.
            val defaultSettings = buildJsonObject {
                put("sections", buildJsonArray {
                    add(buildJsonObject {
                        put("id", "registration")
                        put("components", buildJsonArray {
                            add(buildJsonObject {
                                put("id", "characters")
                                put("type", "textarea")
                                put("value", "")
                            })
                        })
                    })
                })
            }
            call.respond(HttpStatusCode.OK, defaultSettings)
        }

        put("$API_PREFIX/settings") {
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)) return@put
            val toolId = call.request.queryParameters["tool_id"]
            val environment = call.request.queryParameters["environment"] ?: "DEFAULT"
            @Suppress("UNUSED_VARIABLE")
            val blobOwnerKey = "${toolId}_$environment"
            try {
                @Suppress("UNUSED_VARIABLE")
                val blobData = unwrapPayload(call.receiveText())
                // TODO: Validate `blobData` and persist it for `blobOwnerKey`
                //       (e.g. via the Storage Snap). On a validation failure
                //       respond 400 with an ErrorResponse.
                call.respond(HttpStatusCode.OK, SuccessResponse(true))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ErrorResponse("Invalid JSON ${e.message}"))
            }
        }

        // A ii]: New Configuration Tool: Custom HTML Snap Configuration Tool
        get("$API_PREFIX/settings/custom") {
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)) return@get
            val toolId = call.request.queryParameters["tool_id"]
            val environment = call.request.queryParameters["environment"] ?: "DEFAULT"
            @Suppress("UNUSED_VARIABLE")
            val blobOwnerKey = "${toolId}_$environment"
            // The custom HTML tool expects the settings wrapped in a `payload` key.
            // TODO: Fetch the saved settings for `blobOwnerKey` and return them
            //       wrapped as {"payload": <settings>}.
            call.respond(HttpStatusCode.OK, buildJsonObject { put("payload", "") })
        }

        put("$API_PREFIX/settings/custom") {
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)) return@put
            val toolId = call.request.queryParameters["tool_id"]
            val environment = call.request.queryParameters["environment"] ?: "DEFAULT"
            @Suppress("UNUSED_VARIABLE")
            val blobOwnerKey = "${toolId}_$environment"
            try {
                @Suppress("UNUSED_VARIABLE")
                val blobData = unwrapPayload(call.receiveText())
                // TODO: Validate `blobData` and persist it for `blobOwnerKey`.
                //       On a validation failure respond 400 with an ErrorResponse.
                call.respond(HttpStatusCode.OK, SuccessResponse(true))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ErrorResponse("Invalid JSON ${e.message}"))
            }
        }

        // A iii]: User Manager Tool: Custom HTML User Manager Tool
        get("$API_PREFIX/settings/users/{userId}/custom") {
            val userId = call.parameters["userId"] ?: ""
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, userId = userId)) return@get
            // TODO: Look up this user's data (e.g. from the Storage Snap) and
            //       return it wrapped as {"payload": <data>}.
            call.respond(HttpStatusCode.OK, buildJsonObject { put("payload", "") })
        }

        post("$API_PREFIX/settings/users/{userId}/custom") {
            val userId = call.parameters["userId"] ?: ""
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, userId = userId)) return@post
            try {
                @Suppress("UNUSED_VARIABLE")
                val blobData = unwrapPayload(call.receiveText())
                // TODO: Validate `blobData` and persist it for this userId.
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ErrorResponse("Invalid JSON ${e.message}"))
                return@post
            }
            call.respond(HttpStatusCode.OK, SuccessResponse(true))
        }

        // B: Snapend Sync|Clone: Snapser's built-in configuration import/export
        get("$API_PREFIX/settings/export") {
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)) return@get
            // Snapser calls this when cloning/syncing a Snapend. Return your
            // settings for every environment so they can be re-imported elsewhere.
            val emptyToolPayload = buildJsonObject {
                put("sections", buildJsonArray {
                    add(buildJsonObject {
                        put("id", "registration")
                        put("components", buildJsonArray {
                            add(buildJsonObject {
                                put("id", "characters")
                                put("type", "textarea")
                                put("value", "")
                            })
                        })
                    })
                })
            }
            val version = System.getenv("BYOSNAP_VERSION") ?: "v1.0.0"
            val response = buildJsonObject {
                put("version", version)
                put("exported_at", 0)
                put("data", buildJsonObject {
                    // The key here ("characters") is the Tool ID whose payload
                    // you export.
                    put("dev", buildJsonObject { put("characters", emptyToolPayload) })
                    put("stage", buildJsonObject { put("characters", emptyToolPayload) })
                    put("prod", buildJsonObject { put("characters", emptyToolPayload) })
                })
            }
            // TODO: Load the real saved settings per environment (e.g.
            //       batch-get from the Storage Snap) and merge them into `data`.
            call.respond(HttpStatusCode.OK, response)
        }

        post("$API_PREFIX/settings/import") {
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)) return@post
            try {
                val settingsData = parseJsonObject(call.receiveText())
                // TODO: Validate the incoming export payload and persist each
                //       environment's settings (e.g. batch-replace on the
                //       Storage Snap).
                if (settingsData == null) {
                    call.respond(HttpStatusCode.InternalServerError, ErrorResponse("Invalid JSON"))
                    return@post
                }
                call.respond(HttpStatusCode.OK, MessageResponse("Success"))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ErrorResponse("Server Exception${e.message}"))
            }
        }

        post("$API_PREFIX/settings/validate-import") {
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)) return@post
            // Snapser sends the settings it is about to import. Decide whether
            // you can accept them: return 200 with the payload if so, or 500
            // with an error_message if not.
            val settingsData = parseJsonObject(call.receiveText())
            // TODO: Add your own validation here (e.g. check the dev/stage/prod
            //       structure).
            if (settingsData == null) {
                call.respond(HttpStatusCode.InternalServerError, ErrorResponse("Invalid JSON"))
                return@post
            }
            call.respond(HttpStatusCode.OK, settingsData)
        }

        // C: User Tool: Get, Update and Delete User data (GDPR + User Manager)
        get("$API_PREFIX/settings/users/{userId}/data") {
            val userId = call.parameters["userId"] ?: ""
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, userId = userId)) return@get
            // TODO: Fetch and return everything you store for this userId (e.g.
            //       from the Storage Snap).
            call.respond(HttpStatusCode.OK, buildJsonObject { })
        }

        put("$API_PREFIX/settings/users/{userId}/data") {
            val userId = call.parameters["userId"] ?: ""
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, userId = userId)) return@put
            // TODO: Persist the incoming data for this userId.
            call.respond(HttpStatusCode.OK, buildJsonObject { })
        }

        delete("$API_PREFIX/settings/users/{userId}/data") {
            val userId = call.parameters["userId"] ?: ""
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, userId = userId)) return@delete
            // TODO: Delete everything you store for this userId. Used by the
            //       GDPR tool to honor deletion requests.
            call.respond(HttpStatusCode.OK, buildJsonObject { })
        }

        // =================================================================
        // Regular API Endpoints — your Snap's business logic lives here.
        //
        // The stubs below demonstrate each Snapser auth exposure. The
        // x-snapser-auth-types tag in snapser-resources/swagger.json controls
        // which SDK / tool the API surfaces in, and the matching
        // validateAuthorization(...) call enforces it at runtime.
        //
        // A single endpoint can accept MULTIPLE auth types at once (see the
        // last example) — you do not need a separate route per auth type.
        // =================================================================

        // Example endpoint exposed over User auth.
        // x-snapser-auth-types: [user]
        get("$API_PREFIX/users/{userId}/example") {
            val userId = call.parameters["userId"] ?: ""
            if (!validateAuthorization(call, AUTH_TYPE_HEADER_VALUE_USER_AUTH, userId = userId)) return@get
            // TODO: Add your user-scoped business logic here.
            call.respond(HttpStatusCode.OK, MessageResponse("Hello user $userId"))
        }

        // Example endpoint exposed over Api-Key auth.
        // x-snapser-auth-types: [api-key]
        get("$API_PREFIX/example/api-key") {
            if (!validateAuthorization(call, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH)) return@get
            // TODO: Add your api-key-scoped business logic here.
            call.respond(HttpStatusCode.OK, MessageResponse("Hello api-key caller"))
        }

        // Example endpoint exposed over Internal auth.
        // x-snapser-auth-types: [internal]
        get("$API_PREFIX/example/internal") {
            if (!validateAuthorization(call, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE)) return@get
            // TODO: Add your internal-only business logic here.
            call.respond(HttpStatusCode.OK, MessageResponse("Hello internal caller"))
        }

        // Example endpoint surfaced in the special Admin SDK.
        // x-snapser-auth-types: [api-key, internal]
        // x-snapser-sdk-categories: [admin]
        //
        // Note: `admin` is NOT an auth type. The endpoint is exposed over normal
        // auth types (here api-key + internal); the `x-snapser-sdk-categories:
        // admin` tag in snapser-resources/swagger.json is what surfaces it in
        // the Admin SDK (used by admin tooling / the Snapser dashboard).
        get("$API_PREFIX/example/admin") {
            if (!validateAuthorization(
                    call,
                    AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH,
                    GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE,
                )
            ) return@get
            // TODO: Add your admin business logic here.
            call.respond(HttpStatusCode.OK, MessageResponse("Hello admin caller"))
        }

        // Example endpoint that accepts multiple auth types on ONE route.
        // x-snapser-auth-types: [user, api-key, internal]
        //
        // One endpoint reachable by a logged-in user, a valid API key, or an
        // internal Snap. List every auth type you want to allow — no need for a
        // separate route per type. Pass every accepted auth type to both the
        // swagger tag (for SDK exposure) and validateAuthorization (for runtime
        // enforcement).
        get("$API_PREFIX/users/{userId}/example/multi-auth") {
            val userId = call.parameters["userId"] ?: ""
            if (!validateAuthorization(
                    call,
                    AUTH_TYPE_HEADER_VALUE_USER_AUTH,
                    AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH,
                    GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE,
                    userId = userId,
                )
            ) return@get
            // TODO: Add your business logic here.
            call.respond(HttpStatusCode.OK, MessageResponse("Hello, request for user $userId passed multi-auth"))
        }
    }
}

// =========================================================================
// Small JSON helpers used by the stubbed settings handlers.
// =========================================================================

/**
 * Parse a request body into a JsonObject, or return null if the body is empty
 * or not a JSON object. Mirrors the Python `request.get_json()` + falsy check.
 */
private fun parseJsonObject(body: String): JsonObject? {
    if (body.isBlank()) return null
    return try {
        val element: JsonElement = jsonCodec.parseToJsonElement(body)
        element as? JsonObject
    } catch (e: Exception) {
        null
    }
}

/**
 * If the incoming body is an object with a `payload` key, return that inner
 * value; otherwise return the whole parsed element. Mirrors the Python
 * `if 'payload' in blob_data: blob_data = blob_data['payload']` unwrap. Throws
 * if the body is not valid JSON so callers can respond 500.
 */
private fun unwrapPayload(body: String): JsonElement {
    val element = jsonCodec.parseToJsonElement(body)
    if (element is JsonObject && element.containsKey("payload")) {
        return element["payload"] ?: JsonPrimitive("")
    }
    return element
}
