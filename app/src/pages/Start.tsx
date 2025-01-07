import { Button } from "@/components/ui/button";

export function Start() {
  return (
    <div className="flex flex-row justify-center items-center h-full w-full">
      <a href="/chat" className="mr-4 w-3/6 h-3/6 flex flex-col items-end justify-center">
        <Button className="bg-blue-300 bg-opacity-75 text-lg p-4 flex flex-col items-center w-3/6 h-3/6">
          <h3>Go to Chat</h3>
          <small className="text-sm">Start chatting with others</small>
        </Button>
      </a>
      <a href="/settings" className="w-3/6 h-3/6 flex flex-col items-left justify-center">
        <Button className="bg-blue-300 bg-opacity-75  text-lg p-4 flex flex-col items-center w-3/6 h-3/6">
          <h3>Go to Settings</h3>
          <small className="text-sm">Adjust your preferences</small>
        </Button>
      </a>
    </div>
  )
}