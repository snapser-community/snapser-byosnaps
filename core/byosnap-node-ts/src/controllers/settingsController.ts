import { ErrorResponse, SuccessMessageResponse } from '../types/responses';
import { SettingsSchema, getDefaultSettings } from '../models/settingsModel';
import { ExportSettingsSchema } from '../models/exportSettingsModel';
import { CustomSettingsPayload } from '../models/customSettingsModel';
import { authMiddleware } from '../middleware/authMiddleware';
import { Request as ExpressRequest } from 'express';
import { Controller, Route, Get, Put, Post, Delete, Path, Query, Extension, Body, Middlewares, TsoaResponse, Response, Res, Request } from 'tsoa';

// # @GOTCHAS 👋 - Please read GOTCHAS.md

// ===========================================================================
// Settings Controller — System endpoints Snapser expects every BYOSnap to
// expose (configuration tools, import/export, user manager, GDPR).
//
// This is the CORE starter scaffold: every endpoint is present but each handler
// body is a STUB that returns a simple placeholder. Fill in the stubs with your
// own logic. For a complete, working reference (Storage Snap reads/writes, CAS
// handling, validation) see advanced/byosnap-node-ts.
// ===========================================================================

@Route('/v1/byosnap-core/settings')
export class SettingsController extends Controller {

    // ===========================================================================
    // A i]: Configuration Tool: Built using the Snapser UI Builder
    // ===========================================================================

    /**
     * @summary Configuration Tool
     */
    @Get("/")
    @Extension("x-description", 'Get the settings for this Snap. This endpoint is called by the Snapser Configuration Tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Extension("x-snapser-sdk-categories", ["admin"])
    @Response<SettingsSchema>(200, "Settings retrieved successfully")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async getSettings(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Request() req: ExpressRequest,
        @Query() tool_id?: string,
        @Query() environment?: string,
    ): Promise<SettingsSchema> {
        // TODO: Fetch the saved settings for `${tool_id}_${environment}` (e.g. from
        //       the Storage Snap) and return them. For now we return the default.
        //       See advanced/byosnap-node-ts for the full implementation.
        return getDefaultSettings();
    }

    /**
     * @summary Configuration Tool
     */
    @Put("/")
    @Extension("x-description", 'Update the settings for this Snap. This endpoint is called by the Snapser Configuration Tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Extension("x-snapser-sdk-categories", ["admin"])
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
        // TODO: Validate the incoming settings and persist them for
        //       `${tool_id}_${environment}`. On a validation failure return:
        //       return _badRequest(400, { error_message: '...' });
        //       See advanced/byosnap-node-ts for the full implementation.
        return { message: 'Success' };
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
    @Extension("x-snapser-sdk-categories", ["admin"])
    @Response<CustomSettingsPayload>(200, "Custom settings retrieved successfully")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async getSettingsCustom(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Request() req: ExpressRequest,
        @Query() tool_id?: string,
        @Query() environment?: string,
    ): Promise<CustomSettingsPayload> {
        // TODO: Fetch the saved settings for `${tool_id}_${environment}` and return
        //       them wrapped as { payload: <settings> }.
        //       See advanced/byosnap-node-ts for the full implementation.
        return { payload: '' };
    }

    /**
     * @summary Custom Configuration Tool
     */
    @Put("custom")
    @Extension("x-description", 'Update the settings from the custom HTML configuration tool.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Extension("x-snapser-sdk-categories", ["admin"])
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
        // TODO: Validate the incoming settings and persist them for
        //       `${tool_id}_${environment}`.
        //       See advanced/byosnap-node-ts for the full implementation.
        return { message: 'Success' };
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
        // TODO: Load the real saved settings per environment and merge them into
        //       `data`. For now we return defaults for dev/stage/prod.
        //       See advanced/byosnap-node-ts for the full implementation.
        return {
            version: process.env.BYOSNAP_VERSION ?? '1.0.0',
            exported_at: Math.floor(Date.now() / 1000),
            data: {
                dev: { characters: getDefaultSettings() },
                stage: { characters: getDefaultSettings() },
                prod: { characters: getDefaultSettings() },
            },
        };
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
        // TODO: Validate the incoming export payload and persist each environment's
        //       settings. On a validation failure return:
        //       return _serverError(500, { error_message: 'Invalid JSON' });
        //       See advanced/byosnap-node-ts for the full implementation.
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
        // TODO: Add your own validation here. On failure return:
        //       return _serverError(500, { error_message: 'Invalid JSON' });
        //       See advanced/byosnap-node-ts for the full implementation.
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
        // TODO: Look up this user's data and return it wrapped as
        //       { payload: <data> }.
        //       See advanced/byosnap-node-ts for the full implementation.
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
        // TODO: Validate the incoming data and persist it for this userId.
        //       See advanced/byosnap-node-ts for the full implementation.
        return { message: 'Success' };
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
        // TODO: Fetch and return everything you store for this userId.
        //       See advanced/byosnap-node-ts for the full implementation.
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
        // TODO: Persist the incoming data for this userId.
        //       See advanced/byosnap-node-ts for the full implementation.
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
        // TODO: Delete everything you store for this userId.
        //       See advanced/byosnap-node-ts for the full implementation.
        return {};
    }
}
