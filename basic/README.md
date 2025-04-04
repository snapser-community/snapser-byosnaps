# Deploy BYOSnap - Basic Example

BYOSnap is a Snapser feature that allows you to bring your own custom code to Snapser. BYOSnaps run
in containers on Snapser's Kubernetes platform. BYOSnaps can be written in any language and can be
customized to your game's needs. When you deploy a BYOSnap it resides in the same Kubernetes cluster
as the other Snaps in your Snapend. This allows you to easily integrate your custom code with Snapser's
ecosystem.

## Introduction
This guide will walk you through deploying a basic BYOSnap to the Snapser platform. By the end, of this
tutorial you will have actual code running in a Kubernetes cluster on Snapser. Your APIs will be
accessible via the Snapser API Explorer tool and you will also be able to generate SDKs for your APIs.

## Step 0: Prerequisites

### A. Snapser CLI
Before you begin, make sure you have access to use the Snapser CLI tool.

#### Setup Snapser CLI

You can go through the Setup Snapser CLI [tutorial](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic/SETUP.md) to install and configure Snapctl.


<Checkpoint step={0}>
  You are now ready to begin the tutorial.
</Checkpoint>

## Step 1: Check out the example code
We have BYOSnap examples in multiple languages that you can use to get started. Check out the snapser-community BYOSnap [repo](https://github.com/snapser-community/snapser-byosnaps/tree/main/basic)
Snapser has examples for the following languages:
  - C#
  - Go
  - Python
  - Node TypeScript

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
- Chose any language you are most comfortable with for this tutorial.
  <Note>
    We encourage you to read the README.md file in the respective language directory.
  </Note>


<Checkpoint step={1}>
  We are now ready to update the code for our BYOSnap.
</Checkpoint>


## Step 2: Update the code
This codebase comes with 5 endpoints.
1. **health** - A health check endpoint.
1. **api one** - An endpoint which we want to expose to game clients (user auth), trusted servers (api-key auth) and other internal BYOSnaps (internal auth).
1. **api two** - An endpoint which we want to expose only to trusted servers (api-key auth) and other internal BYOSnaps (internal).
1. **api three** - An endpoint which we want to expose only to other internal BYOSnaps (internal).
1. **api four** - An endpoint which you will modify for this tutorial. We want this endpoint to be available to user auth, api-key auth and internal auth.

<Note>
  We highly recommend understanding the **validate_authorization()** function in the codebase. This function
  is responsible for validating the authorization headers for each endpoint.
</Note>

For this tutorial, we just want to update a response message of the **api four** endpoint, deploy it and
see the changes in action. Search for **TODO: Add a message** in the file and replace it with your custom code.

- CSharp
```csharp
[HttpPut("profile")]
[SnapserAuth("user", "api-key", "internal")]
[ValidateAuthorization("user", "api-key", "internal")]
[ProducesResponseType(StatusCodes.Status200OK, Type = typeof(SuccessResponseSchema))]
[ProducesResponseType(StatusCodes.Status400BadRequest, Type = typeof(ErrorResponseSchema))]
[ProducesResponseType(StatusCodes.Status401Unauthorized, Type = typeof(ErrorResponseSchema))]
[SwaggerOperation(Summary = "API Four", Description = "This API will work for all auth types.", OperationId = "API Four")]
public ActionResult<SuccessResponseSchema> ApiFour([FromRoute] UserIdParameterSchema userParams)
{
  var gatewayHeader = HttpContext.Request.Headers["Gateway"].FirstOrDefault();
  var userIdHeader = HttpContext.Request.Headers["User-Id"].FirstOrDefault();
  return Ok(new SuccessResponseSchema
  {
    Api = "UpdateProfile",
    AuthType = gatewayHeader ?? "N/A",
    HeaderUserId = userIdHeader ?? "N/A",
    PathUserId = userParams.UserId,
    Message = "TODO: Add a message"
  });
}
```
- Go
```go
// ApiFourHandler handles the PUT request for an API endpoint. TODO: For you to update
// swagger:operation PUT /v1/byosnap-basic/users/{user_id}/profile apiFour
// ---
// summary: API Four
// description: This API will work only when the call is coming from within the Snapend.
// operationId: API Four
// x-snapser-auth-types: ["user", "api-key", "internal"]
// parameters:
//   - name: user_id
//     in: path
//     required: true
//     description: Unique identifier of the user
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
func ApiFourHandler(w http.ResponseWriter, r *http.Request) {
	// Simulate fetching data or processing something
	// Get the header auth-type from the request
	authType := r.Header.Get("Auth-Type")
	userIdHeader := r.Header.Get("User-Id")
	if userIdHeader == "" {
		userIdHeader = "N/A"
	}
	response := SuccessResponseSchema{
		API:          "ApiFourHandler",
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
- Python
```python
gateway_header = request.headers.get(GATEWAY_HEADER_KEY)
user_id_header = request.headers.get(USER_ID_HEADER_KEY)
@app.route("/v1/byosnap-basic/users/<user_id>/profile", methods=["PUT"])
@validate_authorization(AUTH_TYPE_HEADER_VALUE_USER_AUTH, AUTH_TYPE_HEADER_VALUE_API_KEY_AUTH, GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def api_four(user_id):
  """TODO: API for you to update
  ---
  put:
    summary: 'API Four'
    description: This API will work for all auth types.
    operationId: 'API Four'
    x-snapser-auth-types:
      - user
      - api-key
      - internal
    parameters:
    - in: path
      schema: UserIdParameterSchema
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
        description: 'Bad Request'
      401:
        content:
          application/json:
              schema: ErrorResponseSchema
        description: 'Unauthorized'
  """
  return make_response(jsonify({
      'api': api_four.__name__,
      'auth-type': gateway_header,
      'header-user-id': user_id_header if user_id_header else 'N/A',
      'path-resource-name': resource_name,
      # TODO: Add a message
      'message': 'TODO: Add a message',
  }), 200)
```
- Node Typescript
```typescript
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
```

<Checkpoint step={2}>
  You have successfully updated the code for your BYOSnap. We now need to deploy it.
</Checkpoint>

## Step 3: Deploy the BYOSnap

With our code updated, we now want to deploy our BYOSnap to our Private Snaps dashboard on Snapser.

- Pick a custom BYOSnap Id. For this tutorial lets pick $byosnapId=**byosnap-basic**.
  <Note>
    Please stick to the **byosnap-basic** as the BYOSnap Id. Picking a different Id
    will cause certain examples to fail.
  </Note>
- Pick a version number. $version=`v1.0.0`.
- Find out the full path to the root of your code directory. Eg: `/Users/aj/snapser-byosnaps/basic/byosnap-python`.
- The resources folder is the `snapser-resources` folder in the root of your code directory.

Replace the variables below with your custom values and run the command to deploy your BYOSnap.

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
  The publish command is making your BYOSnap available to other devs in your organization.
  Every subsequent publish you will have to increment the version number.
</Note>

<Checkpoint step={3}>
  You should see this BYOSnap in your Snapser BYOSnap [dashboard](https://snapser.com/snaps). If you do
  not see it, check the logs for any errors.
</Checkpoint>

## Step 4: Create a cluster
Now that we have uploaded a BYOSnap, we can move to the Snapend creation step.
For this tutorial, we are going to create a Snapend with Auth and our BYOSnap. Understanding the
authorization flow in Snapser is crucial. By adding the Auth Snap, you will gain insights into how
Snapser manages authorization.

For this tutorial, we have two options. You can either create the Snapend manually or use a helper
script to create the Snapend. If this is your first time, we highly recommend going through the manual
process.

### A. Manual Cluster Creation

#### Step 1: Manual Cluster Creation: Set up your game

Note: Proceed to the next step, if you already have a game set up.

1. **Log in to your Snapser account** at https://snapser.com/login.
2. Navigate to the **Games dashboard** and click on the **New Game** button located in the upper right corner.
3. **Enter the name of your game** (1) in the designated field. It's advisable to use a name similar to your game's title to avoid confusion among your team members. Click **Add** (2) when done naming your game.

#### Step 2: Manual Cluster Creation: Snapend Creation

1. In the **Games dashboard**, click on the game you have added. This action brings up a view that shows the development, staging, and production environments of the game.
1. In the Development environment, click on the **+ Snapend** button.
1. **Enter the name of your snapend** (1) in the **Name your Snapend** field and click **Continue** (2).
1. For this tutorial, select the **Authentication** (1) and the **BYOSnap** you just uploaded (2) snaps by clicking **Add** for each snap and then click **Continue**. You can use the black filter button to quickly find your BYOSnap by selecting BYOSnaps from the dropdown.
1. Keep hitting continue till you reach the final **Review** step and then click the **Snap it** button. A pop-up window will appear showing you the state of creating your cluster, which takes a moment or two to complete.
1. Once Snapser finishes setting up the Snapend in Kubernetes (which includes infrastructure, configuration of snaps, network and security, and generating your snapend), click the **Game** button to wait for your snapend to be operational.

#### Step 3: Manual Cluster Creation: Configure Snapend

After your snapend is ready, you will see its widget under the game Snapends section. Clicking on this widget will take you to your Snapend home page.

For this demo, we want to enable Anonymous authentication for our BYOSnap. To do this, follow these steps:
1. On your Snapend homepage look for Quick links.
1. Click the **Snaps Configuration** button.
1. Click on the **Configure** button in the **Authentication snap**. Then from the left Navigation select the **Authentication>Connectors** tool.
1. Click the **Connector** button (1) and select **Anonymous** (2). You will then see a form, which shows the new Anonymous Auth state of **active**. Click **Save** to sync the configuration changes with your Snapend.

### Automated Cluster Creation
We have also provided a helper script to create a cluster with the exact end state if you had followed the manual instructions. The script uses Snapctl under the hood.

To run this command you will need the $companyId, $gameId, $byosnapId and the $version of the BYOSnap you want to deploy.
1. Go to the [Game Management](https://snapser.com/games) page on Snapser. Click the Copy Icon you see next to **ID** to copy the $companyId.
1. Click on the game you want to create your Snapend under. This will take you to the Game home page. Click the Copy Icon you see next to **ID** to copy the $gameId.
1. The $byosnapId is the identifier of your BYOSnap. This will be the BYOSnap Id **byosnap-basic** you used in the BYOSnap publish step.
1. Version number that we used in the BYOSnap publish step. Eg: v1.0.0.

```bash
python snapend_create.py $companyId $gameId $byosnapId $version
```

You will see the output from the Snapctl tool as it creates your Snapend. Once the creation is
complete, you will see a success message.

```bash
Success Updated your snapend. Your snapend is Live.
Success Snapend clone successful. Do not forget to download the latest manifest.
Your Snapend is created successfully with Snaps: auth and byosnap-*.
```

<Checkpoint step={4}>
  You now have a configured Snapend with Auth and BYOSnap with Anonymous Auth enabled.
  You are now ready to see your API in action.
</Checkpoint>


## Step 5: Test the new API
Go to the Snapend home dashboard and click on the **API Explorer** button. You will see the API Explorer tool
where you can test your API endpoints.

### A. Create an Anonymous User
1. Click on the **Auth** Snap.
1. Click on the **Anonymous Login > AnonLogin PUT** API.
1. Scroll down to the payload section and update the **user_name** to any name you want. Click on the **PUT** button.
1. You will see a successful response with a **user_id** and **session_token**. This is your Anonymous User ID and the JWT token for the session.
    <Note>
      Please save both the $userId and $sessionToken as you will need them for the next steps.
      You can also click the **History** button at the top of the API Explorer to see all the requests you have made allowing you to copy the user Id and session token for future use.
    </Note>

### B. Test api four
1. Now, Click on the **Back** Icon above the API List navigation, which will take you back to the main API Explorer page.
1. Now, click on the **BYOSnap** Snap and you will see all the 4 publicly available APIs.
1. Click on the **api four** API. Paste the **$userId** from the previous step into the **URL Parameters > user_id**. Paste the **$sessionToken** from the previous step into the **Headers > Token**.
1. Click on the **PUT** button and you will see the response from the API.
    <Note>
      You should see the message you added in the codebase in the response.
    </Note>

<Checkpoint step={5}>
  You have successfully deployed a BYOSnap to Snapser and tested it using the API Explorer.
</Checkpoint>

## Step 6: Swagger to SDK
Snapser unlocks a value add feature for you to generate SDKs for your BYOSnap APIs. This is a powerful
feature that allows you to write your backend code once, annotate it with the appropriate Swagger tags
and then generate SDKs for your game client. Thus, saving precious time and effort for your client developers.

While staying, within the rules of the Swagger spec, we have made some decisions to make the
generated SDKs more user friendly. For example, certain attributes of the Swagger spec can actually be
an empty string or null, but we expect you to add a value for these attributes. These rules are super
easy to follow and give you a lot of value in return.

Essentially, the rules are to make sure:
1. The generated SDKs are developer friendly and have good method names.
1. The Snapend API Explorer is able to show the APIs in a user friendly way.

### Snapser Rules for Swagger
##### Rule 0: Swagger must be 3.x and valid
Snapser uses the Swagger 3.x spec to generate the SDKs. So, make sure you are using the correct version of
Swagger. You can use the [Swagger Editor](https://editor.swagger.io/) to validate your Swagger spec.

#### Rule 1: Every API must have an OperationId
Snapser converts the OperationId of the API to be the method name of the SDK. The API Explorer also uses
this to show the API name. So, make sure you have a unique OperationId for every API.

#### Rule 2: API Summary is used to group APIs
The Summary for the API is what you can use to group APIs in the API Explorer. Generally, APIs for
the same resource should have the same summary. For example, all APIs for the User resource should have the
same summary viz **summary="User APIs"**

#### Rule 3: Every API must have a Description
The Description for the API is what you can use to describe the API. This is shown in the API Explorer
and the Documentation that is generated for the API. This is a free text field and you can use it to describe the API
in detail. For example, you can use it to describe the API in detail and give examples of the API.

### Automated Code Annotations to Swagger
In the examples above, we have already added the Swagger annotations to the APIs and a helper script
to generate the Swagger spec for you. This is how you will generate the Swagger spec for your BYOSnap.
- CSharp
```csharp
// Run this command at the root of your code directory
// ./generate_swagger.sh
```
- Go
```go
// Run this command at the root of your code directory
// ./generate_swagger.sh
```
- Python
```python
# Run this command at the root of your code directory
# python generate_swagger.py
```
- Node Typescript
```typescript
// Run this command at the root of your code directory
// ./generate_swagger.sh
```

### Swagger generation gotchas
<Note>
  Every repo comes with a GOTCHAS.md 👋 Please read this carefully. This file covers some of the
  nuances the languages have when it comes to code annotations to Swagger.
</Note>

- [C# Gotchas Readme](https://github.com/snapser-community/snapser-byosnaps/blob/main/basic/ByoSnapCSharp/GOTCHAS.md)
- [Go Gotchas Readme](https://github.com/snapser-community/snapser-byosnaps/blob/main/basic/byosnap-go/GOTCHAS.md)
- [Python Gotchas Readme](https://github.com/snapser-community/snapser-byosnaps/blob/main/basic/byosnap-python/README.md)
- [Node Gotchas Readme](https://github.com/snapser-community/snapser-byosnaps/blob/main/basic/byosnap-node-ts/GOTCHAS.md)

<Checkpoint step={6}>
  Congratulations! You have successfully completed the BYOSnap tutorial. You have
  learned how to deploy a BYOSnap, test it using the API Explorer and generate SDKs for your
  BYOSnap APIs.
</Checkpoint>

## Next Steps
1. Make sure you understand the Authorization flow in Snapser.
1. Check out the SDK that Snapser generates for your Snapends and try integrating it with your game client.

We are in the process of creating more advanced tutorisl
1. Tutorial to show you how you can talk to your Snapend Snaps from your BYOSnap.
2. Tutorial to show how to integrated your BYOSnap with the various Snapend hooks like, configuration import, user reset and event bus events.
