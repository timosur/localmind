import { ChatLayout } from "@/components/chat/chat-layout";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ChatMessagesProvider } from "@/hooks/useChatMessageContext";

const queryClient = new QueryClient();

export function Chat() {
  return (
    <QueryClientProvider client={queryClient}>
      <ChatMessagesProvider>
        <ChatLayout navCollapsedSize={8} defaultCollapsed={false} />
      </ChatMessagesProvider>
    </QueryClientProvider>
  )
}