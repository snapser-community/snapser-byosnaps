package com.snapser.byosnap.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Readiness / health check.
 *
 * <p>@GOTCHAS - Health Check Endpoint
 * <ol>
 *   <li>The health URL does NOT take any URL prefix like the other APIs. It is
 *       served at the root ({@code /healthz}).</li>
 * </ol>
 */
@RestController
public class HealthController {

    @GetMapping("/healthz")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Ok");
    }
}
