import { ErrorResponse } from '../types/responses';
import { CharactersResponse } from '../models/charactersModel';
import { authMiddleware } from '../middleware/authMiddleware';
import { Request as ExpressRequest } from 'express';
import { Controller, Route, Get, Path, Extension, Middlewares, TsoaResponse, Response, Res, Request } from 'tsoa';

// # @GOTCHAS 👋 - Please read GOTCHAS.md

// ===========================================================================
// Regular API Endpoints exposed by the Snap
// ===========================================================================

@Route('/v1/byosnap-advanced/users')
export class CharactersController extends Controller {

    /**
     * @summary Character APIs
     */
    @Get("{userId}/characters/active")
    @Extension("x-description", 'Get active characters for a user. This API supports User, API-Key, and Internal auth types.')
    @Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
    @Response<CharactersResponse>(200, "Characters retrieved successfully")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["user", "api-key", "internal"])])
    public async getActiveCharacters(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
    ): Promise<CharactersResponse> {
        return {
            characters: [],
        };
    }
}
