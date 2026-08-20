package com.snapser.byosnap.logging;

import java.time.format.DateTimeFormatter;

import com.fasterxml.jackson.core.io.JsonStringEncoder;
import com.snapser.byosnap.AppConstants;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.classic.spi.IThrowableProxy;
import ch.qos.logback.classic.spi.ThrowableProxyUtil;
import ch.qos.logback.core.CoreConstants;
import ch.qos.logback.core.LayoutBase;

/**
 * Emits each log event as ONE JSON object per line on stdout — the format the
 * Snapser Logs tool ingests:
 *
 * <ul>
 *   <li>{@code level} — lowercase {@code debug|info|warn|error}. Snapser parses
 *       this to color the line.</li>
 *   <li>{@code message} — the formatted log text (plus stack trace if any).</li>
 *   <li>{@code timestamp} — ISO-8601.</li>
 *   <li>{@code request-id} — from MDC when present. Snapser correlates all log
 *       lines of one request across snaps by this field, and samples logs
 *       per-request instead of per-line.</li>
 * </ul>
 *
 * <p>Built on logback + Jackson, both already bundled by Spring Boot — no extra
 * dependency (e.g. logstash-logback-encoder) needed.
 */
public class SnapserJsonLayout extends LayoutBase<ILoggingEvent> {

    private static final JsonStringEncoder JSON = JsonStringEncoder.getInstance();

    @Override
    public String doLayout(ILoggingEvent event) {
        StringBuilder sb = new StringBuilder(256);
        sb.append("{\"level\":\"").append(mapLevel(event.getLevel()))
                .append("\",\"message\":\"");
        JSON.quoteAsString(buildMessage(event), sb);
        sb.append("\",\"timestamp\":\"")
                .append(DateTimeFormatter.ISO_INSTANT.format(event.getInstant()))
                .append('"');

        // request-id is bound to MDC once per request by RequestIdFilter.
        String requestId = event.getMDCPropertyMap().get(AppConstants.REQUEST_ID_MDC_KEY);
        if (requestId != null && !requestId.isEmpty()) {
            sb.append(",\"request-id\":\"");
            JSON.quoteAsString(requestId, sb);
            sb.append('"');
        }

        sb.append('}').append(CoreConstants.LINE_SEPARATOR);
        return sb.toString();
    }

    /** Snapser accepts only lowercase debug/info/warn/error. */
    private static String mapLevel(Level level) {
        return switch (level.toInt()) {
            case Level.TRACE_INT, Level.DEBUG_INT -> "debug";
            case Level.WARN_INT -> "warn";
            case Level.ERROR_INT -> "error";
            default -> "info";
        };
    }

    private static String buildMessage(ILoggingEvent event) {
        IThrowableProxy throwable = event.getThrowableProxy();
        if (throwable == null) {
            return event.getFormattedMessage();
        }
        return event.getFormattedMessage() + CoreConstants.LINE_SEPARATOR
                + ThrowableProxyUtil.asString(throwable);
    }
}
