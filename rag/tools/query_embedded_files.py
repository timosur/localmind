from mcp import Tool

from rag_tools.query import query

TOOL_SCHEMA = Tool(
  name="query_embedded_files",
  description="Query embedded files from a vector database. This tool is useful for querying "
  + "embedded files from a vector database. The tool accepts a list of file IDs and returns the "
  + "embedded splits of those files. The splits can be used for further processing or analysis.",
  inputSchema={
    "type": "object",
    "properties": {
      "vector_collection_id": {
        "type": "string",
        "description": "List of file IDs",
      },
      "query": {
        "type": "string",
        "description": "Query string",
      },
    },
    "required": ["file_ids"],
  },
)


def query_embedded_files(arguments: dict) -> dict:
  """Query embedded files."""
  vector_collection_id = arguments["vector_collection_id"]
  user_query = arguments["query"]

  response = query(vector_collection_id, user_query)

  return response
