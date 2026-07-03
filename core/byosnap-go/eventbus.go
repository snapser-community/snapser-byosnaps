package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"
)

// ===========================================================================
// Eventbus: registering custom event types, publishing events, and receiving
// events delivered by the Snapser Eventbus.
//
// Internal Snap-to-Snap calls target the Eventbus service over the internal
// gateway. The base URL comes from the SNAPEND_EVENTBUS_HTTP_URL env var
// (mirrors SNAPEND_STORAGE_HTTP_URL for the Storage Snap) and every request
// carries the `Gateway: internal` header (value read from
// SNAPEND_INTERNAL_HEADER, default "internal").
//
// See advanced/byosnap-go for complete, working implementations.
// ===========================================================================

// eventbusHTTPClient is a short-timeout client for internal Eventbus calls so
// a slow/unreachable Eventbus never blocks boot or an inbound request.
var eventbusHTTPClient = &http.Client{Timeout: 5 * time.Second}

// registerEventTypes registers this Snap's custom event types with the Snapser
// Eventbus. It is called ONCE from main() on startup and is BEST-EFFORT: it
// logs success or failure and never crashes or blocks boot. If
// SNAPEND_EVENTBUS_HTTP_URL is not set (e.g. the Eventbus Snap isn't part of
// this Snapend) it logs and skips.
//
// PUT {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/event-types/{BYOSnapID}
func registerEventTypes() {
	eventbusURL := getEnv(EventbusHTTPURLEnvKey, "")
	if eventbusURL == "" {
		log.Printf("Eventbus: %s not set, skipping event-type registration", EventbusHTTPURLEnvKey)
		return
	}

	// TODO: Customize the event types your Snap emits. `subject` is the routing
	//       key other Snaps subscribe to; `service_name` should be this Snap's
	//       id; `message_type` names the payload shape. Add one entry per event.
	body := map[string]interface{}{
		"event_types": []map[string]interface{}{
			{
				"subject":              fmt.Sprintf("%s.example.created", BYOSnapID),
				"service_name":         BYOSnapID,
				"message_type":         "example",
				"event_type_id":        0,
				"event_type_enum_value": 0,
				"description":          fmt.Sprintf("Example custom event registered by %s", BYOSnapID),
			},
		},
	}

	payload, err := json.Marshal(body)
	if err != nil {
		log.Printf("Eventbus: failed to marshal event-type registration body: %v", err)
		return
	}

	url := fmt.Sprintf("%s/v1/eventbus/byo/event-types/%s", eventbusURL, BYOSnapID)
	req, err := http.NewRequest(http.MethodPut, url, bytes.NewReader(payload))
	if err != nil {
		log.Printf("Eventbus: failed to build event-type registration request: %v", err)
		return
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set(GatewayHeaderKey, getEnv(InternalHeaderEnvKey, DefaultInternalHeaderValue))

	resp, err := eventbusHTTPClient.Do(req)
	if err != nil {
		log.Printf("Eventbus: event-type registration request failed: %v", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		respBody, _ := io.ReadAll(resp.Body)
		log.Printf("Eventbus: event-type registration returned %d: %s", resp.StatusCode, string(respBody))
		return
	}

	log.Printf("Eventbus: registered event types for %s", BYOSnapID)
}

// publishEvent publishes a single event to the Snapser Eventbus. It is a
// reusable, BEST-EFFORT helper: it logs on failure and returns an error you can
// choose to ignore. It is intentionally NOT wired into any endpoint's normal
// flow — call it from your own business logic where an event should fire.
//
// Example:
//
//	go publishEvent(
//	    fmt.Sprintf("%s.example.created", BYOSnapID),
//	    []string{"user-123"},                       // recipients (empty = broadcast)
//	    map[string]interface{}{"example_id": "abc"}, // your payload
//	)
//
// POST {SNAPEND_EVENTBUS_HTTP_URL}/v1/eventbus/byo/events/{BYOSnapID}/{subject}
func publishEvent(subject string, recipients []string, message map[string]interface{}) error {
	eventbusURL := getEnv(EventbusHTTPURLEnvKey, "")
	if eventbusURL == "" {
		log.Printf("Eventbus: %s not set, skipping publish of %q", EventbusHTTPURLEnvKey, subject)
		return nil
	}

	// TODO: Set event_type_id to match the event type you registered in
	//       registerEventTypes(), and populate `message`/`recipients` for your
	//       use case. `payload` is an optional opaque string.
	body := map[string]interface{}{
		"event_type_id": 0,
		"message":       message,
		"payload":       "",
		"recipients":    recipients,
	}

	payload, err := json.Marshal(body)
	if err != nil {
		log.Printf("Eventbus: failed to marshal publish body for %q: %v", subject, err)
		return err
	}

	url := fmt.Sprintf("%s/v1/eventbus/byo/events/%s/%s", eventbusURL, BYOSnapID, subject)
	req, err := http.NewRequest(http.MethodPost, url, bytes.NewReader(payload))
	if err != nil {
		log.Printf("Eventbus: failed to build publish request for %q: %v", subject, err)
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set(GatewayHeaderKey, getEnv(InternalHeaderEnvKey, DefaultInternalHeaderValue))

	resp, err := eventbusHTTPClient.Do(req)
	if err != nil {
		log.Printf("Eventbus: publish request for %q failed: %v", subject, err)
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		respBody, _ := io.ReadAll(resp.Body)
		log.Printf("Eventbus: publish of %q returned %d: %s", subject, resp.StatusCode, string(respBody))
		return fmt.Errorf("eventbus publish returned status %d", resp.StatusCode)
	}

	log.Printf("Eventbus: published event %q", subject)
	return nil
}

// eventHandler receives events delivered by the Snapser Eventbus. The Eventbus
// POSTs to this RESERVED, root-level URL (/internal/events) — no /v1 prefix and
// no BYOSnap id, like /healthz. It is intentionally NOT annotated with
// swagger:operation so it stays out of the generated SDK spec.
//
// This stub reads and logs the delivered body, then returns 200 so the Eventbus
// marks delivery as successful.
func eventHandler(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		log.Printf("Eventbus: failed to read inbound event body: %v", err)
		w.WriteHeader(http.StatusOK)
		return
	}

	log.Printf("Eventbus: received event: %s", string(body))

	// TODO: Parse the body and switch on the event `subject` to dispatch to your
	//       own handlers. Return 200 once you have accepted the event.
	w.WriteHeader(http.StatusOK)
}
