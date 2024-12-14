import "./App.css";
import { Command } from '@tauri-apps/plugin-shell';

function App() {
  const runCommand = async () => {
    // notice that the args array matches EXACTLY what is specified on `tauri.conf.json`.
    const command = Command.sidecar('binaries/main');
    const output = await command.execute();

    console.log(output);
  };

  runCommand();

  return (
    <main className="container">
      <h1>Welcome to Tauri + React</h1>
    </main>
  );
}

export default App;
