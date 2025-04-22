using Newtonsoft.Json;
namespace ByoSnapCSharp.Models
{
  public class ProfileAttributes
  {
    [JsonProperty("gamer_tag")]
    public string gamer_tag { get; set; }

    // Add more fields as needed
  }

  public class UpsertProfileRequestWrapper
  {
    [JsonProperty("profile")]
    public ProfileAttributes Profile { get; set; }
  }
}