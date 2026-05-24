from sys import exception
import dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
from requests import Session
from app.services.gemini_service import get_all_sessions_with_messages, get_gemini_response, delete_session
from pydantic import BaseModel 

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins =["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods =["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        reply = await get_gemini_response(request.message, request.session_id)
        return {"reply": reply, "session_id": request.session_id}
    except ClientError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API error: {exc}"
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        ) from exc

@app.delete("/chat/{session_id}")
async def delete_chat_session(session_id: str):
    try :  
        deleted = delete_session(session_id)  # ← use renamed import
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
        return {"message": f"session{session_id} deleted successfully"}
    except HTTPException:
        raise  # ← re-raise 404 properly
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc
    
@app.get("/chat")
async def root():
 return {"sessions": get_all_sessions_with_messages()}