namespace ByoSnapCSharp.Utilities
{
  public static class AppConstants
  {
    // Snap Identity
    public const string byoSnapId = "byosnap-core";

    // Header Keys
    public const string gatewayHeaderKey = "Gateway";
    public const string authTypeHeaderKey = "Auth-Type";
    public const string userIdHeaderKey = "User-Id";

    // Auth Type Values
    public const string internalAuthType = "internal";
    public const string apiKeyAuthType = "api-key";
    public const string userAuthType = "user";

    // Storage Constants
    public const string characterSettingsBlobKey = "character_settings";
    public const string charactersBlobKey = "characters";
    public const string privateAccessType = "private";
    public const string protectedAccessType = "protected";
    public const string charactersToolId = "characters";

    // Environment Keys
    public const string storageHttpUrlEnvKey = "SNAPEND_STORAGE_HTTP_URL";
    public const string internalHeaderEnvKey = "SNAPEND_INTERNAL_HEADER";
    public const string byoSnapVersionEnvKey = "BYOSNAP_VERSION";
    // TODO: Confirm the exact env var name for your Snapend (it may differ, e.g.
    //       SNAPEND_EVENT_BUS_HTTP_URL) and update this if needed.
    public const string eventbusHttpUrlEnvKey = "SNAPEND_EVENTBUS_HTTP_URL";

    // Default Values
    public const string defaultInternalHeaderValue = "internal";
    public const string defaultByoSnapVersion = "v1.0.0";
    public const string defaultEnvironment = "DEFAULT";
  }
}
