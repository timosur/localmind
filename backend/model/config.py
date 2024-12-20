from model.openai_config import OpenAIConfig
from model.server_config import ServerConfig


class AppConfig:
  config_file_path: str
  db_file_path: str
  server: list[ServerConfig]
  openai: OpenAIConfig

  def __init__(self):
    self.config_file_path = ""
    self.server = []
    self.db_file_path = ""
    self.openai = OpenAIConfig()
