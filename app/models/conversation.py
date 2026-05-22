from typing import List, Dict
from app.schemas.chat import Message

class ConversationManager:
    def __init__(self):
        self.sessions: Dict[str, List[Message]] = {}

    def get_history(self, session_id: str) -> List[Message]:
        return self.sessions.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(Message(role=role, content=content))

    def clear_history(self, session_id: str):
        if session_id in self.sessions:
            self.sessions[session_id] = []

conversation_manager = ConversationManager()