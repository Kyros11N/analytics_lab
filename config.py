import os
from dotenv import load_dotenv
from src.utils.paths import resolved_path_to_repo_root


# Load the .env file from .secrets/ directory at the repo root
SECRETS_PATH = resolved_path_to_repo_root("~/.secrets/local.env", max_parent_elevation=4)
load_dotenv(SECRETS_PATH)

# API Configuration
EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY", "test-key")

# ClickHouse Configuration
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "8123"))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")
