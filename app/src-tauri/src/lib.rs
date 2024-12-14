use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandEvent;

#[tauri::command]
async fn start_py_backend(app: tauri::AppHandle) {
  let sidecar_command = app.shell().sidecar("main").unwrap();
  let (mut rx, mut _child) = sidecar_command
    .spawn()
    .expect("Failed to spawn sidecar");

  tauri::async_runtime::spawn(async move {
    // read events such as stdout
    while let Some(event) = rx.recv().await {
      if let CommandEvent::Stdout(line_bytes) = event {
        let line = String::from_utf8_lossy(&line_bytes);
        println!("stdout: {}", line);
      }
    }
  });
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![start_py_backend])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
