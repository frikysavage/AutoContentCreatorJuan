from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/autocontent"
    VIDEO_PROVIDER: str = "vidu"
    PUBLIC_BASE_URL: str = "http://localhost:8000"
    GOOGLE_AI_STUDIO_API_KEY: str = ""
    VIDU_API_KEY: str = ""
    TTS_API_KEY: str = ""
    YOUTUBE_CLIENT_ID: str = ""
    YOUTUBE_CLIENT_SECRET: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
