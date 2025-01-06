"use client";

import { MoreHorizontal, SquarePen } from "lucide-react";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
  TooltipProvider,
} from "@/components/ui/tooltip";
import { Message } from "@/model/message";

interface SidebarProps {
  isCollapsed: boolean;
  chats: {
    id: string;
    title: string;
    messages: Message[];
    variant: "secondary" | "ghost";
  }[];
  createAction?: () => void;
  isMobile: boolean;
}

export function Sidebar({ chats, isCollapsed, createAction }: SidebarProps) {
  return (
    <div
      data-collapsed={isCollapsed}
      className="relative group flex flex-col h-full bg-muted/10 dark:bg-muted/20 gap-4 p-2 data-[collapsed=true]:p-2 "
    >
      {!isCollapsed && (
        <div className="flex justify-between p-2 items-center">
          <div className="flex gap-2 items-center text-2xl">
            <p className="font-medium">Chats</p>
            <span className="text-zinc-300">({chats.length})</span>
          </div>

          <div className="cursor-pointer">
            <SquarePen onClick={createAction} size={20} />
          </div>
        </div>
      )}
      <nav className="grid gap-1 px-2 group-[[data-collapsed=true]]:justify-center group-[[data-collapsed=true]]:px-2">
        {chats.map((chat, index) =>
          isCollapsed ? (
            <TooltipProvider key={index}>
              <Tooltip key={index} delayDuration={0}>
                <TooltipTrigger asChild>
                  <a
                    href={`/chat/${chat.id}`}
                    className={cn(
                      buttonVariants({ variant: chat.variant, size: "icon" }),
                      "h-11 w-11 md:h-16 md:w-16",
                      chat.variant === "secondary" &&
                      "dark:bg-muted dark:text-muted-foreground dark:hover:bg-muted dark:hover:text-white",
                    )}
                  >
                    <span className="sr-only">{chat.title}</span>
                  </a>
                </TooltipTrigger>
                <TooltipContent
                  side="right"
                  className="flex items-center gap-4"
                >
                  {chat.title}
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          ) : (
            <a
              key={index}
              href={`/chat/${chat.id}`}
              className={cn(
                buttonVariants({ variant: chat.variant, size: "xl" }),
                chat.variant === "secondary" &&
                "dark:bg-muted dark:text-white dark:hover:bg-muted dark:hover:text-white shrink",
                "justify-start gap-4",
              )}
            >
              <div className="flex flex-col max-w-28">
                <span>{chat.title}</span>
              </div>
            </a>
          ),
        )}
      </nav>
    </div>
  );
}