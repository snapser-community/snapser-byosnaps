namespace ByoSnapCSharp.Utilities
{
  public static class AppConstants
  {
    public const string gatewayHeaderKey = "Gateway";
    public const string authTypeHeaderKey = "Auth-Type";
    public const string userIdHeaderKey = "User-Id";
    // Snapser adds this header to every request; used to correlate logs.
    public const string requestIdHeaderKey = "X-Request-Id";
    public const string internalAuthType = "internal";
    public const string apiKeyAuthType = "api-key";
    public const string userAuthType = "user";
  }
}
