using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.OpenApi.Models;
using Microsoft.OpenApi.Any;
using Swashbuckle.AspNetCore.SwaggerGen;
using System;
using System.Linq;

public class RemoveFormatParametersFilter : IOperationFilter
{
  public void Apply(OpenApiOperation operation, OperationFilterContext context)
  {
    // Remove all content types except for 'application/json'
    foreach (var response in operation.Responses)
    {
      response.Value.Content = response.Value.Content
          .Where(c => c.Key.Equals("application/json", StringComparison.OrdinalIgnoreCase))
          .ToDictionary(p => p.Key, p => p.Value);
    }
  }
}
