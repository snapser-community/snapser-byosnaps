import { DocsButton } from '../../../../components/docs/DocsButton.tsx'

export const meta = {
  author: 'AJ Apte',
}

# Bring your own Snap - Advanced

BYOSnap is a Snapser feature that enables you to integrate your own custom code. BYOSnaps run in containers within Snapser's Kubernetes platform and can be written in any programming language to cater to your game's specific needs. Once deployed, a BYOSnap resides within the same Kubernetes cluster as your other Snaps, facilitating seamless integration with the broader Snapser ecosystem.

## Introduction
This guide will walk you through the process of integrating the BYOSnap with the various Snapser hooks. As part of this, you will learn how to create custom configuration tools for your BYOSnap, leverage the Snapend sync and clone features, and utilize the User data reset and delete hooks.

For this tutorial, lets assume a hypothetical game called **Snapser Battle Royale**. The game releases new characters, and the client needs an API to fetch if a character is available or not.

We are going to use this example to demonstrate how to use the Snapser hooks subsystem. At a high level:
1. We will build a BYOSnap configuration tool using the builder tool to render our custom UI that stores the available characters in **Snapser Battle Royale**.
1. Next, we will add endpoints to our BYOSnap code that allows the configuration tool to show and update the available character data.
3. Next, if other developers join our studio, they should be able to get their own backend that is a clone of our backend, including the configuration data. We will do this by using the Snapend sync and clone hooks.
4. Finally, we will add a method to support the User data reset and delete hooks. This means if say a customer service agent or a game developer wanted to reset or delete a user data, they can do so by using the Snapend user data reset tool. Which will call our BYOSnap and we will be able to reset or delete the user data from our BYOSnap.

## Step 0: Pre-requisites
Before you begin, ensure you have access to the Snapser CLI tool and you have gone through the BYOSnap Basic tutorial. This will help you understand the basic concepts of BYOSnap.


<div className="parent">
  <div className="tutorialBox">
    # Setup Snapser CLI

    You can go through the Setup Snapser CLI tutorial to install and configure Snapctl.

    <div>
      <DocsButton href={'/docs/guides/tutorials/setup-snapctl'} variant="contained" color="info" size="small" sx={{ml: 2, mb: 1}}>Tutorial</DocsButton>
    </div>
  </div>
  <div className="servicesBox">
    # BYOSnap Basic
    Please make sure you have a basic understanding of the BYOSnap concept and have gone through the BYOSnap Basic tutorial. Its not required for you to actually deploy the BYOSnap as we will be doing that in this tutorial. But it is highly recommended to go through the tutorial to understand the concepts.

    <div>
      <DocsButton href={'/docs/guides/tutorials/byosnap-basic'} variant="contained" color="info" size="small" sx={{ml: 2, mb: 1}}>Tutorial</DocsButton>
    </div>
  </div>
</div>
<div className="parent">
  <div className="tutorialBox">
    # BYOSnap Intermediate

    Please make sure you have gone through the BYOSnap Intermediate tutorial. This will help you understand how to use the Snapser internal SDK and how to debug your BYOSnap code locally.

    <div>
      <DocsButton href={'/docs/guides/tutorials/byosnap-inter'} variant="contained" color="info" size="small" sx={{ml: 2, mb: 1}}>Tutorial</DocsButton>
    </div>
  </div>
</div>

<Checkpoint step={0}>
  You are now ready to begin the tutorial.
</Checkpoint>

## Step 1: Create a Snapend
We start by creating a Snapend with the **Auth** and **Storage** Snaps. We are going to then download the **Internal SDK** and use it in our BYOSnap. We are going to leverage the Storage snap to store the configuration data for our BYOSnap viz. the list of **available characters** in our game. The **Auth** Snap will be used to authenticate the user and get the user token.

### A. Create a Snapend
1. On your games home page click on the **+ Snapend** button.
   <Note>
    If you have not added a game yet, please add a game first and then go to the games home page.
   </Note>
1. Give your Snapend a name and click continue.
1. Select the **Auth** and **Storage** Snaps from the list of available Snaps and then keep clicking Continue until you reach the **Review** step and finally click on the **Snap it** button.
1. A pop-up window will show the progress of creating your cluster. Your Snapend should be ready in a few moments.
![Snapend Creation](/images/docs/tutorials/byosnap-advanced-snapend-create.png)

### B. Configure your Snaps
1. Once your Snapend is ready, click on the **Configuration Tool** button on the Snapend home page.
1. This will take you to the Configuration tool page where we want to configure the **Auth** and **Storage** Snaps.
1. First, lets click on the **Auth** Snap from the navigation bar on the left and select the **Connectors** tool.
1. Here we want to enable the **Anonymous Auth**. Click on Add Connectors and select Anonymous. Click Save on the form to enable the connector.
![Auth Connector](/images/docs/tutorials/snapend-create-admin-auth-anon.png)
1. Now, click on the Back button to go back to the Configuration tool home page. Now click on the **Storage** Snap from the navigation bar on the left and select the **Blob Keys** tool.
1. Here click on **+ Blob Key** and add the following and then click **Save**:
    - **Blob Keys**: character_settings
    - **Category Type**: blob
    - **Access Type**: private
    - **Access Scope**: internal
    <Note>
      This setup tells Storage that we want a private blob that can only be accessed internally within a Snapend.
    </Note>

![Profile Attribute](/images/docs/tutorials/byosnap-advanced-storage-key.png)

<Checkpoint step={1}>
  You now have a Snapend that has Anonymous Auth enabled and a custom blob key created in the Storage snap. We are now going to download the Internal SDK and use it in our BYOSnap.
</Checkpoint>

## Step 2: Download the Internal SDK

1. Go to the Snapend home page and scroll to the bottom.
1. Here you will see the **Standard Language SDK** widget. Pick the language you are most comfortable with, select **Internal** for the SDK type, Select the **HTTP Library** you like and then click on the **Generate** button.
![Profile Attribute](/images/docs/tutorials/byosnap-advanced-internal-sdk.png)
1. This will generate a custom internal SDK for our Snapend and soon you will see a zip file containing the SDK for the selected language. Unzip the file.
1. The folder structure is different for different languages. Check out the instructions below for Python.
<CollapsableDoc title="Python SDK Structure">
```bash
├── requirements.txt
├── snapser_internal/
│   └── __init__.py
│   └── api/
│   └── api_client.py
│   └── api_responses.py
│   └── ...
│   └── models/
```
</CollapsableDoc>

<Checkpoint step={2}>
  You now have an internal SDK that you can integrate into your BYOSnap. This SDK will allow you to communicate with the other Snaps in your Snapend.
</Checkpoint>

## Step 3: Integrate the Internal SDK
### A. Check out the example code
We currently have the advanced example only in Python. Check out the snapser-community BYOSnap [repo](https://github.com/snapser-community/snapser-byosnaps/tree/main/advanced).
  - [Python](https://github.com/snapser-community/snapser-byosnaps/tree/main/advanced/byosnap-python)

```bash
# For HTTPS based cloning
git clone https://github.com/snapser-community/snapser-byosnaps.git
# For SSH based cloning
git@github.com:snapser-community/snapser-byosnaps.git
```

- In the repo, there is a folder called **advanced/**. Inside this folder, you will find the BYOSnap example code for Python. The folder structure is as follows:
  ```bash
  ├── advanced/
  │   └── byosnap-python/
  ```
  <Note>
  Each language folder contains a subfolder named **snapser-resources/**. Snapser utilizes this folder to access essential resources such as swagger.json, README.md, and BYOSnap profile files. To keep your root directory clean, these files are stored separately.
  </Note>

- Here is how a typical BYOSnap folder structure looks like:

  ```bash
  ├── advanced/
    │   └── byosnap-python/
    │       └── snapser-resources/
    │           ├── .env (👈 Automated Tutorial: Used by snapend_create.py )
    │           ├── README.md (👈 Powers the README of your BYOSNap on the Snapser Web portal )
    │           ├── snapser-base-snapend-manifest.json (👈 Automated Tutorial: Used by snapend_create.py )
    │           ├── snapser-byosnap-profile.json (👈 This powers the hardware and software settings for your BYOSnap )
    │           └── snapser-tool-characters.json (👈 This JSON powers the rendering of the BYOSnap Configuration tool )
    │           └── swagger.json (👈 This powers the SDK and API Explorer. Use the generate_swagger.* script to generate this file )
    │       └── Dockerfile (👈 Used by snapctl to deploy your BYOSnap )
    │       └── GOTCHAS.md (👈 A file you should read to understand the nuances per language )
    │       └── generate_routes.sh (👈 Only present in byosnap-node-ts/ )
    │       └── generate_swagger.sh|py (👈 Script to generate the swagger )
    │       └── README.md (👈 Developer Docs for you to run BYOSnap outside Snapser )
  ```

### B. Copy the Internal SDK Contents
Copy the contents of the Internal SDK to the root of your BYOSnap code directory. Please check out the instructions for each language below. Doing this, will allow you to use the Internal SDK in your BYOSnap.
<CollapsableDoc title="Python Instructions">
For Python, you need to copy the **snapser_internal** folder from the unzipped folder into your BYOSnap code directory. The folder structure should look like this:
```bash
├── requirements.txt
├── snapser_internal/ # 👈 This is the folder you want to copy
│   └── __init__.py
│   └── api/
│   └── api_client.py
│   └── api_responses.py
│   └── ...
│   └── models/
```
</CollapsableDoc>

### C. Add dependencies
Each language has its own set of dependencies that you need to add to your BYOSnap code. Check out the instructions below for Python.
<CollapsableDoc title="Python Dependencies">
- Add the following to your main code's **requirements.txt** file:
```text
python_dateutil >= 2.5.3
setuptools >= 21.0.0
urllib3 >= 1.25.3, < 2.1.0
pydantic >= 1.10.5, < 2
aenum >= 3.1.11
```
<Note>
  You may already have these dependencies in your requirements.txt file. If so, you can skip this step. Just make sure the versions are compatible with the SDK.
</Note>

Then run the following command to install the dependencies:
```bash
pip install -r requirements.txt
```

</CollapsableDoc>

<Checkpoint step={3}>
  With our SDK in and our code compiling / working, we are now ready to update the code for our BYOSnap.
</Checkpoint>


## Step 4: Build UI for BYOSnap Configuration Tool
Now, we want to build a custom configuration tool for our BYOSnap. This tool will allow us to configure the available characters in our game. We will use the **Configuration Builder** tool to create this tool.

### A. Create the Configuration Tool
1. Go to the Snapend home page and click on the **Configuration Builder** under the **BYOSnaps** navigation.
    ![Configuration Builder](/images/docs/tutorials/byosnap-advanced-config-builder.png)
    <Note>
      This tool allows you to create a custom UI for your BYOSnap. This UI will get rendered in the Configuration tool of your Snapend once you deploy your BYOSnap.
    </Note>
1. Add **characters** as the ID of the tool, select **Single** environment and read the callout next to the payload.
    ![Configuration Builder](/images/docs/tutorials/byosnap-advanced-config-tool-start.png)
    <Note>
      The idea here is that, the builder tool generates the JSON that powers the UI. But it also comes up with a payload that you are expected to return from your BYOSnap. This payload is then used to render the data in the Configuration tool.
    </Note>
1. Scroll down to the **Main** section and add the following:
    - **Title**: Available Characters
    - **Description**: List of available in-game characters
    - Then click on **+ Add** to add a section.
    ![Configuration Builder](/images/docs/tutorials/byosnap-advanced-config-tool-title.png)
1. In the **Section** section, add the following:
    - **Id**: registration
    - **Title**: Registration
    - **Subtitle**: ""
    - **Help Text**: These are the characters that are available to the user
    - Then click on **Add** to add the section. You should now see it rendered on the left hand side.
    ![Configuration Builder](/images/docs/tutorials/byosnap-advanced-config-tool-section.png)
1. Now, select the section we just added in the **Select section** selector and click on **+ Textarea**,
    ![Configuration Builder](/images/docs/tutorials/byosnap-advanced-config-tool-section-ta.png)
1. Then add the following:
    - **Id**: characters
    - **Label**: Character Ids
    - **Placeholder**: Please enter comma separated character Ids
    - **Required**: Checked
    - Then click on **Save** to add the text area.
    ![Configuration Builder](/images/docs/tutorials/byosnap-advanced-config-tool-section-ta-details.png)
1. Now, scroll back up and you will see a final render of how your tool is going to look like. Also, copy the payload that your BYOSnap is expected to return. **IMPORTANT**: It is this payload more than the tool.json that our actual BYOSnap code has to deal with.
    ![Configuration Builder](/images/docs/tutorials/byosnap-advanced-config-tool.png)
    <Note>
      Most part of the payload will be static. But the value field is where the actual tool will store the value. When the user clicks Save on the actual tool, this entire payload is sent to your BYOSnap so that we can store it in the Storage snap.
      We are also expected to return this payload when the user loads the tool, so the UI can be pre-populated with the data.
    </Note>
```json
{
  "version": "v1.0.0",
  "id": "characters",
  "endpoint": "",
  "category": "flat_form",
  "env_support": "single",
  "sections": [
    {
      "id": "registration",
      "components": [
        {
          "id": "characters",
          "type": "textarea",
          "value": "" 👈 This is where the actual tool will store the value
        }
      ]
    }
  ]
}
```

### B. Store the Configuration Tool JSON
Finally, click the **Download Tool JSON** button to download the JSON file named **snapser-tool-characters.json**. Notice the word **characters** which is part of the filename. This comes from the main tool ID you added in the first step.

IMPORTANT: This file should be stored in **snapser_resources/** folder or your BYOSnap code directory. The snapctl publish and sync commands will smartly pick this up and deploy it to your Snapend.

<Note>
  A question may come to your mind, what happens if there are multiple tools. You are expected to give a different tool ID during the Configuration tool creation. That way you will have multiple tool JSONs like snapser-tool-idOne.json, snapser-tool-idTwo.json etc. and you can store them in the **snapser_resources/** folder. Snapctl will pick all the files that match the pattern **snapser-tool-*.json** and deploy them to your Snapend.
</Note>

<Checkpoint step={4}>
  You have now created a custom configuration tool for your BYOSnap. This tool will be used to store the available characters in your game. We are now going to update the code for our BYOSnap to use this tool.
</Checkpoint>

## Step 5: Understand the BYOSnap Code
Lets now understand the code that integrates with the three main Snapser hooks:

### A. Configuration Tool Hooks
For the configuration tool to function you need two methods. A getter that sends the caller the configuration tool JSON payload and a setter that saves the configuration tool payload to some storage. We are using the storage Snap **character_settings** blob key that we added in `Step 1 > Configure your Snaps` to store the configuration tool JSON.

Snapser expects you to implement the following two endpoints in your BYOSnap code:
<CollapsableDoc title="View Configuration">
- `Method`: **GET**
- `Endpoint`: **/$byoSnapPrefix/$byosnapId/settings**.
- `Description`: This endpoint is called by the Configuration tool UI to get the configuration tool **payload**. Snapser first uses the **snapser-tool-*.json** file in your BYOSnap code directory to render the Configuration UI. Then the UI, calls this endpoint to get the configuration tool JSON payload. This payload is then used to pre-populate the UI.
- `Response`: This endpoint is expected to return a 200 OK response along with the **configuration tool payload**. If the payload is not found or not valid, the UI will fail to render the tool and show your configuration data.

- `Example`: **GET /v1/byosnap-advanced/settings**
```python
@app.route("/v1/byosnap-advanced/settings", methods=["GET"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def get_settings():
    '''
    Get the settings for the characters microservice
    '''
    # This is coming from the Payload we got in the Configuration tool
    default_settings = {
        "version": "v1.0.0",
        "id": "characters",
        "endpoint": "",
        "category": "flat_form",
        "env_support": "single",
        "sections": [
            {
                "id": "registration",
                "components": [
                    {
                        "id": "characters",
                        "type": "textarea",
                        "value": ""
                    }
                ]
            }
        ]
    }
    configuration = snapser_internal.Configuration()
    with snapser_internal.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = snapser_internal.StorageServiceApi(api_client)
        try:
            # Anonymous Login
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if api_response is None:
                return make_response(jsonify(default_settings), 200)
            return make_response(jsonify(json.loads(api_response.value)), 200)
        except ApiException as e:
            pass
    return make_response(jsonify(default_settings), 200)
```
</CollapsableDoc>
<CollapsableDoc title="Save Configuration">
- `Method`: **PUT**
- `Endpoint`: **/$byoSnapPrefix/$byosnapId/settings**.
- `Description`: This endpoint is called by the Configuration tool to save the configuration tool JSON. This endpoint is called when the user clicks on the **Save** button in the Configuration tool.
- `Response`: This endpoint is expected to return a 200 OK response if the data was saved successfully. If the save was not successful, it should return a 400 Bad Request response with an error message. This message is shown as an **Error Toaster** in the UI.
- `Example`: **PUT /v1/byosnap-advanced/settings**
```python
@app.route("/v1/byosnap-advanced/settings", methods=["PUT"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def update_settings():
    '''
    Update the settings for the characters microservice
    '''
    try:
        blob_data = request.get_json()
        if 'payload' in blob_data:
            blob_data = blob_data['payload']
        character_string = blob_data['sections'][0]['components'][0]['value']
        # Split the characters by comma but also trim the characters
        character_list = character_string.split(',')
        character_list = [character.strip() for character in character_list]
        # Check for duplicates
        if len(character_list) != len(set(character_list)):
            return make_response(jsonify({
                'error_message': 'Duplicate characters found'
            }), 400)
        blob_data['sections'][0]['components'][0]['value'] = ','.join(
            character_list)
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Invalid JSON ' + str(e)
        }), 500)

    configuration = snapser_internal.Configuration()
    with snapser_internal.ApiClient(configuration=configuration) as api_client:
        cas = '12345'
        # Create an instance of the API class
        api_instance = snapser_internal.StorageServiceApi(api_client)
        try:
            # Anonymous Login
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if api_response is not None:
                cas = api_response.cas
        except ApiException:
            # You come here when the doc is not even present
            pass
        try:
            api_response = api_instance.storage_internal_replace_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER'],
                body={
                    "value": json.dumps(blob_data),
                    "ttl": 0,
                    "create": True,
                    "cas": cas
                }
            )
            if api_response is None:
                return make_response(jsonify({
                    'error_message': 'Server Error'
                }), 500)
            return make_response(jsonify(blob_data), 200)
        except ApiException as e:
            return make_response(jsonify({
                'error_message': 'Server Exception: ' + str(e)
            }), 500)
```
</CollapsableDoc>

### B. Snapend Sync and Clone Hooks
The Snapend sync and clone feature allows you to create a new Snapend that is a clone of your existing Snapend. This includes all the Snaps including BYOSnaps and their configuration data. The BYOSnap sync and clone hooks are called when the Snapend is being synced or cloned.

Snapser expects you to implement the following three endpoints:
<CollapsableDoc title="Export Configuration">
- `Method`: **GET**
- `Endpoint`: **/$byoSnapPrefix/$byosnapId/settings/export**.
- `Description`: This endpoint is called when a new Snapend is being cloned and the dev wants to also sync this BYOSnaps configuration data. In our case we are exporting the **character_settings** blob key.
- `Response`: This endpoint is expected to return a 200 OK response with and the exported data needs to have `version`, `exported_at` and `data` keys. The `data` key should contain the configuration data that you want to export.
```json
{
  "version": "v1.0.0",
  "exported_at": 1234567890,
  "data": {} 👈 Any custom data your BYOSnap uses for the configuration
}
```
- `Example`: **GET /v1/byosnap-advanced/settings/export**
```python
@app.route("/v1/byosnap-advanced/settings/export", methods=["GET"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def settings_export():
    """Export Settings
    ---
    get:
      summary: 'Export Settings'
      description: Export Settings
      operationId: Export Settings
      parameters:
      - in: header
        schema: TokenHeaderSchema
      responses:
        200:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
        201:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
    """
    response = {
        "version": os.environ['BYOSNAP_VERSION'], # 👈 Notice Snapser provides an Env var that has your BYOSnap version.
        "exported_at": int(time.time()),
        "data": { # 👈 This can be any object. In our case we are storing the character_settings object
            "character_settings": {
                "version": "v1.0.0",
                "id": "characters",
                "endpoint": "",
                "category": "flat_form",
                "env_support": "single",
                "sections": [
                    {
                        "id": "registration",
                        "components": [
                            {
                                "id": "characters",
                                "type": "textarea",
                                "value": ""
                            }
                        ]
                    }
                ]
            }
        }
    }
    configuration = snapser_internal.Configuration()
    with snapser_internal.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = snapser_internal.StorageServiceApi(api_client)
        try:
            # Storage Settings
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if api_response is None:
                return make_response(jsonify(response), 200)
            response['data']['character_settings'] = json.loads(
                api_response.value)
            return make_response(jsonify(response), 200)
        except ApiException as e:
            pass
    return make_response(jsonify(response), 200)
```
</CollapsableDoc>
<CollapsableDoc title="Import Configuration">
- `Method`: **POST**
- `Endpoint`: **/$byoSnapPrefix/$byosnapId/settings/import**.
- `Description`: This endpoint is called when a cloned Snapend is being created. The data that is sent to this endpoint is the same as the data that is returned from the export endpoint of the parent Snapend. Your new BYOSnap is expected to store this data, thus, ensuring both parent and cloned Snapends have the same configuration data.
- `Response`: This endpoint is expected to return a 200 OK response if the data was imported successfully. If the import was not successful, it should return a 400 Bad Request response with an error message.
- `Example`: **POST /v1/byosnap-advanced/settings/import**
```python
@app.route("/v1/byosnap-advanced/settings/import", methods=["POST"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def settings_import():
    """Import Settings
    ---
    post:
      summary: 'Import Settings'
      description: Import Settings
      operationId: Import Settings
      parameters:
      - in: header
        schema: TokenHeaderSchema
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    character_settings:
                      type: object
                      properties:
                        version:
                          type: string
                        id:
                          type: string
                        endpoint:
                          type: string
                        category:
                          type: string
                        env_support:
                          type: string
                        sections:
                          type: array
                          items:
                            type: object
                            properties:
                              id:
                                type: string
                              components:
                                type: array
                                items:
                                  type: object
                                  properties:
                                    id:
                                      type: string
                                    type:
                                      type: string
                                    value:
                                      type: string
      responses:
        200:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
        201:
          content:
            application/json:
              schema: CharactersResponseSchema
          description: 'Characters retrieved successfully'
    """
    try:
        settings_data = request.get_json()
        if not settings_data or 'data' not in settings_data:
            return make_response(jsonify({
                'error_message': 'Invalid JSON'
            }), 500)
        settings = settings_data['data']['character_settings']
        # Split the characters by comma but also trim the characters
        character_list = settings['sections'][0]['components'][0]['value'].split(
            ',')
        character_list = [character.strip() for character in character_list]
        # Check for duplicates
        if len(character_list) != len(set(character_list)):
            return make_response(jsonify({
                'error_message': 'Duplicate characters found'
            }), 400)
        # Save the characters to the storage
        configuration = snapser_internal.Configuration()
        with snapser_internal.ApiClient(configuration=configuration) as api_client:
            cas = '12345'
            # Create an instance of the API class
            api_instance = snapser_internal.StorageServiceApi(api_client)
            try:
                # Get Storage CAS
                api_response = api_instance.storage_internal_get_blob(
                    access_type='private',
                    blob_key='character_settings',
                    owner_id='byosnap_characters',
                    gateway=os.environ['SNAPEND_INTERNAL_HEADER']
                )
                if api_response is not None:
                    cas = api_response.cas
            except ApiException:
                # You come here when the doc is not even present
                pass
            try:
                api_response = api_instance.storage_internal_replace_blob(
                    access_type='private',
                    blob_key='character_settings',
                    owner_id='byosnap_characters',
                    gateway=os.environ['SNAPEND_INTERNAL_HEADER'],
                    body={
                        "value": json.dumps(settings),
                        "ttl": 0,
                        "create": True,
                        "cas": cas
                    }
                )
                if api_response is None:
                    return make_response(jsonify({
                        'error_message': 'Server Error'
                    }), 500)
                return make_response(jsonify(settings), 200)
            except ApiException as e:
                return make_response(jsonify({
                    'error_message': 'Server Exception: ' + str(e)
                }), 500)
    except Exception as e:
        return make_response(jsonify({
            'error_message': 'Server Exception' + str(e)
        }), 500)
```
</CollapsableDoc>
<CollapsableDoc title="Validate Configuration for Import">
- `Method`: **POST**
- `Endpoint`: **/$byoSnapPrefix/$byosnapId/settings/validate-import**.
- `Description`: This endpoint is called by the sync validator widget, which lets a user know if this Snapend is ready to import and export data or not. This endpoint is also called when the user clicks on the **Validate** button in the sync and clone tool. Whether to accept or reject an import export is entirely up to you. In our case we are checking if the characters are unique and if yes we are accepting the import export. If not we are rejecting it.
- `Response`: This endpoint is expected to return a 200 OK response if the data passes the validation. If it does not pass the validation, it should return a 400 Bad Request response with an error message.
- `Example`: **POST /v1/byosnap-advanced/settings/validate-import**
```python
@app.route("/v1/byosnap-advanced/settings/validate-import", methods=["POST"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def validate_settings():
    '''
    Validate Settings
    '''
    settings_data = request.get_json()
    if 'data' not in settings_data:
        return make_response(jsonify({
            'error_message': 'Invalid JSON'
        }), 500)
    settings = settings_data['data']['character_settings']
    # Split the characters by comma but also trim the characters
    character_list = settings['sections'][0]['components'][0]['value'].split(
        ',')
    character_list = [character.strip() for character in character_list]
    # Check for duplicates
    if len(character_list) != len(set(character_list)):
        return make_response(jsonify({
            'error_message': 'Duplicate characters found'
        }), 400)
    response = {
        'version': os.environ['BYOSNAP_VERSION'],
        'exported_at': int(time.time()),
        'data': {'character_settings':
                 # This part is generated by the BYOSnap Tool builder. We are storing it as is into storage
                 {
                     "version": "v1.0.0",
                     "id": "characters",
                     "endpoint": "",
                     "category": "flat_form",
                     "env_support": "single",
                     "sections": [
                         {
                             "id": "registration",
                             "components": [
                                 {
                                     "id": "characters",
                                     "type": "textarea",
                                     "value": settings['sections'][0]['components'][0]['value']
                                 }
                             ]
                         }
                     ]
                 }}
    }
    configuration = snapser_internal.Configuration()
    with snapser_internal.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = snapser_internal.StorageServiceApi(api_client)
        try:
            # Storage Settings
            api_response = api_instance.storage_internal_get_blob(
                access_type='private',
                blob_key='character_settings',
                owner_id='byosnap_characters',
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if api_response is None:
                return make_response(jsonify(response), 200)
            # Load storage data
            response['data']['character_settings'] = json.loads(
                api_response.value)
            # Update the characters with the imported characters
            response['data']['character_settings']['sections'][0]['components'][0]['value'] = settings['sections'][0]['components'][0]['value']
            return make_response(jsonify(response), 200)
        except ApiException as e:
            pass
    return make_response(jsonify(response), 200)
```
</CollapsableDoc>

### C. User Delete
Snapser provides a User data delete tool that allows you to delete a users game data. Since BYOSnaps are your custom code, Snapser cannot delete data on your behalf and expects you to implement the following endpoint.
<CollapsableDoc title="Delete User Data">
- `Method`: **DELETE**
- `Endpoint`: **/$byoSnapPrefix/$byosnapId/user**.
- `Description`: This endpoint is called when a user deletes their account. This endpoint is expected to delete all the data for the user. In our case, we are deleting the **character_settings** blob key for the user.
- `Response`: This endpoint is expected to return a 200 OK response if the data was deleted successfully. If the data was not found, it should return a 400 Bad Request response.
- `Example URL`: **DELETE /v1/byosnap-advanced/user**
```python
@app.route("/v1/byosnap-advanced/settings/users/<user_id>/data", methods=["DELETE"])
@validate_authorization(GATEWAY_HEADER_INTERNAL_ORIGIN_VALUE, user_id_resource_key="user_id")
def delete_user_data(user_id):
    '''
    Delete User Data
    '''
    gateway = request.headers.get('Gateway')
    if not gateway or gateway.lower() != 'internal':
        return make_response(jsonify({
            'error_message': 'Unauthorized'
        }), 401)
    # Delete the character blob from storage
    configuration = snapser_internal.Configuration()
    with snapser_internal.ApiClient(configuration=configuration) as storage_api_client:
        storage_api_instance = snapser_internal.StorageServiceApi(
            storage_api_client)
        try:
            # Get blob
            storage_api_response = storage_api_instance.storage_internal_delete_blob(
                access_type='private',
                blob_key='characters',
                owner_id=user_id,
                gateway=os.environ['SNAPEND_INTERNAL_HEADER']
            )
            if storage_api_response is None:
                return make_response(jsonify({
                    'error_message': 'No blob'
                }), 400)
        except ApiException:
            pass
    return make_response(jsonify({}), 200)

```
</CollapsableDoc>

<Checkpoint step={5}>
We now have a configuration tool represented as a JSON. All the hooks integrated in our BYOSnap code. We are now ready to publish our BYOSnap to Snapser.
</Checkpoint>

## Step 6: Deploy your BYOSnap
With the code updated, you are now ready to deploy your BYOSnap to the Private Snaps dashboard on Snapser.

- Choose a custom BYOSnap ID. For this tutorial, let's select $byosnapId=**byosnap-advanced**.
  <Note>
    Use **byosnap-advanced** as the BYOSnap ID. If you select a different ID, the Automated tutorial will not work. But if you are following the manual steps, you can use any ID you want.
  </Note>
- Select a version number. Set $version to `v1.0.0`.
- Determine the full path to the root of your code directory, e.g., `/Users/aj/snapser-byosnaps/advanced/byosnap-python`.
- Identify the resources folder, which is the `snapser-resources` folder at the root of your code directory.

Replace the variables below with your custom values and execute the command to deploy your BYOSnap.


<CodeGroup title="Deploy BYOSnap" tag="bash" >
```bash
# $byosnapId = BYOSnap Id. Should start with `byosnap-`. Should not contain spaces and should only contain characters.
# $version = Version number for your BYOSnap. Should be in the format v1.0.0
# $path = Path to the directory where your BYOSnap code resides.
# $tag = Tag for your BYOSnap. This is optional.
snapctl byosnap publish --byosnap-id $byosnapId --version $version --path $rootCodePath --resources-path $rootCodePath/snapser-resources
```
</CodeGroup>

You will see the output from the Snapctl tool as it deploys your BYOSnap to Snapser. Once the deployment is
complete, you will see a success message.
```bash
Success BYOSnap upload successful
Info Uploading swagger.json at ./snapser-resources/swagger.json
Success Uploaded swagger.json
Success Uploaded README.md
Success Uploaded tool snapser-tool-characters.json # 👈 Notice it picks up the configuration tool JSON
Success Completed the docs uploading process
Success BYOSNAP publish successful
Success BYOSNAP publish version successful
Success BYOSNAP published successfully
```
<Note>
  The Snapshots below assume you are using the C# codebase. But the steps are the same for all languages.
</Note>

- Once you publish you will be able to see your BYOSnap in the **Custom Snaps** tool.
![CustomSnaps](/images/docs/tutorials/byosnap-advanced-snaps.png)

<Checkpoint step={6}>
With our BYOSnap deployed, we can now add it to our Snapend.
</Checkpoint>

## Step 7: Add BYOSnap to your Snapend
### A. Manual Cluster Creation
1. Go to the Snapser Web App and click on the Snapend you created in the **Snapend Creation** tutorial.
1. On your Snapend homepage, click the **Edit** button. This will take you to the Snapend Edit page.
![EditSnapend](/images/docs/tutorials/byosnap-advanced-snapend-edit.png)
1. Here, you will find the Snaps already included in your Snapend. Scroll down to locate the BYOSnap you just published and click the **Add** button.
    ![AddBYOSnap](/images/docs/tutorials/byosnap-advanced-byosnap-add.png)
    <Note>
      Use the filter widget at the top right to display only BYOSnaps.
    </Note>
1. Continue clicking **Continue** until you reach the final **Review** step, then click the **Snap it** button.
1. A pop-up window will show the progress of creating your cluster. Your updated Snapend should be ready in a few moments.

### B. Automated Cluster Creation
<Note>
  If you have already completed the manual **Add BYOSnap to Snapend** steps, you can ignore this.
</Note>

After you have published a BYOSnap, we offer a helper script that simulates the end state of following the manual instructions to create a snapend with your BYOSnap in it. This script utilizes Snapctl.

To execute this script, you will need the following:
1. Navigate to the [Game Management](https://snapser.com/games) page on Snapser. Click the Copy Icon next to **ID** to copy the $companyId.
1. Select the game under which you wish to create your Snapend. This will bring you to the game's home page. Click the Copy Icon next to **ID** to copy the $gameId.
1. The $byosnapId is the identifier for your BYOSnap, which is **byosnap-inter** as used in the BYOSnap publish step.
1. Use the version number from the BYOSnap publish step, e.g., v1.0.0.

```bash
python snapend_create.py $companyId $gameId $byosnapId $version
```

You will see the output from the Snapctl tool as it creates your Snapend. Once the creation is complete, you will see a success message.

```bash
Success Updated your snapend. Your snapend is Live.
Success Snapend clone successful. Do not forget to download the latest manifest.
Your Snapend is created successfully with Snaps: auth and byosnap-*.
```

<Checkpoint step={7}>
  You now have a configured Snapend with Auth, Storage and a BYOSnap. Lets now put our hooks integration to a test.
</Checkpoint>

## Step 8: Configuration Tool Hooks
Once your Snapend is up, go to the Snapend home page and click on **Configuration Tools** under the **Quick Links**. This will take you to the Configuration Tools page. Here click on your BYOSnap name on the left nav. Now, lets test the configuration tool we created.
![CustomSnaps](/images/docs/tutorials/byosnap-advanced-config-byosnap.png)
1. Clicking on this should render the UI tool we created.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-byosnap-config-render.png)
1. You should be able to add characters to the text area and click on **Save**. Lets add **Mario, Luigi, Peach** and click on **Save**. This in turns calls the **PUT /v1/byosnap-advanced/settings** endpoint in your BYOSnap code. You should see a success toaster.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-byosnap-config-save.png)
1. Next, hot-reload the page and you should see the characters you added in the text area. This is because the first render of the tool calls the **GET /v1/byosnap-advanced/settings** endpoint in your BYOSnap code. This endpoint returns the configuration tool JSON payload that we created in the first step.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-byosnap-config-hard-reload.png)

<Checkpoint step={8}>
  You have now successfully created a configuration tool for your BYOSnap. This tool is used to store the available characters in your game. We are now going to test the sync and clone hooks.
</Checkpoint>

## Step 9: Snapend Sync and Clone Hooks
Now, lets assume a new dev comes in and wants to clone our Snapend. To do this, they go through the following steps:

1. They can go to the Game home page and click on **+ Snapend**. This will take them to the Snapend creation page.
1. First, they lets say they enter the Snapend name as **clone-my-dev-cluster** and click **Continue**.
1. Here they can click the blue widget button and select Clone.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-byosnap-clone.png)
1. This opens the clone widget, where you can select the Snapend you want to clone. In our case, we select **my-dev-cluster**.
1. When you do this, this widget will hit your BYOSnaps export settings endpoint, and when it gives a successful response, will show the toggle next to the BYOSnap name. Essentially telling the user, that configuration clone is available.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-byosnap-clone-import.png)
    <Note>
      If our BYOSnap had returned a non-200 response, the toggle would have been disabled and a **Error** icon would appear next to it.
    </Note>
1. Toggle all settings to sync and click **Clone**.
1. Now, proceed till the end and click **Snap it!**. This will create a new Snapend with the same configuration as the original Snapend.
1. When the new Snapend comes up before marking it as operational, Snapser calls the import settings endpoint of the new Snapends BYOSnap. Which we have already implemented to store the payload in the Storage snap.
1. Thus, when a new Snapend is created, the configuration tool is automatically populated with the configuration data from the original Snapend.
1. As a final step, to confirm this, once the new cloned Snapend is up, go to its **Snap Configuration** tool and select your BYOSnap. Now, when you see the tool the characters **Mario, Luigi, Peach** should be pre-populated in the text area.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-byosnap-clone-config.png)


<Checkpoint step={9}>
  We have seen how our BYOSnap integrated with the Snapend Sync and Clone hooks. This allows us to clone our Snapend and have the configuration tool pre-populated with the configuration data from the original Snapend. Next, lets look at the final hook which is the User Delete hook.
</Checkpoint>

## Step 10: User Delete Hook
The User Delete hook is called when someone within the game studio uses the User Delete tool. This tool allows you to delete a user from your game. This is useful for testing purposes, as it allows you to delete a user and all their data from your game.

To confirm this works, first we need to:
1. Enable the Anonymous connector in the Auth Snaps - Connector Configuration tool.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-anon.png)
1. Next, lets now go to the API Explorer from the Snapend home page and select the Authentication snap. Next, you will see the AnonymousLogin API in the side nav. Click on it. Then, add any name in the `user_name` field and click **PUT**. With this, you have created a real user for your game.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-anon-api.png)
1. Now lets go back to the Snapend home page and click on the **User Manager Tool** under **Quick Links**.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-user-manager.png)
1. You should now see the user we recently created using the API Explorer. Use the `Copy Icon` to copy their user ID. We are going to need this in the User Reset tool. Next, click on the **Reset Delete Users** button, which will take you to the User Reset tool.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-user-manager-history.png)
1. Now, paste the user Id in the text area and click **Delete**. Snapser will show you a confirmation dialog where you can click **Delete** again.
    ![CustomSnaps](/images/docs/tutorials/byosnap-advanced-user-manager-delete.png)
1. You will see a list of snaps that successfully deleted the user data. What Snapser did here is hit our Delete User data endpoint and waited to get either a 200 or a non-200. Since in our code we are returning back a 200, Snapser added our BYOSnap to the list of snaps that successfully deleted the data.

<Checkpoint step={10}>
  Congratulations! You have successfully completed this tutorial. You now know, how to integrate your BYOSnap with all the Snapser hooks.
</Checkpoint>
