using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Console;
using Swashbuckle.AspNetCore.Swagger;
using System.IO;
using Microsoft.OpenApi.Writers;
using ByoSnapCSharp.Utilities;

namespace ByoSnapCSharp
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var host = CreateHostBuilder(args).Build();

            // dotnet run generate-swagger
            if (args.Length > 0 && args[0] == "generate-swagger")
            {
                GenerateSwaggerJson(host);
            }
            else
            {
                host.Run();
            }
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                // Snapser expects one JSON object per log line on stdout. It
                // parses `level` to color lines in the Logs tool and
                // `request-id` to correlate all lines of one request.
                .ConfigureLogging(logging =>
                {
                    logging.ClearProviders();
                    logging.AddConsole(o => o.FormatterName = SnapserJsonConsoleFormatter.FormatterName);
                    // The formatter walks the scope provider itself, so scope values
                    // (request-id) surface as top-level JSON fields.
                    logging.AddConsoleFormatter<SnapserJsonConsoleFormatter, ConsoleFormatterOptions>(
                        o => o.IncludeScopes = true);
                })
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                    webBuilder.UseUrls("http://*:5003");
                });

        private static void GenerateSwaggerJson(IHost host)
        {
            using (var scope = host.Services.CreateScope())
            {
                var services = scope.ServiceProvider;

                var swaggerGen = services.GetRequiredService<ISwaggerProvider>();
                var swagger = swaggerGen.GetSwagger("v1");
                using (var streamWriter = new StreamWriter("./snapser-resources/swagger.json"))
                {
                    var options = new OpenApiJsonWriter(streamWriter);
                    swagger.SerializeAsV3(options);
                }

                System.Console.WriteLine("Swagger JSON generated at './snapser-resources/swagger.json'");
            }
        }
    }
}
