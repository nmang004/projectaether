"""
User data model for Project Aether.

This module defines the User model that represents a user in the system.
Currently implemented as a Pydantic model for data validation, but will
be replaced with SQLAlchemy models when database integration is complete.
"""

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    User data model.
    
    This model represents a user in the Project Aether system.
    Contains the core user information including ID, email, and
    hashed password for authentication.
    
    Attributes:
        id (int): Unique identifier for the user
        email (EmailStr): User's email address, validated for proper format
        hashed_password (str): Bcrypt hashed password for secure storage
    """
    
    id: int
    email: EmailStr
    hashed_password: str
    
    class Config:
        """Pydantic configuration for the User model."""
        
        # Generate example values for API documentation
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
            }
        }