import { ErrorResponse, SuccessMessageResponse } from '../types/responses';
import { SettingsSchema, getDefaultSettings } from '../models/settingsModel';
import { ExportSettingsSchema } from '../models/exportSettingsModel';
import { CustomSettingsPayload } from '../models/customSettingsModel';
import { authMiddleware } from '../middleware/authMiddleware';
import { Request as ExpressRequest } from 'express';
import { Controller, Route, Get, Put, Post, Delete, Path, Query, Extension, Body, Middlewares, TsoaResponse, Response, Res, Request } from 'tsoa';

// # @GOTCHAS 👋 - Please read GOTCHAS.md

// Constants
const CHARACTERS_TOOL_ID = 'characters';
const CHARACTER_SETTINGS_BLOB_KEY = 'character_settings';
const CHARACTERS_BLOB_KEY = 'characters';
const PRIVATE_ACCESS_TYPE = 'private';
const PROTECTED_ACCESS_TYPE = 'protected';
const DEFAULT_ENVIRONMENT = 'dev';
const DEFAULT_BYOSNAP_VERSION = '1.0.0';
const STORAGE_HTTP_URL_ENV_KEY = 'SNAPEND_STORAGE_HTTP_URL';
const INTERNAL_HEADER_ENV_KEY = 'INTERNAL_HEADER';
const BYOSNAP_VERSION_ENV_KEY = 'BYOSNAP_VERSION';

// TODO: Uncomment when snapser-internal SDK is generated
// import { StorageServiceApi } from '../snapser-internal/api/storageServiceApi';

function getEnv(key: string, defaultValue: string): string {
    return process.env[key] ?? defaultValue;
}

function getDefaultCharactersPayload(): { [toolId: string]: SettingsSchema } {
    return {
        [CHARACTERS_TOOL_ID]: getDefaultSettings(),
    };
}

function validateExportStructure(data: ExportSettingsSchema): boolean {
    if (!data.data) return false;
    for (const env of ['dev', 'stage', 'prod']) {
        if (!data.data[env]) return false;
        if (!data.data[env][CHARACTERS_TOOL_ID]) return false;
    }
    return true;
}

// ===========================================================================
// Settings Controller: Handles configuration tools, import/export, user manager, and GDPR
// ===========================================================================

@Route('/v1/byosnap-advanced/settings')
export class SettingsController extends Controller {

    // ===========================================================================
    // A i]: Configuration Tool: Built using the Snapser UI Builder
    // ===========================================================================

    /**
     * @summary Configuration Tool
     */
    @Get("/")
    @Extension("x-description", 'Get the settings for the characters microservice. This endpoint is called by the Snapser Configuration Tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<SettingsSchema>(200, "Settings retrieved successfully")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async getSettings(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Request() req: ExpressRequest,
        @Query() tool_id?: string,
        @Query() environment?: string,
    ): Promise<SettingsSchema> {
        const env = environment || DEFAULT_ENVIRONMENT;
        const blobOwnerKey = `${tool_id}_${env}`;
        // blobOwnerKey is used when Storage SDK is connected
        void blobOwnerKey;

        // TODO: Uncomment when snapser-internal SDK is generated
        // const storageUrl = getEnv(STORAGE_HTTP_URL_ENV_KEY, 'http://storage-service:8090');
        // const storageApi = new StorageServiceApi(storageUrl);
        // try {
        //   const result = await storageApi.storageGetBlob(
        //     PRIVATE_ACCESS_TYPE, CHARACTER_SETTINGS_BLOB_KEY, blobOwnerKey,
        //     getEnv(INTERNAL_HEADER_ENV_KEY, 'internal')
        //   );
        //   if (result.body?.value) {
        //     return JSON.parse(result.body.value);
        //   }
        // } catch (_) {}

        return getDefaultSettings();
    }

    /**
     * @summary Configuration Tool
     */
    @Put("/")
    @Extension("x-description", 'Update the settings for the characters microservice. This endpoint is called by the Snapser Configuration Tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<SettingsSchema>(200, "Settings updated successfully")
    @Response<ErrorResponse>(400, "Bad request")
    @Response<ErrorResponse>(500, "Server error")
    @Middlewares([authMiddleware(["internal"])])
    public async updateSettings(
        @Res() _badRequest: TsoaResponse<400, ErrorResponse>,
        @Res() _serverError: TsoaResponse<500, ErrorResponse>,
        @Request() req: ExpressRequest,
        @Body() body: Record<string, any>,
        @Query() tool_id?: string,
        @Query() environment?: string,
    ): Promise<Record<string, any>> {
        const env = environment || DEFAULT_ENVIRONMENT;
        const blobOwnerKey = `${tool_id}_${env}`;
        void blobOwnerKey;

        // Extract payload if wrapped
        let blobData = body;
        if (body.payload && typeof body.payload === 'object') {
            blobData = body.payload;
        }

        // TODO: Add any custom validation here and on error return:
        // return _badRequest(400, { error_message: 'Duplicate characters found' });

        // TODO: Uncomment when snapser-internal SDK is generated
        // 1. StorageGetBlob to get current CAS
        // 2. StorageReplaceBlob with the new data and CAS
        // (see Python example for full flow)

        return blobData;
    }

    // ===========================================================================
    // A ii]: New Configuration Tool: Custom HTML Snap Configuration Tool
    // ===========================================================================

    /**
     * @summary Custom Configuration Tool
     */
    @Get("custom")
    @Extension("x-description", 'Get the settings for the custom HTML configuration tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<CustomSettingsPayload>(200, "Custom settings retrieved successfully")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async getSettingsCustom(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Request() req: ExpressRequest,
        @Query() tool_id?: string,
        @Query() environment?: string,
    ): Promise<CustomSettingsPayload> {
        const env = environment || DEFAULT_ENVIRONMENT;
        const blobOwnerKey = `${tool_id}_${env}`;
        void blobOwnerKey;

        // TODO: Uncomment when snapser-internal SDK is generated
        // StorageGetBlob with PRIVATE_ACCESS_TYPE, CHARACTER_SETTINGS_BLOB_KEY, blobOwnerKey
        // If found, wrap in { payload: parsed }

        return { payload: '' };
    }

    /**
     * @summary Custom Configuration Tool
     */
    @Put("custom")
    @Extension("x-description", 'Update the settings from the custom HTML configuration tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response(200, "Custom settings updated successfully")
    @Response<ErrorResponse>(500, "Server error")
    @Middlewares([authMiddleware(["internal"])])
    public async updateSettingsCustom(
        @Res() _serverError: TsoaResponse<500, ErrorResponse>,
        @Request() req: ExpressRequest,
        @Body() body: Record<string, any>,
        @Query() tool_id?: string,
        @Query() environment?: string,
    ): Promise<Record<string, any>> {
        const env = environment || DEFAULT_ENVIRONMENT;
        const blobOwnerKey = `${tool_id}_${env}`;
        void blobOwnerKey;

        // Extract payload if wrapped
        let blobData = body;
        if (body.payload && typeof body.payload === 'object') {
            blobData = body.payload;
        }

        // TODO: Uncomment when snapser-internal SDK is generated
        // 1. StorageGetBlob to get current CAS
        // 2. StorageReplaceBlob with the new data and CAS

        return blobData;
    }

    // ===========================================================================
    // B: Snapend Sync|Clone: Import/Export
    // ===========================================================================

    /**
     * @summary Export Settings
     */
    @Get("export")
    @Extension("x-description", 'Export all settings across environments (dev, stage, prod) for Snapend Sync/Clone.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<ExportSettingsSchema>(200, "Settings exported successfully")
    @Response<ErrorResponse>(500, "Server error")
    @Middlewares([authMiddleware(["internal"])])
    public async exportSettings(
        @Res() _serverError: TsoaResponse<500, ErrorResponse>,
        @Request() req: ExpressRequest,
    ): Promise<ExportSettingsSchema> {
        const response: ExportSettingsSchema = {
            version: getEnv(BYOSNAP_VERSION_ENV_KEY, DEFAULT_BYOSNAP_VERSION),
            exported_at: Math.floor(Date.now() / 1000),
            data: {
                dev: getDefaultCharactersPayload(),
                stage: getDefaultCharactersPayload(),
                prod: getDefaultCharactersPayload(),
            },
        };

        // Remember when storing these blobs we are storing them with
        // `characters_dev`, `characters_stage` and `characters_prod` as the owner_id
        // const blobKeyIDs = [
        //   `${CHARACTERS_TOOL_ID}_dev`,
        //   `${CHARACTERS_TOOL_ID}_stage`,
        //   `${CHARACTERS_TOOL_ID}_prod`,
        // ];

        // TODO: Uncomment when snapser-internal SDK is generated
        // StorageBatchGetBlobs with PRIVATE_ACCESS_TYPE, CHARACTER_SETTINGS_BLOB_KEY, blobKeyIDs
        // For each result, parse the value and update response.data[env][CHARACTERS_TOOL_ID]

        return response;
    }

    /**
     * @summary Import Settings
     */
    @Post("import")
    @Extension("x-description", 'Import settings across environments (dev, stage, prod) for Snapend Sync/Clone.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<SuccessMessageResponse>(200, "Settings imported successfully")
    @Response<ErrorResponse>(400, "Bad request")
    @Response<ErrorResponse>(500, "Server error")
    @Middlewares([authMiddleware(["internal"])])
    public async importSettings(
        @Res() _badRequest: TsoaResponse<400, ErrorResponse>,
        @Res() _serverError: TsoaResponse<500, ErrorResponse>,
        @Request() req: ExpressRequest,
        @Body() body: ExportSettingsSchema,
    ): Promise<SuccessMessageResponse> {
        // Validate the incoming structure
        if (!validateExportStructure(body)) {
            return _serverError(500, { error_message: 'Invalid JSON' });
        }

        // TODO: Uncomment when snapser-internal SDK is generated
        // Build blob payloads for dev, stage, prod with cas="0" (force replace)
        // StorageBatchReplaceBlob with all three blob payloads

        return { message: 'Success' };
    }

    /**
     * @summary Validate Import Settings
     */
    @Post("validate-import")
    @Extension("x-description", 'Validate settings before importing. Snapser sends the settings that are about to be imported - validate if you can accept them.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<ExportSettingsSchema>(200, "Settings are valid")
    @Response<ErrorResponse>(500, "Invalid settings")
    @Middlewares([authMiddleware(["internal"])])
    public async validateImportSettings(
        @Res() _serverError: TsoaResponse<500, ErrorResponse>,
        @Request() req: ExpressRequest,
        @Body() body: ExportSettingsSchema,
    ): Promise<ExportSettingsSchema> {
        // Perform basic validation
        if (!validateExportStructure(body)) {
            return _serverError(500, { error_message: 'Invalid JSON' });
        }

        return body;
    }

    // ===========================================================================
    // A iii]: User Manager Tool: Custom HTML User Manager Tool
    // ===========================================================================

    /**
     * @summary User Manager Tool
     */
    @Get("users/{userId}/custom")
    @Extension("x-description", 'Get the user data for the custom HTML User Manager tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<CustomSettingsPayload>(200, "User data retrieved successfully")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async getUserDataCustom(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
    ): Promise<CustomSettingsPayload> {

        // TODO: Uncomment when snapser-internal SDK is generated
        // StorageGetBlob with PROTECTED_ACCESS_TYPE, CHARACTERS_BLOB_KEY, userId
        // If found, wrap in { payload: parsed }

        return { payload: '' };
    }

    /**
     * @summary User Manager Tool
     */
    @Post("users/{userId}/custom")
    @Extension("x-description", 'Update the user data for the custom HTML User Manager tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response(200, "User data updated successfully")
    @Response<ErrorResponse>(500, "Server error")
    @Middlewares([authMiddleware(["internal"])])
    public async updateUserDataCustom(
        @Res() _serverError: TsoaResponse<500, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
        @Body() body: Record<string, any>,
    ): Promise<Record<string, any>> {
        // Extract payload if wrapped
        let blobData = body;
        if (body.payload && typeof body.payload === 'object') {
            blobData = body.payload;
        }

        // TODO: Uncomment when snapser-internal SDK is generated
        // 1. StorageGetBlob with PROTECTED_ACCESS_TYPE, CHARACTERS_BLOB_KEY, userId to get CAS
        // 2. StorageReplaceBlob with the new data and CAS

        return blobData;
    }

    // ===========================================================================
    // C: User Tool: Get, Update and Delete User data: GDPR
    // ===========================================================================

    /**
     * @summary User Data (GDPR)
     */
    @Get("users/{userId}/data")
    @Extension("x-description", 'Get user data. Used by the GDPR tool and the User Manager tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response(200, "User data retrieved successfully")
    @Response<ErrorResponse>(400, "No data found")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async getUserData(
        @Res() _badRequest: TsoaResponse<400, ErrorResponse>,
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
    ): Promise<Record<string, any>> {

        // TODO: Uncomment when snapser-internal SDK is generated
        // StorageGetBlob with PRIVATE_ACCESS_TYPE, CHARACTERS_BLOB_KEY, userId
        // If found, parse and return the value
        // If not found, return _badRequest(400, { error_message: 'No data' })

        return {};
    }

    /**
     * @summary User Data (GDPR)
     */
    @Put("users/{userId}/data")
    @Extension("x-description", 'Update user data. Used by the GDPR tool and the User Manager tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response(200, "User data updated successfully")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async updateUserData(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
    ): Promise<Record<string, any>> {

        // TODO: Implement user data update using Storage API
        return {};
    }

    /**
     * @summary User Data (GDPR)
     */
    @Delete("users/{userId}/data")
    @Extension("x-description", 'Delete user data. Implements the GDPR right-to-be-forgotten.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response(200, "User data deleted successfully")
    @Response<ErrorResponse>(400, "No blob found")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async deleteUserData(
        @Res() _badRequest: TsoaResponse<400, ErrorResponse>,
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
    ): Promise<Record<string, any>> {

        // TODO: Uncomment when snapser-internal SDK is generated
        // StorageDeleteBlob with PRIVATE_ACCESS_TYPE, CHARACTERS_BLOB_KEY, userId
        // If response is nil, return _badRequest(400, { error_message: 'No blob' })

        return {};
    }
}
