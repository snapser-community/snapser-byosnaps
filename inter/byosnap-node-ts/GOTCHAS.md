# Gotchas
What to Watch Out For When Working in This Repo

## Endpoints
- The Snapend Id is NOT part of the URL. This allows you to use the same BYOSnap in multiple Snapends.
```typescript
@Route('/v1/byosnap-inter/users')
```
- All externally accessible APIs need to start with /$prefix/$byosnapId/remaining_path. where $prefix = v1, $byosnapId = byosnap-inter and remaining_path = /users/<user_id>.
```typescript
@Route('/v1/byosnap-inter/users')
export class UserController extends Controller {

    /**
     * @summary Game APIs
     */
    @Get("{userId}/game")
    ...
```
- Notice the `x-snapser-auth-types` tags in the endpoint annotations and swagger.json. They tell Snapser if it should expose this API in the SDK and the API Explorer. Note: but you should still validate the auth type in the code.
```typescript
@Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
```
IMPORTANT: But you also have to pass those auth types to the middleware so that you get Authorization checks for free. Just adding those tags for swagger, are not going to do the authorization check for you.
```typescript
/**
 * @summary Game APIs
 */
@Get("{userId}/game")
@Extension("x-description", 'This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.')
@Extension("x-snapser-auth-types", ["user", "api-key", "internal"]) //(👈 This controls the x-snapser-auth-types tags in the swagger)
@Response<SuccessResponse>(200, "Successful Response")
@Response<ErrorResponse>(401, "Unauthorized")
@Middlewares([authMiddleware(["user", "api-key", "internal"])]) // (👈 This tells the middleware that user auth, app auth and internal auth are allowed for this method)
public async getGame(
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
```

- Snapser tech automatically adds the correct header to the SDK and API Explorer for your API. So you do not need to add the headers here against your API. Eg: For APIs exposed over User Auth, both the SDK and API Explorer will expose the Token header for you to fill in. For Api-Key Auth, the API Explorer will expose the Api-Key header for you to fill in. For internal APIs, the SDK and API Explorer will expose the Gateway header.
```typescript
//As you can see, we are not adding any Token or Api-Key Auth headers. Snapser handles that for you.
/**
 * @summary Game APIs
 */
@Get("{userId}/game")
@Extension("x-description", 'This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.')
@Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
@Response<SuccessResponse>(200, "Successful Response")
@Response<ErrorResponse>(401, "Unauthorized")
@Middlewares([authMiddleware(["user", "api-key", "internal"])])
public async getGame() {}
```
- The health endpoint does not have to contain the prefix. It should just be available at the root level.
```typescript
// app.ts
app.get('/healthz', (req, res) => { res.send('OK'); });
```
- We use tsoa to convert annotations to swagger.json. The swagger.json is used by Snapser to generate the SDK and power the API Explorer. Swagger generation also has some gotchas. Please see the section below.


## Endpoint generation
- Express allows you to code your controllers first and then generate routes based on it. We have provided you with a helper script to generate your routes. Any changes you make to the controller make sure you are running `./generate_routes.sh`.

## Swagger generation
This repo uses tsoa to convert controller annotations to a Swagger and there are tons of gotchas. We have provided you with a helper script to do this `./generate_swagger.sh`.

- You have to register the controller in the entrypoint file viz. `server.ts`. Else tsoa will not it pick for swagger generation.
```typescript
// server.ts
//This is important - Unless you import your controllers, the tsoa generated routes will not be registered
import './controllers/usersController';
```
- If you add a new response type in your controller, make sure its a relative import. Without this tsoa will not be able to find it. In the example below if you had an absolute import the swagger generator will not convert them to $schemas.
```typescript
// src/controllers/usersController.ts
import { ErrorResponse, SuccessResponse } from '../types/responses';
```
- The @summary comment you see in the controller is actually used to create the swagger summary for the API. So make sure every API has a JDOC
```typescript
/**
 * @summary Game APIs
 */
@Get("{userId}/game")
@Extension("x-description", 'This API will work with User and Api-Key auth. With a valid user token and api-key, you can access this API.')
@Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
@Response<SuccessResponse>(200, "Successful Response")
@Response<ErrorResponse>(401, "Unauthorized")
@Middlewares([authMiddleware(["user", "api-key", "internal"])])
public async getGame() {...}
```
- tsoa converts the JDOC to summary or description not both. So that your APIs have a description we have created a helper. Where you can add `@Extension("x-description", ...)` and the generate_swagger.sh code path will convert that to a proper swagger description. Check the `scripts/fix-swagger.ts` file.

- This example provides you with a helper middleware. Depending on which Auth type you want your API to be validated against, update the `["user", "api-key", "internal"]` array you pass to the `@Middlewares([authMiddleware`.

- This line in the controller `@Res() _unauthorized: TsoaResponse<401, ErrorResponse>,` Makes sure that tsoa picks up the `ErrorResponse`. Without this line, tsoa would not know, it has to crawl to `ErrorResponse` and have it in the swagger.
