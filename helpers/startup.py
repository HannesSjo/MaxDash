import os
import json
import subprocess
import urllib.request
from git import Repo

# Path to the config file (always one folder down from this script)
config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

# Function to check internet connectivity
def is_internet_connected():
    try:
        urllib.request.urlopen('http://www.google.com', timeout=1)
        return True
    except urllib.error.URLError:
        return False

# Read paths from the config file
with open(config_file_path, 'r') as config_file:
    config_data = json.load(config_file)

# Extract paths from the config data
github_repo_url = config_data.get('github_repo_url', '')
local_repo_path = config_data.get('local_repo_path', '')
main_script_path = config_data.get('main_script_path', '')

# Check if the config file exists
if not os.path.exists(config_file_path):
    default_config = {
        "github_repo_url": "https://github.com/HannesSjo/MaxDash",
        "local_repo_path": "/..",
        "main_script_path": "/../maxdash/main.py"
    }
    
    with open(config_file_path, 'w') as config_file:
        json.dump(default_config, config_file)
    
    print("Config file created with default settings. Please edit the config file.")
else:
    # Check for internet connectivity
    if is_internet_connected():
        # Pull updates from the GitHub repository
        repo = Repo(local_repo_path)
        origin = repo.remote()
        origin.pull()
        
        print("GitHub repository updated.")
        
        # Start the main.py script
        subprocess.Popen(["python", main_script_path])
    else:
        print("No internet connection. Skipping GitHub repository update.")