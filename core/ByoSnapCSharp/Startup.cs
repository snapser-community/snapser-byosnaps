using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;
using ByoSnapCSharp.Filters;
using ByoSnapCSharp.Utilities;

namespace ByoSnapCSharp
{
  public class Startup
  {
    public void ConfigureServices(IServiceCollection services)
    {
      // Add controllers
      services.AddControllers();

      // Eventbus (custom BYO events). AddHttpClient supplies the HttpClient the
      // EventbusClient depends on. The hosted service registers this Snap's
      // custom event types ONCE on startup, in the background, best-effort — it
      // never blocks boot or crashes the app / /healthz.
      services.AddHttpClient<EventbusClient>();
      services.AddHostedService<EventbusRegistrationHostedService>();

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
          Title = "BYOSnap Core C# Example",
          Version = "v1",
          Description = "A minimal starter scaffold for a C# BYOSnap. Every endpoint Snapser expects is present but stubbed. See advanced/ByoSnapCSharp for full implementations.",
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
        //Enabled Annotations - So the SwaggerOperation attributes are recognized
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
