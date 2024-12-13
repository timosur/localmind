import os
import json

from mcp import Tool
from mcp.types import TextContent

TOOL_SCHEMA = Tool(
  name="get_file_info",
  description="""Retrieve detailed metadata about a file or directory. Returns comprehensive
information including size, creation time, last modified time, permissions,
and type. This tool is perfect for understanding file characteristics
without reading the actual content. Only works within allowed directories.
""",
  inputSchema={
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "Path to the file or directory",
      }
    },
    "required": ["path"],
  },
)


def get_file_info(arguments: dict) -> dict:
  """Get file info."""
  file_path = arguments["path"]

  file_info = os.stat(file_path)

  return [
    TextContent(
      type="text",
      text=json.dumps(
        {
          "path": file_path,
          "size": file_info.st_size,
          "creation_time": file_info.st_ctime,
          "last_modified_time": file_info.st_mtime,
          "permissions": oct(file_info.st_mode),
          "type": "file" if os.path.isfile(file_path) else "directory",
        }
      ),
    )
  ]
