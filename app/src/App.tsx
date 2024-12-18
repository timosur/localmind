import "./App.css";
import { useEffect, useState, useRef } from "react";

function App() {
  const [messages, setMessages] = useState<{ role: string; content?: string; tool_call?: { name: string; arguments: string } }[]>([]);
  const [input, setInput] = useState("");
  const ws = useRef<WebSocket | null>(null);
  const messageQueue = useRef<string[]>([]);

  const wsUrl = "ws://localhost:8000/chat?command=/Users/timosur/code/standalone-mcp-chat/rag/.venv/bin/python3&args=/Users/timosur/code/standalone-mcp-chat/rag/main.py,/Users/timosur/code/standalone-mcp-chat";

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (ws.current) ws.current.close();
    };
  }, [wsUrl]);

  const connectWebSocket = () => {
    console.log("Connecting to WebSocket...");
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      console.log("Connected to WebSocket");
      while (messageQueue.current.length > 0) {
        if (ws.current) {
          const message = messageQueue.current.shift();
          if (message !== undefined) {
            ws.current.send(message);
          }
        }
      }
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleStreamMessage(data);
    };

    ws.current.onclose = () => {
      console.log("WebSocket closed. Reconnecting...");
      setTimeout(connectWebSocket, 1000);
    };
  };

  const handleStreamMessage = (data: any) => {
    switch (data.type) {
      case "stream":
        const content = data.content;

        switch (content.type) {
          case "message":
            addMessage({
              role: content.role,
              content: content.content,
            });
            break;

          case "content":
            addMessage({
              role: "assistant",
              content: content.content,
            });
            break;

          case "tool_call":
            addMessage({
              role: "tool",
              tool_call: content.content,
            });
            break;

          case "tool_call_response":
            addMessage({
              role: "tool",
              content: content.content,
            });
            break;

          default:
            break;
        }
        break;

      case "error":
        addMessage({
          role: "system",
          content: `Error: ${data.content}`,
        });
        break;

      default:
        break;
    }
  };

  const addMessage = (message: { role: string; content?: string; tool_call?: { name: string; arguments: string } }) => {
    console.log("Adding message", message);
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  const sendMessage = () => {
    setMessages([]);

    if (!input.trim()) return;

    ws.current?.send(input);

    setInput("");
  };

  const getMessageIcon = (role: string) => {
    switch (role) {
      case "user":
        return "👤";
      case "assistant":
        return "🤖";
      case "tool":
        return "🔧";
      default:
        return "💻";
    }
  };

  const getRoleClass = (role: string) => {
    switch (role) {
      case "user":
        return "bg-blue-100";
      case "assistant":
        return "bg-green-100";
      case "tool":
        return "bg-yellow-100";
      case "system":
        return "bg-gray-100";
      default:
        return "bg-gray-100";
    }
  };

  console.log(messages)

  return (
    <div className="max-w-3xl mx-auto bg-white rounded-lg shadow p-5">
      <h1 className="text-2xl font-bold mb-4">Chat Response Display</h1>
      <div id="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-5 p-4 rounded-lg ${getRoleClass(message.role)}`}
          >
            <div className="flex items-center mb-2.5">
              <div className="w-6 h-6 mr-2.5 p-1.5 bg-white rounded-full flex items-center justify-center">
                {getMessageIcon(message.role)}
              </div>
              <span className="font-bold capitalize">
                {message.role}
              </span>
            </div>
            <div className="ml-11 whitespace-pre-wrap">
              {message.content}
              {message.tool_call && (
                <div className="bg-gray-100 p-2.5 rounded mt-2.5 font-mono">
                  <div>Function: {message.tool_call.name}</div>
                  <div>Arguments: {message.tool_call.arguments}</div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-5 flex gap-2.5">
        <input
          type="text"
          className="flex-1 p-2 border border-gray-300 rounded"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter message"
        />
        <button
          className="px-4 py-2 bg-green-500 text-white rounded cursor-pointer hover:bg-green-600"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
