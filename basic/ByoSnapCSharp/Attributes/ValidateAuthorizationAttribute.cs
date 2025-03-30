using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using System;
using System.Linq;
using ByoSnapCSharp.Models;
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
      _userIdResourceKey = "user_id"; // Default key, can be set differently if needed
    }

    public override void OnActionExecuting(ActionExecutingContext context)
    {
      // var logger = context.HttpContext.RequestServices.GetRequiredService<ILogger<ValidateAuthorizationAttribute>>(); // Get the logger
      // logger.LogInformation("Starting authorization check.");
      // logger.LogInformation($"Allowed Auth Types: {string.Join(", ", _allowedAuthTypes)}");

      var httpContext = context.HttpContext;
      var request = httpContext.Request;

      // Get Gateway Header
      var gatewayHeader = request.Headers["Gateway"].FirstOrDefault() ?? "";
      var isInternalCall = gatewayHeader == "internal";

      // Get Auth Type Header
      var authTypeHeader = request.Headers["Auth-Type"].FirstOrDefault() ?? "";
      var isApiKeyAuth = authTypeHeader == "api-key";

      // Get User Id Header
      var userIdHeader = request.Headers["User-Id"].FirstOrDefault() ?? "";
      var targetUser = context.ActionArguments.ContainsKey(_userIdResourceKey) ? context.ActionArguments[_userIdResourceKey]?.ToString() : "";
      var isTargetUser = userIdHeader == targetUser;

      // Validate
      bool validationPassed = false;
      foreach (var authType in _allowedAuthTypes)
      {
        if (authType == "internal" && isInternalCall)
        {
          // logger.LogInformation("Internal call detected.");
          validationPassed = true;
          break;
        }
        else if (authType == "api-key" && !isInternalCall && isApiKeyAuth)
        {
          // logger.LogInformation("API Key auth detected.");
          validationPassed = true;
          break;
        }
        else if (authType == "user" && !isInternalCall && !isApiKeyAuth && !isTargetUser)
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
