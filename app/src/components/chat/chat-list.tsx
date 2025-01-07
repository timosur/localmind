import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import useChatStore from "@/hooks/useChatStore";
import { DesktopIcon, DotsVerticalIcon, PersonIcon } from "@radix-ui/react-icons";
import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useRef } from "react";
import ReactMarkdown from 'react-markdown';
import {
  ChatBubble,
  ChatBubbleAction,
  ChatBubbleActionWrapper,
  ChatBubbleMessage,
  ChatBubbleTimestamp,
} from "../ui/chat/chat-bubble";
import { ChatMessageList } from "../ui/chat/chat-message-list";
import ChatBottombar from "./chat-bottombar";
import { Terminal, TriangleAlertIcon } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ChatListProps {
  isMobile: boolean;
}

export function ChatList({
  isMobile,
}: ChatListProps) {
  const selectedChat = useChatStore((state) => state.selectedChat);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop =
        messagesContainerRef.current.scrollHeight;
    }
  }, [messagesContainerRef, selectedChat]);

  const actionIcons = [
    { icon: DotsVerticalIcon, type: "More" },
  ];

  return (
    <div className="w-full overflow-y-auto h-full flex flex-col">
      <ChatMessageList ref={messagesContainerRef}>
        <AnimatePresence>
          {!selectedChat && (
            <Alert>
              <TriangleAlertIcon className="h-5 w-5" />
              <AlertTitle>Hey!</AlertTitle>
              <AlertDescription>
                Select an existing chat or create a new one to start messaging,
              </AlertDescription>
            </Alert>
          )}
          {selectedChat && selectedChat.messages.length === 0 && (
            <Alert>
              <Terminal className="h-5 w-5" />
              <AlertTitle>Start chatting!</AlertTitle>
              <AlertDescription>
                Send your first message in this chat.
              </AlertDescription>
            </Alert>
          )}
          {selectedChat && selectedChat.messages.length > 0 ? selectedChat.messages.map((message, index) => {
            return (
              <motion.div
                key={index}
                layout
                initial={{ opacity: 0, scale: 1, y: 50, x: 0 }}
                animate={{ opacity: 1, scale: 1, y: 0, x: 0 }}
                exit={{ opacity: 0, scale: 1, y: 1, x: 0 }}
                transition={{
                  opacity: { duration: 0.1 },
                  layout: {
                    type: "spring",
                    bounce: 0.3,
                    duration: index * 0.05 + 0.2,
                  },
                }}
                style={{ originX: 0.5, originY: 0.5 }}
                className="flex flex-col gap-2 p-4"
              >
                {/* Usage of ChatBubble component */}
                <ChatBubble variant={message.role === "user" ? "sent" : "received"}>
                  <ChatBubbleMessage isLoading={message.isLoading}>
                    <div className="mb-2">
                      {message.role === "user" ? (
                        <PersonIcon className="size-7" />
                      ) : (
                        <DesktopIcon className="size-7" />
                      )}
                    </div>
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                    <small><ChatBubbleTimestamp timestamp={new Date(message.timestamp!).toLocaleString()} /></small>
                  </ChatBubbleMessage>
                  <ChatBubbleActionWrapper>
                    {actionIcons.map(({ icon: Icon, type }) => (
                      <ChatBubbleAction
                        className="size-7"
                        key={type}
                        icon={<Icon className="size-4" />}
                        onClick={() =>
                          console.log(
                            "Action " + type + " clicked for message " + index,
                          )
                        }
                      />
                    ))}
                  </ChatBubbleActionWrapper>
                </ChatBubble>
              </motion.div>
            );
          }) : null}
        </AnimatePresence>
      </ChatMessageList>
      <ChatBottombar isMobile={isMobile} />
    </div>
  );
}