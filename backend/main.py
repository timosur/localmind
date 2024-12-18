import asyncio
import logging

import uvicorn
from chat.handler import send_chat_message
from fastapi import FastAPI, WebSocket
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from contextlib import AsyncExitStack


# Configure logging
logging.basicConfig(
  level=logging.DEBUG,  # Setzt das Logging-Level auf DEBUG
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  handlers=[
    logging.StreamHandler()  # Gibt Logs auf der Konsole aus
  ],
)

app = FastAPI()

server_config = {
  "rag": {
    "command": "/Users/timosur/code/standalone-mcp-chat/rag/.venv/bin/python3",
    "args": ["/Users/timosur/code/standalone-mcp-chat/rag/main.py"],
  },
  "sqlite": {
    "command": "uvx",
    "args": [
      "mcp-server-sqlite",
      "--db-path",
      "/Users/timosur/code/standalone-mcp-chat/test.db",
    ],
  },
  "memory": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"]},
}


# Create server parameters for stdio connection
@app.websocket("/chat")
async def chat(websocket: WebSocket):
  await websocket.accept()

  client_sessions = []
  async with AsyncExitStack() as stack:
    # Connect to all servers and set up client sessions
    for server_name, params in server_config.items():
      try:
        logging.debug(f"[{server_name}] Try to connect using params {params}")

        server_params = StdioServerParameters(
          command=params["command"],
          args=params.get("args", []),
        )

        # Enter the stdio_client async context
        read, write = await stack.enter_async_context(stdio_client(server_params))

        # Enter the ClientSession async context
        client_session = await stack.enter_async_context(ClientSession(read, write))

        # Initialize the connection
        await client_session.initialize()
        logging.info(f"[{server_name}] Connected")

        client_sessions.append((server_name, client_session))
      except Exception as e:
        logging.error(f"[{server_name}] Error connecting: {str(e)}")

    # Now all sessions remain open as long as we're inside the async with stack block.
    while True:
      try:
        message = await websocket.receive_text()

        # Process the chat message and stream response
        async for response in send_chat_message(client_sessions, user_message=message):
          await websocket.send_json({"type": "stream", "content": response})
          await asyncio.sleep(0)  # Allow other tasks to run

      except Exception as e:
        await websocket.send_json({"type": "error", "content": str(e)})
        break


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
