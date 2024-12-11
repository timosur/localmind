import logging
from config import load_config
from messages.send_initialize_message import send_initialize
from chat_handler import send_chat_message
from transport.stdio.stdio_client import stdio_client
from fastapi import FastAPI, WebSocket
import uvicorn
import asyncio

# Default path for the configuration file
DEFAULT_CONFIG_FILE = "server_config.json"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Setzt das Logging-Level auf DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Gibt Logs auf der Konsole aus
    ]
)

app = FastAPI()

# Global variables to store initialized streams
read_stream = None
write_stream = None
stdio_client_context = None

@app.on_event("startup")
async def startup_event():
    global read_stream, write_stream, stdio_client_context
    
    # Load server configuration
    server_params = await load_config(DEFAULT_CONFIG_FILE, "filesystem")
    
    # Initialize stdio client and streams
    stdio_client_context = stdio_client(server_params)
    read_stream, write_stream = await stdio_client_context.__aenter__()
    
    # Initialize the server
    init_result = await send_initialize(read_stream, write_stream)
    if not init_result:
        raise RuntimeError("Server initialization failed")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        try:
            message = await websocket.receive_text()
            
            # Process the chat message and stream response
            async for response in send_chat_message(read_stream, write_stream, user_message=message):
                await websocket.send_json({
                    "type": "stream",
                    "content": response
                })
                await asyncio.sleep(0)  # Allow other tasks to run
                    
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "content": str(e)
            })
            break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)