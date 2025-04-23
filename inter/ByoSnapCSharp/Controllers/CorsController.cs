using Microsoft.AspNetCore.Mvc;

namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [ApiExplorerSettings(IgnoreApi = true)]
  public class CorsController : ControllerBase
  {
    // Consolidate all CORS-related actions here if they are simple preflight responses.
    [HttpOptions("v1/byosnap-inter/users/{userId}/game")]
    [HttpOptions("v1/byosnap-inter/users/{userId}")]
    [HttpOptions("v1/byosnap-inter/users/{userId}/profile")]
    public IActionResult CorsOverrides()
    {
      return Ok("Ok");
    }
  }
}