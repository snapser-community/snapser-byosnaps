# Gotchas
What to Watch Out For When Working in This Repo

## Endpoints
- The Snapend Id is NOT part of the URL. This allows you to use the same BYOSnap in multiple Snapends.
```csharp
namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [Route("v1/byosnap-basic/users/{UserId}")] // (👈 No Snapend Id)
  public class UsersController : ControllerBase
  ...
}
```
- All externally accessible APIs need to start with /$prefix/$byosnapId/remaining_path. where $prefix = v1, $byosnapId = byosnap-python-basic and remaining_path = /users/<user_id>.
```csharp
namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [Route("v1/byosnap-basic/users/{UserId}")] // (👈 No Snapend Id)
  public class UsersController : ControllerBase
  ...
}
```
- Notice the `x-snapser-auth-types` tags in the endpoint annotations and swagger.json. They tell Snapser if it should expose this API in the SDK and the API Explorer. Note: but you should still validate the auth type in the code.
```csharp
namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [Route("v1/byosnap-basic/users/{UserId}")]
  public class UsersController : ControllerBase
  {
    [HttpGet("game")]
    [SnapserAuth("user", "api-key", "internal")] // (👈 This gets converted to x-snapser-auth-types in swagger.json)
    ...
  }
}
```

IMPORTANT: But you also have to pass those auth types to the middleware so that you get Authorization checks for free. Just adding those tags for swagger, are not going to do the authorization check for you.
```csharp
[HttpGet("game")]
[SnapserAuth("user", "api-key", "internal")] // (👈 This is just for the swagger)
[ValidateAuthorization("user", "api-key", "internal")] // (👈 This tells the middleware that user auth, app auth and internal auth are allowed)
[ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
[ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
[ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
[SwaggerOperation(OperationId = "Get Game", Summary = "Game APIs", Description = "This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.")]
public ActionResult<SuccessResponseSchema> GetGame([FromRoute] UserIdParameterSchema userParams)
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
```
- Snapser tech automatically adds the correct header to the SDK and API Explorer for your API. So you do not need to add the headers here against your API. Eg: For APIs exposed over User Auth, both the SDK and API Explorer will expose the Token header for you to fill in. For Api-Key Auth, the API Explorer will expose the Api-Key header for you to fill in. For internal APIs, the SDK and API Explorer will expose the Gateway header.
```csharp
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
    [SwaggerOperation(OperationId = "Get Game", Summary = "Game APIs", Description = "This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.")] // (👈 Notice no header has been added here)
    public ActionResult<SuccessResponseSchema> GetGame([FromRoute] UserIdParameterSchema userParams)
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
  }
```
- The health endpoint does not have to contain the prefix. It should just be available at the root level.
```csharp
using Microsoft.AspNetCore.Mvc;

namespace ByoSnapCSharp.Controllers
{
  [ApiController]
  [ApiExplorerSettings(IgnoreApi = true)]
  public class HealthController : ControllerBase
  {
    // This could potentially be in its own file if you have multiple health checks or system-wide actions.
    [HttpGet("healthz")]
    public IActionResult HealthCheck()
    {
      return Ok("Ok");
    }
  }
}
```
- We use Swashbuckle to convert annotations to swagger.json. The swagger.json is used by Snapser to generate the SDK and power the API Explorer. Swagger generation also has some gotchas. Please see the section below.

## Swagger generation
- This repo uses Swashbuckle to convert controller annotations to a Swagger. There are a few gotchas that you need to be aware of.
- You can run the `./generate_swagger.sh` to generate your swagger.
- You need to have the SnapserAuth annotation to create the x-snapser-auth-types extension in the swagger
```csharp
public class UsersController : ControllerBase
{
  [HttpGet("game")]
  [SnapserAuth("user", "api-key", "internal")] // (👈 This is used to create x-snapser-auth-types)
  ...
}
```
- Every API in your BYOSnap should check for authorization.
```csharp
public class UsersController : ControllerBase
{
  [HttpGet("game")]
  [SnapserAuth("user", "api-key", "internal")]
  [ValidateAuthorization("user", "api-key", "internal")] // (👈 Use this to validate one of user, api-key, internal auth for this endpoint)
  ...
}
```
- Every API needs to have a summary, description and operationId
```csharp
public class UsersController : ControllerBase
{
  [HttpGet("game")]
  [SnapserAuth("user", "api-key", "internal")]
  [ValidateAuthorization("user", "api-key", "internal")]
  [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
  [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
  [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
  [SwaggerOperation(OperationId = "Get Game", Summary = "Game APIs", Description = "This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.")] // (👈 OperationId is used to generate the method name in the SDK and in the API Explorer. Summary and Description fields are required.)
...
  }
```
