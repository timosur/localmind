import asyncio
from datetime import datetime
import logging
from contextlib import AsyncExitStack
import uuid

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from chat.handler import send_chat_message
from config import APP_CONFIG

# Configure logging
logging.basicConfig(
  level=logging.DEBUG,  # Setzt das Logging-Level auf DEBUG
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  handlers=[
    logging.StreamHandler()  # Gibt Logs auf der Konsole aus
  ],
)

app = FastAPI()


# Create server parameters for stdio connection
@app.websocket("/chat")
async def chat(websocket: WebSocket):
  client_sessions = []

  try:
    await websocket.accept()

    async with AsyncExitStack() as stack:
      # Connect to all servers and set up client sessions
      for server_config in APP_CONFIG.server:
        try:
          logging.debug(f"[{server_config['name']}] Try to connect")
          logging.debug(f"[{server_config['name']}] {server_config}")

          server_params = StdioServerParameters(
            command=server_config["command"],
            args=server_config.get("args", []),
          )

          # Enter the stdio_client async context
          read, write = await stack.enter_async_context(stdio_client(server_params))

          # Enter the ClientSession async context
          client_session = await stack.enter_async_context(ClientSession(read, write))

          # Initialize the connection
          await client_session.initialize()
          logging.info(f"[{server_config['name']}] Connected")

          client_sessions.append((server_config["name"], client_session))
        except Exception as e:
          logging.error(f"[{server_config['name']}] Error connecting: {str(e)}")
          # Optionally re-raise if you want to fail completely on any server connection error
          # raise

      def convert_message(role: str, type: str, content: str):
        return {
          "id": uuid.uuid4().hex,
          "role": role,
          "type": type,
          "isLoading": False,  # TODO: Implement loading state
          "content": content,
          "timestamp": datetime.now().isoformat(),
        }

      while True:
        try:
          message = await websocket.receive_text()

          # Process the chat message and stream messages back to the client
          async for role, type, content in send_chat_message(
            client_sessions, user_message=message
          ):
            if websocket.client_state.value == WebSocketState.DISCONNECTED:
              logging.info("Client disconnected during message streaming")
              return

            try:
              await websocket.send_json(convert_message(role, type, content))
            except WebSocketDisconnect:
              logging.info("Client disconnected while sending response")
              return

            await asyncio.sleep(0)  # Allow other tasks to run

        except WebSocketDisconnect:
          logging.info("Client disconnected while receiving message")
          return
        except Exception as e:
          logging.error(f"Error processing message: {str(e)}")
          try:
            await websocket.send_json(
              convert_message("system", "error", str(e), isError=True)
            )
          except (WebSocketDisconnect, RuntimeError):
            logging.info("Client disconnected while sending error")
            return

  except WebSocketDisconnect:
    logging.info("Client disconnected during connection setup")
  except Exception as e:
    logging.error(f"Unexpected error in websocket handler: {str(e)}")


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
