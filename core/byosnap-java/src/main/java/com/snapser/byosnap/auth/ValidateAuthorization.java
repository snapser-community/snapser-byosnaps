package com.snapser.byosnap.auth;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Marks a controller handler with the Snapser auth types it accepts.
 *
 * <p>Mirrors the Python {@code @validate_authorization(...)} decorator and the
 * C# {@code [ValidateAuthorization(...)]} attribute. Pass the auth types this
 * endpoint should accept (any of {@code AppConstants.AUTH_TYPE_USER},
 * {@code AppConstants.AUTH_TYPE_API_KEY}, {@code AppConstants.GATEWAY_INTERNAL_ORIGIN}).
 * Snapser injects the relevant headers; {@link AuthorizationInterceptor}
 * enforces them so you get authorization checks for free.
 *
 * <p>Note on Admin-SDK APIs: admin calls reach the Snap through the internal
 * gateway, so guard admin endpoints with {@code GATEWAY_INTERNAL_ORIGIN} and
 * expose them by adding {@code admin} to the swagger {@code x-snapser-auth-types}
 * tag.
 *
 * <p>{@code userIdPathVariable} is the name of the {@code {userId}} path
 * variable used for the User-auth ownership check (empty when the route has no
 * user id in the path, in which case the {@code User-Id} header is used).
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidateAuthorization {

    /** The auth types this endpoint accepts. */
    String[] value();

    /** Name of the path variable holding the target user id (default "userId"). */
    String userIdPathVariable() default "userId";
}
