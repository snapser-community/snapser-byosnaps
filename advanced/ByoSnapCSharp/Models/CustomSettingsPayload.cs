namespace ByoSnapCSharp.Models
{
  /// <summary>
  /// Wrapper for custom HTML tool payloads (GET response and PUT request body).
  /// </summary>
  public class CustomSettingsPayload
  {
    /// <summary>
    /// The payload data for the custom tool.
    /// </summary>
    public object? Payload { get; set; }
  }
}
