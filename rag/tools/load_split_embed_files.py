from uuid import uuid4
from mcp import Tool

from rag_tools.embed import embed_file

TOOL_SCHEMA = Tool(
  name="load_split_embed_files",
  description="Load, split and embed files into a vector database. This tool is useful for "
  + "embedding files into a vector database. The tool accepts a list "
  + "of file paths. The files are read, split into chunks, and embedded into a vector database. "
  + "The tool returns an vector_collection_id for the embedded files and a result array of those embeddings. You can use the vector_collection_id "
  + "to query those files for retrieving relevant splits using the 'query_embedded_files' tool.",
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
)


def load_split_embed_files(arguments: dict) -> dict:
  """Load, split and embed files."""
  files = arguments["files"]
  vector_collection_id = uuid4().hex
  result = []

  for file_path in files:
    embed_result = embed_file(vector_collection_id, file_path)
    result.append(embed_result)

  return {"vector_collection_id": vector_collection_id, "result": result}
