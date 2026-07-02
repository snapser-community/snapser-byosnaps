package com.snapser.byosnap;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Core Java BYOSnap Example — minimal starter scaffold.
 *
 * <p>This is the recommended starting point for a new Java BYOSnap. Every
 * endpoint Snapser expects is present, but each handler body is a STUB: it
 * returns a simple placeholder and carries a {@code // TODO} describing what you
 * would implement here.
 *
 * <p>The boilerplate that is already wired up for you (and should usually stay
 * as-is):
 * <ul>
 *   <li>The {@code BYOSNAP_ID} / {@code API_PREFIX} constants in
 *       {@link AppConstants} that build every route prefix.</li>
 *   <li>The {@code @ValidateAuthorization} annotation + interceptor
 *       (User / Api-Key / Internal auth checks).</li>
 *   <li>The {@code /healthz} readiness endpoint.</li>
 *   <li>The CORS configuration.</li>
 *   <li>The hand-authored {@code snapser-resources/swagger.json} that drives
 *       SDK + API Explorer generation.</li>
 * </ul>
 */
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
