/*
 * Snapser Eventbus integration (stubs).
 *
 * The Eventbus lets Snaps publish custom events and receive events delivered by
 * other Snaps within the same Snapend. Three pieces live here:
 *
 *   1. registerEventTypes() - declare the custom event types this Snap emits.
 *      Called ONCE on startup from main(). BEST-EFFORT: it logs success/failure
 *      and never throws, so a missing/unreachable Eventbus can never crash the
 *      process or block boot / the /healthz probe.
 *   2. publishEvent(...)    - publish a single event onto the bus. A reusable
 *      BEST-EFFORT helper you call from your own business logic. It is
 *      intentionally NOT wired into any existing route's normal flow.
 *   3. installEventbusReceiver() - registers POST /internal/events, the RESERVED
 *      root-level URL (no /v1 prefix, no byosnap id, like /healthz) that the
 *      Eventbus POSTs to when it delivers events to this Snap.
 *
 * Internal Snap-to-Snap calls go through the internal gateway: the base URL
 * comes from the SNAPEND_EVENTBUS_HTTP_URL env var (Snapser injects it when the
 * Eventbus Snap is part of this Snapend) and every request carries the
 * `Gateway: internal` header, whose value comes from SNAPEND_INTERNAL_HEADER
 * (default "internal").
 *
 * The outbound calls use java.net.http.HttpClient (JDK 21) so this scaffold
 * needs no extra Gradle dependency, and the JSON body is built as a raw string.
 */
package com.snapser.byosnap

import io.ktor.http.HttpStatusCode
import io.ktor.server.application.call
import io.ktor.server.request.receiveText
import io.ktor.server.response.respondText
import io.ktor.server.routing.Route
import io.ktor.server.routing.post
import org.slf4j.LoggerFactory
import java.net.URI
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse
import java.time.Duration

// =========================================================================
// Eventbus constants + shared client
// =========================================================================

// Env var Snapser injects with the Eventbus Snap's internal base URL.
// NOTE: confirm the exact name for your Snapend — it may differ (e.g.
// SNAPEND_EVENT_BUS_HTTP_URL).
const val EVENTBUS_HTTP_URL_ENV_KEY = "SNAPEND_EVENTBUS_HTTP_URL"

// Env var holding the value to send in the `Gateway` header for internal calls.
const val INTERNAL_HEADER_ENV_KEY = "SNAPEND_INTERNAL_HEADER"

private val eventbusLogger = LoggerFactory.getLogger("Eventbus")

// Short-timeout client so a slow/unreachable Eventbus never blocks boot or an
// inbound request.
private val eventbusHttpClient: HttpClient = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(5))
    .build()

// Value of the `Gateway` header that marks a call as internal (Snap-to-Snap).
private fun internalHeaderValue(): String =
    System.getenv(INTERNAL_HEADER_ENV_KEY)?.takeIf { it.isNotBlank() }
        ?: GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE

private fun eventbusBaseUrl(): String = System.getenv(EVENTBUS_HTTP_URL_ENV_KEY) ?: ""

// Minimal JSON string escaping for values we interpolate into the raw bodies.
private fun jsonEscape(value: String): String =
    value.replace("\\", "\\\\").replace("\"", "\\\"")

// =========================================================================
// 1] registerEventTypes — called ONCE from main() on startup.
// =========================================================================

/**
 * Register the custom event types this Snap publishes.
 *
 * Call this ONCE on startup (see main() in Application.kt). It is BEST-EFFORT:
 * it logs success or failure and never throws, so a missing/unreachable
 * Eventbus can never crash the process or block the /healthz probe. If
 * SNAPEND_EVENTBUS_HTTP_URL is empty it logs a notice and skips.
 *
 * PUT {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/event-types/{BYOSNAP_ID}
 */
fun registerEventTypes() {
    val baseUrl = eventbusBaseUrl()
    if (baseUrl.isBlank()) {
        eventbusLogger.info(
            "$EVENTBUS_HTTP_URL_ENV_KEY not set - skipping event-type registration.",
        )
        return
    }

    // TODO: Customize the event types your Snap emits. `subject` is the routing
    //       key other Snaps subscribe to; `service_name` should be this Snap's
    //       id; `message_type` names the payload shape. Add one entry per event.
    val body = """
        {"event_types":[{"subject":"$BYOSNAP_ID.example.created","service_name":"$BYOSNAP_ID","message_type":"example","event_type_id":0,"event_type_enum_value":0,"description":"Example custom event registered by $BYOSNAP_ID"}]}
    """.trimIndent()

    try {
        val request = HttpRequest.newBuilder()
            .uri(URI.create("$baseUrl/v1/eventbus/byo/event-types/$BYOSNAP_ID"))
            .timeout(Duration.ofSeconds(5))
            .header("Content-Type", "application/json")
            .header(GATEWAY_HEADER_KEY, internalHeaderValue())
            .PUT(HttpRequest.BodyPublishers.ofString(body))
            .build()

        val response = eventbusHttpClient.send(request, HttpResponse.BodyHandlers.ofString())
        if (response.statusCode() in 200..299) {
            eventbusLogger.info("Registered event types for $BYOSNAP_ID.")
        } else {
            eventbusLogger.warn(
                "Event-type registration returned HTTP ${response.statusCode()}: ${response.body()}",
            )
        }
    } catch (e: Exception) {
        // Best-effort: log and move on. Never rethrow.
        eventbusLogger.warn("Failed to register event types: ${e.message}")
    }
}

// =========================================================================
// 2] publishEvent — reusable helper. NOT wired into any route by default.
// =========================================================================

/**
 * Publish a single event onto the Eventbus.
 *
 * Reusable BEST-EFFORT helper: it logs and swallows errors so a publish never
 * breaks your request flow. Call it from your own business logic wherever you
 * want to emit an event. It is intentionally NOT wired into any existing
 * endpoint's normal flow.
 *
 * POST {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/events/{BYOSNAP_ID}/{subject}
 *
 * @param subject    The event subject, e.g. "byosnap-core.example.created".
 * @param recipients Recipient user IDs the event should be delivered to
 *                   (empty = broadcast).
 * @param message    Arbitrary event payload, already serialized to a JSON string.
 *
 * Example usage:
 * ```
 * publishEvent(
 *     "$BYOSNAP_ID.example.created",
 *     listOf("user-123"),                       // recipients (empty = broadcast)
 *     """{"example_id":"abc","name":"My Example"}""", // your payload as JSON
 * )
 * ```
 */
fun publishEvent(subject: String, recipients: List<String>, message: String) {
    val baseUrl = eventbusBaseUrl()
    if (baseUrl.isBlank()) {
        eventbusLogger.info(
            "$EVENTBUS_HTTP_URL_ENV_KEY not set - skipping publish of \"$subject\".",
        )
        return
    }

    // TODO: Set event_type_id to match the event type you registered in
    //       registerEventTypes(), and populate `message`/`recipients` for your
    //       use case. `payload` is an optional opaque string.
    val recipientsJson = recipients.joinToString(prefix = "[", postfix = "]") { "\"${jsonEscape(it)}\"" }
    val body =
        "{\"event_type_id\":0,\"message\":$message,\"payload\":\"\",\"recipients\":$recipientsJson}"

    try {
        val request = HttpRequest.newBuilder()
            .uri(URI.create("$baseUrl/v1/eventbus/byo/events/$BYOSNAP_ID/$subject"))
            .timeout(Duration.ofSeconds(5))
            .header("Content-Type", "application/json")
            .header(GATEWAY_HEADER_KEY, internalHeaderValue())
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build()

        val response = eventbusHttpClient.send(request, HttpResponse.BodyHandlers.ofString())
        if (response.statusCode() in 200..299) {
            eventbusLogger.info("Published event \"$subject\".")
        } else {
            eventbusLogger.warn(
                "Publishing \"$subject\" returned HTTP ${response.statusCode()}: ${response.body()}",
            )
        }
    } catch (e: Exception) {
        // Best-effort: log and move on. Never rethrow.
        eventbusLogger.warn("Failed to publish event \"$subject\": ${e.message}")
    }
}

// =========================================================================
// 3] Inbound receiver — POST /internal/events (RESERVED root-level URL).
// =========================================================================

/**
 * Registers the inbound Eventbus receiver route.
 *
 * The Snapser Eventbus calls POST /internal/events to DELIVER events to this
 * Snap. It is a RESERVED, root-level URL (like /healthz): NO /v1 prefix and NO
 * byosnap id. It is intentionally kept out of snapser-resources/swagger.json —
 * it is an internal webhook, not an SDK API.
 *
 * Call this from inside the `routing { ... }` block in Application.kt.
 */
fun Route.installEventbusReceiver() {
    post("/internal/events") {
        val body = call.receiveText()
        eventbusLogger.info("Received inbound event: $body")
        // TODO: Parse `body` and switch on the event `subject` to dispatch each
        //       event to the appropriate handler in your business logic.
        call.respondText("Ok", status = HttpStatusCode.OK)
    }
}
