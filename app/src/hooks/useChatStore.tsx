import { Chat } from "@/model/chat";
import { Message } from "@/model/message";
import { create } from "zustand";
import { hook, effect, query, Query, Effect } from "leo-query";

const fetchChats = (): Promise<Chat[]> =>
  fetch("http://localhost:8000/chat").then((res) => res.json());

const createChat = (): Promise<void> =>
  fetch("http://localhost:8000/chat", {
    method: "POST",
  }).then((res) => res.json());


interface ChatState {
  input: string;
  chats: Query<ChatState, Chat[]>;
  selectedChat: Chat | null;
  setSelectedChat: (chat: Chat) => void;
  setInput: (input: string) => void;
  handleInputChange: (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLTextAreaElement>,
  ) => void;
  createChat: Effect<ChatState, []>;
  appendMessage: (message: Message) => void;
}

const useChatStore = create<ChatState>()((set) => ({
  input: "",

  setInput: (input) => set({ input }),
  handleInputChange: (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLTextAreaElement>,
  ) => set({ input: e.target.value }),

  chats: query(fetchChats),
  selectedChat: null,
  setSelectedChat: (selectedChat) => set({ selectedChat }),

  createChat: effect(createChat),
  appendMessage: (message: Message) => set((state) => ({
    selectedChat: {
      ...state.selectedChat,
      messages: [...state.selectedChat!.messages, message],
    },
  } as any)),
}));

export default useChatStore;

export const useChatStoreAsync = hook(useChatStore);