import ChatTopbar from "./chat-topbar";
import { ChatList } from "./chat-list";
import useChatStore from "@/hooks/useChatStore";
import { Chat as ChatModel } from "@/model/chat";

interface ChatProps {
  selectedChat: ChatModel;
  isMobile: boolean;
}

export function Chat({ selectedChat, isMobile }: ChatProps) {
  const messagesState = useChatStore((state) => state.messages);

  return (
    <div className="flex flex-col justify-between w-full h-full">
      <ChatTopbar selectedChat={selectedChat} />

      <ChatList
        messages={messagesState}
        isMobile={isMobile}
      />
    </div>
  );
}