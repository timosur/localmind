from datetime import datetime
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.model.base import Base


class ChatMessage(Base):
  __tablename__ = "messages"
  id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
  chat_id = Column(String, ForeignKey("chats.id"), nullable=False)
  role = Column(String)
  type = Column(String)
  isLoading = Column(Boolean)
  content = Column(String)
  timestamp = Column(String, default=lambda: datetime.now().isoformat())

  def to_dict(self):
    return {
      "id": self.id,
      "role": self.role,
      "type": self.type,
      "isLoading": self.isLoading,
      "content": self.content,
      "timestamp": self.timestamp,
    }


class Chat(Base):
  __tablename__ = "chats"
  id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
  messages = relationship("ChatMessage", backref="chat")

  def to_dict(self):
    return {
      "id": self.id,
      "messages": [message.to_dict() for message in self.messages],
    }
