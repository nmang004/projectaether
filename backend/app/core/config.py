"""
Project Aether Backend Configuration
"""
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Project Aether"
    VERSION: str = "0.1.0"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:5173",  # Vite dev server
            "http://localhost:3000",  # Alternative dev server
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ]
    )
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:password@localhost:5432/project_aether",
        description="Database connection URL"
    )
    
    # Redis Configuration
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    
    # Security Configuration
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production",
        description="Secret key for JWT tokens"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AWS Configuration
    AWS_REGION: str = Field(default="us-east-1", description="AWS region")
    AWS_ACCESS_KEY_ID: str = Field(default="", description="AWS access key")
    AWS_SECRET_ACCESS_KEY: str = Field(default="", description="AWS secret key")
    
    # External API Configuration
    GOOGLE_API_KEY: str = Field(default="", description="Google API key")
    DATAFORSEO_LOGIN: str = Field(default="", description="DataForSEO login")
    DATAFORSEO_PASSWORD: str = Field(default="", description="DataForSEO password")
    
    # Application Configuration
    DEBUG: bool = Field(default=True, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    
    # Celery Configuration
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Celery broker URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/0",
        description="Celery result backend URL"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()