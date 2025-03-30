using Microsoft.AspNetCore.Mvc;
using ByoSnapCSharp.Filters;
using ByoSnapCSharp.Models;
using System.Linq;
using Microsoft.OpenApi.Models;
using Microsoft.OpenApi.Any;
using Swashbuckle.AspNetCore.Annotations;

namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [Route("v1/byosnap-basic/users/{UserId}")]
  public class UsersController : ControllerBase
  {
    [HttpGet("game")]
    [SnapserAuth("user", "api-key", "internal")]
    [ValidateAuthorization("user", "api-key", "internal")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(Summary = "API One", Description = "This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.", OperationId = "API One")]
    public ActionResult<SuccessResponseSchema> ApiOne([FromRoute] UserIdParameterSchema userParams)
    {
      var authTypeHeader = HttpContext.Request.Headers["Auth-Type"].FirstOrDefault();
      var userIdHeader = HttpContext.Request.Headers["User-Id"].FirstOrDefault();
      return Ok(new SuccessResponseSchema
      {
        Api = "GetGame",
        AuthType = authTypeHeader ?? "N/A",
        HeaderUserId = userIdHeader ?? "N/A",
        PathUserId = userParams.UserId,
        Message = "success"
      });
    }

    [HttpPost("game")]
    [SnapserAuth("api-key", "internal")]
    [ValidateAuthorization("api-key", "internal")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(Summary = "API Two", Description = "This API will work only with Api-Key auth. You can access this API with a valid api-key.", OperationId = "API Two")]
    public ActionResult<SuccessResponseSchema> ApiTwo([FromRoute] UserIdParameterSchema userParams)
    {
      var authTypeHeader = HttpContext.Request.Headers["Auth-Type"].FirstOrDefault();
      var userIdHeader = HttpContext.Request.Headers["User-Id"].FirstOrDefault();
      return Ok(new SuccessResponseSchema
      {
        Api = "PostGame",
        AuthType = authTypeHeader ?? "N/A",
        HeaderUserId = userIdHeader ?? "N/A",
        PathUserId = userParams.UserId,
        Message = "success"
      });
    }

    [HttpDelete("")]
    [SnapserAuth("internal")]
    [ValidateAuthorization("internal")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(Summary = "API Three", Description = "This API will work only when the call is coming from within the Snapend.", OperationId = "API Three")]
    public ActionResult<SuccessResponseSchema> ApiThree([FromRoute] UserIdParameterSchema userParams)
    {
      var gatewayHeader = HttpContext.Request.Headers["Gateway"].FirstOrDefault();
      var userIdHeader = HttpContext.Request.Headers["User-Id"].FirstOrDefault();
      return Ok(new SuccessResponseSchema
      {
        Api = "DeleteUser",
        AuthType = gatewayHeader ?? "N/A",
        HeaderUserId = userIdHeader ?? "N/A",
        PathUserId = userParams.UserId,
        Message = "success"
      });
    }

    [HttpPut("profile")]
    [SnapserAuth("user", "api-key", "internal")]
    [ValidateAuthorization("user", "api-key", "internal")]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(Summary = "API Four", Description = "This API will work for all auth types.", OperationId = "API Four")]
    public ActionResult<SuccessResponseSchema> ApiFour([FromRoute] UserIdParameterSchema userParams)
    {
      var gatewayHeader = HttpContext.Request.Headers["Gateway"].FirstOrDefault();
      var userIdHeader = HttpContext.Request.Headers["User-Id"].FirstOrDefault();
      return Ok(new SuccessResponseSchema
      {
        Api = "UpdateProfile",
        AuthType = gatewayHeader ?? "N/A",
        HeaderUserId = userIdHeader ?? "N/A",
        PathUserId = userParams.UserId,
        Message = "TODO: Add a message"
      });
    }
  }
}
