import { Message, UserData } from "@/_data";
import ChatTopbar from "./chat-topbar";
import { ChatList } from "./chat-list";
import useChatStore from "@/hooks/useChatStore";

interface ChatProps {
  messages?: Message[];
  selectedUser: UserData;
  isMobile: boolean;
}

export function Chat({ messages, selectedUser, isMobile }: ChatProps) {
  const messagesState = useChatStore((state) => state.messages);


  return (
    <div className="flex flex-col justify-between w-full h-full">
      <ChatTopbar selectedUser={selectedUser} />

      <ChatList
        messages={messagesState}
        selectedUser={selectedUser}
        isMobile={isMobile}
      />
    </div>
  );
}