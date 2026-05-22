from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    history: List[Message] = []