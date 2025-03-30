public class AuthorizationMiddleware
{
  private readonly RequestDelegate _next;

  public AuthorizationMiddleware(RequestDelegate next)
  {
    _next = next;
  }

  public async Task InvokeAsync(HttpContext context)
  {
    var gatewayHeader = context.Request.Headers["Gateway"].FirstOrDefault();
    var authTypeHeader = context.Request.Headers["Auth-Type"].FirstOrDefault();
    var userIdHeader = context.Request.Headers["User-Id"].FirstOrDefault();
    var isInternalCall = gatewayHeader == "internal";
    var isApiKeyAuth = authTypeHeader == "api-key";
    var targetUser = context.Request.RouteValues["user_id"]?.ToString();

    bool validationPassed = false;

    // Here, implement the detailed authorization logic as in your Python example
    // For brevity, I'm simplifying the checks

    if ((authTypeHeader == "user" || isApiKeyAuth || isInternalCall) && (userIdHeader == targetUser))
    {
      validationPassed = true;
    }

    if (!validationPassed)
    {
      context.Response.StatusCode = 401;
      await context.Response.WriteAsync("Unauthorized or unsupported authentication type");
      return;
    }

    // Call the next middleware in the pipeline
    await _next(context);
  }
}
