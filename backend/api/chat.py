from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from backend.ai.chat_agent import run_chatbot_turn
from backend.ai.memory import get_or_create_assistant

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    user_id: str
    message: str
    chat_history: List[Dict] = []


@router.get("/health")
def chat_health():
    return {"status": "chat ok"}


@router.post("/")
async def chat_with_ai(request: ChatRequest):
    assistant_id = await get_or_create_assistant(request.user_id)

    result = await run_chatbot_turn(
        user_message=request.message,
        assistant_id=assistant_id,
        user_id=request.user_id,
        chat_history=request.chat_history,
    )
    return result