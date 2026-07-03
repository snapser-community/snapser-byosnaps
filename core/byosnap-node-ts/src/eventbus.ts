// ===========================================================================
// Snapser Eventbus integration (stubs).
//
// The Eventbus lets Snaps publish custom events and receive events delivered
// by other Snaps within the same Snapend. Two outbound operations live here:
//
//   1. registerEventTypes() - declare the custom event types this Snap emits.
//      Called ONCE on startup (see server.ts). Best-effort: it must never
//      crash or block boot / the /healthz probe.
//   2. publishEvent(...)    - publish a single event onto the bus. A reusable
//      helper you can call from your own business logic.
//
// Inbound events are delivered by the Eventbus via POST /internal/events,
// which is wired as a raw Express route in app.ts (kept out of the tsoa spec).
//
// Internal Snap-to-Snap calls go through the internal gateway: use the base URL
// from SNAPEND_EVENTBUS_HTTP_URL and send the `Gateway: internal` header (its
// value comes from SNAPEND_INTERNAL_HEADER, defaulting to "internal").
// ===========================================================================

const BYOSNAP_ID = 'byosnap-core';

// Base URL of the Eventbus internal HTTP endpoint. Injected by Snapser at
// runtime. When empty (e.g. local dev without an Eventbus), the calls below
// no-op.
const EVENTBUS_HTTP_URL = process.env.SNAPEND_EVENTBUS_HTTP_URL || '';

// Value of the `Gateway` header that marks a call as internal (Snap-to-Snap).
const INTERNAL_HEADER_VALUE = process.env.SNAPEND_INTERNAL_HEADER || 'internal';

// How long to wait on an Eventbus HTTP call before giving up (ms).
const REQUEST_TIMEOUT_MS = 5000;

function eventbusHeaders(): Record<string, string> {
    return {
        'Content-Type': 'application/json',
        // Marks this as an internal Snap-to-Snap call through the gateway.
        'Gateway': INTERNAL_HEADER_VALUE,
    };
}

/**
 * Register the custom event types this Snap publishes.
 *
 * Call this ONCE on startup (see server.ts). It is BEST-EFFORT: it logs
 * success or failure and never throws, so a missing/unreachable Eventbus can
 * never crash the process or block the /healthz probe.
 *
 * PUT {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/event-types/byosnap-core
 */
export async function registerEventTypes(): Promise<void> {
    if (!EVENTBUS_HTTP_URL) {
        console.log('[eventbus] SNAPEND_EVENTBUS_HTTP_URL not set - skipping event type registration.');
        return;
    }

    const url = `${EVENTBUS_HTTP_URL}/v1/eventbus/byo/event-types/${BYOSNAP_ID}`;

    // TODO: Customize the event types your Snap publishes. Each entry declares
    //       one subject the Eventbus will accept from this Snap.
    const body = {
        event_types: [
            {
                subject: 'byosnap-core.example.created',
                service_name: 'byosnap-core',
                message_type: 'example',
                event_type_id: 0,
                event_type_enum_value: 0,
                description: 'Example custom event registered by byosnap-core',
            },
        ],
    };

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
    try {
        const res = await fetch(url, {
            method: 'PUT',
            headers: eventbusHeaders(),
            body: JSON.stringify(body),
            signal: controller.signal,
        });
        if (res.ok) {
            console.log('[eventbus] Registered event types successfully.');
        } else {
            console.warn(`[eventbus] Event type registration returned HTTP ${res.status}.`);
        }
    } catch (err) {
        // Best-effort: log and move on. Never rethrow.
        console.warn('[eventbus] Failed to register event types:', err);
    } finally {
        clearTimeout(timeout);
    }
}

/**
 * Publish a single event onto the Eventbus.
 *
 * Reusable BEST-EFFORT helper: it logs and swallows errors so a publish never
 * breaks your request flow. Call it from your own business logic wherever you
 * want to emit an event.
 *
 * POST {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/events/byosnap-core/{subject}
 *
 * @param subject    The event subject, e.g. "byosnap-core.example.created".
 * @param recipients Recipient user IDs the event should be delivered to.
 * @param message    Arbitrary event payload object (serialized as JSON).
 *
 * @example
 *   await publishEvent(
 *       'byosnap-core.example.created',
 *       ['user-123'],
 *       { exampleId: 'abc', name: 'My Example' },
 *   );
 */
export async function publishEvent(
    subject: string,
    recipients: string[],
    message: unknown,
): Promise<void> {
    if (!EVENTBUS_HTTP_URL) {
        console.log('[eventbus] SNAPEND_EVENTBUS_HTTP_URL not set - skipping publishEvent.');
        return;
    }

    const url = `${EVENTBUS_HTTP_URL}/v1/eventbus/byo/events/${BYOSNAP_ID}/${subject}`;

    // TODO: Set event_type_id to match the registered event type for `subject`,
    //       and populate `payload` if your consumers expect a raw string body.
    const body = {
        event_type_id: 0,
        message,
        payload: '',
        recipients,
    };

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: eventbusHeaders(),
            body: JSON.stringify(body),
            signal: controller.signal,
        });
        if (res.ok) {
            console.log(`[eventbus] Published event "${subject}".`);
        } else {
            console.warn(`[eventbus] Publishing "${subject}" returned HTTP ${res.status}.`);
        }
    } catch (err) {
        // Best-effort: log and move on. Never rethrow.
        console.warn(`[eventbus] Failed to publish event "${subject}":`, err);
    } finally {
        clearTimeout(timeout);
    }
}
