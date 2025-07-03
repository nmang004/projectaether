"""
Centralized Configuration Management for Project Aether

This module defines the application settings using Pydantic's BaseSettings,
which automatically loads configuration from environment variables.
This follows the 12-factor app principle of configuration via environment,
allowing the same code to run across different environments (local, staging, production)
by simply providing different environment configurations.
"""

from pydantic import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This class defines all configuration variables required by the application.
    Values are automatically loaded from environment variables, with fallback
    defaults provided for development convenience.
    """
    
    # Application metadata
    APP_NAME: str = "Project Aether"
    APP_VERSION: str = "0.1.0"
    
    # Logging configuration
    # LOG_LEVEL controls the verbosity of application logs
    # Valid values: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL: str = "INFO"
    
    # Database configuration
    # DATABASE_URL is required for SQLAlchemy database connections
    # Format: postgresql://user:password@host:port/database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/projectaether"
    
    # Redis configuration for caching and Celery task queue
    # REDIS_URL format: redis://host:port/database
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS configuration
    # FRONTEND_ORIGIN defines which domain can make requests to this API
    # This is critical for browser security - only trusted frontends should be allowed
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    
    # Pydantic V2 configuration
    # This tells Pydantic to automatically load values from .env file
    # env_file_encoding ensures proper handling of non-ASCII characters
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8'
    )