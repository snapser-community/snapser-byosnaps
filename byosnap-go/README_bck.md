# Snapser - Custom Code Example - Go

A very simple microservice written in go, that can be added to your Snapser infrastructure.


## Tool Location
1. To start creating the BYOSnap you need to go to the **Snaps** tool and then select **Private Snaps**.
2. You will then see an option to **Add Custom Code**.
3. This will take you to the tool for adding your BYOSnap.

## Configuration

### Step 1 - Create a BYOSnap
1. You will be asked to enter an ID for your BYOSnap. The UI will have **byosnap-** prefix already in the form, so please
enter **postgame**
2. Give your BYOSnap a name, description, pick your platform and select the language **go** for your BYOSnap.

### Step 2a - Publish your BYOSNap image
1. You will need to download the Snapser CLI tool for this and have docker running locally.
2. You will then use the CLI tool to upload this code to your own private snap marketplace.
```
snapctl byosnap publish-image byosnap-postgame --tag "v0.0.1" --path <path_to_root_of_this_repo>
```
3. Once your code is uploaded go back to the web browser to move to Step 2b.

### Step 2b - Publish your Snap
1. Now that the code image has been uploaded, we want to publish this custom private snap.
2. For this, select the tag from the Select tag drop down. If you were following these instructions the tag should be **v0.0.1**.
3. Next pick **v1** as the prefix and then add dev, staging and prod settings for your BYOSnap. You will
at least need to setup one of the three. We recommend you to add the dev settings to start.
4. Here you will select, CPU, Memory, which you can keep as defaults. Additionally, select **8080** as the Port and hit Publish.

## Create a Snapend
1. Create a snapend with Auth, Stats and Inventory and byosnap-postgame Select Custom code from the filter widget and you will see
your private snaps.
2. In the Auth snap enable anon login
3. In the Statistics snap add the following statistics
 - wins - counter
 - losses - counter
4. In the inventory snap create a currency called coins

## Use
Go to the Snapend API explorer to play around with the APIs

## Generating the OpenAPI spec
1. Install swaggo/swag 
```
go get -u github.com/swaggo/swag/cmd/swag
```
2. Generate the swagger 2.0 doc
```
swag init --output ./docs
```
3. Convert to openapi 3.0
Copy the generated swagger.yaml or swagger.json file into [Swagger Editor](https://editor.swagger.io/). 
Click on Edit -> Convert to OpenAPI 3.0
File -> Convert and save as JSON
4. Save this file in the root folder of the byosnap with the name swagger.json