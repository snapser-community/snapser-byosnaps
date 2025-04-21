using Swashbuckle.AspNetCore.Swagger;
using Swashbuckle.AspNetCore.SwaggerGen;
using System.Collections.Generic;
using Microsoft.OpenApi.Models;
using Microsoft.OpenApi.Any;

//Note: We do not use this filter anymore. As starting RC 48, Snapser adds the appropriate
// headers to the swagger UI automatically.
public class TokenOperationFilter : IOperationFilter
{
  public void Apply(OpenApiOperation operation, OperationFilterContext context)
  {
    operation.Parameters ??= new List<OpenApiParameter>();

    operation.Parameters.Add(new OpenApiParameter
    {
      Name = "Token",
      In = ParameterLocation.Header,
      Description = "User Session Token",
      Required = true,
      Schema = new OpenApiSchema
      {
        Type = "string"
      }
    });
  }
}
