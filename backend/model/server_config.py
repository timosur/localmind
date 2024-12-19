from typing import TypedDict


class ServerConfig(TypedDict):
  name: str
  command: str
  args: list[str]
