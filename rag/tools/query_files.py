import json
from uuid import uuid4

from mcp import Tool
from mcp.types import TextContent
from rag_tools.embed import embed_file
from rag_tools.query import query

TOOL_SCHEMA = Tool(
  name="query_files",
  description="""Query files from a vector database. This tool is useful for querying
files by file path name. It can be helful for querying files by their
content or metadata, to understand the context of the files.
""",
  inputSchema={
    "type": "object",
    "properties": {
      "files": {
        "type": "array",
        "items": {"type": "string"},
        "description": "List of file paths",
      },
      "query": {
        "type": "string",
        "description": "Query string",
      },
    },
    "required": ["files", "query"],
  },
)


def query_files(arguments: dict) -> dict:
  """Load, split and embed files."""
  files = arguments["files"]
  user_query = arguments["query"]
  vector_collection_id = uuid4().hex
  embed_results = []

  for file_path in files:
    embed_result = embed_file(vector_collection_id, file_path)
    embed_results.append(embed_result)

  response = query(vector_collection_id, user_query)

  return [
    TextContent(
      type="text",
      text=json.dumps(
        {
          "user_query": user_query,
          "embed_results": embed_results,
          "query_response": response,
          "vector_collection_id": vector_collection_id,
        }
      ),
    ),
  ]
