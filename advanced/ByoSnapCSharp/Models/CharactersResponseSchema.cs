using System.Collections.Generic;

namespace ByoSnapCSharp.Models
{
  /// <summary>
  /// Represents the characters response.
  /// </summary>
  public class CharactersResponseSchema
  {
    /// <summary>
    /// List of active character identifiers.
    /// </summary>
    public List<string> Characters { get; set; } = new List<string>();
  }
}
