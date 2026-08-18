package com.snapser.byosnap.logging;

import java.io.IOException;

import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import com.snapser.byosnap.AppConstants;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * Binds the Snapser {@code X-Request-Id} header to MDC for the duration of each
 * request.
 *
 * <p>Snapser sends {@code X-Request-Id} on every request and correlates all log
 * lines of one request across snaps by it. Binding it to MDC ONCE here means
 * every log call on the request thread picks it up automatically (see
 * {@link SnapserJsonLayout}) — no need to pass the id to each log statement.
 */
@Component
public class RequestIdFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {
        String requestId = request.getHeader(AppConstants.REQUEST_ID_HEADER_KEY);
        if (requestId != null) {
            requestId = sanitizeRequestId(requestId);
        }
        if (requestId != null && !requestId.isEmpty()) {
            MDC.put(AppConstants.REQUEST_ID_MDC_KEY, requestId);
        }
        try {
            filterChain.doFilter(request, response);
        } finally {
            // Tomcat pools request threads — always clear so no id leaks into
            // the next request served by this thread.
            MDC.remove(AppConstants.REQUEST_ID_MDC_KEY);
        }
    }

    // X-Request-Id is client-supplied: cap the length and allow only safe chars.
    private static String sanitizeRequestId(String value) {
        if (value.length() > 128) {
            value = value.substring(0, 128);
        }
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            boolean ok = (c >= '0' && c <= '9') || (c >= 'a' && c <= 'z')
                    || (c >= 'A' && c <= 'Z') || c == '-' || c == '_' || c == '.';
            if (!ok) {
                return "";
            }
        }
        return value;
    }
}
