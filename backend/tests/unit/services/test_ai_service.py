"""
Unit tests for the AI service module.

This module tests the AI service functions in isolation, mocking all external
dependencies including boto3 calls. These tests ensure the business logic
works correctly without actually calling AWS Bedrock.
"""

import json
import pytest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from app.services import ai_service


class TestInvokeClaudeModel:
    """Test cases for the invoke_claude_model function."""

    def test_invoke_claude_model_success(self, mocker):
        """Test successful Claude model invocation."""
        # Mock the boto3 client
        mock_bedrock_client = MagicMock()
        mock_response = {
            'body': MagicMock()
        }
        mock_response_body = {
            'content': [
                {
                    'text': 'This is a test response from Claude'
                }
            ]
        }
        mock_response['body'].read.return_value = json.dumps(mock_response_body).encode()
        mock_bedrock_client.invoke_model.return_value = mock_response
        
        # Patch the bedrock_client in ai_service
        mocker.patch.object(ai_service, 'bedrock_client', mock_bedrock_client)
        
        # Test parameters
        test_prompt = "What is the capital of France?"
        test_model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        
        # Call the function
        result = ai_service.invoke_claude_model(test_prompt, test_model_id)
        
        # Verify the result
        assert result == 'This is a test response from Claude'
        
        # Verify the boto3 call was made with correct parameters
        mock_bedrock_client.invoke_model.assert_called_once()
        call_args = mock_bedrock_client.invoke_model.call_args
        
        # Check the call arguments
        assert call_args[1]['modelId'] == test_model_id
        assert call_args[1]['accept'] == 'application/json'
        assert call_args[1]['contentType'] == 'application/json'
        
        # Check the payload structure
        body = json.loads(call_args[1]['body'])
        assert body['anthropic_version'] == 'bedrock-2023-05-31'
        assert body['max_tokens'] == 4000
        assert len(body['messages']) == 1
        assert body['messages'][0]['role'] == 'user'
        assert body['messages'][0]['content'] == test_prompt

    def test_invoke_claude_model_empty_prompt(self, mocker):
        """Test error handling for empty prompt."""
        # Mock the bedrock_client
        mock_bedrock_client = MagicMock()
        mocker.patch.object(ai_service, 'bedrock_client', mock_bedrock_client)
        
        # Test with empty prompt
        with pytest.raises(ValueError, match="Prompt cannot be empty or None"):
            ai_service.invoke_claude_model("")
            
        # Test with None prompt
        with pytest.raises(ValueError, match="Prompt cannot be empty or None"):
            ai_service.invoke_claude_model(None)
            
        # Test with whitespace-only prompt
        with pytest.raises(ValueError, match="Prompt cannot be empty or None"):
            ai_service.invoke_claude_model("   ")

    def test_invoke_claude_model_no_client(self, mocker):
        """Test error handling when bedrock client is not available."""
        # Mock bedrock_client as None
        mocker.patch.object(ai_service, 'bedrock_client', None)
        
        with pytest.raises(RuntimeError, match="AWS Bedrock client is not available"):
            ai_service.invoke_claude_model("test prompt")

    def test_invoke_claude_model_client_error(self, mocker):
        """Test error handling for AWS client errors."""
        # Mock the boto3 client to raise ClientError
        mock_bedrock_client = MagicMock()
        mock_bedrock_client.invoke_model.side_effect = ClientError(
            error_response={
                'Error': {
                    'Code': 'ValidationException',
                    'Message': 'Invalid model ID'
                }
            },
            operation_name='InvokeModel'
        )
        
        mocker.patch.object(ai_service, 'bedrock_client', mock_bedrock_client)
        
        # Call the function and expect empty string return
        result = ai_service.invoke_claude_model("test prompt")
        
        # Should return empty string on error
        assert result == ""

    def test_invoke_claude_model_boto_core_error(self, mocker):
        """Test error handling for boto3 core errors."""
        # Mock the boto3 client to raise BotoCoreError
        mock_bedrock_client = MagicMock()
        mock_bedrock_client.invoke_model.side_effect = BotoCoreError()
        
        mocker.patch.object(ai_service, 'bedrock_client', mock_bedrock_client)
        
        # Call the function and expect empty string return
        result = ai_service.invoke_claude_model("test prompt")
        
        # Should return empty string on error
        assert result == ""

    def test_invoke_claude_model_json_decode_error(self, mocker):
        """Test error handling for JSON decode errors."""
        # Mock the boto3 client to return invalid JSON
        mock_bedrock_client = MagicMock()
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = b'invalid json'
        mock_bedrock_client.invoke_model.return_value = mock_response
        
        mocker.patch.object(ai_service, 'bedrock_client', mock_bedrock_client)
        
        # Call the function and expect empty string return
        result = ai_service.invoke_claude_model("test prompt")
        
        # Should return empty string on error
        assert result == ""

    def test_invoke_claude_model_no_content(self, mocker):
        """Test handling of response with no content."""
        # Mock the boto3 client to return response without content
        mock_bedrock_client = MagicMock()
        mock_response = {
            'body': MagicMock()
        }
        mock_response_body = {
            'content': []  # Empty content array
        }
        mock_response['body'].read.return_value = json.dumps(mock_response_body).encode()
        mock_bedrock_client.invoke_model.return_value = mock_response
        
        mocker.patch.object(ai_service, 'bedrock_client', mock_bedrock_client)
        
        # Call the function
        result = ai_service.invoke_claude_model("test prompt")
        
        # Should return empty string when no content
        assert result == ""

    def test_invoke_claude_model_default_parameters(self, mocker):
        """Test that default parameters are used correctly."""
        # Mock the boto3 client
        mock_bedrock_client = MagicMock()
        mock_response = {
            'body': MagicMock()
        }
        mock_response_body = {
            'content': [
                {
                    'text': 'Default model response'
                }
            ]
        }
        mock_response['body'].read.return_value = json.dumps(mock_response_body).encode()
        mock_bedrock_client.invoke_model.return_value = mock_response
        
        mocker.patch.object(ai_service, 'bedrock_client', mock_bedrock_client)
        
        # Call the function with only prompt (using defaults)
        result = ai_service.invoke_claude_model("test prompt")
        
        # Verify the result
        assert result == 'Default model response'
        
        # Verify default model ID was used
        call_args = mock_bedrock_client.invoke_model.call_args
        assert call_args[1]['modelId'] == "anthropic.claude-3-haiku-20240307-v1:0"


class TestGetAvailableModels:
    """Test cases for the get_available_models function."""

    def test_get_available_models_success(self, mocker):
        """Test successful retrieval of available models."""
        # Mock the bedrock_client
        mock_bedrock_client = MagicMock()
        mocker.patch.object(ai_service, 'bedrock_client', mock_bedrock_client)
        
        # Call the function
        result = ai_service.get_available_models()
        
        # Verify the result contains expected models
        expected_models = [
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-opus-20240229-v1:0"
        ]
        assert result == expected_models

    def test_get_available_models_no_client(self, mocker):
        """Test get_available_models when client is not available."""
        # Mock bedrock_client as None
        mocker.patch.object(ai_service, 'bedrock_client', None)
        
        # Call the function
        result = ai_service.get_available_models()
        
        # Should still return default models
        expected_models = [
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-opus-20240229-v1:0"
        ]
        assert result == expected_models


class TestIsServiceAvailable:
    """Test cases for the is_service_available function."""

    def test_is_service_available_true(self, mocker):
        """Test service availability when client is available."""
        # Mock the bedrock_client
        mock_bedrock_client = MagicMock()
        mocker.patch.object(ai_service, 'bedrock_client', mock_bedrock_client)
        
        # Call the function
        result = ai_service.is_service_available()
        
        # Should return True when client is available
        assert result is True

    def test_is_service_available_false(self, mocker):
        """Test service availability when client is not available."""
        # Mock bedrock_client as None
        mocker.patch.object(ai_service, 'bedrock_client', None)
        
        # Call the function
        result = ai_service.is_service_available()
        
        # Should return False when client is not available
        assert result is False