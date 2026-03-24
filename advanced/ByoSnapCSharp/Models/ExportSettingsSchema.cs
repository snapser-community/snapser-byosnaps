using System.Collections.Generic;

namespace ByoSnapCSharp.Models
{
  /// <summary>
  /// Represents the export settings response with versioned data across environments.
  /// </summary>
  public class ExportSettingsSchema
  {
    /// <summary>
    /// The version of the export schema.
    /// </summary>
    public string Version { get; set; } = string.Empty;

    /// <summary>
    /// Unix timestamp of when the export was created.
    /// </summary>
    public long ExportedAt { get; set; }

    /// <summary>
    /// Environment-keyed data (dev, stage, prod) containing tool settings.
    /// </summary>
    public Dictionary<string, Dictionary<string, SettingsSchema>> Data { get; set; }
      = new Dictionary<string, Dictionary<string, SettingsSchema>>();
  }
}
