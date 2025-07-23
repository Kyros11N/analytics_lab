import os
from dotenv import load_dotenv
from src.utils.pathing import resolved_path_to_repo_root


# Load the .env file from .secrets/ directory at the repo root
SECRETS_PATH = resolved_path_to_repo_root("~/.secrets/local.env", max_parent_elevation=4)
load_dotenv(SECRETS_PATH)

# Configuration
EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY", "test-key")
