using Microsoft.AspNetCore.Mvc;

namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [ApiExplorerSettings(IgnoreApi = true)]
  public class HealthController : ControllerBase
  {
    // @GOTCHAS - Health Check Endpoint
    //   1. The health URL does not take any URL prefix like other APIs
    [HttpGet("healthz")]
    public IActionResult HealthCheck()
    {
      return Ok("Ok");
    }
  }
}
