using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace ByoSnapCSharp.Utilities
{
  // =========================================================================
  // Eventbus client (custom BYO events)
  //
  // @GOTCHAS - Eventbus (custom BYO events)
  //   1. Custom event types are registered ONCE with the Eventbus Snap, keyed by
  //      this Snap's id (AppConstants.byoSnapId). After that you can publish
  //      events to those subjects.
  //   2. Internal Snap-to-Snap calls go to the target Snap's base URL (here the
  //      Eventbus, from SNAPEND_EVENTBUS_HTTP_URL) with a `Gateway: internal`
  //      header (value from SNAPEND_INTERNAL_HEADER, default "internal").
  //   3. All of this is BEST-EFFORT. Neither method ever throws to the caller;
  //      failures are caught and logged. Registration must never crash the app
  //      or block boot / the /healthz readiness endpoint.
  // =========================================================================
  public class EventbusClient
  {
    private readonly ILogger<EventbusClient> _logger;
    private readonly HttpClient _httpClient;

    public EventbusClient(ILogger<EventbusClient> logger, HttpClient httpClient)
    {
      _logger = logger;
      _httpClient = httpClient;
    }

    /// <summary>
    /// Base URL of the Eventbus Snap for internal Snap-to-Snap calls. Snapser
    /// injects this into the container's environment when the Eventbus Snap is
    /// part of the Snapend. It is empty in local dev / when the Eventbus is not
    /// attached.
    /// </summary>
    private static string EventbusBaseUrl =>
      Environment.GetEnvironmentVariable(AppConstants.eventbusHttpUrlEnvKey) ?? "";

    /// <summary>
    /// Gateway header value used for internal Snap-to-Snap calls.
    /// </summary>
    private static string GatewayHeaderValue =>
      Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey)
        ?? AppConstants.defaultInternalHeaderValue;

    /// <summary>
    /// Register this Snap's custom event types with the Eventbus Snap.
    ///
    /// Runs ONCE on server startup and is BEST-EFFORT: any failure is logged and
    /// swallowed so it can never crash the app or block boot / /healthz. If the
    /// Eventbus base URL is not configured (e.g. local dev, or the Eventbus Snap
    /// is not part of this Snapend) we log a notice and skip.
    ///
    /// Registration is idempotent, so it is safe to run more than once.
    /// </summary>
    public async Task RegisterEventTypesAsync()
    {
      var baseUrl = EventbusBaseUrl;
      if (string.IsNullOrEmpty(baseUrl))
      {
        _logger.LogInformation(
          "Eventbus base URL not set; skipping custom event type registration");
        return;
      }

      try
      {
        var url = $"{baseUrl}/v1/eventbus/byo/event-types/{AppConstants.byoSnapId}";

        // TODO: Customize the event types you want to register for this Snap.
        var body = new
        {
          event_types = new[]
          {
            new
            {
              subject = "byosnap-core.example.created",
              service_name = "byosnap-core",
              message_type = "example",
              event_type_id = 0,
              event_type_enum_value = 0,
              description = "Example custom event registered by byosnap-core"
            }
          }
        };

        using var request = new HttpRequestMessage(HttpMethod.Put, url)
        {
          Content = new StringContent(
            JsonConvert.SerializeObject(body), Encoding.UTF8, "application/json")
        };
        request.Headers.TryAddWithoutValidation(
          AppConstants.gatewayHeaderKey, GatewayHeaderValue);

        var response = await _httpClient.SendAsync(request);
        _logger.LogInformation(
          "Registered custom event types with the Eventbus (status {StatusCode})",
          (int)response.StatusCode);
      }
      catch (Exception e)
      {
        _logger.LogWarning("Failed to register custom event types: {Message}", e.Message);
      }
    }

    /// <summary>
    /// Publish a custom event to the Eventbus Snap. BEST-EFFORT helper stub.
    ///
    /// Reusable helper you can call from anywhere in your business logic once you
    /// are ready to emit events. Not wired into any endpoint by default.
    ///
    /// Example usage:
    /// <code>
    /// await _eventbusClient.PublishEventAsync(
    ///     "byosnap-core.example.created",
    ///     new[] { "user-123" },
    ///     new { example_id = "abc", created_at = 1700000000 });
    /// </code>
    /// </summary>
    /// <param name="subject">The event subject to publish to.</param>
    /// <param name="recipients">The recipients of the event.</param>
    /// <param name="message">The event message payload (any serializable object).</param>
    public async Task PublishEventAsync(
      string subject, IEnumerable<string> recipients, object message)
    {
      var baseUrl = EventbusBaseUrl;
      if (string.IsNullOrEmpty(baseUrl))
      {
        _logger.LogInformation(
          "Eventbus base URL not set; skipping publish for '{Subject}'", subject);
        return;
      }

      try
      {
        var url = $"{baseUrl}/v1/eventbus/byo/events/{AppConstants.byoSnapId}/{subject}";

        // TODO: Set event_type_id to match the event type you registered above,
        //       and shape `message`/`recipients`/`payload` for your event.
        var body = new
        {
          event_type_id = 0,
          message,
          payload = "",
          recipients
        };

        using var request = new HttpRequestMessage(HttpMethod.Post, url)
        {
          Content = new StringContent(
            JsonConvert.SerializeObject(body), Encoding.UTF8, "application/json")
        };
        request.Headers.TryAddWithoutValidation(
          AppConstants.gatewayHeaderKey, GatewayHeaderValue);

        var response = await _httpClient.SendAsync(request);
        _logger.LogInformation(
          "Published event '{Subject}' (status {StatusCode})",
          subject, (int)response.StatusCode);
      }
      catch (Exception e)
      {
        _logger.LogWarning(
          "Failed to publish event '{Subject}': {Message}", subject, e.Message);
      }
    }
  }
}
