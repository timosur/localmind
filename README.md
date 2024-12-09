# Backend:

```bash
pip install uv
uv sync --reinstall
pyinstaller main.py --onefile
```

Important: The `main.py` file must be in the root directory of the project. Also currently the uv dependencies need to be installed via pip, too.

# Frontend:

```bash
npm install
npm start
```

# Important:

Also you need to create a .env file in the client and backend folder with the following content:

```
OPENAI_API_KEY=xxx
```