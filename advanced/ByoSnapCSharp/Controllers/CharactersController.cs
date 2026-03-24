using Microsoft.AspNetCore.Mvc;
using ByoSnapCSharp.Filters;
using ByoSnapCSharp.Models;
using ByoSnapCSharp.Utilities;
using Swashbuckle.AspNetCore.Annotations;
using System.Collections.Generic;

namespace ByoSnapCSharp.Controllers
{
  // Regular API Endpoints exposed by the Snap

  [ApiController]
  [Route("v1/byosnap-advanced/users/{UserId}")]
  [Produces("application/json")]
  public class CharactersController : ControllerBase
  {
    [HttpGet("characters/active")]
    [SnapserAuth(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(CharactersResponseSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "GetActiveCharacters",
      Summary = "Character APIs",
      Description = "Get active characters for a user. This API supports User, API-Key, and Internal auth types."
    )]
    public ActionResult<CharactersResponseSchema> GetActiveCharacters([FromRoute] UserIdParameterSchema userParams)
    {
      return Ok(new CharactersResponseSchema
      {
        Characters = new List<string>()
      });
    }
  }
}
