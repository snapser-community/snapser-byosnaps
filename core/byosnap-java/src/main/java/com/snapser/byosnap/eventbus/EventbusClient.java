package com.snapser.byosnap.eventbus;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.snapser.byosnap.AppConstants;

/**
 * Snapser Eventbus integration (stubs).
 *
 * <p>The Eventbus lets Snaps publish custom events and receive events delivered
 * by other Snaps within the same Snapend. Two outbound operations live here:
 *
 * <ol>
 *   <li>{@link #registerEventTypes()} — declare the custom event types this
 *       Snap emits. Called ONCE on startup (see
 *       {@code eventbus.EventbusStartup}). BEST-EFFORT: it never crashes or
 *       blocks boot / the {@code /healthz} probe.</li>
 *   <li>{@link #publishEvent(String, List, Object)} — publish a single event
 *       onto the bus. A reusable helper you can call from your own business
 *       logic.</li>
 * </ol>
 *
 * <p>Inbound events are delivered by the Eventbus via {@code POST
 * /internal/events}, wired as a raw root-level route in
 * {@code controller.EventReceiverController} (kept out of the hand-authored
 * swagger spec).
 *
 * <p>Internal Snap-to-Snap calls go through the internal gateway: the base URL
 * comes from {@code SNAPEND_EVENTBUS_HTTP_URL} and every request carries the
 * {@code Gateway} header (value from {@code SNAPEND_INTERNAL_HEADER}, default
 * {@code "internal"}). Uses the JDK's {@link HttpClient} (JDK 21) — no extra
 * dependency.
 */
@Component
public class EventbusClient {

    private static final Logger log = LoggerFactory.getLogger(EventbusClient.class);

    /** How long to wait on an Eventbus HTTP call before giving up. */
    private static final Duration REQUEST_TIMEOUT = Duration.ofSeconds(5);

    // Short-timeout client so a slow/unreachable Eventbus never blocks boot or
    // an inbound request.
    private final HttpClient httpClient = HttpClient.newBuilder()
            .connectTimeout(REQUEST_TIMEOUT)
            .build();

    private final ObjectMapper objectMapper = new ObjectMapper();

    /** Base URL of the Eventbus internal HTTP endpoint (empty when not set). */
    private String eventbusUrl() {
        return System.getenv().getOrDefault(AppConstants.EVENTBUS_HTTP_URL_ENV_KEY, "");
    }

    /** Value of the {@code Gateway} header marking a call as internal. */
    private String internalHeaderValue() {
        return System.getenv().getOrDefault(
                AppConstants.INTERNAL_HEADER_ENV_KEY, AppConstants.DEFAULT_INTERNAL_HEADER_VALUE);
    }

    /**
     * Register the custom event types this Snap publishes.
     *
     * <p>Call this ONCE on startup. It is BEST-EFFORT: it logs success or
     * failure and never throws, so a missing/unreachable Eventbus can never
     * crash the process or block the {@code /healthz} probe. If
     * {@code SNAPEND_EVENTBUS_HTTP_URL} is empty it logs and skips.
     *
     * <p>{@code PUT {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/event-types/byosnap-core}
     */
    public void registerEventTypes() {
        String baseUrl = eventbusUrl();
        if (baseUrl.isEmpty()) {
            log.info("[eventbus] {} not set - skipping event type registration.",
                    AppConstants.EVENTBUS_HTTP_URL_ENV_KEY);
            return;
        }

        String url = baseUrl + "/v1/eventbus/byo/event-types/" + AppConstants.BYOSNAP_ID;

        // TODO: Customize the event types your Snap publishes. Each entry
        //       declares one subject the Eventbus will accept from this Snap.
        Map<String, Object> body = Map.of(
                "event_types", List.of(Map.of(
                        "subject", AppConstants.BYOSNAP_ID + ".example.created",
                        "service_name", AppConstants.BYOSNAP_ID,
                        "message_type", "example",
                        "event_type_id", 0,
                        "event_type_enum_value", 0,
                        "description", "Example custom event registered by " + AppConstants.BYOSNAP_ID)));

        try {
            String json = objectMapper.writeValueAsString(body);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .timeout(REQUEST_TIMEOUT)
                    .header("Content-Type", "application/json")
                    .header(AppConstants.GATEWAY_HEADER_KEY, internalHeaderValue())
                    .PUT(HttpRequest.BodyPublishers.ofString(json))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() >= 200 && response.statusCode() < 300) {
                log.info("[eventbus] Registered event types for {}.", AppConstants.BYOSNAP_ID);
            } else {
                log.warn("[eventbus] Event type registration returned HTTP {}: {}",
                        response.statusCode(), response.body());
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.warn("[eventbus] Interrupted while registering event types.");
        } catch (Exception e) {
            // Best-effort: log and move on. Never rethrow.
            log.warn("[eventbus] Failed to register event types: {}", e.getMessage());
        }
    }

    /**
     * Publish a single event onto the Eventbus.
     *
     * <p>Reusable BEST-EFFORT helper: it logs and swallows errors so a publish
     * never breaks your request flow. Call it from your own business logic
     * wherever you want to emit an event. It is intentionally NOT wired into any
     * endpoint's normal flow.
     *
     * <p>{@code POST {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/events/byosnap-core/{subject}}
     *
     * @param subject    the event subject, e.g. {@code "byosnap-core.example.created"}
     * @param recipients recipient user IDs the event should be delivered to
     *                   (empty for a broadcast)
     * @param message    arbitrary event payload object (serialized as JSON)
     *
     * @implNote Example usage:
     * <pre>{@code
     * eventbusClient.publishEvent(
     *         "byosnap-core.example.created",
     *         List.of("user-123"),
     *         Map.of("example_id", "abc", "name", "My Example"));
     * }</pre>
     */
    public void publishEvent(String subject, List<String> recipients, Object message) {
        String baseUrl = eventbusUrl();
        if (baseUrl.isEmpty()) {
            log.info("[eventbus] {} not set - skipping publish of \"{}\".",
                    AppConstants.EVENTBUS_HTTP_URL_ENV_KEY, subject);
            return;
        }

        String url = baseUrl + "/v1/eventbus/byo/events/" + AppConstants.BYOSNAP_ID + "/" + subject;

        try {
            // TODO: Set event_type_id to match the event type you registered in
            //       registerEventTypes(), and populate `payload` if your
            //       consumers expect a raw string body.
            // A mutable HashMap (not Map.of) so a null message/recipients from
            // a caller is tolerated rather than throwing.
            Map<String, Object> body = new HashMap<>();
            body.put("event_type_id", 0);
            body.put("message", message);
            body.put("payload", "");
            body.put("recipients", recipients);

            String json = objectMapper.writeValueAsString(body);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .timeout(REQUEST_TIMEOUT)
                    .header("Content-Type", "application/json")
                    .header(AppConstants.GATEWAY_HEADER_KEY, internalHeaderValue())
                    .POST(HttpRequest.BodyPublishers.ofString(json))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() >= 200 && response.statusCode() < 300) {
                log.info("[eventbus] Published event \"{}\".", subject);
            } else {
                log.warn("[eventbus] Publishing \"{}\" returned HTTP {}: {}",
                        subject, response.statusCode(), response.body());
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.warn("[eventbus] Interrupted while publishing event \"{}\".", subject);
        } catch (Exception e) {
            // Best-effort: log and move on. Never rethrow.
            log.warn("[eventbus] Failed to publish event \"{}\": {}", subject, e.getMessage());
        }
    }
}
