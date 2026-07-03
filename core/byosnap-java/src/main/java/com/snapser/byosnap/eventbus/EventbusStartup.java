package com.snapser.byosnap.eventbus;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

/**
 * Registers this Snap's custom event types with the Snapser Eventbus ONCE on
 * startup.
 *
 * <p>Runs after the application is fully up ({@link ApplicationReadyEvent} fires
 * exactly once). The registration is done on a background thread and is
 * BEST-EFFORT — {@link EventbusClient#registerEventTypes()} never throws and
 * carries its own short timeout — so it can never block boot or crash the app /
 * the {@code /healthz} probe.
 */
@Component
public class EventbusStartup {

    private static final Logger log = LoggerFactory.getLogger(EventbusStartup.class);

    private final EventbusClient eventbusClient;

    public EventbusStartup(EventbusClient eventbusClient) {
        this.eventbusClient = eventbusClient;
    }

    /** Fires once, after the app is ready. */
    @EventListener(ApplicationReadyEvent.class)
    public void onApplicationReady() {
        // Run off the main thread so even an unexpected delay cannot hold up
        // readiness. registerEventTypes() is already best-effort + time-bounded.
        Thread worker = new Thread(() -> {
            try {
                eventbusClient.registerEventTypes();
            } catch (Exception e) {
                // Defensive: registerEventTypes() should already swallow
                // everything, but never let startup registration escape.
                log.warn("[eventbus] Event type registration failed on startup: {}", e.getMessage());
            }
        }, "eventbus-register");
        worker.setDaemon(true);
        worker.start();
    }
}
