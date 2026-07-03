package com.snapser.byosnap.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Inbound Eventbus receiver.
 *
 * <p>The Snapser Eventbus delivers events to this Snap by POSTing to the
 * RESERVED, root-level URL {@code /internal/events} — like {@code /healthz}, it
 * takes NO {@code /v1} prefix and NO BYOSnap id.
 *
 * <p>Because this route is reserved and not part of the public API, it is
 * intentionally kept OUT of the hand-authored
 * {@code snapser-resources/swagger.json} (so it never surfaces in generated
 * SDKs / the API Explorer). Do not add it there.
 *
 * <p>This stub reads and logs the delivered body, then returns 200 so the
 * Eventbus marks delivery as successful.
 */
@RestController
public class EventReceiverController {

    private static final Logger log = LoggerFactory.getLogger(EventReceiverController.class);

    @PostMapping("/internal/events")
    public ResponseEntity<String> receiveEvent(@RequestBody(required = false) String body) {
        log.info("[eventbus] Received event: {}", body);

        // TODO: Parse the body and switch on the event `subject` to dispatch to
        //       your own handlers. Return 200 once you have accepted the event.
        return ResponseEntity.ok("Ok");
    }
}
