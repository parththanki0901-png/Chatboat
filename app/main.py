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
    message: str

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError(
        "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in .env or environment."
    )

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-flash-latest")

@app.post("/chats")
def chats(request: Chatrequest):
    try:
        response = model.generate_content(request.message)
        return {"reply": response.text}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/chat")
def chat(request: Chatrequest):
    return chats(request)


@app.get("/")
def root():
    return {"status" : "chat API is running"}