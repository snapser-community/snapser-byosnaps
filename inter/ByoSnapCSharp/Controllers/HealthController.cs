using Microsoft.AspNetCore.Mvc;

namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [ApiExplorerSettings(IgnoreApi = true)]
  public class HealthController : ControllerBase
  {
    // This could potentially be in its own file if you have multiple health checks or system-wide actions.
    [HttpGet("healthz")]
    public IActionResult HealthCheck()
    {
      return Ok("Ok");
    }
  }
}