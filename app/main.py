from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Chatrequest(BaseModel):
    session_id: str
    message: str


# Load API key
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise RuntimeError(
        "Missing Gemini API key"
    )

# Configure Gemini
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-flash-latest")

# Store chat history in memory
chat_sessions = {}


# Chat endpoint
@app.post("/chat")
def chat(request: Chatrequest):

    try:
        # Get session ID
        session_id = request.session_id

        # Create new session if it does not exist
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []

        # Load old conversation history
        history = chat_sessions[session_id]

        # Start Gemini chat with history
        chat = model.start_chat(history=history)

        # Send current user message
        response = chat.send_message(request.message)

        # Save user message
        history.append({
            "role": "user",
            "parts": [request.message]
        })

        # Save Gemini response
        history.append({
            "role": "model",
            "parts": [response.text]
        })

        # Return response
        return {
            "reply": response.text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Delete chat history
@app.delete("/chat/{session_id}")
def delete_chat(session_id: str):

    if session_id not in chat_sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    del chat_sessions[session_id]

    return {
        "message": f"Chat history for session '{session_id}' deleted"
    }


# Root endpoint
@app.get("/")
def root():
    return {
        "status": "Chat API is running"
    }