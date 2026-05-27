from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API Key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("Missing GROQ API key")

# Create Groq client
client = Groq(api_key=api_key)

# Store chat sessions
chat_sessions = {}


# Generate AI response
async def get_gemini_response(message, session_id):

    # Create session if not exists
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    # Save user message
    chat_sessions[session_id].append({
        "role": "user",
        "content": message
    })

    # Generate response from Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=chat_sessions[session_id]
    )

    # Extract reply
    reply = response.choices[0].message.content

    # Save assistant response
    chat_sessions[session_id].append({
        "role": "assistant",
        "content": reply
    })

    return reply


# Get all sessions
def get_all_sessions_with_messages():
    return chat_sessions


# Delete session
def delete_session(session_id):

    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return True

    return False