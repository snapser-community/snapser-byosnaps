namespace ByoSnapCSharp.Models
{
  /// <summary>
  /// Represents a successful response.
  /// </summary>
  public class SuccessResponseSchema
  {
    /// <summary>
    /// The API endpoint that was called.
    /// </summary>
    public string Api { get; set; } = string.Empty;
    /// <summary>
    /// The type of authorization used.
    /// </summary>
    public string AuthType { get; set; } = string.Empty;
    /// <summary>
    /// The User-Id header value if present.
    /// </summary>
    public string HeaderUserId { get; set; } = string.Empty;
    /// <summary>
    /// The User-Id path parameter value.
    /// </summary>
    public string PathUserId { get; set; } = string.Empty;
    /// <summary>
    /// A message.
    /// </summary>
    public string Message { get; set; } = string.Empty;
  }
}
