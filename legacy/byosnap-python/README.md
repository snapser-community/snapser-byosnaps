# BYOSnap Python Example

This folder has a Flask microservice written in Python with a couple restful endpoints. This BYOSnap
can be added to any Snapend you build on Snapser.

## Requirement
### Snapctl
Make sure you have the [Snapctl](https://pypi.org/project/snapctl/) installed.

## Important Files
1. **snapser-byosnap-profile.json**: This file holds the details of your BYOSnap. This file is required for the next step **Publish the BYOSnap**.
2. **snapser-snapend-manifest.json**: This is the Infrastructure as Code file that holds the details of the cluster which includes the architecture and the configuration. This is required for the **Setup** phase.

## Setup
### 1. Publish the BYOSnap
Run the following command to publish your BYOSnap to your Snapser account.
```
snapctl byosnap publish byosnap-python --version "v1.0.0" --path $pathToThisFolder
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
- Pick **Authentication** and **BYOSnap Python** snaps
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
