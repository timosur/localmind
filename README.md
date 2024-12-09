# Backend:

create `.env` in `backend` folder with

```
OPENAI_API_KEY=xxx
```

Create or use venv

````
python3.12 -m venv .venv
source .venv/bin/activate
```

when you are done developing

`deactivate`

```bash

pip install uv
uv sync --reinstall
pyinstaller main.py --onefile

i needed to use:
python -m PyInstaller main.py --onefile

```

Important: The `main.py` file must be in the root directory of the project. Also currently the uv dependencies need to be installed via pip, too.

`pip install anyio asyncio fastapi openai python-dotenv requests rich uvicorn pyinstaller`

# Frontend:

create `.env` in `backend` folder with

configure `server_config.json` to use you folders.


```
OPENAI_API_KEY=xxx
```

```bash
npm install
npm start
```

# Important

urrently only works with Azure Cognitive Services.

# Building

PyInstaller is tested against Windows, MacOS X, and Linux. However, it is not a cross-compiler; to make a Windows app you run PyInstaller on Windows, and to make a Linux app you run it on Linux, etc.
````
