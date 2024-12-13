from mcp import Tool

TOOL_SCHEMA = Tool(
  name="list_allowed_directories",
  description="""Returns the list of directories that this server is allowed to access.
Use this to understand which directories are available before trying to access files.""",
  inputSchema={
    "type": "object",
    "properties": {},
    "required": [],
  },
)


def list_allowed_directories(arguments: dict) -> list[str]:
  """List allowed directories."""
  return [
    "/",
  ]
