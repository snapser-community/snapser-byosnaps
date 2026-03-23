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
  // A i]: Configuration Tool: Built using the Snapser UI Builder

  [ApiController]
  [Route("v1/byosnap-advanced/settings")]
  [Produces("application/json")]
  public class SettingsController : ControllerBase
  {
    private readonly ILogger<SettingsController> _logger;

    public SettingsController(ILogger<SettingsController> logger)
    {
      _logger = logger;
    }

    /// <summary>
    /// Returns the default settings payload structure used by the Configuration Tool.
    /// </summary>
    private static SettingsSchema GetDefaultSettings()
    {
      return new SettingsSchema
      {
        Sections = new List<SettingsSectionSchema>
        {
          new SettingsSectionSchema
          {
            Id = "registration",
            Components = new List<SettingsComponentSchema>
            {
              new SettingsComponentSchema
              {
                Id = "characters",
                Type = "textarea",
                Value = ""
              }
            }
          }
        }
      };
    }

    [HttpGet("")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SettingsSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "GetSettings",
      Summary = "Configuration Tool",
      Description = "Get the settings for the characters microservice. This endpoint is called by the Snapser Configuration Tool."
    )]
    public ActionResult GetSettings(
      [FromQuery(Name = "tool_id")] string? toolId,
      [FromQuery(Name = "environment")] string? environment)
    {
      var defaultSettings = GetDefaultSettings();
      var env = environment ?? AppConstants.defaultEnvironment;
      var blobOwnerKey = $"{toolId}_{env}";

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
      //     blobKey: AppConstants.characterSettingsBlobKey,
      //     ownerId: blobOwnerKey,
      //     gateway: Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey) ?? AppConstants.defaultInternalHeaderValue
      //   );
      //   if (apiResponse == null)
      //   {
      //     return Ok(defaultSettings);
      //   }
      //   return Ok(JsonConvert.DeserializeObject(apiResponse.Value));
      // }
      // catch (ApiException e)
      // {
      //   _logger.LogWarning("Storage API exception on GetSettings: {Message}", e.Message);
      // }

      return Ok(defaultSettings);
    }

    [HttpPut("")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SettingsSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status500InternalServerError, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "UpdateSettings",
      Summary = "Configuration Tool",
      Description = "Update the settings for the characters microservice. This endpoint is called by the Snapser Configuration Tool."
    )]
    public ActionResult UpdateSettings(
      [FromQuery(Name = "tool_id")] string? toolId,
      [FromQuery(Name = "environment")] string? environment,
      [FromBody] object body)
    {
      try
      {
        var env = environment ?? AppConstants.defaultEnvironment;
        var blobOwnerKey = $"{toolId}_{env}";

        // Parse the body - extract payload if wrapped
        var blobDataStr = JsonConvert.SerializeObject(body);
        var blobDataDict = JsonConvert.DeserializeObject<Dictionary<string, object>>(blobDataStr);
        if (blobDataDict != null && blobDataDict.ContainsKey("payload"))
        {
          blobDataStr = JsonConvert.SerializeObject(blobDataDict["payload"]);
        }

        // TODO: Add any custom validation here and on error return:
        // return BadRequest(new ErrorResponseSchema { ErrorMessage = "Duplicate characters found" });

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
        //     accessType: AppConstants.privateAccessType,
        //     blobKey: AppConstants.characterSettingsBlobKey,
        //     ownerId: blobOwnerKey,
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
        //     accessType: AppConstants.privateAccessType,
        //     blobKey: AppConstants.characterSettingsBlobKey,
        //     ownerId: blobOwnerKey,
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

    // A ii]: New Configuration Tool: Custom HTML Snap Configuration Tool

    [HttpGet("custom")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(CustomSettingsPayload))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "GetSettingsCustom",
      Summary = "Custom Configuration Tool",
      Description = "Get the settings for the custom HTML configuration tool."
    )]
    public ActionResult GetSettingsCustom(
      [FromQuery(Name = "tool_id")] string? toolId,
      [FromQuery(Name = "environment")] string? environment)
    {
      var defaultSettings = new CustomSettingsPayload { Payload = "" };
      var env = environment ?? AppConstants.defaultEnvironment;
      var blobOwnerKey = $"{toolId}_{env}";

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
      //     blobKey: AppConstants.characterSettingsBlobKey,
      //     ownerId: blobOwnerKey,
      //     gateway: Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey) ?? AppConstants.defaultInternalHeaderValue
      //   );
      //   if (apiResponse == null)
      //   {
      //     return Ok(defaultSettings);
      //   }
      //   return Ok(new CustomSettingsPayload { Payload = JsonConvert.DeserializeObject(apiResponse.Value) });
      // }
      // catch (ApiException e)
      // {
      //   _logger.LogWarning("Storage API exception on GetSettingsCustom: {Message}", e.Message);
      // }

      return Ok(defaultSettings);
    }

    [HttpPut("custom")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status500InternalServerError, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "UpdateSettingsCustom",
      Summary = "Custom Configuration Tool",
      Description = "Update the settings from the custom HTML configuration tool."
    )]
    public ActionResult UpdateSettingsCustom(
      [FromQuery(Name = "tool_id")] string? toolId,
      [FromQuery(Name = "environment")] string? environment,
      [FromBody] object body)
    {
      try
      {
        var env = environment ?? AppConstants.defaultEnvironment;
        var blobOwnerKey = $"{toolId}_{env}";

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
        //     accessType: AppConstants.privateAccessType,
        //     blobKey: AppConstants.characterSettingsBlobKey,
        //     ownerId: blobOwnerKey,
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
        //     accessType: AppConstants.privateAccessType,
        //     blobKey: AppConstants.characterSettingsBlobKey,
        //     ownerId: blobOwnerKey,
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
  }
}
