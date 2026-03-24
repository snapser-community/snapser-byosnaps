using Microsoft.AspNetCore.Mvc;
using ByoSnapCSharp.Filters;
using ByoSnapCSharp.Models;
using ByoSnapCSharp.Utilities;
using Swashbuckle.AspNetCore.Annotations;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;

// TODO: Uncomment when SnapserInternal SDK is generated
// using SnapserInternal.Api;
// using SnapserInternal.Client;
// using SnapserInternal.Model;

namespace ByoSnapCSharp.Controllers
{
  // A iii]: User Manager Tool: Custom HTML User Manager Tool
  // C: User Tool: Get, Update and Delete User data: Used by the GDPR tool and the User Manager tool

  [ApiController]
  [Route("v1/byosnap-advanced/settings/users/{UserId}")]
  [Produces("application/json")]
  public class UserManagerController : ControllerBase
  {
    private readonly ILogger<UserManagerController> _logger;

    public UserManagerController(ILogger<UserManagerController> logger)
    {
      _logger = logger;
    }

    // --- Custom HTML User Manager Tool ---

    [HttpGet("custom")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(CustomSettingsPayload))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "GetUserDataCustom",
      Summary = "User Manager Tool",
      Description = "Get the user data for the custom HTML User Manager tool."
    )]
    public ActionResult GetUserDataCustom([FromRoute] UserIdParameterSchema userParams)
    {
      var defaultPayload = new CustomSettingsPayload { Payload = "" };

      // TODO: Uncomment when SnapserInternal SDK is generated
      // var configuration = new Configuration();
      // configuration.BasePath = Environment.GetEnvironmentVariable(AppConstants.storageHttpUrlEnvKey);
      // using var httpClient = new HttpClient();
      // using var httpClientHandler = new HttpClientHandler();
      // var apiInstance = new StorageServiceApi(httpClient, configuration, httpClientHandler);
      // try
      // {
      //   var apiResponse = apiInstance.StorageGetBlob(
      //     accessType: AppConstants.protectedAccessType,
      //     blobKey: AppConstants.charactersBlobKey,
      //     ownerId: userParams.UserId,
      //     gateway: Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey) ?? AppConstants.defaultInternalHeaderValue
      //   );
      //   if (apiResponse == null)
      //   {
      //     return Ok(defaultPayload);
      //   }
      //   return Ok(new CustomSettingsPayload { Payload = JsonConvert.DeserializeObject(apiResponse.Value) });
      // }
      // catch (ApiException e)
      // {
      //   _logger.LogWarning("Storage API exception on GetUserDataCustom: {Message}", e.Message);
      // }

      return Ok(defaultPayload);
    }

    [HttpPost("custom")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status500InternalServerError, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "UpdateUserDataCustom",
      Summary = "User Manager Tool",
      Description = "Update the user data for the custom HTML User Manager tool."
    )]
    public ActionResult UpdateUserDataCustom(
      [FromRoute] UserIdParameterSchema userParams,
      [FromBody] object body)
    {
      try
      {
        var _toolId = HttpContext.Request.Query["tool_id"].FirstOrDefault();

        // Parse the body - extract payload if wrapped
        var blobDataStr = JsonConvert.SerializeObject(body);
        var blobDataDict = JsonConvert.DeserializeObject<Dictionary<string, object>>(blobDataStr);
        if (blobDataDict != null && blobDataDict.ContainsKey("payload"))
        {
          blobDataStr = JsonConvert.SerializeObject(blobDataDict["payload"]);
        }

        // TODO: Add any custom validation here

        // TODO: Uncomment when SnapserInternal SDK is generated
        // var configuration = new Configuration();
        // configuration.BasePath = Environment.GetEnvironmentVariable(AppConstants.storageHttpUrlEnvKey);
        // using var httpClient = new HttpClient();
        // using var httpClientHandler = new HttpClientHandler();
        // var apiInstance = new StorageServiceApi(httpClient, configuration, httpClientHandler);
        //
        // var cas = "12345";
        // try
        // {
        //   var getResponse = apiInstance.StorageGetBlob(
        //     accessType: AppConstants.protectedAccessType,
        //     blobKey: AppConstants.charactersBlobKey,
        //     ownerId: userParams.UserId,
        //     gateway: Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey) ?? AppConstants.defaultInternalHeaderValue
        //   );
        //   if (getResponse != null)
        //   {
        //     cas = getResponse.Cas;
        //   }
        // }
        // catch (ApiException)
        // {
        //   // Blob does not exist yet - use default CAS
        // }
        //
        // try
        // {
        //   var replaceResponse = apiInstance.StorageReplaceBlob(
        //     accessType: AppConstants.protectedAccessType,
        //     blobKey: AppConstants.charactersBlobKey,
        //     ownerId: userParams.UserId,
        //     gateway: Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey),
        //     body: new Dictionary<string, object>
        //     {
        //       { "value", blobDataStr },
        //       { "ttl", 0 },
        //       { "create", true },
        //       { "cas", cas }
        //     }
        //   );
        //   if (replaceResponse == null)
        //   {
        //     return StatusCode(500, new ErrorResponseSchema { ErrorMessage = "Server Error" });
        //   }
        //   return Ok(JsonConvert.DeserializeObject(blobDataStr));
        // }
        // catch (ApiException e)
        // {
        //   return StatusCode(500, new ErrorResponseSchema { ErrorMessage = "Server Exception: " + e.Message });
        // }

        return Ok(JsonConvert.DeserializeObject(blobDataStr));
      }
      catch (Exception e)
      {
        return StatusCode(500, new ErrorResponseSchema { ErrorMessage = "Invalid JSON " + e.Message });
      }
    }

    // --- GDPR User Data Endpoints ---

    [HttpGet("data")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "GetUserData",
      Summary = "User Data (GDPR)",
      Description = "Get user data. Used by the GDPR tool and the User Manager tool."
    )]
    public ActionResult GetUserData([FromRoute] UserIdParameterSchema userParams)
    {
      var gatewayHeader = HttpContext.Request.Headers[AppConstants.gatewayHeaderKey].FirstOrDefault();
      if (string.IsNullOrEmpty(gatewayHeader) || gatewayHeader.ToLower() != AppConstants.internalAuthType)
      {
        return StatusCode(401, new ErrorResponseSchema { ErrorMessage = "Unauthorized" });
      }

      // TODO: Uncomment when SnapserInternal SDK is generated
      // var configuration = new Configuration();
      // configuration.BasePath = Environment.GetEnvironmentVariable(AppConstants.storageHttpUrlEnvKey);
      // using var httpClient = new HttpClient();
      // using var httpClientHandler = new HttpClientHandler();
      // var apiInstance = new StorageServiceApi(httpClient, configuration, httpClientHandler);
      // try
      // {
      //   var apiResponse = apiInstance.StorageGetBlob(
      //     accessType: AppConstants.privateAccessType,
      //     blobKey: AppConstants.charactersBlobKey,
      //     ownerId: userParams.UserId,
      //     gateway: Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey)
      //   );
      //   if (apiResponse == null)
      //   {
      //     return BadRequest(new ErrorResponseSchema { ErrorMessage = "No data" });
      //   }
      //   return Ok(JsonConvert.DeserializeObject(apiResponse.Value));
      // }
      // catch (ApiException)
      // {
      //   // No blob found
      // }

      return Ok(new { });
    }

    [HttpPut("data")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "UpdateUserData",
      Summary = "User Data (GDPR)",
      Description = "Update user data. Used by the GDPR tool and the User Manager tool."
    )]
    public ActionResult UpdateUserData([FromRoute] UserIdParameterSchema userParams)
    {
      var gatewayHeader = HttpContext.Request.Headers[AppConstants.gatewayHeaderKey].FirstOrDefault();
      if (string.IsNullOrEmpty(gatewayHeader) || gatewayHeader.ToLower() != AppConstants.internalAuthType)
      {
        return StatusCode(401, new ErrorResponseSchema { ErrorMessage = "Unauthorized" });
      }

      // TODO: Implement user data update using Storage API
      return Ok(new { });
    }

    [HttpDelete("data")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "DeleteUserData",
      Summary = "User Data (GDPR)",
      Description = "Delete user data. Implements the GDPR right-to-be-forgotten."
    )]
    public ActionResult DeleteUserData([FromRoute] UserIdParameterSchema userParams)
    {
      var gatewayHeader = HttpContext.Request.Headers[AppConstants.gatewayHeaderKey].FirstOrDefault();
      if (string.IsNullOrEmpty(gatewayHeader) || gatewayHeader.ToLower() != AppConstants.internalAuthType)
      {
        return StatusCode(401, new ErrorResponseSchema { ErrorMessage = "Unauthorized" });
      }

      // TODO: Uncomment when SnapserInternal SDK is generated
      // var configuration = new Configuration();
      // configuration.BasePath = Environment.GetEnvironmentVariable(AppConstants.storageHttpUrlEnvKey);
      // using var httpClient = new HttpClient();
      // using var httpClientHandler = new HttpClientHandler();
      // var apiInstance = new StorageServiceApi(httpClient, configuration, httpClientHandler);
      // try
      // {
      //   var apiResponse = apiInstance.StorageDeleteBlob(
      //     accessType: AppConstants.privateAccessType,
      //     blobKey: AppConstants.charactersBlobKey,
      //     ownerId: userParams.UserId,
      //     gateway: Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey)
      //   );
      //   if (apiResponse == null)
      //   {
      //     return BadRequest(new ErrorResponseSchema { ErrorMessage = "No blob" });
      //   }
      // }
      // catch (ApiException)
      // {
      //   // No blob to delete - that's ok
      // }

      return Ok(new { });
    }
  }
}
