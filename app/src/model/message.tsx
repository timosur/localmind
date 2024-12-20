export interface Message<TContent = any> {
  id: number;
  role: "user" | "assistent" | "system";
  type: "tool_response" | "tool_call" | "message" | "error";
  isLoading?: boolean;
  content?: TContent;
  timestamp?: string;
}