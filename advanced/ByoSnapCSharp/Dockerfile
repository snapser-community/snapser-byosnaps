# Use the official .NET 9.0 SDK image to build the application for arm64
ARG PLATFORM=linux/arm64
FROM --platform=$PLATFORM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /app

# Optionally clear NuGet caches
RUN dotnet nuget locals all --clear

# Example if you want to use Build-kit secrets
# Run this in your terminal
# $ export token_from_env="my-env-secret-123"
# $ echo "my-file-secret-456" > /tmp/test_secret.txt
# Then uncomment the following lines to use the secrets in the Dockerfile

# RUN --mount=type=secret,id=token_from_env \
#   --mount=type=secret,id=token_from_file \
#   echo "Env secret:" && cat /run/secrets/token_from_env && \
#   echo "File secret:" && cat /run/secrets/token_from_file

# You can pass secrets to the snapctl publish command like this:
# snapctl byosnap publish ... --secrets "id=token_from_env,env=token_from_env|id=token_from_file,src=/tmp/test_secret.txt"

# Copy the project file and restore any dependencies
COPY *.csproj ./
RUN dotnet restore --source https://api.nuget.org/v3/index.json

# Copy the rest of the application code
COPY . ./
RUN dotnet publish -c Release -o out

# Use the official ASP.NET Core runtime image for .NET 9.0, targeting arm64
FROM --platform=$PLATFORM mcr.microsoft.com/dotnet/aspnet:9.0 AS runtime
WORKDIR /app

# Copy the build output to the runtime image
COPY --from=build /app/out .

# Set the entry point for the container to run the application
ENTRYPOINT ["dotnet", "ByoSnapCSharp.dll"]

# Expose port 5003 for the RESTful server
EXPOSE 5003

# Set the environment variable to configure the application to listen on port 5003
ENV ASPNETCORE_URLS=http://+:5003
