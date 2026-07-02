using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.OpenApi.Models;
using Microsoft.OpenApi.Any;
using Swashbuckle.AspNetCore.SwaggerGen;
using System;
using System.Linq;

public class SnapserAuthTypesOperationFilter : IOperationFilter
{
  public void Apply(OpenApiOperation operation, OperationFilterContext context)
  {
    var authAttributes = context.MethodInfo.GetCustomAttributes(true)
        .OfType<SnapserAuthAttribute>()
        .FirstOrDefault();

    if (authAttributes != null)
    {
      var authTypes = new OpenApiArray();
      foreach (var authType in authAttributes.AuthTypes)
      {
        authTypes.Add(new OpenApiString(authType));
      }

      if (!operation.Extensions.ContainsKey("x-snapser-auth-types"))
      {
        operation.Extensions.Add("x-snapser-auth-types", authTypes);
      }
    }

    // `admin` is NOT an auth type. The [SnapserSdkCategory("admin")] attribute
    // emits the separate `x-snapser-sdk-categories` extension (an array), which
    // is what surfaces an endpoint in the Admin SDK (independent of its auth types).
    var sdkCategoryAttribute = context.MethodInfo.GetCustomAttributes(true)
        .OfType<SnapserSdkCategoryAttribute>()
        .FirstOrDefault();

    if (sdkCategoryAttribute != null)
    {
      if (!operation.Extensions.ContainsKey("x-snapser-sdk-categories"))
      {
        var sdkCategories = new OpenApiArray { new OpenApiString(sdkCategoryAttribute.Category) };
        operation.Extensions.Add("x-snapser-sdk-categories", sdkCategories);
      }
    }
  }
}
