import { createBrowserRouter } from "react-router-dom";

import { RootLayout } from "@/layout";
import { NotFound } from "@/pages/NotFound";
import { Chat } from "@/pages/Chat";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      {
        path: "",
        element: <Chat></Chat>,
      },
    ],
  },
  {
    path: "*",
    element: <NotFound />,
  },
])