class ChatMessage:
  id: str
  role: str
  type: str
  isLoading: bool
  content: str
  timestamp: str


class Chat:
  id: str
  messages: list[ChatMessage]
