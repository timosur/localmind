import { createBrowserRouter } from "react-router-dom";

import { Chat } from "@/pages/Chat";
import { RootLayout } from "./layout";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout></RootLayout>,
    children: [
      {
        path: "chat",
        element: <Chat></Chat>,
        children: [
          {
            path: ":id",
            element: <Chat></Chat>,
          },
        ],
      },
    ],
  },
  {
    path: "*",
    element: <RootLayout></RootLayout>,
  },
])