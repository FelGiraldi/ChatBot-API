from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Chatbot API 2025"
    GROQ_API_KEY: str
    # Configuración del modelo por defecto
    DEFAULT_MODEL: str = "llama-3.3-70b-versatile"  

    DATABASE_URL: str 

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()