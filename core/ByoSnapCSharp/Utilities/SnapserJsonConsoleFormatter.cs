using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.Extensions.Logging.Console;

namespace ByoSnapCSharp.Utilities
{
  /// <summary>
  /// Writes each log record to stdout as one JSON object per line with `level`,
  /// `message` and `timestamp` fields. Snapser parses `level` to color the line
  /// in the Logs tool, and correlates all lines of one request by the
  /// `request-id` field (bound as a log scope by RequestIdLoggingMiddleware).
  /// </summary>
  public sealed class SnapserJsonConsoleFormatter : ConsoleFormatter
  {
    public const string FormatterName = "snapser-json";

    // Framework scopes (hosting, Kestrel, MVC, activity tracking) add these
    // noisy fields to every request log line. Note Kestrel's `RequestId` is a
    // connection id, NOT the Snapser `request-id`.
    private static readonly HashSet<string> FrameworkScopeKeys = new()
    {
      "SpanId", "TraceId", "ParentId", "ConnectionId",
      "RequestId", "RequestPath", "ActionId", "ActionName"
    };

    public SnapserJsonConsoleFormatter() : base(FormatterName) { }

    public override void Write<TState>(
      in LogEntry<TState> logEntry,
      IExternalScopeProvider? scopeProvider,
      TextWriter textWriter)
    {
      var message = logEntry.Formatter?.Invoke(logEntry.State, logEntry.Exception);
      if (string.IsNullOrEmpty(message) && logEntry.Exception == null)
      {
        return;
      }

      using var stream = new MemoryStream();
      using (var writer = new Utf8JsonWriter(stream))
      {
        writer.WriteStartObject();
        writer.WriteString("level", ToSnapserLevel(logEntry.LogLevel));
        writer.WriteString("message", message);
        // UtcDateTime keeps the ISO-8601 "Z" suffix; the "+00:00" offset form
        // would be escaped as + by Utf8JsonWriter.
        writer.WriteString("timestamp", DateTimeOffset.UtcNow.UtcDateTime.ToString("o"));
        if (logEntry.Exception != null)
        {
          writer.WriteString("exception", logEntry.Exception.ToString());
        }

        // Emit key/value scope items (e.g. request-id) as top-level JSON fields.
        scopeProvider?.ForEachScope((scope, state) =>
        {
          if (scope is IEnumerable<KeyValuePair<string, object>> pairs)
          {
            foreach (var pair in pairs)
            {
              // Skip message-template metadata, reserved field names, and
              // framework scope noise.
              if (pair.Key.StartsWith("{", StringComparison.Ordinal) ||
                  pair.Key is "level" or "message" or "timestamp" or "exception" ||
                  FrameworkScopeKeys.Contains(pair.Key))
              {
                continue;
              }
              state.WriteString(pair.Key, Convert.ToString(pair.Value));
            }
          }
        }, writer);

        writer.WriteEndObject();
      }

      textWriter.WriteLine(Encoding.UTF8.GetString(stream.ToArray()));
    }

    /// <summary>
    /// Maps LogLevel to the lowercase level names Snapser understands.
    /// </summary>
    private static string ToSnapserLevel(LogLevel level) => level switch
    {
      LogLevel.Trace or LogLevel.Debug => "debug",
      LogLevel.Information => "info",
      LogLevel.Warning => "warn",
      _ => "error",
    };
  }
}
