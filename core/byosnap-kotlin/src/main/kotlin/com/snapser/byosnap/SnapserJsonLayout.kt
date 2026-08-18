/*
 * Snapser structured-log layout.
 *
 * Snapser reads a snap's stdout and parses each line as one JSON object:
 *   - `level`      colors the line in the Logs tool (debug/info/warn/error).
 *   - `message`    the log text (plus stack trace when a throwable is logged).
 *   - `timestamp`  ISO-8601 event time.
 *   - `request-id` correlates all log lines of one request across snaps, and
 *                  lets Snapser sample logs per-request instead of per-line.
 *
 * Wired into the ConsoleAppender in src/main/resources/logback.xml through a
 * LayoutWrappingEncoder, so every existing LoggerFactory logger emits this
 * shape with no call-site changes.
 */
package com.snapser.byosnap

import ch.qos.logback.classic.Level
import ch.qos.logback.classic.spi.ILoggingEvent
import ch.qos.logback.classic.spi.ThrowableProxyUtil
import ch.qos.logback.core.CoreConstants
import ch.qos.logback.core.LayoutBase
import java.time.Instant
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put

class SnapserJsonLayout : LayoutBase<ILoggingEvent>() {
    override fun doLayout(event: ILoggingEvent): String {
        // Snapser expects lowercase level names; TRACE folds into debug.
        val level = when (event.level.toInt()) {
            Level.ERROR_INT -> "error"
            Level.WARN_INT -> "warn"
            Level.INFO_INT -> "info"
            else -> "debug"
        }
        val message = buildString {
            append(event.formattedMessage ?: "")
            event.throwableProxy?.let {
                append(CoreConstants.LINE_SEPARATOR)
                append(ThrowableProxyUtil.asString(it))
            }
        }
        // buildJsonObject handles all JSON escaping for us.
        val line = buildJsonObject {
            put("level", level)
            put("message", message)
            put("timestamp", Instant.ofEpochMilli(event.timeStamp).toString())
            // Bound once per request in Application.kt; absent on boot-time logs.
            event.mdcPropertyMap[REQUEST_ID_MDC_KEY]?.takeIf { it.isNotBlank() }?.let {
                put(REQUEST_ID_MDC_KEY, it)
            }
        }
        return line.toString() + CoreConstants.LINE_SEPARATOR
    }
}
