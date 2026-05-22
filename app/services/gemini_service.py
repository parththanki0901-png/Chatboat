from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def get_gemini_response(user_message: str) -> str:
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=user_message
    )
    return response.text