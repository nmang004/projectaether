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
    
    # Frontend Origin (for single origin setups)
    FRONTEND_ORIGIN: str = Field(
        default="http://localhost:3000",
        description="Frontend origin for CORS"
    )
    
    # Application Metadata
    APP_NAME: str = Field(default="Project Aether", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    
    # Database Configuration
    # For Google Cloud SQL with Cloud SQL Auth Proxy:
    # Format: postgresql+asyncpg://<user>:<password>@/<db_name>?host=/cloudsql/<project>:<region>:<instance>
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:password@localhost:5432/project_aether",
        description="Database connection URL - supports Cloud SQL Auth Proxy socket path"
    )
    
    # Database credentials (used to construct Cloud SQL connection string)
    DATABASE_USER: str = Field(default="postgres", description="Database username")
    DATABASE_PASSWORD: str = Field(default="password", description="Database password")
    DATABASE_HOST: str = Field(default="localhost", description="Database host")
    DATABASE_PORT: int = Field(default=5432, description="Database port")
    DATABASE_NAME: str = Field(default="project_aether", description="Database name")
    
    # Redis Configuration
    # For Google Memorystore: redis://<memorystore_ip>:6379
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL - supports Google Memorystore"
    )
    
    # Security Configuration
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production",
        description="Secret key for JWT tokens"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Cloud Configuration
    # AWS Configuration (keeping for boto3 compatibility during transition)
    AWS_REGION: str = Field(default="us-east-1", description="AWS region")
    AWS_ACCESS_KEY_ID: str = Field(default="", description="AWS access key")
    AWS_SECRET_ACCESS_KEY: str = Field(default="", description="AWS secret key")
    
    # GCP Configuration
    GCP_PROJECT_ID: str = Field(default="", description="Google Cloud Project ID")
    GCP_REGION: str = Field(default="us-central1", description="Google Cloud region")
    
    # Google Cloud SQL Configuration
    CLOUD_SQL_INSTANCE_NAME: str = Field(default="", description="Cloud SQL instance name")
    CLOUD_SQL_DATABASE_NAME: str = Field(default="projectaether", description="Cloud SQL database name")
    CLOUD_SQL_CONNECTION_NAME: str = Field(default="", description="Cloud SQL connection name (project:region:instance)")
    
    # Google Memorystore Configuration  
    MEMORYSTORE_IP: str = Field(default="", description="Google Memorystore Redis IP address")
    MEMORYSTORE_PORT: int = Field(default=6379, description="Google Memorystore Redis port")
    
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

    def get_database_url(self) -> str:
        """
        Get the database URL, constructing Cloud SQL Auth Proxy format if needed.
        
        Returns:
            str: Database connection URL
        """
        # If DATABASE_URL is explicitly set and not the default, use it
        if self.DATABASE_URL != "postgresql+asyncpg://postgres:password@localhost:5432/project_aether":
            return self.DATABASE_URL
            
        # If Cloud SQL connection name is provided, construct socket path URL
        if self.CLOUD_SQL_CONNECTION_NAME:
            return (
                f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
                f"@/{self.DATABASE_NAME}?host=/cloudsql/{self.CLOUD_SQL_CONNECTION_NAME}"
            )
        
        # Otherwise construct standard URL
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    def get_redis_url(self) -> str:
        """
        Get the Redis URL, using Memorystore IP if configured.
        
        Returns:
            str: Redis connection URL
        """
        # If REDIS_URL is explicitly set and not the default, use it
        if self.REDIS_URL != "redis://localhost:6379/0":
            return self.REDIS_URL
            
        # If Memorystore IP is provided, construct URL
        if self.MEMORYSTORE_IP:
            return f"redis://{self.MEMORYSTORE_IP}:{self.MEMORYSTORE_PORT}/0"
        
        # Otherwise use default
        return self.REDIS_URL

    def get_celery_broker_url(self) -> str:
        """
        Get the Celery broker URL, using configured Redis URL.
        
        Returns:
            str: Celery broker URL
        """
        # If explicitly set and not default, use it
        if self.CELERY_BROKER_URL != "redis://localhost:6379/0":
            return self.CELERY_BROKER_URL
        
        # Otherwise use the dynamic Redis URL
        return self.get_redis_url()

    def get_celery_result_backend_url(self) -> str:
        """
        Get the Celery result backend URL, using configured Redis URL.
        
        Returns:
            str: Celery result backend URL
        """
        # If explicitly set and not default, use it
        if self.CELERY_RESULT_BACKEND != "redis://localhost:6379/0":
            return self.CELERY_RESULT_BACKEND
        
        # Otherwise use the dynamic Redis URL
        return self.get_redis_url()


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()