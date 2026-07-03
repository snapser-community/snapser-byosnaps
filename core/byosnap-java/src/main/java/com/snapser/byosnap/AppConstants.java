package com.snapser.byosnap;

/**
 * Central constants for the Core Java BYOSnap.
 *
 * <p>BYOSNAP_ID is the URL segment Snapser uses to route to this Snap. Every
 * externally reachable route is prefixed with {@link #API_PREFIX}. Change
 * BYOSNAP_ID in one place instead of editing every route string. Spring
 * {@code @RequestMapping} / {@code @GetMapping} annotations can reference these
 * {@code public static final String} constants directly.
 */
public final class AppConstants {

    private AppConstants() {
    }

    // --- Header Keys ---
    public static final String AUTH_TYPE_HEADER_KEY = "Auth-Type";
    public static final String GATEWAY_HEADER_KEY = "Gateway";
    public static final String USER_ID_HEADER_KEY = "User-Id";

    // --- Header Values ---
    public static final String AUTH_TYPE_USER = "user";
    public static final String AUTH_TYPE_API_KEY = "api-key";
    public static final String GATEWAY_INTERNAL_ORIGIN = "internal";

    // --- BYOSnap Identity ---
    // BYOSNAP_ID is the URL segment Snapser uses to route to this Snap.
    public static final String BYOSNAP_ID = "byosnap-core";
    // Every externally reachable route is prefixed with API_PREFIX ("/v1/byosnap-core").
    public static final String API_PREFIX = "/v1/" + BYOSNAP_ID;

    // --- Environment Keys ---
    public static final String BYOSNAP_VERSION_ENV_KEY = "BYOSNAP_VERSION";
    // Base URL of the Eventbus internal HTTP endpoint (injected by Snapser at
    // runtime). Empty when the Eventbus Snap is not part of this Snapend.
    public static final String EVENTBUS_HTTP_URL_ENV_KEY = "SNAPEND_EVENTBUS_HTTP_URL";
    // Env var whose value is sent as the `Gateway` header on internal calls.
    public static final String INTERNAL_HEADER_ENV_KEY = "SNAPEND_INTERNAL_HEADER";

    // --- Defaults ---
    public static final String DEFAULT_BYOSNAP_VERSION = "v1.0.0";
    public static final String DEFAULT_ENVIRONMENT = "DEFAULT";
    public static final String DEFAULT_INTERNAL_HEADER_VALUE = "internal";
}
