import { cn } from "@/lib/utils";
import { Chat } from "@/model/chat";
import { Info } from "lucide-react";
import { buttonVariants } from "../ui/button";
import { ExpandableChatHeader } from "../ui/chat/expandable-chat";

interface ChatTopbarProps {
  selectedChat: Chat;
}

export const TopbarIcons = [{ icon: Info }];

export default function ChatTopbar({ selectedChat }: ChatTopbarProps) {
  return (
    <ExpandableChatHeader>
      <div className="flex items-center gap-2">
        <div className="flex flex-col">
          <span className="font-medium">{selectedChat.title}</span>
        </div>
      </div>

      <div className="flex gap-1">
        {TopbarIcons.map((icon, index) => (
          <a
            key={index}
            href="#"
            className={cn(
              buttonVariants({ variant: "ghost", size: "icon" }),
              "h-9 w-9",
            )}
          >
            <icon.icon size={20} className="text-muted-foreground" />
          </a>
        ))}
      </div>
    </ExpandableChatHeader>
  );
}