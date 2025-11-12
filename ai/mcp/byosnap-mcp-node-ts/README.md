# BYOSnap Node Typescript - MCP Tutorial

## About
This demo shows you how to build a simple TODO application that is LLM native using MCP. At the end of this tutorial, you can create an App in ChatGPT, point it to your custom Snapser backend and allow the user to chat with ChatGPT to add, list and update a todo list that is stored in the cloud.

## Code
- The main application logic is in **mcpController.ts**
- This example is built using Express

## Pre-Requisites

### A. Install required packages
You need to have npm installed. Once you have it, please install the dependencies.
```bash
npm install
```
Here is a list of the original dependencies
```bash
npm install express tsoa @types/express body-parser cors joi
npm install typescript ts-node @types/node @types/cors @types/joi --save-dev
```

### B. Python Virtual Environment
Create a python virtualenv and then activate the virtualenv
```bash
# Mac
python3 -m venv venv
source snapctl/venv/bin/activate
```
```bash
# Windows
# Go to the root of the folder and start the virtualenv
.\venv\Scripts\activate
```

### C. Snapctl Setup
You need to have a valid setup for Snapctl, which is Snapsers CLI tool. Please follow the step by step (tutorial)[https://snapser.com/docs/guides/tutorials/setup-snapctl] if you do not have Snapctl installed on your machine. You can run the following command to confirm you have a valid snapctl setup.

```bash
# Validate if your snapctl setup is correct
snapctl validate
```

### D. Docker
Make sure Docker engine is running on your machine. Open up Docker desktop and settings. Also, please make sure the setting **Use containerd for pulling and storing images** is **disabled**. You can find this setting in the Docker Desktop settings.

## Resources
All the files that are required by the Snapctl are under the folder `./snapser-resources`
- **snapser-base-snapend-manifest.json** - If you are using the automated setup for your MCP backend using the `python snapend_create.py` script, this manifest is used by the script to spin up a backend on Snapser with your BYOSnap and other dependent snaps.
- **snapser-byosnap-profile.json**: You can use this file to tell Snapser about your BYOSnaps hardware, networking and configuration requirements.
- **swagger.json**: (Recommended but optional) If you have a valid Swagger 3.X file with your BYOSnap, Snapser also generates a SDK for your code and enables this BYOSnap to be usable in its API Explorer.
- **README.md**: (Optional) Optionally you can add a Readme for your devs. This file will be rendered on the Snapser web app.


## Helper Scripts
1. **generate_routes.sh**: Script that generates routes for all the controller code.

Usage
```bash
./generate_routes.sh
```

2. **generate_swagger.sh**: Script that generates a swagger.json based on the method annotations in your code base. This script stores the swagger.json under the `snapser-resources/` folder.

Usage
```bash
./generate_swagger.sh
```

3. **snapend_create.py**: Script to create a new Snapend with an Auth snap and your BYOSnap. You will need your companyId and gameId, which you can retrieve from the Snapser web app.
Usage
```bash
# $companyId = Your company Id
# $gameId = Your game ID
# $byosnapId is the ID of your BYOSnap. For the tutorial, we are using `byosnap-inter`
# $version needs to be in the format "vX.Y.Z" eg: "v1.0.0"
#   [IMPORTANT] You have to increment the version number for each subsequent publish
python snapend_create.py $companyId $gameId $byosnapId $version
```

## Tutorial
### Step 1: Understand Code
For this tutorial, we have added an `/mcp` endpoint. The MCP allows LLMs to power a frontend chat experience allowing the user to view, add and update their Todos. `srs/controllers/mcpController.ts` has the code for our Todo app.

### Step 2 Build
- Build your server: You should see a folder called `dist/`
```bash
npm run build
```
- Build your routes and specs
```bash
./generate_routes.sh
npx tsoa spec
```

### Step 3: Publish the BYOSnap
Run the following command to publish your BYOSnap to your Snapser account.
```
snapctl byosnap publish --byosnap-id byosnap-mcp --version "v1.0.0" --path $pathToThisFolder --resources-path $pathToThisFolder/snapser-resources/
```

IMPORTANT: Please name your byosnap `byosnap-mcp`

### Step 4: Create your cluster
#### Automated Setup
- Run `python snapend_create.py $companyId $gameId $byosnapId $byosnapVersion` which first updates your `snapser-resources/snapser-snapend-manifest.json` file and then deploys it to Snapser via Snapctl.
- Your custom snapend should be up in about 2-4 minutes.

**IMPORTANT**: This script is NOT idempotent. It just creates a backend on Snapser. If you run this script again, you will get an error that you already have a backend with the same name on Snapser.

#### Manual Setup
- Go to your Game on the Web portal.
- Click on **Create a Snapend**.
- Give your Snapend a name and hit Continue.
- Pick **Authentication**, **Storage** and this **BYOSnap**.
- Now keep hitting **Continue** till you reach the Review stage and then click **Snap it**.
- Your custom cluster should be up in about 2-4 minutes.
- Now, go into your Snapend and then click on the **Snapend Configuration**.
- Click on the Storage Snap and then click on the **Blobs** tool.
- Add a blob called `todos` - `type: blob, accessScope: external and accessType: protected`
- There click **Save**.

At the end, you will have a new Snapend running with an Auth, Storage & your BYOSnap and you will get a **$snapendId**. Keep a note of your `snapendId` as you will need this for the next stage. It should be noted that every subsequent `byosnap publish` will need to have a higher version number.

### Step 5: Testing
- Go to the Snapend API explorer, which you can find under **Quick Links** on the Snapend Home page.
- Select the `User` tab in the top section of the Left navigation.
- Select the BYOSnap API, add the payload and click `Post`.
- Example payloads:
    - List your todos
      ```json
      {
        "id": "0",
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
          "name": "list_todos"
        }
      }
      ```
    - Add a todo
      ```json
      {
        "id": "0",
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
          "name": "add_todo",
          "arguments": { "title": "Test todo"}
        }
      }
      ```
    - Complete a todo
      ```json
      {
        "id": "0",
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
          "name": "add_todo",
          "arguments": { "id": "$todoId"}
        }
      }
      ```

## Development Process
### Pre-requisites - Read the Gotchas
- Please read the GOTCHAS.md before you begin Development

### A. Running the Server Locally
```bash
npm run build
```
- Build your routes and specs
```bash
./generate_routes.sh
npx tsoa spec
```
- Run the server locally
```bash
node dist/server.js
```

### B. Actively Coding
If you want to rapidly test your BYOSnap changes on an already deployed BYOSnap you can use the `snapctl byows` command. Please look at the Snapctl documentation to understand the byows command.

### C. Committing your BYOSnap
Once you are happy with the state of your BYOSnap and you want to "commit" it. Which essentially means you are ready to bump the version number.

1. Generate a new swagger if you need to by running `./generate-swagger.sh`.
2. Run `snapctl byosnap publish --byosnap-id byosnap-$byosnapName --version $newVersion --path $rootCodePath --resources-path $rootCodePath/snapser-resources` to publish your new BYOSnap version to Snapser. IMPORTANT: Make sure your new version is greater than the version that is presently on Snapser. Example: If you previously published a version `v1.0.0` your next one should be `v1.0.1` or higher.
3. Any new or existing Snapend can now just update to this new version of your BYOSnap. There is a handy command `snapctl snapend update byosnaps ...` that allows you to "Commit" your changes to any existing BYOSnap using the CLI. You can always do this using the web app as well by clicking on `Edit Snapend`.
