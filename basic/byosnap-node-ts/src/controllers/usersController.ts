import { ErrorResponse, SuccessResponse } from '../types/responses';
import { authMiddleware } from '../middleware/authMiddleware';
import { Request as ExpressRequest } from 'express';
import { Controller, Route, Get, Path, Post, Put, Delete, Extension, Header, Middlewares, TsoaResponse, Response, Res, Request } from 'tsoa';

// # @GOTCHAS 👋 - Please read GOTCHAS.md

@Route('/v1/byosnap-basic/users')
export class UserController extends Controller {

    /**
     * @summary Api One
     */
    @Get("{userId}/game")
    @Extension("x-description", 'This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.')
    @Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
    @Response<SuccessResponse>(200, "Successful Response")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["user", "api-key", "internal"])])
    public async apiOne(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest
    ): Promise<SuccessResponse> {
      const expressReq = req as ExpressRequest;
      const authType = expressReq.header("Auth-Type");
      const headerUserId = expressReq.header("User-Id");
      return {
        api: 'getGame',
        authType: authType ?? 'N/A',
        headerUserId: headerUserId ?? 'N/A',
        pathUserId: userId,
        message: 'success'
      };
    }

    /**
     * @summary Api Two
     */
    @Post("{userId}/game")
    @Extension("x-description", 'This API will work only with Api-Key auth. You can access this API with a valid api-key.')
    @Extension("x-snapser-auth-types", ["api-key", "internal"])
    @Response<SuccessResponse>(200, "Successful Response")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["api-key", "internal"])])
    public async apiTwo(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest
    ): Promise<SuccessResponse> {
      const expressReq = req as ExpressRequest;
      const authType = expressReq.header("Auth-Type");
      const headerUserId = expressReq.header("User-Id");
      return {
        api: 'postGame',
        authType: authType ?? 'N/A',
        headerUserId: headerUserId ?? 'N/A',
        pathUserId: userId,
        message: 'success'
      };
    }

    /**
     * @summary Api Three
     */
    @Delete("{userId}")
    @Extension("x-description", 'This API will work only when the call is coming from within the Snapend.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<SuccessResponse>(200, "Successful Response")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async apiThree(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest
    ): Promise<SuccessResponse> {
      const expressReq = req as ExpressRequest;
      const gatewayHeader = expressReq.header("Gateway");
      const headerUserId = expressReq.header("User-Id");
      return {
        api: 'deleteUser',
        authType: gatewayHeader ?? 'N/A',
        headerUserId: headerUserId ?? 'N/A',
        pathUserId: userId,
        message: 'success'
      };
    }

    /**
     * @summary Api Four
     */
    @Put("{userId}/profile")
    @Extension("x-description", 'This API will work for all auth types.')
    @Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
    @Response<SuccessResponse>(200, "Successful Response")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["user", "api-key", "internal"])])
    public async apiFour(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest
    ): Promise<SuccessResponse> {
      const expressReq = req as ExpressRequest;
      const authType = expressReq.header("Auth-Type");
      const headerUserId = expressReq.header("User-Id");
      return {
        api: 'updateProfile',
        authType: authType ?? 'N/A',
        headerUserId: headerUserId ?? 'N/A',
        pathUserId: userId,
        message: 'TODO: Add a message'
      };
    }
}
