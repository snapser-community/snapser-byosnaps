# Bring your own Snap - Basic

BYOSnap is a Snapser feature that enables you to integrate your own custom code. BYOSnaps run in containers within Snapser's Kubernetes platform and can be written in any programming language to cater to your game's specific needs. Once deployed, a BYOSnap resides within the same Kubernetes cluster as your other Snaps, facilitating seamless integration with the broader Snapser ecosystem.

## Introduction
This guide will walk you through the process of deploying a basic BYOSnap to the Snapser platform. By the end of this tutorial, you will have your code running on a Kubernetes cluster in Snapser, with your APIs accessible via the Snapser API Explorer and SDKs generated for your APIs.

## Step 0: Pre-requisites
Before you begin, ensure you have access to the Snapser CLI tool and a basic Snapend with the Authentication Snap and Anonymous connector enabled. The following tutorials will assist you:


<div className="parent">
  <div className="servicesBox">
    # Create a Snapend

    Check out the tutorial to create a Snapend with the Authentication snap with the Anonymous Connector enabled.

    <div>
      <DocsButton href={'/docs/guides/tutorials/create-snapend'} variant="contained" color="info" size="small" sx={{ml: 2, mb: 1}}>Tutorial</DocsButton>
    </div>
  </div>
  <div className="tutorialBox">
    # Setup Snapser CLI

    You can go through the Setup Snapser CLI tutorial to install and configure Snapctl.

    <div>
      <DocsButton href={'/docs/guides/tutorials/setup-snapctl'} variant="contained" color="info" size="small" sx={{ml: 2, mb: 1}}>Tutorial</DocsButton>
    </div>
  </div>
</div>

<Checkpoint step={0}>
  You are now ready to begin the tutorial.
</Checkpoint>

## Step 1: Check out the example code
We have BYOSnap examples in multiple languages that you can use to get started. Check out the snapser-community BYOSnap [repo](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic).
Snapser has examples for the following languages:
  - [C#](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic/ByoSnapCSharp)
  - [Go](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic/byosnap-go)
  - [Python](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic/byosnap-python)
  - [Node TypeScript](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic/byosnap-node-ts)

```bash
# For HTTPS based cloning
git clone https://github.com/snapser-community/snapser-byosnaps.git
# For SSH based cloning
git@github.com:snapser-community/snapser-byosnaps.git
```

- In the repo, there is a folder called **basic/**. Inside this folder, you will find the
  BYOSnap example code for C#, Go, Python and Node (Typescript). The folder structure is as follows:
  ```bash
  ├── basic/
  │   ├── ByoSnapCSharp/
  │   ├── byosnap-go/
  │   ├── byosnap-node-ts/
  │   └── byosnap-python/
  ```
  <Note>
  Each language folder contains a subfolder named **snapser-resources/**. Snapser utilizes this folder to access essential resources such as swagger.json, README.md, and BYOSnap profile files. To keep your root directory clean, these files are stored separately.
  </Note>

- Chose any language you are most comfortable with for this tutorial. Here is how a typical BYOSnap folder structure looks like:

  ```bash
  ├── basic/
    │   ├── ByoSnapCSharp/
    │   ├── byosnap-go/
    │   ├── byosnap-node-ts/
    │   └── byosnap-python/
    │       └── snapser-resources/
    │           ├── .env (👈 Automated Tutorial: Used by snapend_create.py )
    │           ├── README.md (👈 Powers the README of your BYOSNap on the Snapser Web portal )
    │           ├── snapser-base-snapend-manifest.json (👈 Automated Tutorial: Used by snapend_create.py )
    │           ├── snapser-byosnap-profile.json (👈 This powers the hardware and software settings for your BYOSnap )
    │           └── swagger.json (👈 This powers the SDK and API Explorer. Use the generate_swagger.* script to generate this file )
    │       └── Dockerfile (👈 Used by snapctl to deploy your BYOSnap )
    │       └── GOTCHAS.md (👈 A file you should read to understand the nuances per language )
    │       └── generate_routes.sh (👈 Only present in byosnap-node-ts/ )
    │       └── generate_swagger.sh|py (👈 Script to generate the swagger )
    │       └── README.md (👈 Developer Docs for you to run BYOSnap outside swagger )
  ```

<Checkpoint step={1}>
  We are now ready to update the code for our BYOSnap.
</Checkpoint>

## Step 2: Update the code
Each codebase includes 5 endpoints, located in the files specified below:
- C# - `/Controllers/UsersController.cs`
- Go - `/main.go`
- Python - `/app.py`
- Node - `/src/controllers/usersController.ts`

### Endpoints
1. **health** - A health check endpoint.
1. **GetGame** - An endpoint intended for exposure to game clients (user auth), trusted servers (api-key auth), and other internal BYOSnaps (internal auth).
1. **PostGame** - An endpoint designed to be accessible only to trusted servers (api-key auth) and other internal BYOSnaps (internal).
1. **DeleteUser** - An endpoint restricted to other internal BYOSnaps (internal).
1. **UpdateUserProfile** - An endpoint that you will modify in this tutorial, intended to be available to user auth, api-key auth, and internal auth.

**IMPORTANT**: We highly recommend understanding the **Validate Authorization** helper available in all the BYOSnap examples. This function is essential for validating the authorization headers for each endpoint:
  - C# - Located at `/Attributes/ValidateAuthorizationAttribute.cs`
  - Go - Found in `middleware.go`, method: `validateAuthorization`
  - Python - Available at `app.py`, method: `validate_authorization`
  - Node - Situated in `/src/middlewares/validateAuthorization.ts`

#### A: Update the API code
For this tutorial, you will update the response message of the **UpdateUserProfile** endpoint, deploy it, and observe the changes in action. Search for **TODO: Add a message** in the file and replace it with your custom message.

```csharp
[HttpPut("profile")]
[SnapserAuth(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
[ValidateAuthorization(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
[ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
[ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
[ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
[SwaggerOperation(OperationId = "Update User Profile", Summary = "User APIs", Description = "This API will work for all auth types.")]
public ActionResult<SuccessResponseSchema> UpdateUserProfile([FromRoute] UserIdParameterSchema userParams)
{
  var gatewayHeader = HttpContext.Request.Headers[AppConstants.gatewayHeaderKey].FirstOrDefault();
  var userIdHeader = HttpContext.Request.Headers[AppConstants.userIdHeaderKey].FirstOrDefault();
  return Ok(new SuccessResponseSchema
  {
    Api = "UpdateUserProfile",
    AuthType = gatewayHeader ?? "N/A",
    HeaderUserId = userIdHeader ?? "N/A",
    PathUserId = userParams.UserId,
    Message = "TODO: Add a message"
  });
}
```
```go
// UpdateUserProfileHandler handles the PUT request for an API endpoint. TODO: For you to update
// swagger:operation PUT /v1/byosnap-basic/users/{user_id}/profile updateUserProfile
// ---
// summary: User APIs
// description: This API will work only when the call is coming from within the Snapend.
// operationId: Update User Profile
// x-snapser-auth-types: ["user", "api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
//   - name: Token
//     in: header
//     required: true
//     description: User Session Token
//     type: string
// responses:
//   200:
//     description: Successfully retrieved data
//     schema:
//       $ref: '#/definitions/SuccessResponseSchema'
//   401:
//     description: Unauthorized access
//     schema:
//       $ref: '#/definitions/ErrorResponseSchema'
func UpdateUserProfile(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	if userIdHeader == "" {
		userIdHeader = "N/A"
	}
	response := SuccessResponseSchema{
		API:          "UpdateUserProfile",
		AuthType:     authType,
		HeaderUserID: userIdHeader,
		PathUserID:   mux.Vars(r)["user_id"],
		Message:      "TODO: Add your message here",
	}

	// Marshal the struct to JSON
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		http.Error(w, "Error creating response", http.StatusInternalServerError)
		return
	}

	// Set the content type and write the response
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonResponse)
}
```
```python
@app.route("/v1/byosnap-basic/users/<user_id>/profile", methods=["PUT"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def update_user_profile(user_id):
    """TODO: API for you to update
    ---
    put:
      summary: 'User APIs'
      description: This API will work for all auth types.
      operationId: 'Update User Profile'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      parameters:
      - in: path
        schema: UserIdParameterSchema
      - in: header
        schema: TokenHeaderSchema
      responses:
        200:
          content:
            application/json:
              schema: SuccessResponseSchema
          description: 'A successful response'
        400:
          content:
            application/json:
              schema: ErrorResponseSchema
          description: 'Unauthorized'
        401:
          content:
            application/json:
               schema: ErrorResponseSchema
          description: 'Unauthorized'
    """
    gateway_header = request.headers.get(GATEWAY_HEADER_KEY)
    user_id_header = request.headers.get(USER_ID_HEADER_KEY)
    return make_response(jsonify({
        'api': update_user_profile.__name__,
        'auth-type': gateway_header,
        'header-user-id': user_id_header if user_id_header else 'N/A',
        'path-user-id': user_id,
        # TODO: Add a message
        'message': 'TODO: Add a message',
    }), 200)
```
```typescript
/**
 * @summary User APIs
 */
@Put("{userId}/profile")
@Extension("x-description", 'This API will work for all auth types.')
@Extension("x-snapser-auth-types", ["user", "api-key", "internal"])
@Response<SuccessResponse>(200, "Successful Response")
@Response<ErrorResponse>(401, "Unauthorized")
@Middlewares([authMiddleware(["user", "api-key", "internal"])])
public async updateUserProfile(
    @Header('Token') token: string,
    @Res() _unauthorized: TsoaResponse<401, ErrorResponse>,
    @Path() userId: string,
    @Request() req: ExpressRequest
): Promise<SuccessResponse> {
  const expressReq = req as ExpressRequest;
  const authType = expressReq.header("Auth-Type");
  const headerUserId = expressReq.header("User-Id");
  return {
    api: 'updateUserProfile',
    authType: authType ?? 'N/A',
    headerUserId: headerUserId ?? 'N/A',
    pathUserId: userId,
    message: 'TODO: Add a message'
  };
}
```

<Note>
  If you have just updated the message in the API, you do not need to generate routes and swaggers. But follow the next steps to just get used to the process.
</Note>

#### B: Generate routes
<Note>
  Skip this step if you are using the C#, Go, or Python codebases.
</Note>
This step is only required if you are using the Node (Typescript) codebase. The Node codebase uses a helper script to generate the routes for your BYOSnap.

#### C: Generate the Swagger spec

After updating the code, you need to generate the Swagger spec for your BYOSnap. This spec is essential for generating SDKs and powering the API Explorer. Use the following helper script to generate the Swagger spec for your BYOSnap.

```csharp
// Run this command in the root of your code directory
./generate_swagger.sh
```
```go
// Run this command in the root of your code directory
./generate_swagger.sh
```
```python
# Run this command in the root of your code directory
python generate_swagger.py
```
```typescript
// Run this command in the root of your code directory
./generate_swagger.sh
```

<Checkpoint step={2}>
  You have successfully updated the code for your BYOSnap. We now need to deploy it.
</Checkpoint>

## Step 3: Deploy the BYOSnap

With the code updated, you are now ready to deploy your BYOSnap to the Private Snaps dashboard on Snapser.

- Choose a custom BYOSnap ID. For this tutorial, let's select $byosnapId=**byosnap-basic**.
  <Note>
    Use **byosnap-basic** as the BYOSnap ID. If you select a different ID, the Automated tutorial will not work. But if you are following the manual steps, you can use any ID you want.
  </Note>
- Select a version number. Set $version to `v1.0.0`.
- Determine the full path to the root of your code directory, e.g., `/Users/aj/snapser-byosnaps/basic/byosnap-python`.
- Identify the resources folder, which is the `snapser-resources` folder at the root of your code directory.

Replace the variables below with your custom values and execute the command to deploy your BYOSnap.


```bash
# $byosnapId = BYOSnap Id. Should start with `byosnap-`. Should not contain spaces and should only contain characters.
# $version = Version number for your BYOSnap. Should be in the format v1.0.0
# $path = Path to the directory where your BYOSnap code resides.
# $tag = Tag for your BYOSnap. This is optional.
snapctl byosnap publish --byosnap-id $byosnapId --version $version --path $rootCodePath --resources-path $rootCodePath/snapser-resources
```

You will see the output from the Snapctl tool as it deploys your BYOSnap to Snapser. Once the deployment is
complete, you will see a success message.
```bash
Success BYOSnap upload successful
Success Uploaded swagger.json
Success Uploaded README.md
Success Completed the docs uploading process
Success BYOSNAP publish successful
Success BYOSNAP publish version successful
Success BYOSNAP published successfully
BYOSnap published successfully with version v1.0.0
```

<Note>
  The publish command makes your BYOSnap available to other developers in your organization. You must increment the version number with each subsequent publish.
</Note>

<Checkpoint step={3}>
  You should see this BYOSnap in your Snapser BYOSnap [dashboard](https://snapser.com/snaps). If it is not visible, check the [logs](https://snapser.com/snapend/infrastructure/logs) for any errors.
</Checkpoint>

## Step 4: Add BYOSnap to Snapend
Now that we have published a BYOSnap, let's integrate it into a Snapend.

1. Go to the Snapser Web App and click on the Snapend you created in the **Snapend Creation** tutorial.
1. On your Snapend homepage, click the **Edit** button. This will take you to the Snapend Edit page.
1. Here, you will find the Snaps already included in your Snapend. Scroll down to locate the BYOSnap you just published and click the **Add** button.
<Note>
  Use the filter widget at the top right to display only BYOSnaps.
</Note>
1. Continue clicking **Continue** until you reach the final **Review** step, then click the **Snap it** button.
1. A pop-up window will show the progress of creating your cluster, which may take a few moments.

<Checkpoint step={4}>
  You now have a configured Snapend with both Auth and BYOSnap with Anonymous Auth enabled. You are ready to test your API.
</Checkpoint>

## Step 5: Test the new API
Navigate to the Snapend home dashboard and click on the **API Explorer** button under **Quick Links** to access the tool where you can test your API endpoints.

### A. Create an Anonymous User
1. Click on the **Auth** Snap.
1. Select the **Anonymous Login > AnonLogin PUT** API.
1. In the payload section, update the **user_name** to any name you prefer and click on the **PUT** button.
1. You will receive a successful response with a **user_id** and **session_token**. This is your Anonymous User ID and the JWT token for the session.
    <Note>
      Please save both the $userId and $sessionToken as you will need them for subsequent steps.
      You can also click the **History** button at the top of the API Explorer to view and copy the user ID and session token for future use.
    </Note>

### B. Test UpdateUserProfile
1. Click on the **Back** Icon above the API List navigation to return to the main API Explorer page.
1. Click on the **BYOSnap** Snap to view all four publicly available APIs.
1. Select the **UpdateUserProfile** API. Paste the **$userId** from the previous step into the **URL Parameters > user_id** and the **$sessionToken** from the previous step into the **Headers > Token**.
1. Click on the **PUT** button to receive a response from the API.
    <Note>
      The response should display the message you programmed into the codebase.
    </Note>

<Checkpoint step={5}>
  You have successfully deployed a BYOSnap to Snapser and tested it using the API Explorer.
</Checkpoint>

## Step 6: Swagger powering SDKs & API Explorer
Snapser introduces a valuable feature that enables you to generate SDKs for your BYOSnap and access the APIs via the API Explorer, all based on a Swagger 3.X file. This capability allows you to write your backend code once, annotate it with the appropriate Swagger tags, and subsequently generate SDKs for your game client, significantly saving time and effort for your client developers.

While adhering to the Swagger specification, we have implemented certain practices to enhance the user-friendliness of the generated SDKs. For instance, while certain attributes of the Swagger spec may be left as an empty string or null, we require that you provide values for these attributes. These rules are straightforward and offer substantial benefits.

### Key Rules for Enhancing SDKs and API Explorer Usability

<Note>
These rules are essential for both the generation of SDKs and the presentation of APIs in the API Explorer.
</Note>

#### Rule 0: Swagger must be 3.x and valid
Ensure you are using the Swagger 3.x specification to generate the SDKs. Use the [Swagger Editor](https://editor.swagger.io/) to validate your Swagger spec.

#### Rule 1: Every API must have an OperationId
The OperationId of each API is converted into the method name in the SDK. The API Explorer also utilizes this to display the API name, so it's crucial to assign a unique OperationId to every API.

#### Rule 2: API Summary is used to group APIs
Use the API Summary to group APIs in the API Explorer. Typically, APIs associated with the same resource should share the same summary, e.g., all APIs for the User resource should use the summary "User APIs."

#### Rule 3: Every API must have a Description
The Description of the API is used to provide detailed information about the API in the API Explorer and the generated documentation. This should be a free text field where you can elaborate on the API's functionality and provide examples.

### Automated Code Annotations to Swagger
We have pre-added Swagger annotations to the APIs, along with a helper script to generate the Swagger spec for your BYOSnap. Use the following commands to generate the Swagger spec for your BYOSnap, depending on your development environment:

```csharp
// Run this command in the root of your code directory
// ./generate_swagger.sh
```
```go
// Run this command in the root of your code directory
// ./generate_swagger.sh
```
```python
# Run this command in the root of your code directory
# python generate_swagger.py
```
```typescript
// Run this command in the root of your code directory
// ./generate_swagger.sh
```

## Step 7: Understand Gotchas
Each programming language has its own nuances, known as "gotchas". While we strive to make the BYOSnap experience as seamless as possible, it's important to be aware of these nuances, particularly how they affect route creation, API annotation, and Swagger specification generation. We've documented these issues thoroughly, but if you have any questions, please reach out to us.

- [C# Gotchas Readme](https://github.com/snapser-community/snapser-byosnaps/blob/main/basic/ByoSnapCSharp/GOTCHAS.md)
- [Go Gotchas Readme](https://github.com/snapser-community/snapser-byosnaps/blob/main/basic/byosnap-go/GOTCHAS.md)
- [Python Gotchas Readme](https://github.com/snapser-community/snapser-byosnaps/blob/main/basic/byosnap-python/README.md)
- [Node Gotchas Readme](https://github.com/snapser-community/snapser-byosnaps/blob/main/basic/byosnap-node-ts/GOTCHAS.md)

<Checkpoint step={7}>
  Congratulations! You have successfully completed the BYOSnap tutorial. You have learned how to deploy a BYOSnap, test it using the API Explorer, and generate SDKs for your BYOSnap APIs.
</Checkpoint>

## Automated Tutorial
After you have published a BYOSnap, we offer a helper script that simulates the end state of following the manual instructions to create a snapend with your BYOSnap in it. This script utilizes Snapctl.

<Note>
  If you have already completed the manual instructions, this script is unnecessary.
</Note>

To execute this script, you will need the following:
1. Navigate to the [Game Management](https://snapser.com/games) page on Snapser. Click the Copy Icon next to **ID** to copy the $companyId.
1. Select the game under which you wish to create your Snapend. This will bring you to the game's home page. Click the Copy Icon next to **ID** to copy the $gameId.
1. The $byosnapId is the identifier for your BYOSnap, which is **byosnap-basic** as used in the BYOSnap publish step.
1. Use the version number from the BYOSnap publish step, e.g., v1.0.0.

```bash
python snapend_create.py $companyId $gameId $byosnapId $version
```

You will see the output from the Snapctl tool as it creates your Snapend. Once the creation is complete, you will see a success message.

```bash
Success Updated your snapend. Your snapend is Live.
Success Snapend clone successful. Do not forget to download the latest manifest.
Your Snapend is created successfully with Snaps: auth and byosnap-*.
```

## Next Steps
1. Make sure you understand the Authorization flow in Snapser.
1. Check out the SDK that Snapser generates for your Snapends and try integrating it with your game client.
