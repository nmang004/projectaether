"""Sites management endpoints."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def list_sites():
    """List all sites."""
    return JSONResponse(
        content={
            "data": [],
            "message": "Sites list endpoint - to be implemented",
            "status": "placeholder"
        }
    )


@router.post("/")
async def create_site():
    """Create a new site."""
    return JSONResponse(
        content={
            "message": "Create site endpoint - to be implemented",
            "status": "placeholder"
        }
    )