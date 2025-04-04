using Swashbuckle.AspNetCore.Swagger;
using Swashbuckle.AspNetCore.SwaggerGen;
using System.Collections.Generic;
using Microsoft.OpenApi.Models;
using Microsoft.OpenApi.Any;

//TODO: Deprecate this once 0.48 goes out, as Snapser handles this for users for free.
public class AddHeaderAttribute : IOperationFilter
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
