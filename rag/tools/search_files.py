import os
import re

from mcp import Tool

TOOL_SCHEMA = Tool(
  name="search_files",
  description="Recursively search for files and directories matching a pattern. "
  + "Searches through all subdirectories from the starting path. The search "
  + "is case-insensitive and matches partial names. Returns full paths to all "
  + "matching items. Great for finding files when you don't know their exact location. "
  + "Only searches within allowed directories.",
  inputSchema={
    "type": "object",
    "properties": {
      "path": {"type": "string", "description": "Path to the directory"},
      "pattern": {
        "type": "string",
        "description": "Pattern to search for",
      },
      "excludePatterns": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Patterns to exclude",
      },
    },
    "required": ["path", "pattern"],
  },
)


def search_files(arguments):
  directory_path = arguments["path"]
  pattern = arguments["pattern"]
  exclude_patterns = arguments.get("excludePatterns", [])

  # Search for files
  matching_files = []

  for root, _, files in os.walk(directory_path):
    for file in files:
      full_path = os.path.join(root, file)

      # Check if the file matches the pattern
      if all(
        exclude_pattern not in full_path for exclude_pattern in exclude_patterns
      ) and re.search(pattern, file, re.IGNORECASE):
        matching_files.append(full_path)

  return matching_files
