# BYOSnap Python Basic Tutorial

## Application
- The main application logic is in **app.py**
- This example is built using Flask and is served via gunicorn

## Pre-Requisites

### A. Python Virtual Environment
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

### B. Snapctl Setup
You need to have a valid setup for Snapctl, which is Snapsers CLI tool. Please follow the step by step (tutorial)[https://snapser.com/docs/guides/tutorials/setup-snapctl] if you do not have Snapctl installed on your machine. You can run the following command to confirm you have a valid snapctl setup.

```bash
# Validate if your snapctl setup is correct
snapctl validate
```

### C. Docker
Make sure Docker engine is running on your machine. Open up Docker desktop and settings. Also, please make sure the setting **Use containerd for pulling and storing images** is **disabled**. You can find this setting in the Docker Desktop settings.

## Resources
All the files that are required by the Snapctl are under this folder
- **Dockerfile**: BYOSnap needs a Dockerfile. Snapser uses this file to containerize your application and deploy it.
- **snapser-byosnap-profile.json**: You can use this file to tell Snapser about your BYOSnaps hardware, networking and configuration requirements.
- **swagger.json**: (Recommended but optional) If you have a valid Swagger 3.X file with your BYOSnap, Snapser also
  generates a SDK for your code and enables this BYOSnap to be usable in its API Explorer.
- **README.md**: (Optional) Optionally you can add a Readme for your devs. This file will be rendered on the Snapser web app.


## Helper Scripts
- **generate_swagger.py**: Script that generates a swagger.json based on the method annotations in app.py. This script stores the swagger.json under the `snapser-resources/` folder.

Usage
```bash
python generate_swagger.py
```

- **snapend_create.py**: Script to create a new Snapend with an Auth snap and your BYOSnap. You will need your companyId and gameId, which you can retrieve from the Snapser web app.
Usage
```bash
# $companyId = Your company Id
# $gameId = Your game ID
# $byosnapId is the ID of your BYOSnap. For the tutorial, we are using `byosnap-basic`
# $version needs to be in the format "vX.Y.Z" eg: "v1.0.0"
#   [IMPORTANT] You have to increment the version number for each subsequent publish
python snapend_create.py $companyId $gameId $byosnapId $version
```

## Tutorial
### Step 0: Read the Gotchas
- Please read the GOTCHAS.md before you begin Development

### Step 1: Update Code
For this tutorial, we want to update `api_four` return message, deploy it to Snapser and see it live. Please go to `api.py` and search for `api_four` and update the return message.

### Step 2 Build
- Build your swagger
```bash
python generate_swagger.py
```
- Build your server
```bash
./run_dev_server.sh
```

### Step 3: Publish the BYOSnap
Run the following command to publish your BYOSnap to your Snapser account.
```
snapctl byosnap publish byosnap-basic --version "v1.0.0" --path $pathToThisFolder --resources-path $pathToThisFolder/snapser-resources/
```

### Step 4: Create your cluster
#### Automated Setup
- Run `python snapend_create.py $companyId $gameId $byosnapId $byosnapVersion` which first updates your `snapser-resources/snapser-snapend-manifest.json` file and then deploys it to Snapser via Snapctl.
- Your custom snapend should be up in about 2-4 minutes.

#### Manual Setup
- Go to your Game on the Web portal.
- Click on **Create a Snapend**.
- Give your Snapend a name and hit Continue.
- Pick **Authentication** and this **BYOSnap**.
- Now keep hitting **Continue** till you reach the Review stage and then click **Snap it**.
- Your custom cluster should be up in about 2-4 minutes.
- Now, go into your Snapend and then click on the **Snapend Configuration**.
- Click on the Authentication Snap and then click on the **Connector** tool.
- There select **Anon** and hit Save.

At the end, you will have a new Snapend running with an Auth Snap & your BYOSnap and you will get a **$snapendId**. Keep a note of your `snapendId` as you will need this for the next stage. It should be noted that every subsequent `byosnap publish` will need to have a higher version number.

### Step 5: Testing
- Go to the Snapend API explorer, which you can find under **Quick Links** on the Snapend Home page.
- Use the Authentication.AnonLogin to create a test user.
- The API Explorer History button will show you details of the created users Id and session token.
- Then you can go to the BYOSnap API, add the users session token, and access the BYOSnap endpoint `API Four` to see your updated message.

## Development Process
### Pre-requisites - Read the Gotchas
- Please read the GOTCHAS.md before you begin Development

### A. Running the Server Locally
- Build your swagger
```bash
python generate_swagger.py
```
- Build your server
```bash
./run_dev_server.sh
```

### B. Actively Coding
If you want to rapidly test your BYOSnap changes on an already deployed BYOSnap you can use the `snapctl byosnap sync` command. Note: The sync command only works if your BYOSnap was deployed to a Snapend. If you have followed this tutorial, you will need the $snapendId of the deployed Snapend to use this command along with the `$version` that you had deployed the BYOSnap with.

1. Update your code.
2. Generate a new swagger if you need to by running `python generate_swagger.py`.
3. Run `snapctl byosnap sync --snapend-id $snapendId --byosnap-id $byosnapId --version $version --path $rootCodePath --resources-path $rootCodePath/snapser-resources` to sync your new BYOSnap to Snapser. Sync essentially is taking your local code and making it live on your Snapend.

IMPORTANT: The Sync command reuses the published `$version` tag but keeps building and updating the remote image. This is how your Snapend can quickly download and run your latest code.

### C. Committing your BYOSnap
Once you are happy with the state of your BYOSnap and you want to "commit" it. Which essentially means you are ready to bump the version number.

1. Generate a new swagger if you need to by running `python generate_swagger.py`.
2. Run `snapctl byosnap publish --byosnap-id byosnap-$byosnapName --version $newVersion --path $rootCodePath --resources-path $rootCodePath/snapser-resources` to publish your new BYOSnap version to Snapser. IMPORTANT: Make sure your new version is greater than the version that is presently on Snapser.
3. Any new or existing Snapend can now just use this new version of your BYOSnap. There is a handy command `snapctl snapend update byosnaps ...` that allows you to "Commit" your changes to any existing BYOSnap using the CLI. You can always do this using the web app as well by clicking on `Edit Snapend`.
