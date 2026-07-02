package com.snapser.byosnap.controller;

import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import com.snapser.byosnap.AppConstants;
import com.snapser.byosnap.auth.ValidateAuthorization;

/**
 * Example business-logic endpoints — templates for your own APIs.
 *
 * <p>Each stub demonstrates one Snapser auth exposure. The
 * {@code x-snapser-auth-types} tag in {@code snapser-resources/swagger.json}
 * controls which SDK / tool the API surfaces in, and the matching
 * {@link ValidateAuthorization} annotation enforces it at runtime. Add, rename,
 * or remove these to fit your Snap.
 *
 * <p>A single endpoint can accept MULTIPLE auth types at once (see the last
 * example) — you do NOT need a separate route per auth type.
 */
@RestController
public class ExampleController {

    /** Example endpoint exposed over User auth. */
    @GetMapping(AppConstants.API_PREFIX + "/users/{userId}/example")
    @ValidateAuthorization(AppConstants.AUTH_TYPE_USER)
    public ResponseEntity<Object> exampleUser(@PathVariable String userId) {
        // TODO: add your business logic here
        return ResponseEntity.ok(Map.of("message", "Hello user " + userId));
    }

    /** Example endpoint exposed over Api-Key auth. */
    @GetMapping(AppConstants.API_PREFIX + "/example/api-key")
    @ValidateAuthorization(AppConstants.AUTH_TYPE_API_KEY)
    public ResponseEntity<Object> exampleApiKey() {
        // TODO: add your business logic here
        return ResponseEntity.ok(Map.of("message", "Hello api-key caller"));
    }

    /** Example endpoint exposed over Internal auth. */
    @GetMapping(AppConstants.API_PREFIX + "/example/internal")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> exampleInternal() {
        // TODO: add your business logic here
        return ResponseEntity.ok(Map.of("message", "Hello internal caller"));
    }

    /**
     * Example endpoint surfaced in the special Admin SDK.
     *
     * <p>Note: {@code admin} is NOT an auth type. The endpoint is exposed over
     * normal auth types (here api-key + internal); the
     * {@code x-snapser-sdk-categories: [admin]} tag in the swagger is what places it
     * in the Admin SDK (used by admin tooling / the Snapser dashboard). List the
     * real auth types you want to allow in both the swagger
     * {@code x-snapser-auth-types} tag and the {@link ValidateAuthorization}
     * annotation below.
     */
    @GetMapping(AppConstants.API_PREFIX + "/example/admin")
    @ValidateAuthorization({
            AppConstants.AUTH_TYPE_API_KEY,
            AppConstants.GATEWAY_INTERNAL_ORIGIN
    })
    public ResponseEntity<Object> exampleAdmin() {
        // This endpoint is reachable via api-key or internal auth (enforced by
        // the annotation). The x-snapser-sdk-categories: [admin] tag in the swagger
        // is what surfaces it in the Admin SDK.
        // TODO: add your business logic here
        return ResponseEntity.ok(Map.of("message", "Hello admin caller"));
    }

    /**
     * Example endpoint that accepts multiple auth types on ONE route.
     *
     * <p>One endpoint can be reachable by a logged-in user, a valid API key, or
     * an internal Snap. List every auth type you want to allow in both the
     * swagger {@code x-snapser-auth-types} tag (for SDK exposure) and the
     * {@link ValidateAuthorization} annotation (for runtime enforcement) — no
     * need for a separate route per type.
     */
    @GetMapping(AppConstants.API_PREFIX + "/users/{userId}/example/multi-auth")
    @ValidateAuthorization({
            AppConstants.AUTH_TYPE_USER,
            AppConstants.AUTH_TYPE_API_KEY,
            AppConstants.GATEWAY_INTERNAL_ORIGIN
    })
    public ResponseEntity<Object> exampleMultiAuth(@PathVariable String userId) {
        // TODO: add your business logic here
        return ResponseEntity.ok(Map.of("message", "Hello, request for user " + userId + " passed multi-auth"));
    }
}
