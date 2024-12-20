import yaml
import os
from dotenv import load_dotenv

from model.config import AppConfig

# Load environment variables
load_dotenv()


# Function to get environment variables
def get_env_variable(key: str, default: str = None) -> str:
  value = os.getenv(key)
  if value is None:
    if default is not None:
      return default
    raise ValueError(f"Environment variable {key} not set.")
  return value


APP_CONFIG: AppConfig = AppConfig()

APP_CONFIG.db_file_path = get_env_variable("APP_DB_FILE_PATH", "./db.sqlite")

# Get app config file directory from environment variable
APP_CONFIG.config_file_path = get_env_variable("APP_CONFIG_FILE_PATH")

# Load the config file
with open(APP_CONFIG.config_file_path, "r") as file:
  config_file = yaml.safe_load(file)

# Append the config file to the APP_CONFIG
APP_CONFIG.server = config_file["server"]

# Set the openai config
APP_CONFIG.openai.api_key = get_env_variable("AZURE_OPENAI_API_KEY")
APP_CONFIG.openai.azure_endpoint = get_env_variable("AZURE_OPENAI_ENDPOINT")
APP_CONFIG.openai.openai_api_version = get_env_variable("AZURE_OPENAI_API_VERSION")
APP_CONFIG.openai.openai_chat_model = get_env_variable("AZURE_OPENAI_CHAT_MODEL")
