using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using System;
using System.Linq;
using ByoSnapCSharp.Models;
using ByoSnapCSharp.Utilities;
using Microsoft.Extensions.Logging;

namespace ByoSnapCSharp.Filters
{
  public class ValidateAuthorizationAttribute : ActionFilterAttribute
  {
    private readonly string[] _allowedAuthTypes;
    private readonly string _userIdResourceKey;

    public ValidateAuthorizationAttribute(params string[] allowedAuthTypes)
    {
      _allowedAuthTypes = allowedAuthTypes;
      _userIdResourceKey = "userParams"; // Default key, can be set differently if needed
    }

    private string ExtractUserId(ActionExecutingContext context)
    {
      if (context.ActionArguments.TryGetValue(_userIdResourceKey, out var userParams))
      {
        // Try to cast the object to UserIdParameterSchema
        if (userParams is UserIdParameterSchema userIdParams)
        {
          // Now you can access the UserId property
          return userIdParams.UserId;
        }
      }
      return "";
    }

    public override void OnActionExecuting(ActionExecutingContext context)
    {
      var logger = context.HttpContext.RequestServices.GetRequiredService<ILogger<ValidateAuthorizationAttribute>>(); // Get the logger
      // logger.LogInformation("Starting authorization check.");
      // logger.LogInformation($"Allowed Auth Types: {string.Join(", ", _allowedAuthTypes)}");

      var httpContext = context.HttpContext;
      var request = httpContext.Request;

      // Get Gateway Header
      var gatewayHeaderValue = request.Headers[AppConstants.gatewayHeaderKey].FirstOrDefault() ?? "";
      var isInternalCall = gatewayHeaderValue.ToLower() == AppConstants.internalAuthType;

      // Get Auth Type Header
      var authTypeHeaderValue = request.Headers[AppConstants.authTypeHeaderKey].FirstOrDefault() ?? "";
      var isApiKeyAuth = authTypeHeaderValue.ToLower() == AppConstants.apiKeyAuthType;

      // Get User Id Header
      var userIdHeaderValue = request.Headers[AppConstants.userIdHeaderKey].FirstOrDefault() ?? "";
      var targetUser = ExtractUserId(context);
      var isTargetUser = userIdHeaderValue == targetUser && !string.IsNullOrEmpty(userIdHeaderValue);
      // logger.LogInformation("User ID auth detected." + userIdHeaderValue + " == " + targetUser);

      // Validate
      bool validationPassed = false;
      foreach (var authType in _allowedAuthTypes)
      {
        if (authType == AppConstants.internalAuthType && isInternalCall)
        {
          // logger.LogInformation("Internal call detected.");
          validationPassed = true;
          break;
        }
        else if (authType == AppConstants.apiKeyAuthType && isApiKeyAuth && !isInternalCall)
        {
          // logger.LogInformation("API Key auth detected.");
          validationPassed = true;
          break;
        }
        else if (authType == AppConstants.userAuthType && isTargetUser && !isInternalCall && !isApiKeyAuth)
        {
          // logger.LogInformation("User auth detected.");
          validationPassed = true;
          break;
        }
      }

      if (!validationPassed)
      {
        context.Result = new ObjectResult(new ErrorResponseSchema { ErrorMessage = "Unauthorized " }) { StatusCode = 401 };
      }

      base.OnActionExecuting(context);
    }
  }
}
