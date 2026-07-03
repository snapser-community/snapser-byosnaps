# Snapser Resources

This folder contains Snapser-specific resource files used for deploying and configuring the BYOSnap microservice.

## Files

- `snapser-byosnap-profile.json` - BYOSnap deployment profile (ports, resources, env vars)
- `snapser-snapend-manifest.json` - Full Snapend manifest with all service definitions and settings
- `snapser-base-snapend-manifest.json` - Base manifest without the BYOSnap service definition
- `snapser-tool-characters.json` - Configuration tool definition for the Snapser UI Builder
- `_complex-snapser-tool-characters.json` - Complex configuration tool example with multiple component types
- `snapser-config-tool-characters-custom.html` - Custom HTML configuration tool
- `snapser-user-tool-characters-custom.html` - Custom HTML user manager tool
- `swagger.json` - Generated OpenAPI spec (run `npm run build:swagger` to generate)
- `.env` - Environment configuration for the Snapser Companion
