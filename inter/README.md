import { DocsButton } from '../../../../components/docs/DocsButton.tsx'

export const meta = {
  author: 'AJ Apte',
}

# Bring your own Snap - Intermediate

BYOSnap is a Snapser feature that enables you to integrate your own custom code. BYOSnaps run in containers within Snapser's Kubernetes platform and can be written in any programming language to cater to your game's specific needs. Once deployed, a BYOSnap resides within the same Kubernetes cluster as your other Snaps, facilitating seamless integration with the broader Snapser ecosystem.

## Introduction
This guide will walk you through the process of integrating the BYOSnap with the **Internal SDK**, allowing you to communicate with other Snaps in your Snapend. You will also learn how to **locally debug** your code using Snapser's **Bring your own workstation** technology and then deploy it to a Snapend.

## Step 0: Pre-requisites
Before you begin, ensure you have access to the Snapser CLI tool and you have gone through the BYOSnap Basic tutorial. This will help you understand the basic concepts of BYOSnap.


<div className="parent">
  <div className="tutorialBox">
    # Setup Snapser CLI

    You can go through the Setup Snapser CLI tutorial to install and configure Snapctl.

    <div>
      <DocsButton href={'/docs/guides/tutorials/setup-snapctl'} variant="contained" color="info" size="small" sx={{ml: 2, mb: 1}}>Tutorial</DocsButton>
    </div>
  </div>
  <div className="servicesBox">
    # BYOSnap Basic
    Please make sure you have a basic understanding of the BYOSnap concept and have gone through the BYOSnap Basic tutorial. Its not required for you to actually deploy the BYOSnap as we will be doing that in this tutorial. But it is highly recommended to go through the tutorial to understand the concepts.

    <div>
      <DocsButton href={'/docs/guides/tutorials/byosnap-basic'} variant="contained" color="info" size="small" sx={{ml: 2, mb: 1}}>Tutorial</DocsButton>
    </div>
  </div>
</div>

<Checkpoint step={0}>
  You are now ready to begin the tutorial.
</Checkpoint>

## Step 1: Create a Snapend
We start by creating a Snapend with the **Auth** and **Profile** Snaps. We are going to then download the **Internal SDK** and use it in our BYOSnap. This will allow us to communicate with the other Snaps in our Snapend.

### A. Create a Snapend
1. On your games home page click on the **+ Snapend** button.
   <Note>
    If you have not added a game yet, please add a game first and then go to the games home page.
   </Note>
1. Give your Snapend a name and click continue.
1. Select the **Auth** and **Profile** Snaps from the list of available Snaps and then keep clicking Continue until you reach the **Review** step and finally click on the **Snap it** button.
1. A pop-up window will show the progress of creating your cluster. Your Snapend should be ready in a few moments.
![Snapend Creation](/images/docs/tutorials/byosnap-inter-snapend-create.png)

### B. Configure your Snaps
1. Once your Snapend is ready, click on the **Configuration Tool** button on the Snapend home page.
1. This will take you to the Configuration tool page where we want to configure the **Auth** and **Profile** Snaps.
1. First, lets click on the **Auth** Snap from the navigation bar on the left and select the **Connectors** tool.
1. Here we want to enable the **Anonymous Auth**. Click on Add Connectors and select Anonymous. Click Save on the form to enable the connector.
![Auth Connector](/images/docs/tutorials/snapend-create-admin-auth-anon.png)
1. Now, click on the Back button to go back to the Configuration tool home page. Now click on the **Profile** Snap from the navigation bar on the left and select the **Attributes** tool.
1. Here click on **+ Attribute** and add the following and then click **Save**:
    - **Attribute Name**: gamer_tag
    - **Category**: Unique
    - **Attribute Type**: text
    - **Required**: Yes
    - **Public**: Yes
![Profile Attribute](/images/docs/tutorials/byosnap-inter-profile-attribute-add.png)

<Checkpoint step={1}>
  You now have a Snapend that has Anonymous Auth enabled and a custom attribute called gamer_tag in the Profile Snap. We are now going to download the Internal SDK and use it in our BYOSnap.
</Checkpoint>

## Step 2: Download and integrate Internal SDK

1. Go to the Snapend home page and scroll to the bottom.
1. Here you will see the **Standard Language SDK** widget. Pick the language you are most comfortable with, select **Internal** for the SDK type, Select the **HTTP Library** you like and then click on the **Generate** button.
![Profile Attribute](/images/docs/tutorials/byosnap-inter-internal-sdk.png)
1. This will generate a custom internal SDK for our Snapend and soon you will see a zip file containing the SDK for the selected language. Unzip the file.
1. The folder structure is different for different languages. Check out the instructions below for each language.
<CollapsableDoc title="C# SDK Structure">
```bash
├── api/
├── src/
│   └── SnapserInternal/
│       └── Api/
│       └── Client/
│       └── Model/
│       └── SnapserInternal.csproj
```
</CollapsableDoc>
<CollapsableDoc title="Go SDK Structure">
```bash
├── api/
├── ...
├── client.go
├── ...
```
</CollapsableDoc>
<CollapsableDoc title="Node Typescript SDK Structure">
```bash
├── api/
├── api.ts
├── model/
```
</CollapsableDoc>
<CollapsableDoc title="Python SDK Structure">
```bash
├── requirements.txt
├── snapser_internal/
│   └── __init__.py
│   └── api/
│   └── api_client.py
│   └── api_responses.py
│   └── ...
│   └── models/
```
</CollapsableDoc>

<Checkpoint step={2}>
  You now have an internal SDK that you can integrate into your BYOSnap. This SDK will allow you to communicate with the other Snaps in your Snapend.
</Checkpoint>

## Step 3: Integrate the Internal SDK
### A. Check out the example code
We have BYOSnap examples in multiple languages that you can use to get started. Check out the snapser-community BYOSnap [repo](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic).
Snapser has examples for the following languages:
  - [C#](https://github.com/snapser-community/snapser-byosnaps/tree/main/inter/ByoSnapCSharp)
  - [Go](https://github.com/snapser-community/snapser-byosnaps/tree/main/inter/byosnap-go)
  - [Python](https://github.com/snapser-community/snapser-byosnaps/tree/main/inter/byosnap-python)
  - [Node TypeScript](https://github.com/snapser-community/snapser-byosnaps/tree/main/inter/byosnap-node-ts)

```bash
# For HTTPS based cloning
git clone https://github.com/snapser-community/snapser-byosnaps.git
# For SSH based cloning
git@github.com:snapser-community/snapser-byosnaps.git
```

- In the repo, there is a folder called **inter/**. Inside this folder, you will find the
  BYOSnap example code for C#, Go, Python and Node (Typescript). The folder structure is as follows:
  ```bash
  ├── inter/
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
  ├── inter/
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
    │       └── README.md (👈 Developer Docs for you to run BYOSnap outside Snapser )
  ```

### B. Copy the Internal SDK Contents
Copy the contents of the Internal SDK to the root of your BYOSnap code directory. Please check out the instructions for each language below. Doing this, will allow you to use the Internal SDK in your BYOSnap.
<CollapsableDoc title="C# Instructions">
For C#, you need to copy the **SnapserInternal** folder from the unzipped folder into your BYOSnap code directory. The folder structure should look like this:
```bash
├── api/
├── src/
│   └── SnapserInternal/  # 👈 This is the folder you want to copy
│       └── Api/
│       └── Client/
│       └── Model/
│       └── SnapserInternal.csproj
```
</CollapsableDoc>
<CollapsableDoc title="Go Instructions">
For Go, you need to create a folder called **snapser_internal** at the root of your BYOSnap and copy the contents of the the entire SDK into it. The folder structure should look like this:
```bash
├── api/
├── ...
├── client.go
├── ...
```
</CollapsableDoc>
<CollapsableDoc title="Node Typescript Instructions">
For Node Typescript, you need to create a folder called **snapser_internal** inside the root `src/` of your BYOSnap and copy the contents of the the entire SDK into it. The folder structure should look like this:
```bash
├── api/
├── api.ts
├── model/
```
</CollapsableDoc>
<CollapsableDoc title="Python Instructions">
For Python, you need to copy the **snapser_internal** folder from the unzipped folder into your BYOSnap code directory. The folder structure should look like this:
```bash
├── requirements.txt
├── snapser_internal/ # 👈 This is the folder you want to copy
│   └── __init__.py
│   └── api/
│   └── api_client.py
│   └── api_responses.py
│   └── ...
│   └── models/
```
</CollapsableDoc>

### C. Add dependencies
Each language has its own set of dependencies that you need to add to your BYOSnap code. Check out the instructions below for each language.
<CollapsableDoc title="C# Dependencies">
- Add the following to your main code's **.csproj** file:
```xml
<ItemGroup>
  ...
  <!-- These are the reference that your SDK needs to work. You can add them to your project file. -->
  <PackageReference Include="JsonSubTypes" Version="2.0.1" />
  <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  <PackageReference Include="Polly" Version="7.2.3" />
  <PackageReference Include="System.ComponentModel.Annotations" Version="5.0.0" />
</ItemGroup>
```
- Now compile your code using the following command:
```bash
dotnet build
```
</CollapsableDoc>
<CollapsableDoc title="Go Dependencies">
- Add the following to your go.mod file just above the first require statement:
```go
module byosnap-go

go 1.21.13

// 👇 Add this line
replace snapser_internal => ./snapser_internal

require (
  ...
)
```

- Now go to your main.go file and add the following import statement and the instantiation of the SDK.
```go
import (
  ...
  snapser_internal "snapser_internal"

  github.com...
)

var snapserClient *snapser_internal.APIClient
```

- Now run go.mod tidy at the root of your BYOSnap code directory to install the dependencies:
```bash
go mod tidy
```

</CollapsableDoc>
<CollapsableDoc title="Python Dependencies">
- Add the following to your main code's **requirements.txt** file:
```text
python_dateutil >= 2.5.3
setuptools >= 21.0.0
urllib3 >= 1.25.3, < 2.1.0
pydantic >= 1.10.5, < 2
aenum >= 3.1.11
```
<Note>
  You may already have these dependencies in your requirements.txt file. If so, you can skip this step. Just make sure the versions are compatible with the SDK.
</Note>

Then run the following command to install the dependencies:
```bash
pip install -r requirements.txt
```

</CollapsableDoc>

<CollapsableDoc title="Node Typescript Dependencies">
- The SDK uses the **requests** library for making HTTP calls. You need to add the following to your main code's **package.json** file:
```json
"dependencies": {
  ...
  "@types/request": "^2.48.12",
  "request": "^2.88.2",
},

```
<Note>
  You may already have these dependencies in your package.json file. If so, you can skip this step. Just make sure the versions are compatible with the SDK.
</Note>

Then run the following command to install the dependencies:
```bash
npm install
```

**IMPORTANT**: Additionally, there is a known bug with the Node Typescript SDK. It gives you a compilation error. Please open protobufAny.ts file and replace its contents with
```typescript
import { RequestFile } from './models';
export class ProtobufAny {
    'type'?: string;

    static discriminator: string | undefined = undefined;

    static attributeTypeMap: Array<{name: string, baseName: string, type: string}> = [
        {
            "name": "type",
            "baseName": "@type",
            "type": "string"
        }    ];

    static getAttributeTypeMap() {
        return ProtobufAny.attributeTypeMap;
    }
}
```

</CollapsableDoc>

<Checkpoint step={3}>
  With our SDK in and our code compiling / working, we are now ready to update the code for our BYOSnap.
</Checkpoint>

## Step 4: Update the code
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

<Note>
We highly recommend understanding the **Validate Authorization** helper available in all the BYOSnap examples. This function is essential for validating the authorization headers for each endpoint:
  - C# - Located at `/Attributes/ValidateAuthorizationAttribute.cs`
  - Go - Found in `middleware.go`, method: `validateAuthorization`
  - Python - Available at `app.py`, method: `validate_authorization`
  - Node - Situated in `/src/middlewares/validateAuthorization.ts`
</Note>

#### A: Update the API code
For this tutorial, our plan is to use BYOSnap as a proxy to the Profile Snap API. We will update the **UpdateUserProfile** endpoint to call the Profile Snaps **UpsertProfile API** and return the response. Uncomment the code under The TODO comment in the code below to use the Internal SDK. This will allow you to call the Profile Snap API directly from your BYOSnap.
<Note>
  In reality, you could have gone to the Profile Snap API directly. But we are using BYOSnap as a proxy to show you how to use the Internal SDK.
</Note>

<CodeGroup title="Update BYOSnap Code" tag="byosnap" >
```csharp
//File: Controllers/UsersController.cs
//Add the import statements at the top of the file
using SnapserInternal.Api;
using SnapserInternal.Client;
using SnapserInternal.Model;
using System.Net.Http;

...
// Update the UpdateUserProfile method in the UsersController.cs file
[HttpPut("profile")]
[SnapserAuth(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
[ValidateAuthorization(AppConstants.userAuthType, AppConstants.apiKeyAuthType, AppConstants.internalAuthType)]
[ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
[ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
[ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
[SwaggerOperation(OperationId = "UpdateUserProfile", Summary = "User APIs", Description = "This API will work for all auth types.")]
public ActionResult<SuccessResponseSchema> UpdateUserProfile(
  [FromRoute] UserIdParameterSchema userParams,
  [FromBody] UpsertProfileRequestWrapper body)
{
  try
  {
    var gatewayHeader = HttpContext.Request.Headers[AppConstants.gatewayHeaderKey].FirstOrDefault();
    var userIdHeader = HttpContext.Request.Headers[AppConstants.userIdHeaderKey].FirstOrDefault();
    Object result = null;
    // TODO: Uncomment the following code to use the SnapserInternal API
    // // // 👇 [IMPORTANT]: You have to set the baseURL using the Snapser provided
    // // //    environment variables. There will be a different environment variable
    // // //    for each snap. Eg: for the Profile Snap, Snapser sets the
    // // //    SNAPEND_PROFILES_HTTP_URL, For the Auth snap it will be SNAPEND_AUTH_HTTP_URL
    // Configuration config = new Configuration();
    // config.BasePath = Environment.GetEnvironmentVariable("SNAPEND_PROFILES_HTTP_URL") ?? config.GetOperationServerUrl("ProfilesServiceApi.ProfilesInternalUpsertProfile", 0);
    // HttpClient httpClient = new HttpClient();
    // HttpClientHandler httpClientHandler = new HttpClientHandler();
    // var apiInstance = new ProfilesServiceApi(httpClient, config, httpClientHandler);

    // // Profile Upsert Request
    // var upsertRequest = new UpsertProfileRequest(profile: body.Profile);
    // result = apiInstance.ProfilesInternalUpsertProfile(userParams.UserId, "internal", upsertRequest);
    return Ok(new SuccessResponseSchema
    {
      Api = "UpdateUserProfile",
      AuthType = gatewayHeader ?? "N/A",
      HeaderUserId = userIdHeader ?? "N/A",
      PathUserId = userParams.UserId,
      Message = result.ToString()
    });
  }
  catch (ApiException e)
  {
    return BadRequest(new ErrorResponseSchema
    {
      ErrorMessage = e.Message
    });
  }
}
```
```go
var profilesClient *snapser_internal.APIClient

func main() {
  ...
  // // 👇 [IMPORTANT]: You have to set the baseURL using the Snapser provided
  // //    environment variables. There will be a different environment variable
  // //    for each snap. Eg: for the Profile Snap, Snapser sets the
  // //    SNAPEND_PROFILES_HTTP_URL, For the Auth snap it will be SNAPEND_AUTH_HTTP_URL
  //Init the snapser client
	config := snapser_internal.NewConfiguration()
	config.Servers[0].URL = os.Getenv("SNAPEND_PROFILES_HTTP_URL")
	profilesClient = snapser_internal.NewAPIClient(config)

  ...
}

...

// UpdateUserProfileHandler handles the PUT request for an API endpoint. TODO: For you to update
// swagger:operation PUT /v1/byosnap-inter/users/{user_id}/profile updateUserProfile
// ---
// summary: User APIs
// description: This API will work only when the call is coming from within the Snapend.
// operationId: UpdateUserProfile
// x-snapser-auth-types: ["user", "api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
//     type: string
//   - name: profile_payload
//     in: body
//     required: true
//     description: Payload containing profile fields
//     schema:
//       $ref: "#/definitions/ProfilePayloadSchema"
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
	// // TODO: Uncomment the code below to enable the functionality
	// // Simulate fetching data or processing something
	// // Get the header auth-type from the request
	// authType := r.Header.Get("Auth-Type")
	// userIdHeader := r.Header.Get("User-Id")
	// if userIdHeader == "" {
	// 	userIdHeader = "N/A"
	// }
	// var profilePayload ProfilePayloadSchema
	// bodyBytes, _ := io.ReadAll(r.Body)
	// err := json.Unmarshal(bodyBytes, &profilePayload)
	// if err != nil {
	// 	w.Write([]byte(`{"error_message": "Error un-marshalling request body"}`))
	// 	w.WriteHeader(http.StatusBadRequest)
	// 	return
	// }
	// if profilePayload.Profile == nil {
	// 	w.Write([]byte(`{"error_message": "Profile is required"}`))
	// 	w.WriteHeader(http.StatusBadRequest)
	// 	return
	// }
	// req := profilesClient.ProfilesServiceAPI.ProfilesInternalUpsertProfile(r.Context(), userIdHeader).Gateway("internal").Body(snapser_internal.UpsertProfileRequest{
	// 	Profile: profilePayload.Profile,
	// })
	// snapserRes, httpResp, err := req.Execute()
	// if httpResp == nil {
	// 	w.Write([]byte(`{"error_message": "Error calling snapser"}`))
	// 	w.WriteHeader(http.StatusInternalServerError)
	// 	return
	// }
	// if err != nil {
	// 	body := httpResp.Body
	// 	bodyBytes, _ := io.ReadAll(body)
	// 	body.Close()

	// 	w.Header().Set("Content-Type", "application/json")
	// 	w.WriteHeader(httpResp.StatusCode)
	// 	w.Write(bodyBytes)
	// 	return
	// }

	// jsonResponse, err := json.Marshal(snapserRes)
	// if err != nil {
	// 	w.WriteHeader(httpResp.StatusCode)
	// 	w.Write([]byte(`{"error_message": "Error creating response"}`))
	// 	return
	// }

	// response := SuccessResponseSchema{
	// 	API:          "UpdateUserProfile",
	// 	AuthType:     authType,
	// 	HeaderUserID: userIdHeader,
	// 	PathUserID:   mux.Vars(r)["user_id"],
	// 	Message:     string(jsonResponse),
	// }

	// // Marshal the struct to JSON
	// jsonResponse, err = json.Marshal(response)
	// if err != nil {
	// 	http.Error(w, "Error creating response", http.StatusInternalServerError)
	// 	return
	// }

	// // Set the content type and write the response
	// w.Header().Set("Content-Type", "application/json")
	// w.WriteHeader(http.StatusOK)
	// w.Write(jsonResponse)
}
```
```python
# File: app.py
# Import the internal SDK
import snapser_internal
from snapser_internal.rest import ApiException

...

@app.route("/v1/byosnap-inter/users/<user_id>/profile", methods=["PUT"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def update_user_profile(user_id):
    """API that is accessible by User, Api-Key and Internal auth
    ---
    put:
      summary: 'User APIs'
      description: This API will work for all auth types.
      operationId: 'UpdateUserProfile'
      x-snapser-auth-types:
        - user
        - api-key
        - internal
      parameters:
      - in: path
        schema: UserIdParameterSchema
      requestBody:
        required: true
        content:
          application/json:
            schema: ProfilePayloadSchema
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
    payload = request.get_json()
    if not payload or "profile" not in payload:
        return jsonify({"error": "Missing profile"}), 400

    message = ''
    # # TODO: Uncomment the following code to use the SnapserInternal API
    # # 👇 [IMPORTANT]: You have to set the baseURL using the Snapser provided
    # # environment variables. There will be a different environment variable
    # # for each snap. Eg: for the Profile Snap, Snapser sets the
    # # SNAPEND_PROFILES_HTTP_URL, For the Auth snap it will be SNAPEND_AUTH_HTTP_URL
    # configuration = snapser_internal.Configuration(
    #     host=os.getenv("SNAPEND_PROFILES_HTTP_URL"))
    # with snapser_internal.ApiClient(configuration) as api_client:
    #     # Create an instance of the API class
    #     api_instance = snapser_internal.ProfilesServiceApi(api_client)
    #     body = snapser_internal.UpsertProfileRequest(
    #         profile=payload["profile"])
    #     try:
    #         # Anonymous Login
    #         api_response = api_instance.profiles_internal_upsert_profile(
    #             user_id_header, 'internal', body)
    #         message = api_response
    #     except ApiException as e:
    #         message = e

    return make_response(jsonify({
        'api': update_user_profile.__name__,
        'auth-type': gateway_header,
        'header-user-id': user_id_header if user_id_header else 'N/A',
        'path-user-id': user_id,
        'message': message
    }), 200)
```
```typescript
//File: src/controllers/usersController.ts
// Import the internal SDK
import { ProfilesServiceApi }  from '../snapser-internal/api/profilesServiceApi'
import { UpsertProfileRequest } from '../snapser-internal/model/upsertProfileRequest';

...

// Update the updateUserProfile function in usersController.ts
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
  // TODO: Uncomment the following code
  // // 👇 [IMPORTANT]: You have to set the baseURL using the Snapser provided
  // //    environment variables. There will be a different environment variable
  // //    for each snap. Eg: for the Profile Snap, Snapser sets the
  // //    SNAPEND_PROFILES_HTTP_URL, For the Auth snap it will be SNAPEND_AUTH_HTTP_URL
  // const baseUrl = process.env.SNAPEND_PROFILES_HTTP_URL ?? 'http://profiles-service:8090';
  // const profilesApi = new ProfilesServiceApi(baseUrl);
  // const payload: UpsertProfileRequest = {
  //   profile: body.profile
  // };
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
```
</CodeGroup>

<Note>
  **IMPORTANT**: The Internal SDK uses a special **Internal URL** per snap. This ensures that your API calls are going to get routed directly within the Snapend. Without, them having to go out to the internet. This is important for performance and security.
</Note>

#### B: Generate routes
<Note>
  Skip this step if you are using the C#, Go, or Python codebases.
</Note>
This step is only required if you are using the Node (Typescript) codebase. The Node codebase uses a helper script to generate the routes for your BYOSnap.

#### C: Generate the Swagger spec

After updating the code, you need to generate the Swagger spec for your BYOSnap. This spec is essential for generating SDKs and powering the API Explorer. Use the following helper script to generate the Swagger spec for your BYOSnap.

<CodeGroup title="Generate Swagger Spec" tag="bash" >
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
</CodeGroup>

<Checkpoint step={4}>
  You have successfully updated the code for your BYOSnap. We now need to deploy it.
</Checkpoint>

## Step 5: Deploy the BYOSnap

With the code updated, you are now ready to deploy your BYOSnap to the Private Snaps dashboard on Snapser.

- Choose a custom BYOSnap ID. For this tutorial, let's select $byosnapId=**byosnap-inter**.
  <Note>
    Use **byosnap-inter** as the BYOSnap ID. If you select a different ID, the Automated tutorial will not work. But if you are following the manual steps, you can use any ID you want.
  </Note>
- Select a version number. Set $version to `v1.0.0`.
- Determine the full path to the root of your code directory, e.g., `/Users/aj/snapser-byosnaps/inter/ByoSnapCSharp`.
- Identify the resources folder, which is the `snapser-resources` folder at the root of your code directory.

Replace the variables below with your custom values and execute the command to deploy your BYOSnap.


<CodeGroup title="Deploy BYOSnap" tag="bash" >
```bash
# $byosnapId = BYOSnap Id. Should start with `byosnap-`. Should not contain spaces and should only contain characters.
# $version = Version number for your BYOSnap. Should be in the format v1.0.0
# $path = Path to the directory where your BYOSnap code resides.
# $tag = Tag for your BYOSnap. This is optional.
snapctl byosnap publish --byosnap-id $byosnapId --version $version --path $rootCodePath --resources-path $rootCodePath/snapser-resources
```
</CodeGroup>

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
  The Snapshots below assume you are using the C# codebase. But the steps are the same for all languages.
</Note>

- Once you publish you will be able to see your BYOSnap in the **Custom Snaps** tool.
![CustomSnaps](/images/docs/tutorials/byosnap-inter-snaps.png)

<Note>
  The publish command makes your BYOSnap available to other developers in your organization. You must increment the version number with each subsequent publish.
</Note>

<Checkpoint step={5}>
  Now that our BYOSnap is published, we are ready to add it to our Snapend.
</Checkpoint>

## Step 6: Add BYOSnap to Snapend
Now that we have published a BYOSnap, let's integrate it into a Snapend.

### A. Manual Cluster Creation
1. Go to the Snapser Web App and click on the Snapend you created in the **Snapend Creation** tutorial.
1. On your Snapend homepage, click the **Edit** button. This will take you to the Snapend Edit page.
![EditSnapend](/images/docs/tutorials/byosnap-inter-snapend-edit.png)
1. Here, you will find the Snaps already included in your Snapend. Scroll down to locate the BYOSnap you just published and click the **Add** button.
    ![AddBYOSnap](/images/docs/tutorials/byosnap-inter-byosnap-add.png)
    <Note>
      Use the filter widget at the top right to display only BYOSnaps.
    </Note>
1. Continue clicking **Continue** until you reach the final **Review** step, then click the **Snap it** button.
1. A pop-up window will show the progress of creating your cluster. Your updated Snapend should be ready in a few moments.

### B. Automated Cluster Creation
<Note>
  If you have already completed the manual **Add BYOSnap to Snapend** steps, you can ignore this.
</Note>

After you have published a BYOSnap, we offer a helper script that simulates the end state of following the manual instructions to create a snapend with your BYOSnap in it. This script utilizes Snapctl.

To execute this script, you will need the following:
1. Navigate to the [Game Management](https://snapser.com/games) page on Snapser. Click the Copy Icon next to **ID** to copy the $companyId.
1. Select the game under which you wish to create your Snapend. This will bring you to the game's home page. Click the Copy Icon next to **ID** to copy the $gameId.
1. The $byosnapId is the identifier for your BYOSnap, which is **byosnap-inter** as used in the BYOSnap publish step.
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

<Checkpoint step={6}>
  You now have a configured Snapend with Auth, Profiles and a BYOSnap that can access the Profile Snap API. Let's now put this to the test.
</Checkpoint>

## Step 7: Test the new API
Navigate to the Snapend home dashboard and click on the **API Explorer** button under **Quick Links** to access the tool where you can test your API endpoints.
![API Explorer](/images/docs/tutorials/byosnap-inter-ql-api.png)
### A. Create an Anonymous User
1. Click on the **Auth** Snap.
    ![API Explorer Home](/images/docs/tutorials/byosnap-inter-api-home.png)
1. Select the **Anonymous Login > AnonLogin PUT** API.
1. In the payload section, update the **user_name** to any name you prefer and click on the **PUT** button.
    ![API Call](/images/docs/tutorials/byosnap-inter-anon-login.png)
1. You will receive a successful response with a **user_id** and **session_token**. This is your Anonymous User ID and the JWT token for the session.
    ![Anon User](/images/docs/tutorials/byosnap-inter-anon-user.png)
    <Note>
      Please save both the $userId and $sessionToken as you will need them for subsequent steps.
      You can also click the **History** button at the top of the API Explorer to view and copy the user ID and session token for future use.
    </Note>

### B. Test UpdateUserProfile
1. Click on the **Back** Icon above the API List navigation to return to the main API Explorer page.
1. Click on the **BYOSnap** Snap to view all four publicly available APIs.
    ![API Home BYOSnap](/images/docs/tutorials/byosnap-inter-api-home-byosnap.png)
1. Select the **UpdateUserProfile** API. Paste the **$userId** from the previous step into the **URL Parameters > user_id** and the **$sessionToken** from the previous step into the **Headers > Token**.
    ![BYOSnap API](/images/docs/tutorials/byosnap-inter-byosnap-api.png)
1. Click on the **PUT** button to receive a response from the API.
    ![BYOSnap API Response](/images/docs/tutorials/byosnap-inter-byosnap-api-response.png)
    <Note>
      The responses message field, should show the response from the Profile Snaps **UpsertProfile** API.
    </Note>

<Checkpoint step={7}>
  Congratulations! You have successfully deployed a BYOSnap to Snapser, integrated the Internal SDK and tested an API using the API Explorer.
</Checkpoint>

## Step 8: Local Testing
You may have noticed one issue. Each time you make a change, to your BYOSnap code, you have to either publish the BYOSnap or use the **snapctl byosnap sync** command. This isnt the ideal setup for local development. You want to be able to test your code locally without having to publish it every time.
![BYOSnap Sync](/images/docs/tutorials/byosnap-sync.png)

🎉🎉🎉 Good news, is that Snapser supports "Bring your own Workstation" (BYOWs) for local development. This means you can run your BYOSnap locally and remotely attach it to the Snapend. Any requests that are meant to go to your BYOSnap, actually get redirected to your lap top. Since your workstation gets added to the remote network, your existing internal SDKs continue to function as your lap top is able to make internal calls to other Snaps. If you have any external HTTP or gRPC calls outside the Snapend, they will continue to work as well. This is a great way to test your BYOSnap locally without having to publish it every time.

!![BYOWs](/images/docs/tutorials/byosnap-byows.png)

Let's see how to do this.
### A. Update the code
Let's update the code so we know that the BYOSnap is running locally. You can update the **UpdateUserProfile** method to return a different message when running locally. This will help you test if your BYOSnap is running locally or not.
<CodeGroup title="Update BYOSnap Code - Local mode" tag="byosnap" >
```csharp
//File: Controllers/UsersController.cs Method: UpdateUserProfile
// Update the Api response to include the local mode message
return Ok(new SuccessResponseSchema
{
  Api = "UpdateUserProfile" + "(Local mode)",
  AuthType = gatewayHeader ?? "N/A",
  HeaderUserId = userIdHeader ?? "N/A",
  PathUserId = userParams.UserId,
  Message = result.ToString()
});
```
```go
//File: main.go Method: UpdateUserProfile
// Update the Api response to include the local mode message
response := SuccessResponseSchema{
  API:          "UpdateUserProfile" + "(Local mode)",
  AuthType:     authType,
  HeaderUserID: userIdHeader,
  PathUserID:   mux.Vars(r)["user_id"],
  Message:     string(jsonResponse),
}
```
```python
#File: app.py Method: update_user_profile
# Update the Api response to include the local mode message
return make_response(jsonify({
    'api': update_user_profile.__name__ + "(Local mode)",
    'auth-type': gateway_header,
    'header-user-id': user_id_header if user_id_header else 'N/A',
    'path-user-id': user_id,
    'message': message
}), 200)
```
```typescript
//File: src/controllers/usersController.ts Method: updateUserProfile
// Update the Api response to include the local mode message
return {
  api: 'updateUserProfile' + "(Local mode)",
  authType: authType ?? 'N/A',
  headerUserId: headerUserId ?? 'N/A',
  pathUserId: userId,
  message: JSON.stringify(body)
};
```
</CodeGroup>

### B. Run your BYOWS command to enable port forward
- Run the following command to enable port forwarding for your BYOSnap. This will allow you to access your BYOSnap locally.
```bash
snapctl byows forward --snapend-id=$snapendId --byosnap-id=$byosnapId --local-port $port
```
- As an example, you will see the following output:
```bash
Forwarding: https://gateway.snapser.com/s6rvl02d/v1/byosnap-inter/* -> http://localhost:5003/
  Your BYOSnap gRPC server should be listening on: localhost:5002
               Connect to othe snaps over gRPC on: localhost:4002
Press <ctrl-c> to stop forwarding.
```
- This means any calls going to `https://gateway.snapser.com/s6rvl02d/v1/byosnap-inter/*` will be forwarded to your local machine on port 5003. You can now run your BYOSnap locally and test it.


### C. Run your BYOSnap locally
All the examples have a **run_dev_server.sh** script that you can use to run your BYOSnap locally. This script will start a local server on port 5003.

### D. Test your BYOSnap
1. Go to the API Explorer from under **Quick Links** and select the **BYOSnap** Snap.
  ![API Home BYOSnap](/images/docs/tutorials/byosnap-inter-api-home-byosnap.png)
1. Select the **UpdateUserProfile** API. Paste the **$userId** from the previous step into the **URL Parameters > user_id** and the **$sessionToken** from the previous step into the **Headers > Token**.
    ![BYOSnap API](/images/docs/tutorials/byosnap-inter-byosnap-api.png)
1. Click on the **PUT** button to receive a response from the API. You should see the call hit your BYOSnap on your local machine. Additionally, you should see the message in the response include **(Local mode)**.

{/* TODO: Add an image */}

<Checkpoint step={8}>
  Congratulations! You have completed the tutorial. You have learnt how to integrate an internal SDK, deploy your BYOSnap, run it locally and test it using the API Explorer.
</Checkpoint>

{/* <div className="parent">
  <div className="servicesBox">
    # BYOSnap Intermediate Tutorial

    Check out the intermediate tutorial for your BYOSnap where you can learn how to integrate your
    BYOSnap with other Snaps in your Snapend.

    <div>
      <DocsButton href={'/docs/guides/tutorials/setup-snapctl'} variant="contained" color="info" size="small" sx={{ml: 2, mb: 1}}>Tutorial</DocsButton>
    </div>
  </div>
  <div className="resourcesBox">
    # BYOSnap Advanced Tutorial

    Check out the advanced tutorial for your BYOSnap where you will integrate with all the Snapend
    hooks like Snap configuration import and export, User reset hook, configuration tool setup and more.

    <div>
      <DocsButton href={'/docs/guides/tutorials/setup-snapctl'} variant="contained" color="info" size="small" sx={{ml: 2, mb: 1}}>Tutorial</DocsButton>
    </div>
  </div>
</div> */}
