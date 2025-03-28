import sys
import re
import subprocess
import os

# Helper


def load_env(parent_folder, env_file='.env'):
    """Manually load a .env file into environment variables."""
    file_path = os.path.join(parent_folder, env_file)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace and ignore comments and empty lines
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


# Check if enough arguments have been passed
if len(sys.argv) < 3:
    print("Usage: python byosnap_sync.py $version $snapendId")
    print("Note: If you have version v1.0.0 running in the Snapend, you can just pass the version as v1.0.0 and Snapser will automatically just overwrite the remote code under the same version.")
    sys.exit(1)

# Accessing user arguments
version = sys.argv[1]
snapendId = sys.argv[2]


# Constants
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, 'resources')
load_env(RESOURCES_DIR)
byosnap_name = os.getenv('BYOSNAP_NAME', 'byosnap-basic')
BYOSNAP_ID = f"byosnap-{byosnap_name}"


# Validation
if not re.match(r'^v\d+\.\d+\.\d+$', version):
    print("Version should be in the format vX.Y.Z Eg: v1.0.0")
    sys.exit(1)

# snapctl byosnap sync --snapend-id "${2}" --byosnap-id byosnap-python-basic --version "${1}" --resources-path "$(pwd)/resources" --path "$(pwd)"
cmd = [
    'snapctl', 'byosnap', 'sync',
    '--snapend-id', snapendId, '--byosnap-id', BYOSNAP_ID,
    '--version', version, '--resources-path', RESOURCES_DIR,
    '--path', CURRENT_DIR, '--blocking'
]

response = subprocess.run(cmd)

if response.returncode == 0:
    print(
        f"BYOSnap synced successfully with your snapend {snapendId} at version {version}")
else:
    print(response)
    print(
        f"Failed to sync BYOSnap with your snapend {snapendId} at version {version}")
    sys.exit(1)
