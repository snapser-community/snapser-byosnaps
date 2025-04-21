[AttributeUsage(AttributeTargets.Method, AllowMultiple = false)]
public class SnapserAuthAttribute : Attribute
{
  public string[] AuthTypes { get; }

  public SnapserAuthAttribute(params string[] authTypes)
  {
    AuthTypes = authTypes;
  }
}
