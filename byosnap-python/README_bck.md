# Snapser - Custom Code Example - Python

A very simple microservice written in python, that can be added to your Snapser infrastructure.

## Tool Location
1. To start creating the BYOSnap you need to go to the **Snaps** tool and then select **Private Snaps**.
2. You will then see an option to **Add Custom Code**.
3. This will take you to the tool for adding your BYOSnap.

## Configuration

### Step 1 - Create a BYOSnap
1. You will be asked to enter an ID for your BYOSnap. The UI will have **byosnap-** prefix already in the form, so please
enter **jinks-flask**
2. Give your BYOSnap a name, description, pick your platform and select the language **python** for your BYOSnap.

### Step 2a - Publish your BYOSNap image
1. You will need to download the Snapser CLI tool for this and have docker running locally.
2. You will then use the CLI tool to upload this code to your own private snap marketplace.
```
snapctl byosnap publish-image byosnap-jinks-flask --tag "v0.0.1" --path <path_to_root_of_this_repo>
```
3. Once your code is uploaded go back to the web browser to move to Step 2b.

### Step 2b - Publish your Snap
1. Now that the code image has been uploaded, we want to publish this custom private snap.
2. For this, select the tag from the Select tag drop down. If you were following these instructions the tag should be **v0.0.1**.
3. Next pick **v1** as the prefix and then add dev, staging and prod settings for your BYOSnap. You will
at least need to setup one of the three. We recommend you to add the dev settings to start.
4. Here you will select, CPU, Memory, which you can keep as defaults. Additionally, select **5003** as the Port and hit Publish.

## Create a Snapend
1. Create a snapend with Auth
2. In the Auth snap enable anon login

## Use
Go to the Snapend API explorer to play around with the APIs
