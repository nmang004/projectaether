"""
Authentication schemas for Project Aether.

This module defines the Pydantic models used for API request and response validation
in the authentication system. These schemas ensure data integrity and provide
automatic documentation for the API endpoints.
"""

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """
    Schema for user registration requests.
    
    This model validates user registration data, ensuring that email addresses
    are properly formatted and passwords meet minimum security requirements.
    
    Attributes:
        email (EmailStr): User's email address, validated for proper format
        password (str): Plain text password that will be hashed before storage
    """
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters long"
    )
    
    class Config:
        """Pydantic configuration for UserCreate schema."""
        
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UserPublic(BaseModel):
    """
    Schema for public user information.
    
    This model represents user data that is safe to return in API responses.
    It deliberately excludes sensitive information like passwords or internal IDs.
    
    Attributes:
        id (int): User's unique identifier
        email (EmailStr): User's email address
    """
    
    id: int = Field(..., description="User's unique identifier")
    email: EmailStr = Field(..., description="User's email address")
    
    class Config:
        """Pydantic configuration for UserPublic schema."""
        
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com"
            }
        }


class Token(BaseModel):
    """
    Schema for JWT token responses.
    
    This model represents the response structure for successful authentication.
    It includes the JWT access token and token type for proper client handling.
    
    Attributes:
        access_token (str): JWT access token for authenticated requests
        token_type (str): Token type, always "bearer" for JWT tokens
    """
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(
        default="bearer",
        description="Token type, always 'bearer' for JWT tokens"
    )
    
    class Config:
        """Pydantic configuration for Token schema."""
        
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """
    Schema for JWT token payload data.
    
    This model represents the data that is encoded inside the JWT token.
    It contains the user identification information required for authorization.
    
    Attributes:
        sub (str): Subject claim - typically the user's email or ID
    """
    
    sub: str = Field(..., description="Subject claim - user identifier")
    
    class Config:
        """Pydantic configuration for TokenData schema."""
        
        schema_extra = {
            "example": {
                "sub": "user@example.com"
            }
        }