import logging
import sys
import anyio
from config import load_config
from messages.send_initialize_message import send_initialize
from chat_handler import send_chat_message
from transport.stdio.stdio_client import stdio_client
from fastapi import FastAPI
import uvicorn

# Default path for the configuration file
DEFAULT_CONFIG_FILE = "server_config.json"

# Configure logging
logging.basicConfig(
    level=logging.CRITICAL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)

app = FastAPI()


@app.get("/")
async def send_message(message: str):
    result = None

    """Main function to manage server initialization, communication, and shutdown."""
    # Load server configuration
    server_params = await load_config(DEFAULT_CONFIG_FILE, "filesystem")

    # Establish stdio communication
    async with stdio_client(server_params) as (read_stream, write_stream):
        # Initialize the server
        init_result = await send_initialize(read_stream, write_stream)
        if not init_result:
            print("[red]Server initialization failed[/red]")
            return

        # Startup fastapi server
        result = await send_chat_message(
            read_stream, write_stream, user_message=message
        )

        # Try closing streams with a timeout
        with anyio.move_on_after(1):  # wait up to 1 second
            await read_stream.aclose()
            await write_stream.aclose()

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
