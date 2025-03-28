import sys
import re
import platform
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
if len(sys.argv) < 2:
    print("Usage: python byosnap_publish.py $version")
    sys.exit(1)

# Accessing user arguments
version = sys.argv[1]

# Constants
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, 'resources')
load_env(RESOURCES_DIR)
byosnap_name = os.getenv('BYOSNAP_NAME', 'byosnap-basic')
BYOSNAP_ID = f"byosnap-{byosnap_name}"
print(BYOSNAP_ID)

# Validation
if not re.match(r'^v\d+\.\d+\.\d+$', version):
    print("Version should be in the format vX.Y.Z Eg: v1.0.0")
    print("Note: With every publish you need to increment at least the patch version.")
    sys.exit(1)

cmd = [
    'snapctl', 'byosnap', 'publish', '--byosnap-id', BYOSNAP_ID,
    '--version', version, '--resources-path', RESOURCES_DIR,
    '--path', CURRENT_DIR
]

response = subprocess.run(cmd)

if response.returncode == 0:
    print(f"BYOSnap published successfully with version {version}")
else:
    print(response)
    print(f"Failed to publish BYOSnap with version {version}")
    sys.exit(1)
