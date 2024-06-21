using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System.Linq;

namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [Route("v1/byosnap-csharp/[controller]")]
  [EnableCors("AllowSpecificOrigin")] // Apply CORS policy to this controller
  public class HelloController : ControllerBase
  {
    private readonly ILogger<HelloController> _logger;

    public HelloController(ILogger<HelloController> logger)
    {
      _logger = logger;
    }

    [HttpGet]
    public IActionResult Get()
    {
      if (Request.Headers.ContainsKey("Token"))
      {
        var token = Request.Headers["Token"].FirstOrDefault();
        if (!string.IsNullOrEmpty(token))
        {
          return Ok("Hello, World!");
        }
      }

      return Unauthorized();
    }
  }
}
