# BYOSnap Csharp Basic Tutorial

## Application
- The main application logic is in **UsersController.cs**.
- This example uses Swashbuckle for generating a swagger based on controller annotations.


## Pre-Requisites
### A. Install dotnet and dependencies

#### Install dotnet
If you are on a MAC install dotnet via homebrew
```
brew install --cask dotnet-sdk
```

#### Install the packages
```
dotnet add package Microsoft.AspNetCore.OpenApi
dotnet add package Microsoft.OpenApi
dotnet add package Swashbuckle.AspNetCore
dotnet add package Swashbuckle.AspNetCore.Annotations
```

#### Install the .NET Runtime
You may need to install the [.NET Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

#### B. Python Virtual Environment
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

## Resources
All the files that are required by the Snapctl are under this folder
- **Dockerfile**: BYOSnap needs a Dockerfile. Snapser uses this file to containerize your application and deploy it.
- **snapser-byosnap-profile.json**: You can use this file to tell Snapser about your BYOSnaps hardware, networking and configuration requirements.
- **swagger.json**: (Recommended but optional) If you have a valid Swagger 3.X file with your BYOSnap, Snapser also
  generates a SDK for your code and enables this BYOSnap to be usable in its API Explorer.
- **README.md**: (Optional) Optionally you can add a Readme for your devs. This file will be rendered on the Snapser web app.

## Helper Scripts
- **Generate Swagger**: A way for you to generate a swagger file based on annotations. This script stores the swagger.json under the `snapser-resources/` folder.

Usage
```bash
dotnet run generate-swagger
```

- **snapend_create.py**: Script to create a new Snapend with an Auth snap and your BYOSnap. You will need your companyId and gameId, which you can retrieve from the Snapser web app.
Usage
```bash
# $version needs to be in the format "vX.Y.Z" eg: "v1.0.0"
#   [IMPORTANT] You have to increment the version number for each subsequent publish
# $snapendId is the ID of your Snapend
python snapend_create.py $companyId $gameId $version
```

## Development Process
### A. Get up and running initially
1. Update your code in UsersContoller.cs
2. Run `dotnet run generate-swagger` to build a new swagger.
3. Run `snapctl byosnap publish --byosnap-id $byosnapId --version $version --path $rootCodePath --resources-path $rootCodePath/snapser-resources` to publish your new BYOSnap to Snapser. BYOSnap Id
has to start with `byosnap-` Eg: `byosnap-basic`.
4. Run `python create_snapend.py $companyId $gameId $byosnapId $byosnapVersion` which first updates your `snapser-resources/snapser-snapend-manifest.json` file and then deploys it to Snapser via Snapctl.

At the end, you will have a new Snapend running with an Auth Snap & your BYOSnap and you will
get a **$snapendId**. Keep a note of your `snapendId` as you will need this for the next stage.
It should be noted that every subsequent `byosnap publish` will need to have a higher version number.


### B. Development
#### Actively Coding
1. Update your code in UsersContoller.cs
2. Generate a new swagger if you need to by running `dotnet run generate-swagger`.
3. Run `snapctl byosnap sync --snapend-id $snapendId --byosnap-id $byosnapId --version $version --path $rootCodePath --resources-path $rootCodePath/snapser-resources` to sync your new BYOSnap to Snapser. Sync essentially is taking your local code and making it live on your Snapend.

#### Commit
1. Once you are happy with the state of your BYOSnap, you can publish it as a new version. This way, other team members can consume it.
2. Run `snapctl byosnap publish --byosnap-id byosnap-$byosnapName --version $newVersion --path $rootCodePath --resources-path $rootCodePath/snapser-resources` to publish your new BYOSnap version to Snapser. Make sure your new version is greater than the version that is presently on Snapser.
3. Any new or existing Snapend can now just use this new version of your BYOSnap. There is a handy command `snapctl snapend update byosnaps ...` that allows you to "Commit" your changes to any existing BYOSnap using the CLI. You can always do this using the web app as well.


## Setup
### 1. Publish the BYOSnap
Run the following command to publish your BYOSnap to your Snapser account.
```
snapctl byosnap publish byosnap-csharp --version "v1.0.0" --path $pathToThisFolder
```

### 2. Create your cluster
#### Automated Setup
Snapser supports infrastructure as code. In this folder you will find a file called `snapser-snapend-manifest.json`. You can use this file to directly create your cluster on Snapser.
- Go to your Game on the Web portal.
- Click on **Create a Snapend**.
- Give your Snapend a name and hit Continue.
- Click on the Blue button icon and pick **Import**.
- There select the `snapser-snapend-manifest.json` from this folder and hit **Import**.
- Next, search for your BYOSnap and add that in.
- Now keep hitting **Continue** till you reach the Review stage and then click **Snap it**.
- Your custom cluster should be up in about 2-4 minutes.

#### Manual Setup
- Go to your Game on the Web portal.
- Click on **Create a Snapend**.
- Give your Snapend a name and hit Continue.
- Pick **Authentication** and **BYOSnap Csharp** snaps
- Now keep hitting **Continue** till you reach the Review stage and then click **Snap it**.
- Your custom cluster should be up in about 2-4 minutes.
- Now, go into your Snapend and then click on the **Snapend Configuration**.
- Click on the Authentication Snap and then click on the **Connector** tool.
- There select **Anon** and hit Save.

## Testing
- Go to the Snapend API explorer, which you can find under **Quick Links** on the Snapend Home page.
- Use the Authentication.AnonLogin to create a test user.
- The API Explorer History button will show you details of the created users Id and session token.
- Then you can go to the BYOSnap API, add the users session token, and access the BYOSnap endpoint.
