using System.ComponentModel.DataAnnotations;

namespace ByoSnapCSharp.Models
{
  /// <summary>
  /// Represents a user Session parameter.
  /// </summary>
  public class TokenHeaderSchema
  {
    /// <summary>
    /// The users session token.
    /// </summary>
    [Required]
    public string Token { get; set; } = string.Empty;
  }
}
