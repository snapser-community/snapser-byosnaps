import { ErrorResponse, SuccessResponse } from '../types/responses';
import { ProfilePayload } from '../models/profilePayloadModel';
import { authMiddleware } from '../middleware/authMiddleware';
import { Request as ExpressRequest } from 'express';
import { Controller, Route, Get, Path, Post, Put, Delete, Extension, Body, Middlewares, TsoaResponse, Response, Res, Request } from 'tsoa';
import { ProfilesServiceApi }  from '../snapser-internal/api/profilesServiceApi'
import { UpsertProfileRequest } from '../snapser-internal/model/upsertProfileRequest';

// # @GOTCHAS 👋 - Please read GOTCHAS.md

@Route('/v1/byosnap-inter/users')
export class UserController extends Controller {

    /**
     * @summary Game APIs
     */
    @Get("{userId}/game")
    @Extension("x-description", 'This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.')
    @Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
    @Response<SuccessResponse>(200, "Successful Response")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["user", "api-key", "internal"])])
    public async getGame(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
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
     * @summary Game APIs
     */
    @Post("{userId}/game")
    @Extension("x-description", 'This API will work only with Api-Key auth. You can access this API with a valid api-key.')
    @Extension("x-snapser-auth-types", ["api-key", "internal"])
    @Response<SuccessResponse>(200, "Successful Response")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["api-key", "internal"])])
    public async saveGame(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
    ): Promise<SuccessResponse> {
      const expressReq = req as ExpressRequest;
      const authType = expressReq.header("Auth-Type");
      const headerUserId = expressReq.header("User-Id");
      return {
        api: 'saveGame',
        authType: authType ?? 'N/A',
        headerUserId: headerUserId ?? 'N/A',
        pathUserId: userId,
        message: 'success'
      };
    }

    /**
     * @summary User APIs
     */
    @Delete("{userId}")
    @Extension("x-description", 'This API will work only when the call is coming from within the Snapend.')
    @Extension("x-snapser-auth-types", ["internal"])
    @Response<SuccessResponse>(200, "Successful Response")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Middlewares([authMiddleware(["internal"])])
    public async deleteUser(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
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
     * @summary User APIs
     */
    @Put("{userId}/profile")
    @Extension("x-description", 'This API will work for all auth types.')
    @Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
    @Response<SuccessResponse>(200, "Successful Response")
    @Response<ErrorResponse>(401, "Unauthorized")
    @Response<ErrorResponse>(400, "Bad Request")
    @Middlewares([authMiddleware(["user", "api-key", "internal"])])
    public async updateUserProfile(
        @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
        @Res() _badRequest: TsoaResponse<400, ErrorResponse>,
        @Path() userId: string,
        @Request() req: ExpressRequest,
        @Body() body: ProfilePayload
    ): Promise<SuccessResponse> {
      const expressReq = req as ExpressRequest;
      const authType = expressReq.header("Auth-Type");
      const headerUserId = expressReq.header("User-Id");
      const baseUrl = process.env.SNAPEND_PROFILES_HTTP_URL ?? 'http://profiles-service:8090';
      const profilesApi = new ProfilesServiceApi(baseUrl);
      const payload: UpsertProfileRequest = {
        profile: body.profile
      };
      // TODO: Uncomment the following code
      // try {
      //   const result = await profilesApi.profilesInternalUpsertProfile(userId, 'internal', payload);
      //   const body = result.body;

      //   return {
      //     api: 'updateUserProfile',
      //     authType: authType ?? 'N/A',
      //     headerUserId: headerUserId ?? 'N/A',
      //     pathUserId: userId,
      //     message: JSON.stringify(body)
      //   };
      // } catch (error) {
      //     //Send ErrorResponse
      //     return _badRequest(400, {
      //       error_message: error?.message || "Upsert failed"
      //     });
      // }
      // TODO: Once you uncomment the above code, remove the following code
      return {
        api: 'updateUserProfile',
        authType: authType ?? 'N/A',
        headerUserId: headerUserId ?? 'N/A',
        pathUserId: userId,
        message: 'Remove this'
      };
    }
}
