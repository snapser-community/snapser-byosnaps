using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace ByoSnapCSharp.Controllers
{
  // @GOTCHAS - Eventbus Inbound Receiver
  //   1. This is a RESERVED URL: root-level, with NO /v1 prefix and NO byosnap id
  //      (just like /healthz). The Eventbus Snap calls this URL to DELIVER events
  //      to your Snap.
  //   2. [ApiExplorerSettings(IgnoreApi = true)] keeps it OUT of the generated
  //      Swagger / SDK spec — it is an internal webhook, not a public API.

  [ApiController]
  [ApiExplorerSettings(IgnoreApi = true)]
  public class EventsController : ControllerBase
  {
    private readonly ILogger<EventsController> _logger;

    public EventsController(ILogger<EventsController> logger)
    {
      _logger = logger;
    }

    /// <summary>
    /// Inbound Eventbus receiver. The Eventbus Snap POSTs delivered events here.
    /// </summary>
    [Route("internal/events")]
    [HttpPost]
    public async Task<IActionResult> ReceiveEvent()
    {
      using var reader = new StreamReader(Request.Body);
      var rawBody = await reader.ReadToEndAsync();
      _logger.LogInformation("Received event from Eventbus: {Body}", rawBody);
      // TODO: Parse the payload and switch on the event subject to route it to
      //       the right handler in your business logic.
      return Ok();
    }
  }
}
