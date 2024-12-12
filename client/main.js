const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile('index.html');

  // Start the Python backend
  // If development, use the Python script in the parent directory
  // If production, use the Python script in the resources directory
  if (process.env.NODE_ENV === 'development') {
    pythonProcess = spawn('../.venv/bin/python3', ['../backend/main.py']);
  } else {
    pythonProcess = spawn('../backend/dist/main');
  }

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python backend: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python backend error: ${data}`);
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (pythonProcess) {
      pythonProcess.kill();
    }
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});