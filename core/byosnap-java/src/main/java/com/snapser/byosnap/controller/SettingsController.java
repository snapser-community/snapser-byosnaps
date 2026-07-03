package com.snapser.byosnap.controller;

import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.snapser.byosnap.AppConstants;
import com.snapser.byosnap.auth.ValidateAuthorization;

/**
 * System endpoints Snapser expects every BYOSnap to expose.
 *
 * <p>These power the Configuration Tool (UI Builder + Custom HTML), the User
 * Manager Tool, the Snapend Sync/Clone import-export system, and the GDPR user
 * data tooling. Every handler here is guarded {@code internal} because Snapser
 * calls them through the internal gateway. Each body is a STUB — fill in the
 * TODOs with your own persistence (e.g. via the Snapser Storage snap).
 */
@RestController
public class SettingsController {

    // =====================================================================
    // A i] Configuration Tool: built with the Snapser UI Builder
    // =====================================================================

    @GetMapping(AppConstants.API_PREFIX + "/settings")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> getSettings(
            @RequestParam(name = "tool_id", required = false) String toolId,
            @RequestParam(name = "environment", required = false, defaultValue = AppConstants.DEFAULT_ENVIRONMENT) String environment) {
        // This is the default payload shape the Configuration Tool expects.
        Map<String, Object> defaultSettings = Map.of(
                "sections", List.of(Map.of(
                        "id", "registration",
                        "components", List.of(Map.of(
                                "id", "characters",
                                "type", "textarea",
                                "value", "")))));
        String blobOwnerKey = toolId + "_" + environment;
        // TODO: Fetch the saved settings for `blobOwnerKey` (e.g. from the Storage
        //       snap) and return them. For now we return the default shape.
        return ResponseEntity.ok(defaultSettings);
    }

    @PutMapping(AppConstants.API_PREFIX + "/settings")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> updateSettings(
            @RequestParam(name = "tool_id", required = false) String toolId,
            @RequestParam(name = "environment", required = false, defaultValue = AppConstants.DEFAULT_ENVIRONMENT) String environment,
            @RequestBody(required = false) Map<String, Object> body) {
        String blobOwnerKey = toolId + "_" + environment;
        Object blobData = (body != null && body.containsKey("payload")) ? body.get("payload") : body;
        // TODO: Validate `blobData` and persist it for `blobOwnerKey` (e.g. via
        //       the Storage snap). On a validation failure return a 400 with an
        //       error_message body.
        return ResponseEntity.ok(Map.of("success", true));
    }

    // =====================================================================
    // A ii] Configuration Tool: custom HTML Snap configuration tool
    // =====================================================================

    @GetMapping(AppConstants.API_PREFIX + "/settings/custom")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> getSettingsCustom(
            @RequestParam(name = "tool_id", required = false) String toolId,
            @RequestParam(name = "environment", required = false, defaultValue = AppConstants.DEFAULT_ENVIRONMENT) String environment) {
        String blobOwnerKey = toolId + "_" + environment;
        // TODO: Fetch the saved settings for `blobOwnerKey` and return them
        //       wrapped as {"payload": <settings>}.
        return ResponseEntity.ok(Map.of("payload", ""));
    }

    @PutMapping(AppConstants.API_PREFIX + "/settings/custom")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> updateSettingsCustom(
            @RequestParam(name = "tool_id", required = false) String toolId,
            @RequestParam(name = "environment", required = false, defaultValue = AppConstants.DEFAULT_ENVIRONMENT) String environment,
            @RequestBody(required = false) Map<String, Object> body) {
        String blobOwnerKey = toolId + "_" + environment;
        Object blobData = (body != null && body.containsKey("payload")) ? body.get("payload") : body;
        // TODO: Validate `blobData` and persist it for `blobOwnerKey`. On a
        //       validation failure return a 400 with an error_message body.
        return ResponseEntity.ok(Map.of("success", true));
    }

    // =====================================================================
    // A iii] User Manager Tool: custom HTML user manager tool
    // =====================================================================

    @GetMapping(AppConstants.API_PREFIX + "/settings/users/{userId}/custom")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> getUserDataCustom(@PathVariable String userId) {
        // TODO: Look up this user's data (e.g. from the Storage snap) and return
        //       it wrapped as {"payload": <data>}.
        return ResponseEntity.ok(Map.of("payload", ""));
    }

    @PostMapping(AppConstants.API_PREFIX + "/settings/users/{userId}/custom")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> updateUserDataCustom(
            @PathVariable String userId,
            @RequestBody(required = false) Map<String, Object> body) {
        Object blobData = (body != null && body.containsKey("payload")) ? body.get("payload") : body;
        // TODO: Validate `blobData` and persist it for this userId.
        return ResponseEntity.ok(Map.of("success", true));
    }

    // =====================================================================
    // B] Snapend Sync/Clone: Snapser's built-in configuration import/export
    // =====================================================================

    @GetMapping(AppConstants.API_PREFIX + "/settings/export")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> settingsExport() {
        // Snapser calls this when cloning/syncing a Snapend. Return your settings
        // for every environment so they can be re-imported elsewhere.
        Map<String, Object> emptyToolPayload = Map.of(
                "sections", List.of(Map.of(
                        "id", "registration",
                        "components", List.of(Map.of(
                                "id", "characters",
                                "type", "textarea",
                                "value", "")))));
        String version = System.getenv().getOrDefault(
                AppConstants.BYOSNAP_VERSION_ENV_KEY, AppConstants.DEFAULT_BYOSNAP_VERSION);
        Map<String, Object> response = Map.of(
                "version", version,
                "exported_at", 0,
                "data", Map.of(
                        // The key here ("characters") is the Tool ID whose payload you export.
                        "dev", Map.of("characters", emptyToolPayload),
                        "stage", Map.of("characters", emptyToolPayload),
                        "prod", Map.of("characters", emptyToolPayload)));
        // TODO: Load the real saved settings per environment (e.g. batch-get from
        //       the Storage snap) and merge them into response["data"].
        return ResponseEntity.ok(response);
    }

    @PostMapping(AppConstants.API_PREFIX + "/settings/import")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> settingsImport(@RequestBody(required = false) Map<String, Object> body) {
        // TODO: Validate the incoming export payload and persist each
        //       environment's settings (e.g. batch-replace on the Storage snap).
        if (body == null || body.isEmpty()) {
            return ResponseEntity.internalServerError().body(Map.of("error_message", "Invalid JSON"));
        }
        return ResponseEntity.ok(Map.of("message", "Success"));
    }

    @PostMapping(AppConstants.API_PREFIX + "/settings/validate-import")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> validateSettingsImport(@RequestBody(required = false) Map<String, Object> body) {
        // Snapser sends the settings it is about to import. Decide whether you
        // can accept them: return 200 with the payload if so, 500 otherwise.
        // TODO: Add your own validation here (e.g. check the dev/stage/prod
        //       structure).
        if (body == null || body.isEmpty()) {
            return ResponseEntity.internalServerError().body(Map.of("error_message", "Invalid JSON"));
        }
        return ResponseEntity.ok(body);
    }

    // =====================================================================
    // C] User Tool: get / update / delete user data
    //    Used by the GDPR tool and the User Manager tool.
    // =====================================================================

    @GetMapping(AppConstants.API_PREFIX + "/settings/users/{userId}/data")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> getUserData(@PathVariable String userId) {
        // TODO: Fetch and return everything you store for this userId (e.g. from
        //       the Storage snap).
        return ResponseEntity.ok(Map.of());
    }

    @PutMapping(AppConstants.API_PREFIX + "/settings/users/{userId}/data")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> updateUserData(
            @PathVariable String userId,
            @RequestBody(required = false) Map<String, Object> body) {
        // TODO: Persist the incoming data for this userId.
        return ResponseEntity.ok(Map.of());
    }

    @DeleteMapping(AppConstants.API_PREFIX + "/settings/users/{userId}/data")
    @ValidateAuthorization(AppConstants.GATEWAY_INTERNAL_ORIGIN)
    public ResponseEntity<Object> deleteUserData(@PathVariable String userId) {
        // TODO: Delete everything you store for this userId (right-to-be-forgotten).
        return ResponseEntity.ok(Map.of());
    }
}
