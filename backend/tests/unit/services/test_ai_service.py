"""
Unit tests for the AI service module.

This module tests the AI service functions in isolation, mocking all external
dependencies including Vertex AI calls. These tests ensure the business logic
works correctly without actually calling Google Vertex AI.
"""

import json
import pytest
from unittest.mock import MagicMock, patch, Mock
from google.api_core import exceptions as google_exceptions

from app.services import ai_service


class TestInvokeGeminiModel:
    """Test cases for the invoke_gemini_model function."""

    def test_invoke_gemini_model_success(self, mocker):
        """Test successful Gemini model invocation."""
        # Mock the vertex model
        mock_vertex_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = 'This is a test response from Gemini'
        mock_vertex_model.generate_content.return_value = mock_response
        
        # Patch the vertex_model in ai_service
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Test parameters
        test_prompt = "What is the capital of France?"
        test_model_name = "gemini-2.5-pro"
        
        # Call the function
        result = ai_service.invoke_gemini_model(test_prompt, test_model_name)
        
        # Verify the result
        assert result == 'This is a test response from Gemini'
        
        # Verify the Vertex AI call was made
        mock_vertex_model.generate_content.assert_called_once()
        call_args = mock_vertex_model.generate_content.call_args
        
        # Check the prompt was passed correctly
        assert call_args[0][0] == test_prompt

    def test_invoke_gemini_model_empty_prompt(self, mocker):
        """Test error handling for empty prompt."""
        # Mock the vertex_model
        mock_vertex_model = MagicMock()
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Test with empty prompt
        with pytest.raises(ValueError, match="Prompt cannot be empty or None"):
            ai_service.invoke_gemini_model("")
            
        # Test with None prompt
        with pytest.raises(ValueError, match="Prompt cannot be empty or None"):
            ai_service.invoke_gemini_model(None)
            
        # Test with whitespace-only prompt
        with pytest.raises(ValueError, match="Prompt cannot be empty or None"):
            ai_service.invoke_gemini_model("   ")

    def test_invoke_gemini_model_no_client(self, mocker):
        """Test error handling when vertex model is not available."""
        # Mock vertex_model as None
        mocker.patch.object(ai_service, 'vertex_model', None)
        
        with pytest.raises(RuntimeError, match="Google Vertex AI client is not available"):
            ai_service.invoke_gemini_model("test prompt")

    def test_invoke_gemini_model_invalid_argument_error(self, mocker):
        """Test error handling for Google API invalid argument errors."""
        # Mock the vertex model to raise InvalidArgument
        mock_vertex_model = MagicMock()
        mock_vertex_model.generate_content.side_effect = google_exceptions.InvalidArgument(
            "Invalid argument"
        )
        
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Call the function and expect empty string return
        result = ai_service.invoke_gemini_model("test prompt")
        
        # Should return empty string on error
        assert result == ""

    def test_invoke_gemini_model_resource_exhausted_error(self, mocker):
        """Test error handling for quota exceeded errors."""
        # Mock the vertex model to raise ResourceExhausted
        mock_vertex_model = MagicMock()
        mock_vertex_model.generate_content.side_effect = google_exceptions.ResourceExhausted(
            "Quota exceeded"
        )
        
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Call the function and expect empty string return
        result = ai_service.invoke_gemini_model("test prompt")
        
        # Should return empty string on error
        assert result == ""

    def test_invoke_gemini_model_permission_denied_error(self, mocker):
        """Test error handling for permission denied errors."""
        # Mock the vertex model to raise PermissionDenied
        mock_vertex_model = MagicMock()
        mock_vertex_model.generate_content.side_effect = google_exceptions.PermissionDenied(
            "Permission denied"
        )
        
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Call the function and expect empty string return
        result = ai_service.invoke_gemini_model("test prompt")
        
        # Should return empty string on error
        assert result == ""

    def test_invoke_gemini_model_general_api_error(self, mocker):
        """Test error handling for general Google API errors."""
        # Mock the vertex model to raise GoogleAPIError
        mock_vertex_model = MagicMock()
        mock_vertex_model.generate_content.side_effect = google_exceptions.GoogleAPIError(
            "API Error"
        )
        
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Call the function and expect empty string return
        result = ai_service.invoke_gemini_model("test prompt")
        
        # Should return empty string on error
        assert result == ""

    def test_invoke_gemini_model_no_content(self, mocker):
        """Test handling of response with no content."""
        # Mock the vertex model to return response without text
        mock_vertex_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = None
        mock_vertex_model.generate_content.return_value = mock_response
        
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Call the function
        result = ai_service.invoke_gemini_model("test prompt")
        
        # Should return empty string when no content
        assert result == ""

    def test_invoke_gemini_model_default_parameters(self, mocker):
        """Test that default parameters are used correctly."""
        # Mock the vertex model
        mock_vertex_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = 'Default model response'
        mock_vertex_model.generate_content.return_value = mock_response
        
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Call the function with only prompt (using defaults)
        result = ai_service.invoke_gemini_model("test prompt")
        
        # Verify the result
        assert result == 'Default model response'
        
        # Verify the call was made
        mock_vertex_model.generate_content.assert_called_once()


class TestInvokeClaudeModel:
    """Test cases for the backward compatibility invoke_claude_model function."""

    def test_invoke_claude_model_compatibility(self, mocker):
        """Test that invoke_claude_model calls invoke_gemini_model correctly."""
        # Mock invoke_gemini_model
        mock_invoke_gemini = mocker.patch.object(
            ai_service, 
            'invoke_gemini_model',
            return_value='Gemini response'
        )
        
        # Call the compatibility function
        result = ai_service.invoke_claude_model("test prompt", "ignored-model-id")
        
        # Verify it called invoke_gemini_model
        mock_invoke_gemini.assert_called_once_with(
            "test prompt", 
            response_mime_type="application/json"
        )
        
        # Verify the result
        assert result == 'Gemini response'


class TestGetAvailableModels:
    """Test cases for the get_available_models function."""

    def test_get_available_models_success(self, mocker):
        """Test successful retrieval of available models."""
        # Mock the vertex_model
        mock_vertex_model = MagicMock()
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Call the function
        result = ai_service.get_available_models()
        
        # Verify the result contains expected models
        expected_models = [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.0-pro"
        ]
        assert result == expected_models

    def test_get_available_models_no_client(self, mocker):
        """Test get_available_models when client is not available."""
        # Mock vertex_model as None
        mocker.patch.object(ai_service, 'vertex_model', None)
        
        # Call the function
        result = ai_service.get_available_models()
        
        # Should still return default models
        expected_models = [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.0-pro"
        ]
        assert result == expected_models


class TestIsServiceAvailable:
    """Test cases for the is_service_available function."""

    def test_is_service_available_true(self, mocker):
        """Test service availability when client is available."""
        # Mock the vertex_model
        mock_vertex_model = MagicMock()
        mocker.patch.object(ai_service, 'vertex_model', mock_vertex_model)
        
        # Call the function
        result = ai_service.is_service_available()
        
        # Should return True when client is available
        assert result is True

    def test_is_service_available_false(self, mocker):
        """Test service availability when client is not available."""
        # Mock vertex_model as None
        mocker.patch.object(ai_service, 'vertex_model', None)
        
        # Call the function
        result = ai_service.is_service_available()
        
        # Should return False when client is not available
        assert result is False