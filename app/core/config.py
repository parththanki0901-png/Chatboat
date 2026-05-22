from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    APP_NAME: str = "Chatboat"
    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()