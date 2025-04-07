using Microsoft.AspNetCore.Mvc;
using ByoSnapCSharp.Filters;
using ByoSnapCSharp.Models;
using ByoSnapCSharp.Utilities;
using System.Linq;
using Microsoft.OpenApi.Models;
using Microsoft.OpenApi.Any;
using Swashbuckle.AspNetCore.Annotations;
using System;


namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [Route("v1/byosnap-basic/users/{UserId}")]
  [Produces("application/json")]
  public class UsersController : ControllerBase
  {
    [HttpGet("game")]
    [SnapserAuth(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(OperationId = "Get Game", Summary = "Game APIs", Description = "This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.")]
    public ActionResult<SuccessResponseSchema> GetGame([FromRoute] UserIdParameterSchema userParams)
    {
      var authTypeHeader = HttpContext.Request.Headers[AppConstants.authTypeHeaderKey].FirstOrDefault();
      var userIdHeader = HttpContext.Request.Headers[AppConstants.userIdHeaderKey].FirstOrDefault();
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
    [SnapserAuth(AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(OperationId = "Save Game", Summary = "Game APIs", Description = "This API will work only with Api-Key auth. You can access this API with a valid api-key.")]
    public ActionResult<SuccessResponseSchema> SaveGame([FromRoute] UserIdParameterSchema userParams)
    {
      var authTypeHeader = HttpContext.Request.Headers[AppConstants.authTypeHeaderKey].FirstOrDefault();
      var userIdHeader = HttpContext.Request.Headers[AppConstants.userIdHeaderKey].FirstOrDefault();
      return Ok(new SuccessResponseSchema
      {
        Api = "SaveGame",
        AuthType = authTypeHeader ?? "N/A",
        HeaderUserId = userIdHeader ?? "N/A",
        PathUserId = userParams.UserId,
        Message = "success"
      });
    }

    [HttpDelete("")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(OperationId = "Delete User", Summary = "User APIs", Description = "This API will work only when the call is coming from within the Snapend.")]
    public ActionResult<SuccessResponseSchema> DeleteUser([FromRoute] UserIdParameterSchema userParams)
    {
      var gatewayHeader = HttpContext.Request.Headers[AppConstants.gatewayHeaderKey].FirstOrDefault();
      var userIdHeader = HttpContext.Request.Headers[AppConstants.userIdHeaderKey].FirstOrDefault();
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
    [SnapserAuth(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(OperationId = "Update User Profile", Summary = "User APIs", Description = "This API will work for all auth types.")]
    public ActionResult<SuccessResponseSchema> UpdateUserProfile([FromRoute] UserIdParameterSchema userParams)
    {
      var gatewayHeader = HttpContext.Request.Headers[AppConstants.gatewayHeaderKey].FirstOrDefault();
      var userIdHeader = HttpContext.Request.Headers[AppConstants.userIdHeaderKey].FirstOrDefault();
      return Ok(new SuccessResponseSchema
      {
        Api = "UpdateUserProfile",
        AuthType = gatewayHeader ?? "N/A",
        HeaderUserId = userIdHeader ?? "N/A",
        PathUserId = userParams.UserId,
        Message = "TODO: Add a message"
      });
    }
  }
}
