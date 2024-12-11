# MCP Standalone Client

## Backend

Create `.env` in `backend` folder with

```
OPENAI_API_KEY=xxx
```

Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

When you are done developing

```bash
deactivate
```

To build the backend in one file for the frontend:

```bash
python3 -m PyInstaller main.py --onefile
```

## Frontend

Create `.env` in `client` folder with

```bash
OPENAI_API_KEY=xxx
```

configure `server_config.json` to use your folders.

```bash
npm install
npm start
```

## Important

Currently only works with Azure OpenAI Service.
