from threading import RLock
from pydantic import BaseModel, Field
from llm_server.model import Message, Model


class Chat(BaseModel):
    id: str
    messages: list[Message] = Field(..., default_factory=list)
    # created_at: str
    # user_id: str


class ChatService:
    def __init__(self, max_context: int = 100):
        self.chats: dict[str, Chat] = dict()
        self.model = Model()
        self.model.load()
        self.max_context = max_context

        self.lock = RLock()

    def chat(self, chat_id: str, message: str):
        with self.lock:
            if chat_id not in self.chats:
                self.chats[chat_id] = Chat(id=chat_id)

            chat = self.chats[chat_id]
            context = chat.messages[: self.max_context]

            response = self.model.chat(message, context)

            chat.messages.append(Message(role="user", content=message))
            chat.messages.append(response)

        return response.content
