# BYOSnap Node Typescript MCP Example
 This is the documentation for your BYOSnap. You can update it the section below to what you want.

 ## Demo
 - We are going to follow the OpenAI [quick start guide](https://developers.openai.com/apps-sdk/quickstart)
 - The MCP will be hosted as a Snapser BYOSnap.

 IMPORTANT: At the moment, OpenAI does not support custom Auth. For now, you have to let Snapser know your companyId and AppId so that the Snapser team can add OpenAi to the allowlist to hit your `/mcp` endpoint. Once OpenAi supports custom auth, we can then add the Snapser supported `api-key`.

 ## Concept
 - OpenAI App hits the `/mcp` endpoint of this BYOSnap which is a RPC API.
 - You can then add code to integrate with other Snapser snaps.

 ## Limitation
 - There is no notion of a user that OpenAI passes to the calling MCP.
 - For now all todo lists get stored against a single uer.