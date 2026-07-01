import { ErrorResponse, SuccessMessageResponse } from '../types/responses';
import { authMiddleware } from '../middleware/authMiddleware';
import { Request as ExpressRequest } from 'express';
import { Controller, Route, Get, Path, Extension, Middlewares, TsoaResponse, Response, Res, Request } from 'tsoa';

// # @GOTCHAS 👋 - Please read GOTCHAS.md

// ===========================================================================
// Example Controller — your Snap's business logic lives here.
//
// The stubs below demonstrate each Snapser auth exposure. The
// `x-snapser-auth-types` extension controls which SDK / tool the API surfaces
// in, and the matching `authMiddleware([...])` enforces it at runtime. Add,
// rename, or remove these to fit your Snap.
//
// A single endpoint can accept MULTIPLE auth types at once (see the last
// example) — you do not need a separate route per auth type.
//
// For complete, working reference implementations see advanced/byosnap-node-ts.
// ===========================================================================

@Route('/v1/byosnap-core')
export class ExampleController extends Controller {

    /**
     * @summary Example: User Auth
     */
    @Get("users/{userId}/example")
    @Extension("x-description", 'Accessible by a logged-in user, validated against the User-Id in their token. Surfaces in the client/game SDK.')
    @Extension("x-snapser-auth-types", ["user"])
    @Response<SuccessMessageResponse>(200, "Success")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["user"])])
    public async exampleUserAuth(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
    ): Promise<SuccessMessageResponse> {
        // TODO: Add your user-scoped business logic here.
        //       See advanced/byosnap-node-ts for a full implementation.
        return { message: `Hello user ${userId}` };
    }

    /**
     * @summary Example: Api-Key Auth
     */
    @Get("example/api-key")
    @Extension("x-description", 'Accessible with a valid API key. Use for trusted server-to-server calls.')
    @Extension("x-snapser-auth-types", ["api-key"])
    @Response<SuccessMessageResponse>(200, "Success")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["api-key"])])
    public async exampleApiKeyAuth(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Request() req: ExpressRequest,
    ): Promise<SuccessMessageResponse> {
        // TODO: Add your api-key-scoped business logic here.
        //       See advanced/byosnap-node-ts for a full implementation.
        return { message: 'Hello api-key caller' };
    }

    /**
     * @summary Example: Internal Auth
     */
    @Get("example/internal")
    @Extension("x-description", 'Callable only by other Snaps within the same Snapend (internal gateway). Surfaces in the internal SDK.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<SuccessMessageResponse>(200, "Success")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async exampleInternalAuth(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Request() req: ExpressRequest,
    ): Promise<SuccessMessageResponse> {
        // TODO: Add your internal-only business logic here.
        //       See advanced/byosnap-node-ts for a full implementation.
        return { message: 'Hello internal caller' };
    }

    /**
     * @summary Example: Admin SDK
     */
    @Get("example/admin")
    @Extension("x-description", 'Surfaces in the Admin SDK for admin tooling / the Snapser dashboard. `admin` controls SDK exposure, not authentication.')
    @Extension("x-snapser-auth-types", ["admin"])
    @Response<SuccessMessageResponse>(200, "Success")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async exampleAdminSdk(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Request() req: ExpressRequest,
    ): Promise<SuccessMessageResponse> {
        // NOTE: `admin` is NOT an auth type. Tagging an endpoint with `admin` in
        // x-snapser-auth-types only makes it surface in the Admin SDK; the request
        // itself still arrives through the internal gateway, so we guard it with
        // the INTERNAL auth check.
        // TODO: Add your admin-only business logic here.
        //       See advanced/byosnap-node-ts for a full implementation.
        return { message: 'Hello admin caller' };
    }

    /**
     * @summary Example: Multi Auth
     */
    @Get("users/{userId}/example/multi-auth")
    @Extension("x-description", 'One endpoint reachable by a logged-in user, a valid API key, or an internal Snap. List every auth type you want to allow - no need for a separate route per type.')
    @Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
    @Response<SuccessMessageResponse>(200, "Success")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["user", "api-key", "internal"])])
    public async exampleMultiAuth(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
    ): Promise<SuccessMessageResponse> {
        // One endpoint can accept multiple auth types. Pass every accepted auth
        // type to both the x-snapser-auth-types extension (for SDK exposure) and
        // the authMiddleware (for runtime enforcement).
        // TODO: Add your business logic here.
        //       See advanced/byosnap-node-ts for a full implementation.
        return { message: `Hello, request for user ${userId} passed multi-auth` };
    }
}
