from db.model.chat import Chat, ChatMessage


def create_chat(db, chat: Chat):
  db.add(chat)
  db.commit()
  db.refresh(chat)
  return chat


def create_message(db, message: ChatMessage):
  db.add(message)
  db.commit()
  db.refresh(message)
  return message


def get_chat(db, chat_id: str):
  return db.query(Chat).filter(Chat.id == chat_id).first()


def get_messages(db, chat_id: str):
  return db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).all()


def update_message(db, message: ChatMessage):
  db.merge(message)
  db.commit()
  return message


def delete_chat(db, chat_id: str):
  chat = db.query(Chat).filter(Chat.id == chat_id).first()
  db.delete(chat)
  db.commit()


def delete_message(db, message_id: str):
  message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
  db.delete(message)
  db.commit()
