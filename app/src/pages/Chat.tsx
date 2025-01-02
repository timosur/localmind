import { ChatLayout } from "@/components/chat/chat-layout";
import { Suspense } from "react";

export function Chat() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ChatLayout navCollapsedSize={8} defaultCollapsed={false} />
    </Suspense>
  )
}