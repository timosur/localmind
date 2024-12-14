from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
  command="python3",  # Executable
  args=[
    "main.py",
    "/Users/timosur/code/mcp/standalone-mcp-chat",
  ],  # Optional command line arguments
  env=None,  # Optional environment variables
)


async def run():
  async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
      # Initialize the connection
      await session.initialize()

      # List available prompts
      print("##### list_tools #####")
      tools = await session.list_tools()

      print(tools)

      print("##### list_directory #####")
      result = await session.call_tool(
        "list_directory",
        arguments={"path": "/Users/timosur/code/mcp/standalone-mcp-chat"},
      )

      print(result)

      print("##### get_file_info #####")
      result = await session.call_tool(
        "get_file_info",
        arguments={"path": "/Users/timosur/code/mcp/standalone-mcp-chat/README.md"},
      )

      print(result)

      print("##### list_allowed_directories #####")
      result = await session.call_tool(
        "list_allowed_directories",
        arguments={},
      )

      print(result)

      print("##### search_files #####")
      result = await session.call_tool(
        "search_files",
        arguments={
          "pattern": ".py",
          "path": "/Users/timosur/code/mcp/standalone-mcp-chat",
          "exclude_patterns": [
            "tools",
            "rag_tools",
            "__pycache__",
            ".venv",
            "dist",
            "build",
            "node_modules",
            "backend",
          ],
        },
      )

      print(result)

      print("##### load_split_embed_files #####")
      result = await session.call_tool(
        "load_split_embed_files",
        arguments={
          "files": [
            "/Users/timosur/code/mcp/standalone-mcp-chat/kurzanleitungen_pdfa.pdf",
          ],
        },
      )

      print(result)

      print("##### query_embedded_files #####")
      result = await session.call_tool(
        "query_embedded_files",
        arguments={
          "query": "kurzanleitung",
          "vector_collection_id": "e018c498c7584de0a0d4e737198fc14f",
        },
      )

      print(result)

      """
      Other example calls include:

      # List available resources
      resources = await session.list_resources()

      # List available tools
      tools = await session.list_tools()

      # Read a resource
      resource = await session.read_resource("file://some/path")

      # Call a tool
      result = await session.call_tool("tool-name", arguments={"arg1": "value"})
      """


if __name__ == "__main__":
  import asyncio

  asyncio.run(run())
