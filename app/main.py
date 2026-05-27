from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

from app.services.gemini_service import (
    get_gemini_response,
    get_all_sessions_with_messages,
    delete_session
)

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body
class ChatRequest(BaseModel):
    message: str
    session_id: str


# Chat API
@app.post("/chat")
async def chat(request: ChatRequest):

    try:

        reply = await get_gemini_response(
            request.message,
            request.session_id
        )

        return {
            "reply": reply,
            "session_id": request.session_id
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


# Delete chat session
@app.delete("/chat/{session_id}")
async def delete_chat_session(session_id: str):

    deleted = delete_session(session_id)

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "message": "Session deleted successfully"
    }


# Get all sessions
@app.get("/chat")
async def root():

    return {
        "sessions": get_all_sessions_with_messages()
    }