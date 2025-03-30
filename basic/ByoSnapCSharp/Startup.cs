using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;
using ByoSnapCSharp.Middleware;

namespace ByoSnapCSharp
{
  public class Startup
  {
    public void ConfigureServices(IServiceCollection services)
    {
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
        c.SwaggerDoc("v1", new OpenApiInfo { Title = "ByoSnapCSharp", Version = "v1" });
        c.AddSecurityDefinition("Token", new OpenApiSecurityScheme
        {
          In = ParameterLocation.Header,
          Description = "Please insert token",
          Name = "Token",
          Type = SecuritySchemeType.ApiKey
        });
        c.AddSecurityRequirement(new OpenApiSecurityRequirement
          {
                    {
                        new OpenApiSecurityScheme
                        {
                            Reference = new OpenApiReference
                            {
                                Type = ReferenceType.SecurityScheme,
                                Id = "Token"
                            }
                        },
                        new string[] { }
                    }
          });
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

      app.UseMiddleware<AuthorizationMiddleware>();

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
