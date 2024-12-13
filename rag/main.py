import asyncio
import os
import sys
from collections.abc import Sequence
from typing import Any

from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
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
server = Server("filesystem-rag")

# Parse allowed directories from command line arguments
allowed_directories = []

if len(sys.argv) > 1:
  allowed_directories = sys.argv[1:]


@server.list_tools()
async def list_tools() -> list[Tool]:
  """List available tools."""
  return [
    LIST_DIRECTORY_TOOL_SCHEMA,
    GET_FILE_INFO_TOOL_SCHEMA,
    SEARCH_FILES_TOOL_SCHEMA,
    LIST_ALLOWED_DIRECTORIES_TOOL_SCHEMA,
    LOAD_SPLIT_EMBED_FILES_TOOL_SCHEMA,
  ]


@server.call_tool()
async def call_tool(
  name: str, arguments: Any
) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
  """Handle tool calls."""
  try:
    match name:
      case "list_directory":
        return list_directory(arguments)
      case "get_file_info":
        return get_file_info(arguments)
      case "search_files":
        return search_files(arguments)
      case "list_allowed_directories":
        return list_allowed_directories(arguments, allowed_directories)
      case "load_split_embed_files":
        return load_split_embed_files(arguments)
      case _:
        raise ValueError(f"Unknown tool: {name}")
  except Exception as e:
    return [{"type": "error", "content": str(e)}]


async def main():
  async with stdio_server() as (read_stream, write_stream):
    await server.run(
      read_stream,
      write_stream,
      InitializationOptions(
        server_name="filesystem-rag",
        server_version="0.1.0",
        capabilities=server.get_capabilities(
          notification_options=NotificationOptions(),
          experimental_capabilities={},
        ),
      ),
    )


if __name__ == "__main__":
  asyncio.run(main())
