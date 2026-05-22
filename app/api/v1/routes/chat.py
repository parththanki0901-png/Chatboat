from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.gemini_service import get_gemini_response
from app.models.conversation import conversation_manager

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = await get_gemini_response(request.session_id, request.message)
    history = conversation_manager.get_history(request.session_id)
    return ChatResponse(
        reply=reply,
        session_id=request.session_id,
        history=history
    )

@router.get("/history/{session_id}")
async def get_history(session_id: str):
    history = conversation_manager.get_history(session_id)
    return {"session_id": session_id, "history": history}

@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    conversation_manager.clear_history(session_id)
    return {"message": "History cleared", "session_id": session_id}