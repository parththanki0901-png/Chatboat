from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.genai.errors import ClientError
from app.services.gemini_service import get_gemini_response
from pydantic import BaseModel 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins =["http://127.0.0.1:8000/"],
    allow_methods =["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        reply = await get_gemini_response(request.message)
        return {"reply": reply}
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
