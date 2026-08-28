import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "TransformIQ — Business Transformation AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment & Database
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:///./transformiq.db"
    
    # JWT Auth
    SECRET_KEY: str = "transformiq-super-secret-jwt-key-for-chaos2commit-2026-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # AI Provider settings
    AI_PROVIDER: str = "deterministic_smart"  # options: deterministic_smart, openai, azure_openai
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_API_BASE: Optional[str] = None
    
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_DEPLOYMENT: Optional[str] = "gpt-4o"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    
    # Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 25
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
