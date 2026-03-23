using System.Collections.Generic;

namespace ByoSnapCSharp.Models
{
  /// <summary>
  /// Represents the settings payload used by the Configuration Tool.
  /// Mirrors the BYO Tool Payload structure.
  /// </summary>
  public class SettingsSchema
  {
    /// <summary>
    /// The sections of the configuration tool.
    /// </summary>
    public List<SettingsSectionSchema> Sections { get; set; } = new List<SettingsSectionSchema>();
  }

  /// <summary>
  /// Represents a section within the settings payload.
  /// </summary>
  public class SettingsSectionSchema
  {
    /// <summary>
    /// The unique identifier for the section.
    /// </summary>
    public string Id { get; set; } = string.Empty;

    /// <summary>
    /// The components within this section.
    /// </summary>
    public List<SettingsComponentSchema> Components { get; set; } = new List<SettingsComponentSchema>();
  }

  /// <summary>
  /// Represents a component within a settings section.
  /// </summary>
  public class SettingsComponentSchema
  {
    /// <summary>
    /// The unique identifier for the component.
    /// </summary>
    public string Id { get; set; } = string.Empty;

    /// <summary>
    /// The type of the component (e.g., text, textarea, number, select, multi_select, checkbox, radio, group).
    /// </summary>
    public string Type { get; set; } = string.Empty;

    /// <summary>
    /// The value of the component.
    /// </summary>
    public object? Value { get; set; }

    /// <summary>
    /// Child components (used when Type is "group").
    /// </summary>
    public List<GroupComponentItemSchema>? Components { get; set; }
  }

  /// <summary>
  /// Represents a group component item.
  /// </summary>
  public class GroupComponentItemSchema
  {
    /// <summary>
    /// First component in the group.
    /// </summary>
    public SettingsComponentSchema? ComponentOne { get; set; }

    /// <summary>
    /// Second component in the group.
    /// </summary>
    public SettingsComponentSchema? ComponentTwo { get; set; }

    /// <summary>
    /// Third component in the group.
    /// </summary>
    public SettingsComponentSchema? ComponentThree { get; set; }

    /// <summary>
    /// Fourth component (boolean flag).
    /// </summary>
    public bool? ComponentFour { get; set; }
  }
}
