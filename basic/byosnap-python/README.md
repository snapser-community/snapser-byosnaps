# BYOSnap Python Basic Tutorial

## Application
- The main application logic is in **app.py**
- This example is built using Flask and is served via gunicorn

## Pre-Requisites

#### A. Python Virtual Environment
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

#### B. Snapctl Setup
You need to have a valid setup for Snapctl, which is Snapsers CLI tool. Please follow the step by step (tutorial)[https://snapser.com/docs/guides/tutorials/setup-snapctl] if you do not have Snapctl installed on your machine. You can run the following command to confirm you have a valid snapctl setup.

```bash
# Validate if your snapctl setup is correct
snapctl validate
```

#### C. Docker
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
# $version needs to be in the format "vX.Y.Z" eg: "v1.0.0"
#   [IMPORTANT] You have to increment the version number for each subsequent publish
# $snapendId is the ID of your Snapend
python snapend_create.py $companyId $gameId $version
```


## Development Process
### A. Get up and running initially
1. Update your code in app.py
2. Run `python generate_swagger.py` to build a new swagger.
3. Run `snapctl byosnap publish --byosnap-id $byosnapId --version $version --path $rootCodePath --resources-path $rootCodePath/snapser-resources` to publish your new BYOSnap to Snapser. BYOSnap Id
has to start with `byosnap-` Eg: `byosnap-basic`.
4. Run `python create_snapend.py $companyId $gameId $byosnapId $byosnapVersion` which first updates your `snapser-resources/snapser-snapend-manifest.json` file and then deploys it to Snapser via Snapctl.

At the end, you will have a new Snapend running with an Auth Snap & your BYOSnap and you will
get a **$snapendId**. Keep a note of your `snapendId` as you will need this for the next stage.
It should be noted that every subsequent `byosnap publish` will need to have a higher version number.


### B. Development
#### Actively Coding
1. Update your code in app.py
2. Generate a new swagger if you need to by running `python generate_swagger.py`.
3. Run `snapctl byosnap sync --snapend-id $snapendId --byosnap-id $byoSnapId --version $version --path $rootCodePath --resources-path $rootCodePath/snapser-resources` to sync your new BYOSnap to Snapser. Sync essentially is taking your local code and making it live on your Snapend.

#### Commit
1. Once you are happy with the state of your BYOSnap, you can publish it as a new version. This way, other team members can consume it.
2. Run `snapctl byosnap publish --byosnap-id $byoSnapId --version $newVersion --path $rootCodePath --resources-path $rootCodePath/snapser-resources` to publish your new BYOSnap version to Snapser. Make sure your new version is greater than the version that is presently on Snapser.
3. Any new or existing Snapend can now just use this new version of your BYOSnap. There is a handy command `snapctl snapend update byosnaps ...` that allows you to "Commit" your changes to any existing BYOSnap using the CLI. You can always do this using the web app as well.
