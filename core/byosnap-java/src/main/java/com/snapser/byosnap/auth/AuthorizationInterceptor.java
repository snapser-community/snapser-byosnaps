package com.snapser.byosnap.auth;

import java.util.Map;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.HandlerMapping;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.snapser.byosnap.AppConstants;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * Enforces the {@link ValidateAuthorization} annotation on controller handlers.
 *
 * <p>This is the Java analog of the Python {@code validate_authorization}
 * decorator and the C# {@code ValidateAuthorizationAttribute} action filter.
 * It reads the {@code Auth-Type}, {@code Gateway} and {@code User-Id} headers
 * that Snapser injects, then applies the exact same pass/fail logic:
 * <ul>
 *   <li>an internal call (Gateway: internal) satisfies the {@code internal}
 *       auth type;</li>
 *   <li>an api-key call (not internal, Auth-Type: api-key) satisfies the
 *       {@code api-key} auth type;</li>
 *   <li>a user call (not internal, not api-key, User-Id header equals the target
 *       user id) satisfies the {@code user} auth type.</li>
 * </ul>
 * On failure it returns HTTP 400 with {@code {"error_message":"Unauthorized"}}.
 */
@Component
public class AuthorizationInterceptor implements HandlerInterceptor {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        // Only guard controller methods; let static resources / error pages through.
        if (!(handler instanceof HandlerMethod handlerMethod)) {
            return true;
        }

        ValidateAuthorization annotation = handlerMethod.getMethodAnnotation(ValidateAuthorization.class);
        if (annotation == null) {
            // No annotation => no auth requirement (e.g. /healthz, CORS preflight).
            return true;
        }

        String[] allowedAuthTypes = annotation.value();

        // Gateway header -> internal call?
        String gatewayHeaderValue = safe(request.getHeader(AppConstants.GATEWAY_HEADER_KEY));
        boolean isInternalCall = gatewayHeaderValue.equalsIgnoreCase(AppConstants.GATEWAY_INTERNAL_ORIGIN);

        // Auth-Type header -> api-key call?
        String authTypeHeaderValue = safe(request.getHeader(AppConstants.AUTH_TYPE_HEADER_KEY));
        boolean isApiKeyAuth = authTypeHeaderValue.equalsIgnoreCase(AppConstants.AUTH_TYPE_API_KEY);

        // User-Id header vs. the target user id.
        String userIdHeaderValue = safe(request.getHeader(AppConstants.USER_ID_HEADER_KEY));
        // If the route has a {userId} path variable, use that as the target user.
        // Otherwise fall back to the User-Id header value (same as Python).
        String targetUser = extractPathUserId(request, annotation.userIdPathVariable(), userIdHeaderValue);
        boolean isTargetUser = !userIdHeaderValue.isEmpty() && userIdHeaderValue.equals(targetUser);

        boolean validationPassed = false;
        for (String authType : allowedAuthTypes) {
            if (AppConstants.GATEWAY_INTERNAL_ORIGIN.equals(authType)) {
                // internal: the call must be internal.
                if (!isInternalCall) {
                    continue;
                }
                validationPassed = true;
            } else if (AppConstants.AUTH_TYPE_API_KEY.equals(authType)) {
                // api-key: if not internal, the call must pass the api-key check.
                if (!isInternalCall && !isApiKeyAuth) {
                    continue;
                }
                validationPassed = true;
            } else if (AppConstants.AUTH_TYPE_USER.equals(authType)) {
                // user: if not internal or api-key, the User-Id must match the target.
                if (!isInternalCall && !isApiKeyAuth && !isTargetUser) {
                    continue;
                }
                validationPassed = true;
            }
        }

        if (!validationPassed) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.setContentType(MediaType.APPLICATION_JSON_VALUE);
            response.getWriter().write(MAPPER.writeValueAsString(Map.of("error_message", "Unauthorized")));
            return false;
        }
        return true;
    }

    @SuppressWarnings("unchecked")
    private static String extractPathUserId(HttpServletRequest request, String pathVariable, String defaultValue) {
        Object attr = request.getAttribute(HandlerMapping.URI_TEMPLATE_VARIABLES_ATTRIBUTE);
        if (attr instanceof Map<?, ?> vars) {
            Object value = ((Map<String, String>) vars).get(pathVariable);
            if (value != null) {
                return value.toString();
            }
        }
        return defaultValue;
    }

    private static String safe(String value) {
        return value == null ? "" : value;
    }
}
