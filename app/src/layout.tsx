import "./globals.css";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import { GitHubLogoIcon } from "@radix-ui/react-icons";
import { ThemeProvider } from "@/components/theme-provider";
import { ModeToggle } from "@/components/mode-toggle";
import ChatSupport from "@/components/chat/chat-support";
import { Outlet } from "react-router-dom";

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: 1,
};

export function RootLayout() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <main className="flex h-[calc(100dvh)] flex-col items-center justify-center p-4 md:px-24 py-32 gap-4">
        <div className="flex justify-between max-w-5xl w-full items-center">
          <div className="flex gap-3 md:gap-6 items-center">
            <a
              href="#"
              className="text-xl sm:text-2xl md:text-4xl font-bold text-gradient"
            >
              MCP LLM Chat
            </a>
          </div>
          <div className="flex gap-1 items-center">
            <a
              href="https://github.com/timosur/standalone-mcp-chat"
              className={cn(
                buttonVariants({ variant: "ghost", size: "icon" }),
                "size-7",
              )}
            >
              <GitHubLogoIcon className="size-7" />
            </a>
            <ModeToggle />
          </div>
        </div>

        <div className="z-10 border rounded-lg max-w-5xl w-full h-full text-sm flex">
          {/* Page content */}
          <Outlet />
        </div>

        {/* Footer */}
        <div className="flex justify-between max-w-5xl w-full items-start text-xs md:text-sm text-muted-foreground ">
          <p className="max-w-[150px] sm:max-w-lg">
            Built by{" "}
            <a
              className="font-semibold"
              href="https://github.com/timosur/"
            >
              Timo Sur
            </a>
            .
          </p>
          <p className="max-w-[150px] sm:max-w-lg text-right">
            Source code available on{" "}
            <a
              className="font-semibold"
              href="https://github.com/timosur/standalone-mcp-chat"
            >
              GitHub
            </a>
            .
          </p>
        </div>

        {/* Chat support component */}
        <ChatSupport />
      </main>
    </ThemeProvider>
  );
}