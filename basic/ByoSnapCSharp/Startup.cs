using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;
using ByoSnapCSharp.Filters;

namespace ByoSnapCSharp
{
  public class Startup
  {
    public void ConfigureServices(IServiceCollection services)
    {
      // Add controllers
      services.AddControllers();

      // Add CORS policy
      services.AddCors(options =>
      {
        options.AddPolicy("AllowSpecificOrigin",
                  builder => builder
                      .AllowAnyOrigin()
                      .AllowAnyMethod()
                      .AllowAnyHeader());
      });

      services.AddSwaggerGen(c =>
      {
        c.SwaggerDoc("v1", new OpenApiInfo
        {
          Title = "BYOSnap Basic C# Example",
          Version = "v1",
          Description = "A simple example BYOSnap example",
          TermsOfService = new Uri("https://snapser.com/resources/tos"),
          Contact = new OpenApiContact
          {
            Name = "Snapser Admin",
            Email = "admin@snapser.com",
            Url = new Uri("https://twitter.com/example"),
          },
        });
        //Adds the Auth Types to the Swagger UI
        c.OperationFilter<SnapserAuthTypesOperationFilter>();
        //CSharp automatically adds text/plain, application/json and application/xml to the response content types. This filter removes all but application/json.
        c.OperationFilter<RemoveFormatParametersFilter>();
        //Enabled Annotations - So the SwaggerOperation attributes in the UsersController.cs file are recognized
        c.EnableAnnotations();
      });
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
      if (env.IsDevelopment())
      {
        app.UseDeveloperExceptionPage();
      }

      app.UseSwagger();
      app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "ByoSnapCSharp v1"));

      app.UseRouting();

      // Enable CORS
      app.UseCors("AllowSpecificOrigin");

      app.UseAuthorization();

      app.UseEndpoints(endpoints =>
      {
        endpoints.MapControllers();
      });
    }
  }
}
