namespace ByoSnapCSharp.Models
{
  /// <summary>
  /// Represents the session token header.
  /// NOTE: TokenHeaderSchema is not used any more. Snapser automatically adds
  /// the right header in the SDK and API explorer.
  /// </summary>
  public class TokenHeaderSchema
  {
    /// <summary>
    /// The session token.
    /// </summary>
    public string Token { get; set; } = string.Empty;
  }
}
