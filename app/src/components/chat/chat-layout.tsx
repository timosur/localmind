import { useEffect, useState } from "react";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import { cn } from "@/lib/utils";
import { Sidebar } from "../sidebar";
import { Chat } from "./chat";
import useChatStore from "@/hooks/useChatStore";
import { useParams } from "react-router-dom";

interface ChatLayoutProps {
  navCollapsedSize: number;
  defaultCollapsed?: boolean;
}

const fetchChats = (): Promise<any[]> =>
  fetch("http://localhost:8000/chat").then((res) => res.json());

export function ChatLayout({
  navCollapsedSize,
  defaultCollapsed = false,
}: ChatLayoutProps) {
  const { id } = useParams();
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);
  const [isMobile, setIsMobile] = useState(false);
  const [chats, setChats] = useState<any[]>([]);
  const setSelectedChat = useChatStore((state) => state.setSelectedChat);
  const createChat = useChatStore((state) => state.createChat);

  useEffect(() => {
    const checkScreenWidth = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    // Initial check
    checkScreenWidth();

    // Event listener for screen width changes
    window.addEventListener("resize", checkScreenWidth);

    fetchChats().then((chats) => {
      setChats(chats);
      setSelectedChat(chats.find((chat) => chat.id === id));
    });

    // Cleanup the event listener on component unmount
    return () => {
      window.removeEventListener("resize", checkScreenWidth);
    };
  }, [id]);

  return (
    <ResizablePanelGroup
      direction="horizontal"
      className="h-full items-stretch"
    >
      <ResizablePanel
        defaultSize={320}
        collapsedSize={navCollapsedSize}
        collapsible={true}
        minSize={isMobile ? 0 : 24}
        maxSize={isMobile ? 8 : 30}
        onCollapse={() => {
          setIsCollapsed(true);
        }}
        onExpand={() => {
          setIsCollapsed(false);
        }}
        className={cn(
          isCollapsed &&
          "min-w-[50px] md:min-w-[70px] transition-all duration-300 ease-in-out",
        )}
      >
        <Sidebar
          isCollapsed={isCollapsed || isMobile}
          chats={chats?.map((chat) => ({
            id: chat.id,
            title: chat.title,
            messages: [],
            variant: chat.id === id ? "secondary" : "ghost",
          }))}
          isMobile={isMobile}
          createAction={createChat}
        />
      </ResizablePanel>
      <ResizableHandle withHandle />
      <ResizablePanel defaultSize={480} minSize={30}>
        <Chat
          isMobile={isMobile}
        />
      </ResizablePanel>
    </ResizablePanelGroup>
  );
}