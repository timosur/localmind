// Import necessary hooks and libraries
import { createContext, useCallback, useContext, useEffect, ReactNode } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { useQueryClient } from "@tanstack/react-query";
import useChatStore from "./useChatStore";

// Define the type for the chat messages context
interface ChatMessagesContextType {
  canSendMessages: boolean;
  sendMessage: (content: string) => void;
}

// Create a context for chat messages
const ChatMessagesContext = createContext<ChatMessagesContextType | null>(null);

export const queryKey = ["chat_messages"];

// Define the ChatMessagesProvider component to provide chat messages context
interface ChatMessagesProviderProps {
  children: ReactNode;
}

export const ChatMessagesProvider = ({ children }: ChatMessagesProviderProps) => {
  const selectedChat = useChatStore((state) => state.selectedChat);

  if (!selectedChat) {
    return null;
  }

  // Initialize the WebSocket connection and retrieve necessary properties
  const {
    sendMessage: sM,
    lastMessage,
    readyState,
  } = useWebSocket("ws://localhost:8000/chat?id=" + selectedChat!.id, {
    shouldReconnect: () => true,
  });
  // Initialize the queryClient from react-query
  const queryClient = useQueryClient();
  // Check if WebSocket connection is open and ready for sending messages
  const canSendMessages = readyState === ReadyState.OPEN;

  // Handle the incoming WebSocket messages
  useEffect(() => {
    if (lastMessage && lastMessage.data) {
      const payload = JSON.parse(lastMessage.data);
      // Update the local chat messages state based on the message type
      queryClient.setQueryData(queryKey, (oldData: any) => {
        return [...oldData, payload];
      });
    }
  }, [lastMessage, queryClient]);

  // Define the sendMessage function to send messages through the WebSocket connection
  const sendMessage = useCallback(
    (content: string) => {
      if (canSendMessages)
        sM(content);
    },
    [canSendMessages, sM],
  );

  // Render the ChatMessagesContext.Provider component and pass the necessary values
  return (
    <ChatMessagesContext.Provider value={{ canSendMessages, sendMessage }}>
      {children}
    </ChatMessagesContext.Provider>
  );
};

// Define a custom hook to access the chat messages context
export const useChatMessagesContext = () => useContext(ChatMessagesContext);