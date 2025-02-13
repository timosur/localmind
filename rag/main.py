import asyncio
from collections.abc import Sequence
from typing import Any

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import EmbeddedResource, ImageContent, TextContent, Tool
from tools.query_files import TOOL_SCHEMA as QUERY_EMBEDDED_FILES_TOOL_SCHEMA
from tools.query_files import query_files

# Create a server instance
server = Server("filesystem-rag")


@server.list_tools()
async def list_tools() -> list[Tool]:
  """List available tools."""
  return [
    QUERY_EMBEDDED_FILES_TOOL_SCHEMA,
  ]


@server.call_tool()
async def call_tool(
  name: str, arguments: Any
) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
  """Handle tool calls."""
  try:
    match name:
      case "query_files":
        return query_files(arguments)
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
