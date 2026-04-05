from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Backend"
    API_V1_STR: str = "/api/v1"
    
    GOOGLE_API_KEY: str
    CHROMA_PATH: str = str(BASE_DIR / "chroma_db")
    MODEL_NAME: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()