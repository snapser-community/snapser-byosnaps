using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

namespace ByoSnapCSharp.Utilities
{
  /// <summary>
  /// Binds the incoming X-Request-Id header to a log scope once per request, so
  /// every log line in the request gets a `request-id` JSON field. Snapser
  /// correlates all log lines of one request across snaps by this field —
  /// no need to pass the id to each log call.
  /// </summary>
  public class RequestIdLoggingMiddleware
  {
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestIdLoggingMiddleware> _logger;

    public RequestIdLoggingMiddleware(
      RequestDelegate next, ILogger<RequestIdLoggingMiddleware> logger)
    {
      _next = next;
      _logger = logger;
    }

    // X-Request-Id is client-supplied: cap the length and allow only safe chars.
    public static string SanitizeRequestId(string value)
    {
      if (value.Length > 128) value = value.Substring(0, 128);
      foreach (var c in value)
      {
        if (!char.IsAsciiLetterOrDigit(c) && c != '-' && c != '_' && c != '.')
          return string.Empty;
      }
      return value;
    }

    public async Task InvokeAsync(HttpContext context)
    {
      var requestId = SanitizeRequestId(
        context.Request.Headers[AppConstants.requestIdHeaderKey].ToString());
      if (string.IsNullOrEmpty(requestId))
      {
        await _next(context);
        return;
      }

      using (_logger.BeginScope(
        new Dictionary<string, object> { ["request-id"] = requestId }))
      {
        await _next(context);
      }
    }
  }
}
