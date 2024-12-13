from mcp import Tool

TOOL_SCHEMA = (
  Tool(
    name="load_split_embed_files",
    description="Load, split and embed files into a vector database. This tool is useful for "
    + "embedding files into a vector database. The tool accepts a list "
    + "of file paths. The files are read, split into chunks, and embedded into a vector database. "
    + "The tool returns an ID of the files in the vector database. The ID can be used to query "
    + "those files for retrieving relevant splits of those files using the 'query_embedded_files' tool.",
    inputSchema={
      "type": "object",
      "properties": {
        "files": {
          "type": "array",
          "items": {"type": "string"},
          "description": "List of file paths",
        }
      },
      "required": ["files"],
    },
  ),
)


def load_split_embed_files(arguments: dict) -> dict:
  """Load, split and embed files."""
  files = arguments["files"]
