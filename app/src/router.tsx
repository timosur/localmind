import { createBrowserRouter } from "react-router-dom";

import { RootLayout } from "./layout";
import { Chat } from "@/pages/Chat";
import { Start } from "@/pages/Start";
import { Settings } from "@/pages/Settings";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout></RootLayout>,
    children: [
      {
        path: "/",
        element: <Start />,
      },
      {
        path: "chat",
        element: <Chat />,
        children: [
          {
            path: ":id",
            element: <Chat />,
          },
        ],
      },
      {
        path: "/settings",
        element: <Settings />,
      }
    ],
  },
  {
    path: "*",
    element: <RootLayout></RootLayout>,
  },
])