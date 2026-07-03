using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace ByoSnapCSharp.Utilities
{
  /// <summary>
  /// Registers this Snap's custom event types with the Eventbus Snap ONCE on
  /// application startup.
  ///
  /// This is a BackgroundService so registration runs in the background and never
  /// blocks application boot or the /healthz readiness endpoint. The underlying
  /// EventbusClient.RegisterEventTypesAsync is itself best-effort (it catches and
  /// logs all errors), and this service adds a second try/catch as a safety net
  /// so a startup failure can never crash the host.
  /// </summary>
  public class EventbusRegistrationHostedService : BackgroundService
  {
    private readonly ILogger<EventbusRegistrationHostedService> _logger;
    private readonly EventbusClient _eventbusClient;

    public EventbusRegistrationHostedService(
      ILogger<EventbusRegistrationHostedService> logger,
      EventbusClient eventbusClient)
    {
      _logger = logger;
      _eventbusClient = eventbusClient;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
      try
      {
        await _eventbusClient.RegisterEventTypesAsync();
      }
      catch (Exception e)
      {
        // Defensive: RegisterEventTypesAsync already swallows its own errors,
        // but never let a startup task crash the host.
        _logger.LogWarning(
          "Eventbus registration hosted service failed: {Message}", e.Message);
      }
    }
  }
}
