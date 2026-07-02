[AttributeUsage(AttributeTargets.Method, AllowMultiple = false)]
public class SnapserSdkCategoryAttribute : Attribute
{
  public string Category { get; }

  public SnapserSdkCategoryAttribute(string category)
  {
    Category = category;
  }
}
