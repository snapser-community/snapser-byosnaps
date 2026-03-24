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
  }
}
