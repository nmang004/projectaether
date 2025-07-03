"""
Core pytest fixtures for Project Aether test suite.

This module provides shared fixtures that can be used across all test files.
It includes test client configuration, authentication overrides, and other
common test utilities.
"""

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from fastapi.testclient import TestClient

from app.main import app
from app.auth.dependencies import get_current_user


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Async test client fixture for integration tests.
    
    This fixture provides an httpx.AsyncClient configured to make requests
    to the FastAPI application. It's the primary tool for testing API endpoints
    and ensures proper async handling of requests.
    
    Yields:
        AsyncClient: Configured async client for making HTTP requests
    """
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
def sync_client() -> TestClient:
    """
    Synchronous test client fixture for simple tests.
    
    This fixture provides a FastAPI TestClient for synchronous testing.
    Use this for simple tests that don't require async handling.
    
    Returns:
        TestClient: Configured sync client for making HTTP requests
    """
    return TestClient(app)


@pytest.fixture
def override_get_current_user():
    """
    Override authentication dependency for testing.
    
    This fixture replaces the real get_current_user dependency with a mock
    that returns a test user. This allows testing of protected endpoints
    without the complexity of generating real JWT tokens.
    
    Returns:
        str: Mock user identifier for testing
    """
    def mock_get_current_user() -> str:
        return "testuser@example.com"
    
    # Override the dependency
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    yield mock_get_current_user
    
    # Clean up after test
    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(override_get_current_user):
    """
    Authenticated test client fixture.
    
    This fixture provides a test client with authentication dependency
    overridden to return a mock user. Use this for testing protected endpoints.
    
    Args:
        override_get_current_user: The authentication override fixture
        
    Returns:
        TestClient: Configured client with authentication bypass
    """
    return TestClient(app)


@pytest.fixture
async def authenticated_async_client(override_get_current_user) -> AsyncGenerator[AsyncClient, None]:
    """
    Authenticated async test client fixture.
    
    This fixture provides an async test client with authentication dependency
    overridden to return a mock user. Use this for async testing of protected endpoints.
    
    Args:
        override_get_current_user: The authentication override fixture
        
    Yields:
        AsyncClient: Configured async client with authentication bypass
    """
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
def sample_audit_payload():
    """
    Sample payload for audit endpoint testing.
    
    Returns:
        dict: Valid audit request payload for testing
    """
    return {
        "root_url": "https://example.com",
        "max_depth": 3,
        "max_pages": 100
    }