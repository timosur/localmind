import asyncio
from collections.abc import Sequence
from typing import Any

from mcp.server import Server
from mcp.types import EmbeddedResource, ImageContent, TextContent, Tool

from tools.allowed_directories import (
  TOOL_SCHEMA as LIST_ALLOWED_DIRECTORIES_TOOL_SCHEMA,
)
from tools.allowed_directories import list_allowed_directories
from tools.get_file_info import TOOL_SCHEMA as GET_FILE_INFO_TOOL_SCHEMA
from tools.get_file_info import get_file_info
from tools.list_directory import TOOL_SCHEMA as LIST_DIRECTORY_TOOL_SCHEMA
from tools.list_directory import list_directory
from tools.load_split_embed_files import (
  TOOL_SCHEMA as LOAD_SPLIT_EMBED_FILES_TOOL_SCHEMA,
)
from tools.load_split_embed_files import load_split_embed_files
from tools.search_files import TOOL_SCHEMA as SEARCH_FILES_TOOL_SCHEMA
from tools.search_files import search_files

# Create a server instance
app = Server("filesystem-rag")


@app.list_tools()
async def list_tools() -> list[Tool]:
  """List available tools."""
  return [
    LIST_DIRECTORY_TOOL_SCHEMA,
    GET_FILE_INFO_TOOL_SCHEMA,
    SEARCH_FILES_TOOL_SCHEMA,
    LIST_ALLOWED_DIRECTORIES_TOOL_SCHEMA,
    LOAD_SPLIT_EMBED_FILES_TOOL_SCHEMA,
  ]


@app.call_tool()
async def call_tool(
  name: str, arguments: Any
) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
  """Handle tool calls."""
  match name:
    case "list_directory":
      return await list_directory(arguments)
    case "get_file_info":
      return await get_file_info(arguments)
    case "search_files":
      return await search_files(arguments)
    case "list_allowed_directories":
      return await list_allowed_directories(arguments)
    case "load_split_embed_files":
      return await load_split_embed_files(arguments)
    case _:
      raise ValueError(f"Unknown tool: {name}")


async def main():
  # Import here to avoid issues with event loops
  from mcp.server.stdio import stdio_server

  async with stdio_server() as (read_stream, write_stream):
    await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
  import asyncio

  asyncio.run(main())
if __name__ == "__main__":
  import asyncio

  asyncio.run(main())
