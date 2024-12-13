import os
import re

from mcp import Tool
from mcp.types import TextContent

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
      "exclude_patterns": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Patterns to exclude",
      },
    },
    "required": ["path", "pattern"],
  },
)


def search_files(arguments):
  """
  Search for files in a directory matching a pattern while excluding specified patterns.

  Args:
      arguments: Dictionary containing:
          - path: Base directory to search in
          - pattern: Regex pattern to match files
          - excludePatterns: List of patterns to exclude (optional)

  Returns:
      List of full file paths that match the criteria

  Raises:
      ValueError: If path doesn't exist or pattern is invalid
      TypeError: If arguments are of incorrect type
  """
  try:
    directory_path = str(arguments["path"])
    pattern = str(arguments["pattern"])
    exclude_patterns = arguments.get("exclude_patterns", [])

    if not os.path.exists(directory_path):
      raise ValueError(f"Directory not found: {directory_path}")

    # Validate pattern
    try:
      re.compile(pattern)
    except re.error as e:
      raise ValueError(f"Invalid regex pattern: {str(e)}")

    # Search for files
    matching_files = []

    for root, _, files in os.walk(directory_path):
      for file in files:
        full_path = os.path.join(root, file)

        # Check if file should be excluded
        should_exclude = any(
          re.search(exclude_pattern, full_path, re.IGNORECASE)
          for exclude_pattern in exclude_patterns
        )

        # Check if file matches pattern
        if not should_exclude and re.search(pattern, file, re.IGNORECASE):
          matching_files.append(TextContent(type="text", text=str(full_path)))

    if not matching_files:
      return [TextContent(type="text", text="No files found")]

    return matching_files

  except KeyError as e:
    return [TextContent(type="text", text=f"Missing argument: {str(e)}")]
  except TypeError as e:
    return [TextContent(type="text", text=f"Invalid argument type: {str(e)}")]
