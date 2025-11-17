from fastapi import APIRouter

from llm_server.schemas import Reply
from llm_server.service import ChatService

chat_service = ChatService()

api_router = APIRouter(prefix="/api/v1", tags=["API"])


@api_router.get("/chat/{chat_id}")
def get_chat(chat_id: str):
    if chat_id not in chat_service.chats:
        return 404, f"Chat with id={chat_id} not found."

    return 200, chat_service.chats[chat_id]


@api_router.post("/chat/{chat_id}")
def new_reply(chat_id: str, reply: Reply):
    response = chat_service.chat(chat_id, reply.message)

    return Reply(message=response)
