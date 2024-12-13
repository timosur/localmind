import os
import json

from mcp import Tool
from mcp.types import TextContent

TOOL_SCHEMA = Tool(
  name="list_directory",
  description="""Get a detailed listing of all files and directories in a specified path.
Results clearly distinguish between files and directories with [FILE] and [DIR]
prefixes. This tool is essential for understanding directory structure and
finding specific files within a directory. Only works within allowed directories.""",
  inputSchema={
    "type": "object",
    "properties": {"path": {"type": "string", "description": "Path to the directory"}},
    "required": ["path"],
  },
)


def list_directory(arguments: dict) -> dict:
  """List the contents of a directory."""
  path = arguments["path"]

  contents = []

  for item in os.listdir(path):
    if os.path.isdir(os.path.join(path, item)):
      contents.append(f"[DIR] {item}")
    else:
      contents.append(f"[FILE] {item}")

  return [
    TextContent(
      type="text",
      text=json.dumps(contents, indent=2),
    )
  ]
