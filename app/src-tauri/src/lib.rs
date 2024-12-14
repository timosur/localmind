use tauri_plugin_shell::ShellExt;

#[tauri::command]
async fn start_py_backend(app_handle: tauri::AppHandle) {
  let sidecar_command = app_handle
    .shell()
    .sidecar("main")
    .unwrap();
  let (mut _rx, mut _child) = sidecar_command.spawn().unwrap();
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![start_py_backend])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
