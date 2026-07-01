using Microsoft.AspNetCore.Mvc;

namespace ByoSnapCSharp.Controllers
{
  // @GOTCHAS - CORS
  //   1. Snapser API Explorer tool runs in the browser. Enabling CORS allows you to access the APIs via the API Explorer.

  [ApiController]
  [ApiExplorerSettings(IgnoreApi = true)]
  public class CorsController : ControllerBase
  {
    // Consolidate all CORS-related actions here if they are simple preflight responses.
    [HttpOptions("v1/byosnap-core/settings")]
    [HttpOptions("v1/byosnap-core/settings/custom")]
    [HttpOptions("v1/byosnap-core/settings/export")]
    [HttpOptions("v1/byosnap-core/settings/import")]
    [HttpOptions("v1/byosnap-core/settings/validate-import")]
    [HttpOptions("v1/byosnap-core/settings/users/{userId}/custom")]
    [HttpOptions("v1/byosnap-core/settings/users/{userId}/data")]
    [HttpOptions("v1/byosnap-core/users/{userId}/example")]
    [HttpOptions("v1/byosnap-core/example/api-key")]
    [HttpOptions("v1/byosnap-core/example/internal")]
    [HttpOptions("v1/byosnap-core/example/admin")]
    [HttpOptions("v1/byosnap-core/users/{userId}/example/multi-auth")]
    public IActionResult CorsOverrides()
    {
      return Ok("Ok");
    }
  }
}
