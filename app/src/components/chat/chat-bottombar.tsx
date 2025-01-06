import {
  FileImage,
  Mic,
  Paperclip,
  PlusCircle,
  SendHorizontal,
} from "lucide-react";
import React, { useEffect, useRef, useState } from "react";
import { Button, buttonVariants } from "../ui/button";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";
import { Popover, PopoverContent, PopoverTrigger } from "../ui/popover";
import { ChatInput } from "../ui/chat/chat-input";
import { useChatMessagesContext } from "@/hooks/useChatMessageContext";

interface ChatBottombarProps {
  isMobile: boolean;
}

export const BottombarIcons = [{ icon: FileImage }, { icon: Paperclip }];

export default function ChatBottombar({ isMobile }: ChatBottombarProps) {
  const [message, setMessage] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const { sendMessage, canSendMessages } = useChatMessagesContext();

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(event.target.value);
  };

  const handleSend = () => {
    if (!message.trim()) {
      return;
    }

    if (canSendMessages) {
      sendMessage(message);
      setMessage("");
    } else {
      console.error("WebSocket is not open.");
    }

    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleKeyPress = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }

    if (event.key === "Enter" && event.shiftKey) {
      event.preventDefault();
      setMessage((prev) => prev + "\n");
    }
  };

  return (
    <div className="px-2 py-4 flex justify-between w-full items-center gap-2">
      <div className="flex">
        <Popover>
          <PopoverTrigger asChild>
            <a
              href="#"
              className={cn(
                buttonVariants({ variant: "ghost", size: "icon" }),
                "h-9 w-9",
                "shrink-0",
              )}
            >
              <PlusCircle size={22} className="text-muted-foreground" />
            </a>
          </PopoverTrigger>
          <PopoverContent side="top" className="w-full p-2">
            {message.trim() || isMobile ? (
              <div className="flex gap-2">
                <a
                  href="#"
                  className={cn(
                    buttonVariants({ variant: "ghost", size: "icon" }),
                    "h-9 w-9",
                    "shrink-0",
                  )}
                >
                  <Mic size={22} className="text-muted-foreground" />
                </a>
                {BottombarIcons.map((icon, index) => (
                  <a
                    key={index}
                    href="#"
                    className={cn(
                      buttonVariants({ variant: "ghost", size: "icon" }),
                      "h-9 w-9",
                      "shrink-0",
                    )}
                  >
                    <icon.icon size={22} className="text-muted-foreground" />
                  </a>
                ))}
              </div>
            ) : (
              <a
                href="#"
                className={cn(
                  buttonVariants({ variant: "ghost", size: "icon" }),
                  "h-9 w-9",
                  "shrink-0",
                )}
              >
                <Mic size={22} className="text-muted-foreground" />
              </a>
            )}
          </PopoverContent>
        </Popover>
        {!message.trim() && !isMobile && (
          <div className="flex">
            {BottombarIcons.map((icon, index) => (
              <a
                key={index}
                href="#"
                className={cn(
                  buttonVariants({ variant: "ghost", size: "icon" }),
                  "h-9 w-9",
                  "shrink-0",
                )}
              >
                <icon.icon size={22} className="text-muted-foreground" />
              </a>
            ))}
          </div>
        )}
      </div>

      <AnimatePresence initial={false}>
        <motion.div
          key="input"
          className="w-full relative"
          layout
          initial={{ opacity: 0, scale: 1 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 1 }}
          transition={{
            opacity: { duration: 0.05 },
            layout: {
              type: "spring",
              bounce: 0.15,
            },
          }}
        >
          <ChatInput
            value={message}
            ref={inputRef}
            onKeyDown={handleKeyPress}
            onChange={handleInputChange}
            placeholder="Type a message..."
            className="rounded-full"
            disabled={!canSendMessages}
          />
        </motion.div>

        {message.trim() ? (
          <Button
            className="h-9 w-9 shrink-0"
            onClick={handleSend}
            disabled={!canSendMessages}
            variant="ghost"
            size="icon"
          >
            <SendHorizontal size={22} className="text-muted-foreground" />
          </Button>
        ) : <></>}
      </AnimatePresence>
    </div>
  );
}