"""
Data models for Project Aether.

This module contains all the data models used throughout the application.
Currently uses Pydantic models for data validation, but will be migrated
to SQLAlchemy models when database integration is implemented.
"""

from .user import User

__all__ = ["User"]