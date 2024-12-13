from mcp import Tool

TOOL_SCHEMA = Tool(
  name="query_embedded_files",
  description="Query embedded files from a vector database. This tool is useful for querying "
  + "embedded files from a vector database. The tool accepts a list of file IDs and returns the "
  + "embedded splits of those files. The splits can be used for further processing or analysis.",
  inputSchema={
    "type": "object",
    "properties": {
      "file_ids": {
        "type": "array",
        "items": {"type": "string"},
        "description": "List of file IDs",
      }
    },
    "required": ["file_ids"],
  },
)


def query_embedded_files(arguments: dict) -> dict:
  """Query embedded files."""
  file_ids = arguments["file_ids"]
