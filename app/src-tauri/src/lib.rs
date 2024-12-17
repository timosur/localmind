use std::sync::{Arc, Mutex};
use sysinfo::{Pid, Signal, System};

use tauri::Emitter;
use tauri::Manager;
use tauri_plugin_shell::process::CommandEvent;
use tauri_plugin_shell::ShellExt;

fn kill_process(pid: u32) {
    let s = System::new_all();
    if let Some(process) = s.process(Pid::from_u32(pid)) {
        process.kill_with(Signal::Term);

        println!("Process {} killed", pid);
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            // Your sidecar setup code goes here
            let window: tauri::WebviewWindow = app.get_webview_window("main").unwrap();
            let sidecar_command = app.shell().sidecar("main").unwrap();
            let (mut rx, sidecar_child) = sidecar_command.spawn().expect("Failed to spawn sidecar");

            println!("{}", sidecar_child.pid());

            // Wrap the child process in Arc<Mutex<>> for shared access
            let child = Arc::new(Mutex::new(Some(sidecar_child)));

            // Clone the Arc to move into the async task
            let child_clone = Arc::clone(&child);

            window.on_window_event(move |event| {
                if let tauri::WindowEvent::CloseRequested { .. } = event {
                    let mut child_lock = child_clone.lock().unwrap();
                    if let Some(child_process) = child_lock.take() {
                        kill_process(child_process.pid());
                    }
                }
            });

            tauri::async_runtime::spawn(async move {
                while let Some(event) = rx.recv().await {
                    match event {
                        CommandEvent::Stdout(line) => {
                            // Handle stdout
                            let output = String::from_utf8_lossy(&line);
                            println!("Stdout: {}", output);
                            // Optionally emit to frontend
                            window
                                .emit("sidecar-stdout", Some(output.to_string()))
                                .expect("failed to emit stdout");
                        }
                        CommandEvent::Stderr(line) => {
                            // Handle stderr
                            let error = String::from_utf8_lossy(&line);
                            eprintln!("Stderr: {}", error);
                            // Optionally emit to frontend
                            window
                                .emit("sidecar-stderr", Some(error.to_string()))
                                .expect("failed to emit stderr");
                        }
                        CommandEvent::Error(error) => {
                            // Handle process errors
                            eprintln!("Process error: {}", error);
                            window
                                .emit("sidecar-error", Some(error.to_string()))
                                .expect("failed to emit error");
                        }
                        CommandEvent::Terminated(payload) => {
                            // Handle process termination
                            println!("Process terminated with code: {:?}", payload.code);
                            window
                                .emit("sidecar-terminated", Some(payload.code))
                                .expect("failed to emit termination");
                        }
                        _ => {}
                    }
                }
            });

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
