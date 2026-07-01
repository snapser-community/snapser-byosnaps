using Microsoft.AspNetCore.Mvc;
using ByoSnapCSharp.Filters;
using ByoSnapCSharp.Models;
using ByoSnapCSharp.Utilities;
using Swashbuckle.AspNetCore.Annotations;

namespace ByoSnapCSharp.Controllers
{
  // =========================================================================
  // Regular API Endpoints — your Snap's business logic lives here.
  //
  // The stubs below demonstrate each Snapser auth exposure. The
  // [SnapserAuth(...)] attribute drives the `x-snapser-auth-types` tag in the
  // generated swagger (which controls which SDK / tool the API surfaces in),
  // and the matching [ValidateAuthorization(...)] enforces it at runtime. Add,
  // rename, or remove these to fit your Snap.
  //
  // A single endpoint can accept MULTIPLE auth types at once (see the last
  // example) — you do not need a separate route per auth type.
  // =========================================================================

  [ApiController]
  [Route("v1/byosnap-core")]
  [Produces("application/json")]
  public class ExampleController : ControllerBase
  {
    private readonly ILogger<ExampleController> _logger;

    public ExampleController(ILogger<ExampleController> logger)
    {
      _logger = logger;
    }

    /// <summary>
    /// Example endpoint exposed over User auth. Accessible by a logged-in user,
    /// validated against the User-Id in their token. Surfaces in the client/game SDK.
    /// </summary>
    [HttpGet("users/{UserId}/example")]
    [SnapserAuth(AppConstants.userAuthType)]
    [ValidateAuthorization(AppConstants.userAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessMessageSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "ExampleUserAuth",
      Summary = "Example: User Auth",
      Description = "Accessible by a logged-in user, validated against the User-Id in their token. Surfaces in the client/game SDK."
    )]
    public ActionResult ExampleUserAuth([FromRoute] UserIdParameterSchema userParams)
    {
      // TODO: Add your user-scoped business logic here.
      //       See advanced/ByoSnapCSharp for the full implementation.
      return Ok(new SuccessMessageSchema
      {
        Message = $"Hello user {userParams.UserId}"
      });
    }

    /// <summary>
    /// Example endpoint exposed over Api-Key auth. Accessible with a valid API
    /// key. Use for trusted server-to-server calls.
    /// </summary>
    [HttpGet("example/api-key")]
    [SnapserAuth(AppConstants.apiKeyAuthType)]
    [ValidateAuthorization(AppConstants.apiKeyAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessMessageSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "ExampleApiKeyAuth",
      Summary = "Example: Api-Key Auth",
      Description = "Accessible with a valid API key. Use for trusted server-to-server calls."
    )]
    public ActionResult ExampleApiKeyAuth()
    {
      // TODO: Add your api-key-scoped business logic here.
      //       See advanced/ByoSnapCSharp for the full implementation.
      return Ok(new SuccessMessageSchema
      {
        Message = "Hello api-key caller"
      });
    }

    /// <summary>
    /// Example endpoint exposed over Internal auth. Callable only by other Snaps
    /// within the same Snapend (internal gateway). Surfaces in the internal SDK.
    /// </summary>
    [HttpGet("example/internal")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessMessageSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "ExampleInternalAuth",
      Summary = "Example: Internal Auth",
      Description = "Callable only by other Snaps within the same Snapend (internal gateway). Surfaces in the internal SDK."
    )]
    public ActionResult ExampleInternalAuth()
    {
      // TODO: Add your internal-only business logic here.
      //       See advanced/ByoSnapCSharp for the full implementation.
      return Ok(new SuccessMessageSchema
      {
        Message = "Hello internal caller"
      });
    }

    /// <summary>
    /// Example endpoint surfaced in the special Admin SDK.
    ///
    /// Note: `admin` is NOT an auth type. Tagging an endpoint with `admin` only
    /// makes it surface in the Admin SDK (used by admin tooling / the Snapser
    /// dashboard). The request itself still arrives through the internal gateway,
    /// so this is guarded with the INTERNAL check.
    /// </summary>
    [HttpGet("example/admin")]
    [SnapserAuth("admin")]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessMessageSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "ExampleAdminSdk",
      Summary = "Example: Admin SDK",
      Description = "Surfaces in the Admin SDK for admin tooling / the Snapser dashboard. `admin` controls SDK exposure, not authentication."
    )]
    public ActionResult ExampleAdminSdk()
    {
      // Admin-SDK calls reach the Snap through the internal gateway, so we guard
      // this with the INTERNAL check. The `admin` tag above is what makes this
      // API surface in the Admin SDK.
      // TODO: Add your admin-only business logic here.
      //       See advanced/ByoSnapCSharp for the full implementation.
      return Ok(new SuccessMessageSchema
      {
        Message = "Hello admin caller"
      });
    }

    /// <summary>
    /// Example endpoint that accepts MULTIPLE auth types on ONE route. One
    /// endpoint reachable by a logged-in user, a valid API key, or an internal
    /// Snap. List every auth type you want to allow — no need for a separate
    /// route per type.
    /// </summary>
    [HttpGet("users/{UserId}/example/multi-auth")]
    [SnapserAuth(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessMessageSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "ExampleMultiAuth",
      Summary = "Example: Multi Auth",
      Description = "One endpoint reachable by a logged-in user, a valid API key, or an internal Snap. List every auth type you want to allow — no need for a separate route per type."
    )]
    public ActionResult ExampleMultiAuth([FromRoute] UserIdParameterSchema userParams)
    {
      // Pass every accepted auth type to both the [SnapserAuth(...)] tag (for SDK
      // exposure) and the [ValidateAuthorization(...)] attribute (for runtime
      // enforcement).
      // TODO: Add your business logic here.
      //       See advanced/ByoSnapCSharp for the full implementation.
      return Ok(new SuccessMessageSchema
      {
        Message = $"Hello, request for user {userParams.UserId} passed multi-auth"
      });
    }
  }
}
