"""
Authentication API endpoints for Project Aether.

This module defines the REST API endpoints for user authentication including
login and user information retrieval. All endpoints follow REST conventions
and include proper error handling and security measures.
"""

from datetime import timedelta
from typing import Dict, Any

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependencies import get_current_user
from app.auth.schemas import Token, UserPublic, UserCreate
from app.auth.service import verify_password, create_access_token, get_password_hash


# Initialize structured logger
logger = structlog.get_logger()

# Create router with prefix and tags for API organization
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        401: {"description": "Unauthorized"},
        422: {"description": "Validation Error"},
    }
)


# Temporary in-memory user store for demonstration
# TODO: Replace with actual database integration in Phase 1 Step 3
TEMP_USERS_DB: Dict[str, Dict[str, Any]] = {
    "demo@projectaether.com": {
        "id": 1,
        "email": "demo@projectaether.com",
        "hashed_password": get_password_hash("demopassword123"),
    }
}


def authenticate_user(email: str, password: str) -> Dict[str, Any] | None:
    """
    Authenticate a user with email and password.
    
    This function verifies user credentials against the stored user data.
    In the current implementation, it uses an in-memory store, but will be
    replaced with database queries in the next phase.
    
    Args:
        email (str): User's email address
        password (str): User's plain text password
        
    Returns:
        Dict[str, Any] | None: User data if authentication succeeds, None otherwise
        
    Security Notes:
        - Uses constant-time password verification to prevent timing attacks
        - Does not leak information about whether the email exists
        - Logs authentication attempts for security monitoring
    """
    # Log authentication attempt (without sensitive data)
    logger.info("Authentication attempt", email=email)
    
    # Check if user exists
    user = TEMP_USERS_DB.get(email)
    if not user:
        logger.warning("Authentication failed - user not found", email=email)
        return None
    
    # Verify password using constant-time comparison
    if not verify_password(password, user["hashed_password"]):
        logger.warning("Authentication failed - invalid password", email=email)
        return None
    
    logger.info("Authentication successful", email=email, user_id=user["id"])
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    User login endpoint.
    
    This endpoint authenticates a user with email and password, and returns
    a JWT access token for subsequent authenticated requests.
    
    Args:
        form_data (OAuth2PasswordRequestForm): Login form data containing username and password
        
    Returns:
        Token: JWT access token and token type
        
    Raises:
        HTTPException: 401 Unauthorized if credentials are invalid
        
    Security Notes:
        - Uses OAuth2PasswordRequestForm for standard compliance
        - Rate limiting should be implemented at the reverse proxy level
        - Failed attempts are logged for security monitoring
        - Token expiration is set to a reasonable timeframe
    """
    # Authenticate the user (username field contains email in our case)
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        # Return generic error message to prevent username enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with user information
    access_token_expires = timedelta(hours=24)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    logger.info(
        "User login successful", 
        email=user["email"], 
        user_id=user["id"],
        token_expires_hours=24
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserPublic)
async def get_current_user_info(current_user: str = Depends(get_current_user)) -> UserPublic:
    """
    Get current user information.
    
    This endpoint returns the current user's information based on the provided
    JWT token. It serves as both a token validation endpoint and a way to
    retrieve user profile information.
    
    Args:
        current_user (str): User identifier from the JWT token
        
    Returns:
        UserPublic: Current user's public information
        
    Raises:
        HTTPException: 401 Unauthorized if token is invalid
        HTTPException: 404 Not Found if user no longer exists
        
    Security Notes:
        - Only returns public user information (no sensitive data)
        - Validates JWT token automatically through dependency
        - Can be used to validate token validity from client applications
    """
    # Look up user in the temporary store
    # TODO: Replace with database query in Phase 1 Step 3
    user = TEMP_USERS_DB.get(current_user)
    
    if not user:
        logger.error("User not found for valid token", email=current_user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    logger.info("User information retrieved", email=current_user, user_id=user["id"])
    
    return UserPublic(
        id=user["id"],
        email=user["email"]
    )


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate) -> UserPublic:
    """
    User registration endpoint (placeholder).
    
    This endpoint allows new users to register with the system.
    Currently implemented as a placeholder for future development.
    
    Args:
        user_data (UserCreate): User registration data
        
    Returns:
        UserPublic: Created user's public information
        
    Raises:
        HTTPException: 400 Bad Request if user already exists
        
    Note:
        This is a placeholder implementation. Full user registration
        will be implemented when database integration is complete.
    """
    # Check if user already exists
    if user_data.email in TEMP_USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user (placeholder implementation)
    new_user_id = len(TEMP_USERS_DB) + 1
    hashed_password = get_password_hash(user_data.password)
    
    new_user = {
        "id": new_user_id,
        "email": user_data.email,
        "hashed_password": hashed_password,
    }
    
    # Store user in temporary database
    TEMP_USERS_DB[user_data.email] = new_user
    
    logger.info("New user registered", email=user_data.email, user_id=new_user_id)
    
    return UserPublic(
        id=new_user["id"],
        email=new_user["email"]
    )