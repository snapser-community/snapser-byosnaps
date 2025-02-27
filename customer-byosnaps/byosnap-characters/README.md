# BYOSnap Characters

BYOSnap created to support characters in game. This BYOSnap creates a character map,
containing an ID and a Session token for each character, allowing game studios to start
storing information into the Snaps for each character.

## Requirement
### Snapctl
Make sure you have the [Snapctl](https://pypi.org/project/snapctl/) installed.

## Important Files
1. **snapser-byosnap-profile.json**: This file holds the details of your BYOSnap. This file is required for the next step **Publish the BYOSnap**.
2. **snapser-snapend-manifest.json**: This is the Infrastructure as Code file that holds the details of the cluster which includes the architecture and the configuration. This is required for the **Setup** phase.
3. **snapser-tool-characters.json**: This is the tools file. Snapser allows game studios, to
build custom tools for their BYOSnaps using the **BYOSnap Tool Builder**. That tool, outputs
this file which allows the Snapser web portal to render your custom tool, under the
Snapend BYOSnap Configuration tools page.

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
- Pick **Authentication**, **Storage** and **BYOSnap Characters** snaps
- Now keep hitting **Continue** till you reach the Review stage and then click **Snap it**.
- Your custom cluster should be up in about 2-4 minutes.
- Now, go into your Snapend and then click on the **Snapend Configuration**.
- Click on the Authentication Snap and then click on the **Connector** tool. There select **Anon** and hit Save.
- Now, go into the Storage snaps configuration tool and add two blobs: **characters** and
  **character_settings** and select type=blob, access=private and scope=internal.
- Now, go into the BYOSnaps configuration tool. In this tool, you can add a comma separated
  ids of your characters. eg: **ember,wade,bernice** and hit Save.

## Testing
- Go to the Snapend API explorer, which you can find under **Quick Links** on the Snapend Home page.
- Use the Authentication.AnonLogin to create a test user.
- The API Explorer History button will show you details of the created users Id and session token.
- Then you can go to the BYOSnap API, add the users session token, and access the BYOSnap endpoint to Get characters and Activate characters.
