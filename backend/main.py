import asyncio
import logging
import json
from contextlib import AsyncExitStack

from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uvicorn
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketState
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from sqlalchemy.ext.asyncio import AsyncSession

from db.model.chat import Chat, ChatMessage
from db import get_async_session
from chat.handler import send_chat_message
from config import APP_CONFIG
from db.model import Base
from db import sync_engine

# Configure logging
logging.basicConfig(
  level=logging.DEBUG,  # Setzt das Logging-Level auf DEBUG
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  handlers=[
    logging.StreamHandler()  # Gibt Logs auf der Konsole aus
  ],
)

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Create the database tables
Base.metadata.create_all(sync_engine)


@app.get("/chat")
async def list_chats(session: AsyncSession = Depends(get_async_session)):
  stmt = select(Chat).options(selectinload(Chat.messages))
  result = await session.execute(stmt)
  chats = result.scalars().all()

  return chats


@app.post("/chat")
async def create_chat(session: AsyncSession = Depends(get_async_session)):
  chat = Chat()
  session.add(chat)
  await session.commit()

  return chat.id


@app.get("/chat/{chat_id}")
async def get_chat(chat_id: str, session: AsyncSession = Depends(get_async_session)):
  stmt = select(Chat).options(selectinload(Chat.messages)).filter(Chat.id == chat_id)
  result = await session.execute(stmt)
  chat = result.scalars().first()

  return chat


# Create server parameters for stdio connection
@app.websocket("/chat")
async def chat(
  websocket: WebSocket,
  id: str = None,
  session: AsyncSession = Depends(get_async_session),
):
  client_sessions = []
  chat_interaction_history = []
  messages = []

  if id is None:
    chat = Chat()
    session.add(chat)
    await session.commit()
    id = chat.id
  else:
    stmt = select(Chat).filter(Chat.id == id)
    result = await session.execute(stmt)
    chat = result.scalars().first()
    if chat is None:
      return {"error": "Chat not found"}, 404

    # Load all messages for the chat
    stmt = select(ChatMessage).filter(ChatMessage.chat_id == id)
    result = await session.execute(stmt)
    messages = result.scalars().all()

    # Parse the interaction history from the messages
    for message in messages:
      chat_interaction_history.extend(json.loads(message.interaction_history))

  logging.debug(f"Chat ID: {id}")
  logging.debug(f"Chat Interaction History: {chat_interaction_history}")

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

      async def create_message(
        role: str, type: str, content: str, interaction_history=[]
      ):
        # Create message in database
        message = ChatMessage(
          chat_id=id,
          role=role,
          type=type,
          content=content,
          interaction_history=json.dumps(interaction_history),
        )
        session.add(message)
        await session.commit()

        return message.to_dict()

      while True:
        try:
          message = await websocket.receive_text()

          # Process the chat message and stream messages back to the client
          async for role, type, content, interaction_history in send_chat_message(
            client_sessions,
            user_message=message,
            chat_interaction_history=chat_interaction_history,
          ):
            if websocket.client_state.value == WebSocketState.DISCONNECTED:
              logging.info("Client disconnected during message streaming")
              return

            try:
              message = await create_message(role, type, content, interaction_history)
              await websocket.send_json(message)
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
            message = await create_message("system", "error", str(e), isError=True)
            await websocket.send_json(message)
          except (WebSocketDisconnect, RuntimeError):
            logging.info("Client disconnected while sending error")
            return

  except WebSocketDisconnect:
    logging.info("Client disconnected during connection setup")
  except Exception as e:
    logging.error(f"Unexpected error in websocket handler: {str(e)}")


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
