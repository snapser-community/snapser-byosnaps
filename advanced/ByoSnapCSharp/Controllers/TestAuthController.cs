using Microsoft.AspNetCore.Mvc;
using ByoSnapCSharp.Filters;
using ByoSnapCSharp.Models;
using ByoSnapCSharp.Utilities;
using Swashbuckle.AspNetCore.Annotations;
using System.Linq;

namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [Route("v1/byosnap-advanced")]
  [Produces("application/json")]
  public class TestAuthController : ControllerBase
  {
    private readonly ILogger<TestAuthController> _logger;

    public TestAuthController(ILogger<TestAuthController> logger)
    {
      _logger = logger;
    }

    /// <summary>
    /// Test endpoint for user authentication.
    /// </summary>
    [HttpGet("user-auth/{UserId}")]
    [SnapserAuth(AppConstants.userAuthType)]
    [ValidateAuthorization(AppConstants.userAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessMessageSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "TestUserAuth",
      Summary = "Test User Authentication",
      Description = "Test endpoint to validate user authentication. Requires User-Id header."
    )]
    public ActionResult TestUserAuth([FromRoute] string UserId)
    {
      return Ok(new SuccessMessageSchema
      {
        Message = $"Hello User {UserId}, you have passed the User Auth validation"
      });
    }

    /// <summary>
    /// Test endpoint for API key authentication.
    /// </summary>
    [HttpGet("api-key-auth")]
    [SnapserAuth(AppConstants.apiKeyAuthType)]
    [ValidateAuthorization(AppConstants.apiKeyAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessMessageSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "TestApiKeyAuth",
      Summary = "Test API Key Authentication",
      Description = "Test endpoint to validate API key authentication. Reads Api-Key-Name header."
    )]
    public ActionResult TestApiKeyAuth()
    {
      var apiKeyName = Request.Headers["Api-Key-Name"].FirstOrDefault() ?? "unknown";
      return Ok(new SuccessMessageSchema
      {
        Message = $"You have passed the API Key Auth validation using the key {apiKeyName}"
      });
    }
  }
}
