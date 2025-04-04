export const meta = {
  author: 'AJ Apte',
}

# Setup Snapctl

Snapctl is a command-line interface (CLI) tool built by Snapser that allows you to interact with your Snapser account.

## Introduction
This beginner-friendly guide assists users who are new to Snapser in setting up the Snapser CLI tool on their local machine. You will learn how to install Snapctl, authenticate with Snapser, and configure Snapctl to interact with your Snapser account.

## Step 0: Check for Access
Before you begin, make sure you have access to use the Snapser CLI tool. Only users with the following
roles can use Snapctl:
- **company-admin**
- **company-edit**
- **game-admin**
- **game-edit**

<Checkpoint step={0}>
  Once you have verified that you have one of the above roles, you can proceed to the next step.
</Checkpoint>

## Step 1: Install dependencies

### A. Python 3.X
The Snapser CLI tool depends on Python 3.X and Pipx. MacOS comes pre installed with Python. But
please make sure you are running Python 3.X. On Windows, you can download Python 3.X from the
Windows store.

### B. Pipx
For installing Pipx, you can use the following commands:

#### Installing PIP on MacOS

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

#### Installing PIP on Windows

```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

<Note>
  **What is pipx?**
  pipx is a tool for installing and running Python applications in isolated environments. It's similar to pip, which is Python's package installer, but pipx is specifically designed for the installation of command-line tools written in Python. It installs each tool in its own virtual environment, ensuring that dependencies for one tool don't interfere with dependencies for another tool.
</Note>

### C. Docker
Some of the commands also need docker. You can download the latest version of Docker from the [Docker website](https://www.docker.com/products/docker-desktop).

<Note>
  **IMPORTANT**: Open up Docker desktop and settings. Make sure the setting
    **Use containerd for pulling and storing images** is **disabled**.  This is because Snapser uses Docker
  to build and push images to the Snapser registry. Having this setting enabled will
  cause issues with the Snapser CLI tool.
</Note>

<Checkpoint step={1}>
  With the dependencies installed and Docker settings configured, you are ready to install Snapctl.
</Checkpoint>

## Step 2: Install Snapctl

Run the following command to install Snapctl:

```bash
pipx install snapctl
```

<Note>
  After you install snapctl you may have to add the python bin folder to your
  path. For example, on MacOSX this is usually `~/Library/Python/3.9/bin`. On
  Windows this is usually
  `C:\Users\username\AppData\Roaming\Python\Python39\Scripts`.
</Note>

<Checkpoint step={2}>
  You have successfully installed Snapctl on your local machine. You are now ready to add your
  Snapctl credentials.
</Checkpoint>

## Step 3: Local Setup

### A. Generate Snapctl Developer Key

Log in to your Snapser account. Click on your user icon on the top right and select, User Account.
In the left navigation click on **Developer** which will bring up your Personal API Key widget.
If you have not generated an API Key yet click on the **Generate** button to generate a new key.
You can generate up to 3 API Keys per user account.

<Note>
  Please make sure you save your API key in a safe place. You will not be able
  to see it again.
</Note>

### B. Setup Key
Create a file named `~/.snapser/config`. Open it using the editor of your choice and replace `$your_api_key`
with your personal Snapser Access key. Save the file.

```bash
[default]
snapser_access_key=$your_api_key
```

Or you can run the following command

on MacOSX

```bash
# $your_api_key = Your Snapser developer key
echo -e "[default]\nSNAPSER_API_KEY=$your_api_key" > ~/.snapser/config
```

on Windows Powershell

```
# $your_api_key = Your Snapser developer key
echo "[default]
SNAPSER_API_KEY=$your_api_key" | Out-File -encoding utf8 ~\.snapser\config
```

<Note>
  The Developer Key is a sensitive piece of information. Please make sure you do not share it with anyone.
  Also the key has an expiry. When the key expires you will have to generate a new key and update the config file.
</Note>

<Checkpoint step={3}>
  You have successfully added your Snapctl credentials. You are now ready to use Snapctl.
</Checkpoint>

## Step 4: Validate Setup

Use the following command to validate your setup:
```bash
snapctl validate
```
Running this command should output something similar to the following:

```bash
 ____
/ ___| _ __   __ _ _ __  ___  ___ _ __
\___ \| '_ \ / _` | '_ \/ __|/ _ \ '__|
 ___) | | | | (_| | |_) \__ \  __/ |
|____/|_| |_|\__,_| .__/|___/\___|_|
                  |_|

Success API Key validated
Success Setup is valid
```
Output will tell you if the Snapctl was able successfully validate your setup with the remote Snapser server
or not.

<Checkpoint step={4}>
  You have successfully set up Snapctl on your local machine. You can now use
  the various Snapctl commands at your disposal.
</Checkpoint>



