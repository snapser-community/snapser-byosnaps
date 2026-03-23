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
  // B: Snapend Sync|Clone: Used by Snapser's built-in configuration import export system

  [ApiController]
  [Route("v1/byosnap-advanced/settings")]
  [Produces("application/json")]
  public class ExportImportController : ControllerBase
  {
    private readonly ILogger<ExportImportController> _logger;

    public ExportImportController(ILogger<ExportImportController> logger)
    {
      _logger = logger;
    }

    /// <summary>
    /// Returns the default settings structure per environment.
    /// </summary>
    private static Dictionary<string, SettingsSchema> GetDefaultCharactersPayload()
    {
      return new Dictionary<string, SettingsSchema>
      {
        {
          AppConstants.charactersToolId, new SettingsSchema
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
          }
        }
      };
    }

    /// <summary>
    /// Returns the default export response with empty settings for all environments.
    /// </summary>
    private static ExportSettingsSchema GetDefaultExportResponse()
    {
      return new ExportSettingsSchema
      {
        Version = Environment.GetEnvironmentVariable(AppConstants.byoSnapVersionEnvKey) ?? AppConstants.defaultByoSnapVersion,
        ExportedAt = DateTimeOffset.UtcNow.ToUnixTimeSeconds(),
        Data = new Dictionary<string, Dictionary<string, SettingsSchema>>
        {
          { "dev", GetDefaultCharactersPayload() },
          { "stage", GetDefaultCharactersPayload() },
          { "prod", GetDefaultCharactersPayload() }
        }
      };
    }

    [HttpGet("export")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ExportSettingsSchema))]
    [ProducesResponseType(StatusCodes.Status500InternalServerError, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "ExportSettings",
      Summary = "Export Settings",
      Description = "Export all settings across environments (dev, stage, prod) for Snapend Sync/Clone."
    )]
    public ActionResult ExportSettings()
    {
      var response = GetDefaultExportResponse();
      var blobKeyIds = new[]
      {
        $"{AppConstants.charactersToolId}_dev",
        $"{AppConstants.charactersToolId}_stage",
        $"{AppConstants.charactersToolId}_prod"
      };

      // TODO: Uncomment when SnapserInternal SDK is generated
      // var configuration = new Configuration();
      // configuration.BasePath = Environment.GetEnvironmentVariable(AppConstants.storageHttpUrlEnvKey);
      // using var httpClient = new HttpClient();
      // using var httpClientHandler = new HttpClientHandler();
      // var apiInstance = new StorageServiceApi(httpClient, configuration, httpClientHandler);
      // try
      // {
      //   // Remember when storing these blobs we are storing them with `characters_dev`,
      //   // `characters_stage` and `characters_prod` as the owner_id
      //   var apiResponse = apiInstance.StorageBatchGetBlobs(
      //     accessType: AppConstants.privateAccessType,
      //     blobKey: AppConstants.characterSettingsBlobKey,
      //     ownerId: blobKeyIds,
      //     gateway: Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey) ?? AppConstants.defaultInternalHeaderValue
      //   );
      //   if (apiResponse == null)
      //   {
      //     return Ok(response);
      //   }
      //   foreach (var result in apiResponse.Results)
      //   {
      //     if (result.Success && result.Response?.Value != null && result.Response.Value != "")
      //     {
      //       var parsedSettings = JsonConvert.DeserializeObject<SettingsSchema>(result.Response.Value);
      //       if (result.Response.OwnerId == blobKeyIds[0])
      //       {
      //         response.Data["dev"][AppConstants.charactersToolId] = parsedSettings;
      //       }
      //       else if (result.Response.OwnerId == blobKeyIds[1])
      //       {
      //         response.Data["stage"][AppConstants.charactersToolId] = parsedSettings;
      //       }
      //       else if (result.Response.OwnerId == blobKeyIds[2])
      //       {
      //         response.Data["prod"][AppConstants.charactersToolId] = parsedSettings;
      //       }
      //     }
      //   }
      //   return Ok(response);
      // }
      // catch (ApiException e)
      // {
      //   return StatusCode(500, new ErrorResponseSchema { ErrorMessage = "API Exception: " + e.Message });
      // }

      return Ok(response);
    }

    [HttpPost("import")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessMessageSchema))]
    [ProducesResponseType(StatusCodes.Status201Created, Type = typeof(SuccessMessageSchema))]
    [ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
    [ProducesResponseType(StatusCodes.Status500InternalServerError, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "ImportSettings",
      Summary = "Import Settings",
      Description = "Import settings across environments (dev, stage, prod) for Snapend Sync/Clone."
    )]
    public ActionResult ImportSettings([FromBody] ExportSettingsSchema settingsData)
    {
      try
      {
        // Validate the incoming structure
        if (settingsData?.Data == null ||
            !settingsData.Data.ContainsKey("dev") ||
            !settingsData.Data.ContainsKey("stage") ||
            !settingsData.Data.ContainsKey("prod") ||
            !settingsData.Data["dev"].ContainsKey(AppConstants.charactersToolId) ||
            !settingsData.Data["stage"].ContainsKey(AppConstants.charactersToolId) ||
            !settingsData.Data["prod"].ContainsKey(AppConstants.charactersToolId))
        {
          return StatusCode(500, new ErrorResponseSchema { ErrorMessage = "Invalid JSON" });
        }

        // TODO: Uncomment when SnapserInternal SDK is generated
        // var blobDev = new Dictionary<string, object>
        // {
        //   { "value", JsonConvert.SerializeObject(settingsData.Data["dev"][AppConstants.charactersToolId]) },
        //   { "ttl", 0 },
        //   { "owner_id", $"{AppConstants.charactersToolId}_dev" },
        //   { "create", true },
        //   { "cas", "0" },  // Force replace
        //   { "blob_key", AppConstants.characterSettingsBlobKey },
        //   { "access_type", AppConstants.privateAccessType }
        // };
        // var blobStage = new Dictionary<string, object>
        // {
        //   { "value", JsonConvert.SerializeObject(settingsData.Data["stage"][AppConstants.charactersToolId]) },
        //   { "ttl", 0 },
        //   { "owner_id", $"{AppConstants.charactersToolId}_stage" },
        //   { "create", true },
        //   { "cas", "0" },  // Force replace
        //   { "blob_key", AppConstants.characterSettingsBlobKey },
        //   { "access_type", AppConstants.privateAccessType }
        // };
        // var blobProd = new Dictionary<string, object>
        // {
        //   { "value", JsonConvert.SerializeObject(settingsData.Data["prod"][AppConstants.charactersToolId]) },
        //   { "ttl", 0 },
        //   { "owner_id", $"{AppConstants.charactersToolId}_prod" },
        //   { "create", true },
        //   { "cas", "0" },  // Force replace
        //   { "blob_key", AppConstants.characterSettingsBlobKey },
        //   { "access_type", AppConstants.privateAccessType }
        // };
        // var payload = new Dictionary<string, object>
        // {
        //   { "blobs", new[] { blobDev, blobStage, blobProd } }
        // };
        //
        // var configuration = new Configuration();
        // configuration.BasePath = Environment.GetEnvironmentVariable(AppConstants.storageHttpUrlEnvKey);
        // using var httpClient = new HttpClient();
        // using var httpClientHandler = new HttpClientHandler();
        // var apiInstance = new StorageServiceApi(httpClient, configuration, httpClientHandler);
        // try
        // {
        //   var apiResponse = apiInstance.StorageBatchReplaceBlob(
        //     gateway: Environment.GetEnvironmentVariable(AppConstants.internalHeaderEnvKey),
        //     body: payload
        //   );
        //   if (apiResponse == null)
        //   {
        //     return StatusCode(500, new ErrorResponseSchema { ErrorMessage = "Server Error" });
        //   }
        //   return Ok(new SuccessMessageSchema { Message = "Success" });
        // }
        // catch (ApiException e)
        // {
        //   return StatusCode(500, new ErrorResponseSchema { ErrorMessage = "Server Exception: " + e.Message });
        // }

        return Ok(new SuccessMessageSchema { Message = "Success" });
      }
      catch (Exception e)
      {
        return StatusCode(500, new ErrorResponseSchema { ErrorMessage = "Server Exception: " + e.Message });
      }
    }

    [HttpPost("validate-import")]
    [SnapserAuth(AppConstants.internalAuthType)]
    [ValidateAuthorization(AppConstants.internalAuthType)]
    [ProducesResponseType(StatusCodes.Status200OK, Type = typeof(ExportSettingsSchema))]
    [ProducesResponseType(StatusCodes.Status500InternalServerError, Type = typeof(ErrorResponseSchema))]
    [SwaggerOperation(
      OperationId = "ValidateImportSettings",
      Summary = "Validate Import Settings",
      Description = "Validate settings before importing. Snapser sends the settings that are about to be imported - validate if you can accept them."
    )]
    public ActionResult ValidateImportSettings([FromBody] ExportSettingsSchema settingsData)
    {
      // Perform basic validation. You can add more validation by fetching the
      // settings from storage and comparing with the incoming settings.
      if (settingsData?.Data == null ||
          !settingsData.Data.ContainsKey("dev") ||
          !settingsData.Data.ContainsKey("stage") ||
          !settingsData.Data.ContainsKey("prod") ||
          !settingsData.Data["dev"].ContainsKey(AppConstants.charactersToolId) ||
          !settingsData.Data["stage"].ContainsKey(AppConstants.charactersToolId) ||
          !settingsData.Data["prod"].ContainsKey(AppConstants.charactersToolId))
      {
        return StatusCode(500, new ErrorResponseSchema { ErrorMessage = "Invalid JSON" });
      }

      return Ok(settingsData);
    }
  }
}
