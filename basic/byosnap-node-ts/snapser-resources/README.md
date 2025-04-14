# BYOSnap Typescript Basic Example
 This BYOSnap has 4 Restful endpoints

 ## Concept
 When a Snapend has the Auth snap, you get authentication and authorization sorted out for you.

 ### Authorization
 Snapser supports three kinds of Authorization schemes
 1. **user auth**: (External Access) This term is used to refer when an external client is trying to access your endpoint. The client has to pass the clients session token as a header viz **Token: $sessionToken$** which your **gateway+auth** snap validate and send down the calling user Id via a header **User-Id** on validation.
 1. **api-key auth**: (External Access) In the Auth Snaps configuration tool, you can add API Keys can nominate APIs you want the key to be able to access. The caller has to pass the API-Key with each request as a header which your gateway+auth snap validate and allow validated calls to reach your BYOSnap.
 1. **internal auth**: (Internal Access) Use this scheme, if you do not want to allow any external access to your endpoint. Only snaps within your Snapend like other BYOSnaps will be able to call this endpoint.

**[IMPORTANT]**: It should be noted that all external calls viz calls coming over user or api-key auth, get validated for you by your Gateway+Auth Snap. However, for internal calls your API should check for the "Gateway: Internal" header to confirm the call is indeed coming from within your Snapend. Check the **validate_authorization** decorator in your main application file, to understand this.

 ## Endpoints
 1. GetGame: The endpoint that this method exposes is accessible both externally (over user and api-key auth) and internally.
 1. SaveGame: The endpoint that this method exposes is accessible only over api-key auth and internally.
 1. DeleteUser: The endpoint that this method exposes is only available internally.
 1. UpdateUserProfile: This is for you to update as part of the tutorial.
