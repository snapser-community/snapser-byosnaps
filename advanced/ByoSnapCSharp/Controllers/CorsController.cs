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
    [HttpOptions("v1/byosnap-advanced/users/{userId}/characters/active")]
    [HttpOptions("v1/byosnap-advanced/settings")]
    [HttpOptions("v1/byosnap-advanced/settings/custom")]
    [HttpOptions("v1/byosnap-advanced/settings/export")]
    [HttpOptions("v1/byosnap-advanced/settings/import")]
    [HttpOptions("v1/byosnap-advanced/settings/validate-import")]
    [HttpOptions("v1/byosnap-advanced/settings/users/{userId}/custom")]
    [HttpOptions("v1/byosnap-advanced/settings/users/{userId}/data")]
    [HttpOptions("v1/byosnap-advanced/user-auth/{UserId}")]
    [HttpOptions("v1/byosnap-advanced/api-key-auth")]
    public IActionResult CorsOverrides()
    {
      return Ok("Ok");
    }
  }
}
