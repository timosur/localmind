import { Chat } from "@/model/chat";
import { Message } from "@/model/message";
import { create } from "zustand";

const fetchChats = (): Promise<Chat[]> =>
  fetch("http://localhost:8000/chat").then((res) => res.json());

const createChat = (): Promise<Chat> =>
  fetch("http://localhost:8000/chat", {
    method: "POST",
  }).then((res) => res.json());


interface ChatState {
  input: string;
  chats: Chat[];
  setChats: (chats: Chat[]) => void;
  selectedChat: Chat | null;
  setSelectedChat: (chat: Chat) => void;
  setInput: (input: string) => void;
  handleInputChange: (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLTextAreaElement>,
  ) => void;
  createChat: () => void;
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

  chats: [],
  setChats: (chats) => set({ chats }),
  selectedChat: null,
  setSelectedChat: (selectedChat) => set({ selectedChat }),

  createChat: async () => {
    const newChat = await createChat();
    location.href = "/chat/" + newChat.id;
  },
  appendMessage: (message: Message) => set((state) => ({
    selectedChat: {
      ...state.selectedChat,
      messages: [...state.selectedChat!.messages, message],
    },
  } as any)),
}));

export default useChatStore;