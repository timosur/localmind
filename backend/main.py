import asyncio
import logging

import uvicorn
from chat.handler import send_chat_message
from fastapi import FastAPI, WebSocket
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

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
async def chat(
  websocket: WebSocket, command: str = "python3", args: str = None, env: str = None
):
  await websocket.accept()
  # Log the query parameters
  logging.debug(
    f"WebSocket connection established with command: {command}, args: {args}, env: {env}"
  )

  # Update server_params with query string values
  server_params = StdioServerParameters(
    command=command,
    args=args.split(",") if args else [],
    env=dict(e.split("=") for e in env.split(",")) if env else {},
  )

  async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
      # Initialize the connection
      await session.initialize()
      while True:
        try:
          message = await websocket.receive_text()

          # Process the chat message and stream response
          async for response in send_chat_message(session, user_message=message):
            await websocket.send_json({"type": "stream", "content": response})
            await asyncio.sleep(0)  # Allow other tasks to run

        except Exception as e:
          await websocket.send_json({"type": "error", "content": str(e)})
          break


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
