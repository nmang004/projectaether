"""Authentication endpoints."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/login")
async def login():
    """User login endpoint."""
    return JSONResponse(
        content={
            "message": "Login endpoint - to be implemented",
            "status": "placeholder"
        }
    )


@router.post("/register")
async def register():
    """User registration endpoint."""
    return JSONResponse(
        content={
            "message": "Register endpoint - to be implemented",
            "status": "placeholder"
        }
    )