"""
Project Aether Backend - Main FastAPI Application

This module serves as the entry point for the FastAPI application.
It configures structured logging, CORS middleware, and the core application instance.
The configuration is designed to be production-ready with proper observability
and security considerations from the start.
"""

import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import Settings
from app.auth.router import router as auth_router
from app.api.v1.api import api_router


# Initialize settings - single source of truth for configuration
settings = Settings()


def configure_logging() -> None:
    """
    Configure structured logging using structlog.
    
    This setup ensures all logs are output as JSON format, making them
    easily parsable by AWS CloudWatch and other log aggregation systems.
    The configuration also processes logs from the standard Python logging
    library, ensuring we capture logs from third-party libraries correctly.
    """
    # Configure structlog to output JSON logs
    structlog.configure(
        processors=[
            # Add context variables to log entries
            structlog.contextvars.merge_contextvars,
            # Add timestamps to all log entries
            structlog.processors.TimeStamper(fmt="iso"),
            # Add log level to entries
            structlog.processors.add_log_level,
            # Add logger name to entries
            structlog.processors.add_logger_name,
            # Convert to JSON format for structured logging
            structlog.processors.JSONRenderer()
        ],
        # Use structlog's logger factory
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Cache loggers for performance
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging to work with structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    This function handles startup and shutdown events for the FastAPI application.
    It's the proper place to initialize resources like database connections,
    cache connections, and other shared resources.
    """
    # Configure logging before anything else
    configure_logging()
    
    # Get a structured logger
    logger = structlog.get_logger()
    
    # Startup
    logger.info(
        "Starting Project Aether Backend",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        log_level=settings.LOG_LEVEL
    )
    
    yield
    
    # Shutdown
    logger.info("Shutting down Project Aether Backend")


# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Unified SEO Intelligence Platform",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# Configure CORS middleware
# This allows the frontend application to make requests to this API
# The origin is configured via environment variables for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routers
# V1 API endpoints are included under /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

# Legacy authentication router (will be removed once V1 API is fully integrated)
# app.include_router(auth_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancers and monitoring systems.
    
    This endpoint provides a simple way to verify that the application
    is running and responsive. It returns the application version,
    which is useful for deployment verification.
    """
    return JSONResponse(
        content={
            "status": "ok",
            "version": settings.APP_VERSION
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application with uvicorn
    # This is primarily for local development
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
    )