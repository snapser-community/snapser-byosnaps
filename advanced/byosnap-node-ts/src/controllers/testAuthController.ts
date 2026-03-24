import { ErrorResponse, SuccessMessageResponse } from '../types/responses';
import { authMiddleware } from '../middleware/authMiddleware';
import { Request as ExpressRequest } from 'express';
import { Controller, Route, Get, Path, Extension, Middlewares, TsoaResponse, Response, Res, Request } from 'tsoa';

// # @GOTCHAS 👋 - Please read GOTCHAS.md

// ===========================================================================
// Test Auth Endpoints
// ===========================================================================

@Route('/v1/byosnap-advanced')
export class TestAuthController extends Controller {

    /**
     * @summary Test User Auth
     */
    @Get("user-auth/{userId}")
    @Extension("x-description", 'Test endpoint for user auth validation. Returns a message if user auth passes.')
    @Extension("x-snapser-auth-types", ["user"])
    @Response<SuccessMessageResponse>(200, "User auth validation passed")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["user"])])
    public async test_user_auth(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
    ): Promise<SuccessMessageResponse> {
        return {
            message: `Hello User ${userId}, you have passed the User Auth validation`,
        };
    }

    /**
     * @summary Test API Key Auth
     */
    @Get("api-key-auth")
    @Extension("x-description", 'Test endpoint for API key auth validation. Returns a message if API key auth passes.')
    @Extension("x-snapser-auth-types", ["api-key"])
    @Response<SuccessMessageResponse>(200, "API key auth validation passed")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["api-key"])])
    public async test_api_key_auth(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Request() req: ExpressRequest,
    ): Promise<SuccessMessageResponse> {
        const apiKeyName = req.headers['api-key-name'] as string || 'Unknown';
        return {
            message: `You have passed the API Key Auth validation using the key ${apiKeyName}`,
        };
    }
}
