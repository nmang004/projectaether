"""
Security dependencies for Project Aether.

This module provides reusable FastAPI dependencies for authentication and authorization.
These dependencies can be injected into any endpoint to enforce security requirements
and provide user context to the request handlers.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError

from app.auth.service import decode_access_token


# OAuth2 password bearer configuration
# This tells FastAPI where to find the login endpoint for token acquisition
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency to get the current authenticated user from a JWT token.
    
    This function validates the JWT token and extracts the user information.
    It serves as the primary authentication dependency for protected endpoints.
    
    Args:
        token (str): The JWT token from the Authorization header
        
    Returns:
        str: The user identifier (email or ID) from the token's 'sub' claim
        
    Raises:
        HTTPException: 401 Unauthorized if the token is invalid or expired
        
    Security Notes:
        - Validates token signature and expiration automatically
        - Provides specific error messages for different failure modes
        - Returns only the user identifier to minimize data exposure
        - Uses proper HTTP status codes for different authentication failures
    """
    # Create a generic credentials exception for security
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and validate the JWT token
        payload = decode_access_token(token)
        
        # Extract the user identifier from the 'sub' claim
        user_id: str = payload.get("sub")
        
        # Ensure the user identifier exists
        if user_id is None:
            raise credentials_exception
            
        return user_id
        
    except ExpiredSignatureError:
        # Handle expired tokens with a specific error message
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    except JWTError:
        # Handle all other JWT-related errors
        raise credentials_exception


async def get_current_active_user(current_user: str = Depends(get_current_user)) -> str:
    """
    Dependency to get the current active user.
    
    This function extends the basic user authentication to include user status checks.
    Currently, it simply returns the user identifier, but can be extended to include
    additional checks like user account status, permissions, etc.
    
    Args:
        current_user (str): The user identifier from the get_current_user dependency
        
    Returns:
        str: The active user identifier
        
    Future Enhancements:
        - Check if user account is active/enabled
        - Verify user permissions and roles
        - Implement user session management
        - Add rate limiting per user
    """
    # In the current implementation, all authenticated users are considered active
    # This can be extended to check user status from the database
    return current_user


# Optional: Additional security dependencies for different permission levels
async def get_admin_user(current_user: str = Depends(get_current_active_user)) -> str:
    """
    Dependency to ensure the current user has admin privileges.
    
    This function can be used to protect admin-only endpoints.
    Currently returns the user identifier, but should be extended to include
    proper role-based access control.
    
    Args:
        current_user (str): The user identifier from get_current_active_user
        
    Returns:
        str: The admin user identifier
        
    Raises:
        HTTPException: 403 Forbidden if the user is not an admin
        
    Note:
        This is a placeholder implementation. In a production system,
        this would check user roles/permissions from the database.
    """
    # TODO: Implement proper role-based access control
    # For now, this is a placeholder that would need to be connected to a user roles system
    
    # Example implementation (would need database integration):
    # user = get_user_by_id(current_user)
    # if not user.is_admin:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not enough permissions"
    #     )
    
    return current_user