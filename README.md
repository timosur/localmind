# LocalMind

LocalMind is an local LLM Chat App fully compatible with the Model Context Protocol.
It uses Azure OpenAI as a LLM backend and you can connect it to all MCP Servers out there.

## Development

Create a .env file in the backend folder:

```txt
APP_CONFIG_FILE_PATH=config.yaml
AZURE_OPENAI_API_KEY=x
AZURE_OPENAI_DEPLOYMENT=x
AZURE_OPENAI_ENDPOINT=https://x.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-07-01-preview
AZURE_OPENAI_CHAT_MODEL=gpt-4o
AZURE_OPENAI_EMBEDDINGS_MODEL=embedding
```

```yaml
server:
- name: [SERVER_NAME]
  command: [SERVER_COMMAND]
  args:
  - [SERVER_ARGS]
[...]
```

To work on the frontend in browser with the python backend up and running:

```bash
./dev.sh frontend-dev
```

To run the Tauri App in development mode with the python backend:

```bash
./dev.sh app-dev
```

## Important

Currently only works with Azure OpenAI Service.
