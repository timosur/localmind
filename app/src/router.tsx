import { createBrowserRouter } from "react-router-dom";

import { RootLayout } from "@/layout";
import { ChatLayout } from "@/components/chat/chat-layout";
import { NotFound } from "@/pages/NotFound";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      {
        path: "",
        element: <ChatLayout defaultLayout={[0, 0]} navCollapsedSize={8} />,
      },
    ],
  },
  {
    path: "*",
    element: <NotFound />,
  },
])