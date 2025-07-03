"""
Integration tests for the audits API endpoints.

These tests verify the complete request-response cycle for audit endpoints,
including authentication, request validation, task creation, and response formatting.
They use real HTTP requests to test the full API stack.
"""

import pytest
from unittest.mock import MagicMock
from httpx import AsyncClient
from fastapi.testclient import TestClient

from app.main import app
from app.tasks.crawler_tasks import run_site_crawl


class TestStartAuditEndpoint:
    """Test cases for the POST /api/v1/audits/start endpoint."""

    def test_start_audit_success(self, authenticated_client, sample_audit_payload, mocker):
        """Test successful audit start with valid payload."""
        # Mock the Celery task
        mock_task_result = MagicMock()
        mock_task_result.id = "test-task-id-12345"
        
        mock_delay = mocker.patch.object(run_site_crawl, 'delay', return_value=mock_task_result)
        
        # Make the request
        response = authenticated_client.post(
            "/api/v1/audits/start",
            json=sample_audit_payload
        )
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["task_id"] == "test-task-id-12345"
        assert response_data["status"] == "pending"
        assert response_data["message"] == "Site audit task started successfully"
        assert response_data["root_url"] == sample_audit_payload["root_url"]
        
        # Verify the task was called with correct parameters
        mock_delay.assert_called_once_with(
            project_id=1,  # Default project ID
            root_url=sample_audit_payload["root_url"],
            max_depth=sample_audit_payload["max_depth"],
            max_pages=sample_audit_payload["max_pages"]
        )

    async def test_start_audit_success_async(self, authenticated_async_client, sample_audit_payload, mocker):
        """Test successful audit start with async client."""
        # Mock the Celery task
        mock_task_result = MagicMock()
        mock_task_result.id = "async-test-task-id"
        
        mock_delay = mocker.patch.object(run_site_crawl, 'delay', return_value=mock_task_result)
        
        # Make the async request
        response = await authenticated_async_client.post(
            "/api/v1/audits/start",
            json=sample_audit_payload
        )
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["task_id"] == "async-test-task-id"
        assert response_data["status"] == "pending"
        assert response_data["root_url"] == sample_audit_payload["root_url"]
        
        # Verify the task was called
        mock_delay.assert_called_once()

    def test_start_audit_invalid_url(self, authenticated_client, mocker):
        """Test audit start with invalid URL."""
        # Mock the Celery task (shouldn't be called)
        mock_delay = mocker.patch.object(run_site_crawl, 'delay')
        
        # Invalid payload with malformed URL
        invalid_payload = {
            "root_url": "not-a-valid-url",
            "max_depth": 3,
            "max_pages": 100
        }
        
        # Make the request
        response = authenticated_client.post(
            "/api/v1/audits/start",
            json=invalid_payload
        )
        
        # Verify response
        assert response.status_code == 422  # Validation error
        
        # Verify the task was not called
        mock_delay.assert_not_called()

    def test_start_audit_missing_required_fields(self, authenticated_client, mocker):
        """Test audit start with missing required fields."""
        # Mock the Celery task (shouldn't be called)
        mock_delay = mocker.patch.object(run_site_crawl, 'delay')
        
        # Payload missing root_url
        invalid_payload = {
            "max_depth": 3,
            "max_pages": 100
        }
        
        # Make the request
        response = authenticated_client.post(
            "/api/v1/audits/start",
            json=invalid_payload
        )
        
        # Verify response
        assert response.status_code == 422  # Validation error
        
        # Verify the task was not called
        mock_delay.assert_not_called()

    def test_start_audit_default_values(self, authenticated_client, mocker):
        """Test audit start with default values for optional fields."""
        # Mock the Celery task
        mock_task_result = MagicMock()
        mock_task_result.id = "default-values-task-id"
        
        mock_delay = mocker.patch.object(run_site_crawl, 'delay', return_value=mock_task_result)
        
        # Minimal payload using defaults
        minimal_payload = {
            "root_url": "https://example.com"
        }
        
        # Make the request
        response = authenticated_client.post(
            "/api/v1/audits/start",
            json=minimal_payload
        )
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["task_id"] == "default-values-task-id"
        
        # Verify the task was called with default values
        mock_delay.assert_called_once_with(
            project_id=1,
            root_url="https://example.com",
            max_depth=3,  # Default value
            max_pages=100  # Default value
        )

    def test_start_audit_unauthenticated(self, sync_client, sample_audit_payload, mocker):
        """Test audit start without authentication."""
        # Mock the Celery task (shouldn't be called)
        mock_delay = mocker.patch.object(run_site_crawl, 'delay')
        
        # Make the request without authentication
        response = sync_client.post(
            "/api/v1/audits/start",
            json=sample_audit_payload
        )
        
        # Verify response
        assert response.status_code == 401  # Unauthorized
        
        # Verify the task was not called
        mock_delay.assert_not_called()

    def test_start_audit_task_creation_failure(self, authenticated_client, sample_audit_payload, mocker):
        """Test audit start when task creation fails."""
        # Mock the Celery task to raise an exception
        mock_delay = mocker.patch.object(run_site_crawl, 'delay', side_effect=Exception("Task creation failed"))
        
        # Make the request
        response = authenticated_client.post(
            "/api/v1/audits/start",
            json=sample_audit_payload
        )
        
        # Verify response
        assert response.status_code == 500  # Internal server error
        
        response_data = response.json()
        assert response_data["detail"] == "Failed to start site audit task"
        
        # Verify the task was called
        mock_delay.assert_called_once()


class TestGetAuditStatusEndpoint:
    """Test cases for the GET /api/v1/audits/status/{task_id} endpoint."""

    def test_get_audit_status_pending(self, authenticated_client, mocker):
        """Test getting status of a pending task."""
        # Mock the Celery AsyncResult
        mock_task_result = MagicMock()
        mock_task_result.status = "PENDING"
        mock_task_result.info = None
        mock_task_result.result = None
        
        # Mock the celery_app.AsyncResult
        mock_async_result = mocker.patch("app.tasks.crawler_tasks.celery_app.AsyncResult", return_value=mock_task_result)
        
        # Make the request
        task_id = "test-task-id-pending"
        response = authenticated_client.get(f"/api/v1/audits/status/{task_id}")
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["task_id"] == task_id
        assert response_data["status"] == "PENDING"
        assert response_data["message"] == "Task is waiting to be processed"
        assert response_data["result"] is None
        assert response_data["progress"] is None
        assert response_data["error"] is None
        
        # Verify AsyncResult was called with correct task_id
        mock_async_result.assert_called_once_with(task_id)

    def test_get_audit_status_in_progress(self, authenticated_client, mocker):
        """Test getting status of a task in progress."""
        # Mock the Celery AsyncResult
        mock_task_result = MagicMock()
        mock_task_result.status = "PROGRESS"
        mock_task_result.info = {
            "phase": "crawling",
            "progress": 45,
            "total": 100,
            "crawled": 45
        }
        mock_task_result.result = None
        
        # Mock the celery_app.AsyncResult
        mock_async_result = mocker.patch("app.tasks.crawler_tasks.celery_app.AsyncResult", return_value=mock_task_result)
        
        # Make the request
        task_id = "test-task-id-progress"
        response = authenticated_client.get(f"/api/v1/audits/status/{task_id}")
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["task_id"] == task_id
        assert response_data["status"] == "PROGRESS"
        assert response_data["message"] == "Task is being processed"
        assert response_data["progress"] == mock_task_result.info
        assert response_data["result"] is None
        assert response_data["error"] is None

    def test_get_audit_status_success(self, authenticated_client, mocker):
        """Test getting status of a successfully completed task."""
        # Mock the Celery AsyncResult
        mock_task_result = MagicMock()
        mock_task_result.status = "SUCCESS"
        mock_task_result.info = None
        mock_task_result.result = {
            "project_id": 1,
            "root_url": "https://example.com",
            "crawl_summary": {
                "total_pages_crawled": 50,
                "crawl_status": "completed"
            }
        }
        
        # Mock the celery_app.AsyncResult
        mock_async_result = mocker.patch("app.tasks.crawler_tasks.celery_app.AsyncResult", return_value=mock_task_result)
        
        # Make the request
        task_id = "test-task-id-success"
        response = authenticated_client.get(f"/api/v1/audits/status/{task_id}")
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["task_id"] == task_id
        assert response_data["status"] == "SUCCESS"
        assert response_data["message"] == "Task completed successfully"
        assert response_data["result"] == mock_task_result.result
        assert response_data["progress"] is None
        assert response_data["error"] is None

    def test_get_audit_status_failure(self, authenticated_client, mocker):
        """Test getting status of a failed task."""
        # Mock the Celery AsyncResult
        mock_task_result = MagicMock()
        mock_task_result.status = "FAILURE"
        mock_task_result.info = Exception("Task processing failed")
        mock_task_result.result = None
        
        # Mock the celery_app.AsyncResult
        mock_async_result = mocker.patch("app.tasks.crawler_tasks.celery_app.AsyncResult", return_value=mock_task_result)
        
        # Make the request
        task_id = "test-task-id-failure"
        response = authenticated_client.get(f"/api/v1/audits/status/{task_id}")
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["task_id"] == task_id
        assert response_data["status"] == "FAILURE"
        assert response_data["message"] == "Task failed to complete"
        assert response_data["result"] is None
        assert response_data["progress"] is None
        assert response_data["error"] == "Task processing failed"

    def test_get_audit_status_unauthenticated(self, sync_client, mocker):
        """Test getting audit status without authentication."""
        # Mock the celery_app.AsyncResult (shouldn't be called)
        mock_async_result = mocker.patch("app.tasks.crawler_tasks.celery_app.AsyncResult")
        
        # Make the request without authentication
        task_id = "test-task-id"
        response = sync_client.get(f"/api/v1/audits/status/{task_id}")
        
        # Verify response
        assert response.status_code == 401  # Unauthorized
        
        # Verify AsyncResult was not called
        mock_async_result.assert_not_called()

    def test_get_audit_status_internal_error(self, authenticated_client, mocker):
        """Test getting audit status when an internal error occurs."""
        # Mock the celery_app.AsyncResult to raise an exception
        mock_async_result = mocker.patch("app.tasks.crawler_tasks.celery_app.AsyncResult", side_effect=Exception("Internal error"))
        
        # Make the request
        task_id = "test-task-id-error"
        response = authenticated_client.get(f"/api/v1/audits/status/{task_id}")
        
        # Verify response
        assert response.status_code == 500  # Internal server error
        
        response_data = response.json()
        assert response_data["detail"] == "Failed to retrieve task status"


class TestGetAuditHistoryEndpoint:
    """Test cases for the GET /api/v1/audits/history endpoint."""

    def test_get_audit_history_success(self, authenticated_client):
        """Test successful retrieval of audit history."""
        # Make the request
        response = authenticated_client.get("/api/v1/audits/history")
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert "audits" in response_data
        assert "total" in response_data
        assert "limit" in response_data
        assert "offset" in response_data
        assert "message" in response_data
        
        # Verify default pagination values
        assert response_data["limit"] == 10
        assert response_data["offset"] == 0
        assert response_data["total"] == 0
        assert response_data["audits"] == []

    def test_get_audit_history_with_pagination(self, authenticated_client):
        """Test audit history with custom pagination parameters."""
        # Make the request with pagination
        response = authenticated_client.get("/api/v1/audits/history?limit=20&offset=10")
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["limit"] == 20
        assert response_data["offset"] == 10

    def test_get_audit_history_unauthenticated(self, sync_client):
        """Test getting audit history without authentication."""
        # Make the request without authentication
        response = sync_client.get("/api/v1/audits/history")
        
        # Verify response
        assert response.status_code == 401  # Unauthorized

    async def test_get_audit_history_async(self, authenticated_async_client):
        """Test audit history with async client."""
        # Make the async request
        response = await authenticated_async_client.get("/api/v1/audits/history")
        
        # Verify response
        assert response.status_code == 200
        
        response_data = response.json()
        assert "audits" in response_data
        assert "total" in response_data