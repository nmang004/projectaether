"""
AI Service for AWS Bedrock integration.

This module provides the sole gateway to AWS Bedrock for Claude model interactions.
It handles all communication with AWS Bedrock and includes robust error handling
for credential, region, and API-related issues.
"""

import json
import boto3
import structlog
from typing import Optional
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError


# Initialize structured logger
logger = structlog.get_logger(__name__)

# Initialize Bedrock client with error handling
bedrock_client = None

try:
    # Initialize the bedrock-runtime client
    bedrock_client = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1'  # Default region, can be overridden by AWS_DEFAULT_REGION
    )
    logger.info("AWS Bedrock client initialized successfully")
except NoCredentialsError as e:
    logger.error("AWS credentials not found", error=str(e))
    bedrock_client = None
except Exception as e:
    logger.error("Failed to initialize AWS Bedrock client", error=str(e))
    bedrock_client = None


def invoke_claude_model(
    prompt: str, 
    model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"
) -> str:
    """
    Invoke Claude model via AWS Bedrock.
    
    This function constructs the precise JSON payload required by the Bedrock
    InvokeModel API for Claude 3 models and handles all error scenarios gracefully.
    
    Args:
        prompt (str): The prompt to send to the Claude model
        model_id (str): The Claude model ID to use (defaults to Haiku)
        
    Returns:
        str: The model's response text, or empty string on failure
        
    Raises:
        RuntimeError: If Bedrock client is not initialized
        ValueError: If prompt is empty or None
    """
    # Validate inputs
    if not prompt or not prompt.strip():
        logger.error("Empty or None prompt provided")
        raise ValueError("Prompt cannot be empty or None")
    
    # Check if client is initialized
    if bedrock_client is None:
        logger.error("Bedrock client is not initialized")
        raise RuntimeError("AWS Bedrock client is not available")
    
    try:
        # Construct the Claude 3 API payload
        # This follows the exact format required by Bedrock for Claude models
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Convert payload to JSON string
        body = json.dumps(payload)
        
        logger.info(
            "Invoking Claude model",
            model_id=model_id,
            prompt_length=len(prompt)
        )
        
        # Make the API call to Bedrock
        response = bedrock_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        
        # Parse the response
        response_body = json.loads(response.get('body').read())
        
        # Extract the content from Claude's response
        # Claude 3 API returns content in a specific format
        if 'content' in response_body and len(response_body['content']) > 0:
            content = response_body['content'][0].get('text', '')
            logger.info(
                "Claude model invocation successful",
                model_id=model_id,
                response_length=len(content)
            )
            return content
        else:
            logger.warning("No content in Claude response", response_body=response_body)
            return ""
            
    except ClientError as e:
        # Handle specific AWS API errors
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', str(e))
        
        logger.error(
            "AWS Bedrock API error",
            error_code=error_code,
            error_message=error_message,
            model_id=model_id
        )
        return ""
        
    except BotoCoreError as e:
        # Handle boto3 core errors (network, timeout, etc.)
        logger.error(
            "Boto3 core error during model invocation",
            error=str(e),
            model_id=model_id
        )
        return ""
        
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        logger.error(
            "Failed to parse response JSON",
            error=str(e),
            model_id=model_id
        )
        return ""
        
    except Exception as e:
        # Handle any other unexpected errors
        logger.error(
            "Unexpected error during model invocation",
            error=str(e),
            model_id=model_id
        )
        return ""


def get_available_models() -> list:
    """
    Get list of available Claude models from AWS Bedrock.
    
    Returns:
        list: List of available Claude model IDs
    """
    # Common Claude 3 model IDs available on Bedrock
    claude_models = [
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-opus-20240229-v1:0"
    ]
    
    if bedrock_client is None:
        logger.warning("Bedrock client not available, returning default models")
        return claude_models
    
    try:
        # In a production environment, you might want to dynamically fetch
        # available models using bedrock_client.list_foundation_models()
        # For now, we return the known Claude models
        logger.info("Returning available Claude models", count=len(claude_models))
        return claude_models
        
    except Exception as e:
        logger.error("Failed to get available models", error=str(e))
        return claude_models


def is_service_available() -> bool:
    """
    Check if the AI service is available and properly configured.
    
    Returns:
        bool: True if service is available, False otherwise
    """
    return bedrock_client is not None