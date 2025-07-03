"""
API Version 1 Router Aggregator for Project Aether.

This module serves as the central aggregator for all Version 1 API endpoints.
It consolidates all feature-specific routers into a single router that can be
easily included in the main FastAPI application. This pattern promotes clean
organization and makes it simple to manage API versioning.
"""

from fastapi import APIRouter

# Import all endpoint routers
from app.api.v1.endpoints import audits, ai, auth, sites


# Create the main V1 API router
# This router will include all feature-specific routers
api_router = APIRouter()


# Include all endpoint routers with their respective configurations
# Each router maintains its own prefix, tags, and dependencies

# Authentication endpoints
# Handles user login, registration, and token management
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Site audit endpoints
# Handles site crawling, analysis, and audit task management
api_router.include_router(
    audits.router,
    # prefix="/audits" is already defined in the router
    tags=["Site Audits"]
)

# AI-powered feature endpoints
# Handles keyword clustering, content briefs, and schema generation
api_router.include_router(
    ai.router,
    # prefix="/ai" is already defined in the router
    tags=["AI Services"]
)

# Site management endpoints
# Handles site registration, configuration, and management
api_router.include_router(
    sites.router,
    prefix="/sites",
    tags=["Site Management"]
)


# Health check endpoint specific to V1 API
@api_router.get("/health")
async def v1_health_check():
    """
    Health check endpoint for V1 API.
    
    This endpoint provides a quick way to verify that the V1 API
    is properly configured and all routers are loaded correctly.
    It can be used by monitoring systems to check API availability.
    
    Returns:
        Dict containing API version and status information
    """
    return {
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "authentication": "/api/v1/auth",
            "site_audits": "/api/v1/audits",
            "ai_services": "/api/v1/ai",
            "site_management": "/api/v1/sites"
        },
        "message": "Project Aether API v1 is operational"
    }


# Optional: API information endpoint
@api_router.get("/info")
async def v1_api_info():
    """
    API information endpoint for V1.
    
    This endpoint provides comprehensive information about the V1 API,
    including available endpoints, authentication requirements, and
    usage guidelines. It serves as a programmatic way to discover API capabilities.
    
    Returns:
        Dict containing detailed API information
    """
    return {
        "version": "1.0.0",
        "title": "Project Aether API",
        "description": "Unified SEO Intelligence Platform API",
        "authentication": {
            "type": "JWT Bearer Token",
            "endpoints": {
                "login": "/api/v1/auth/login",
                "register": "/api/v1/auth/register"
            }
        },
        "features": {
            "site_audits": {
                "description": "Comprehensive site crawling and SEO analysis",
                "endpoints": [
                    "POST /api/v1/audits/start",
                    "GET /api/v1/audits/status/{task_id}",
                    "GET /api/v1/audits/history"
                ]
            },
            "ai_services": {
                "description": "AI-powered SEO tools and content optimization",
                "endpoints": [
                    "POST /api/v1/ai/keyword-clusters",
                    "POST /api/v1/ai/schema-markup",
                    "POST /api/v1/ai/content-brief",
                    "GET /api/v1/ai/service-status"
                ]
            },
            "site_management": {
                "description": "Site registration and configuration management",
                "endpoints": [
                    "GET /api/v1/sites",
                    "POST /api/v1/sites"
                ]
            }
        },
        "rate_limiting": {
            "enabled": False,
            "note": "Rate limiting should be implemented for production use"
        },
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        }
    }