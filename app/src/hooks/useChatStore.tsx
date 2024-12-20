import { chatData } from "@/_data";
import { Chat } from "@/model/chat";
import { Message } from "@/model/message";
import { create } from "zustand";

export interface Example {
  name: string;
  url: string;
}

interface State {
  input: string;
  messages: Message[];
}

interface Actions {
  selectedChat: Chat;
  setInput: (input: string) => void;
  handleInputChange: (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLTextAreaElement>,
  ) => void;
  setMessages: (fn: (messages: Message[]) => Message[]) => void;
}

const useChatStore = create<State & Actions>()((set) => ({
  selectedChat: chatData[0],

  input: "",

  setInput: (input) => set({ input }),
  handleInputChange: (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLTextAreaElement>,
  ) => set({ input: e.target.value }),

  messages: chatData[0].messages,
  setMessages: (fn) => set(({ messages }) => ({ messages: fn(messages) })),
}));

export default useChatStore;