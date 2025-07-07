"""
AI Service for Google Vertex AI integration.

This module provides the sole gateway to Google Vertex AI for Gemini model interactions.
It handles all communication with Vertex AI and includes robust error handling
for authentication, configuration, and API-related issues.
"""

import json
import structlog
from typing import Optional, List
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from google.api_core import exceptions as google_exceptions
import os


# Initialize structured logger
logger = structlog.get_logger(__name__)

# Initialize Vertex AI client with error handling
vertex_model = None

try:
    # Initialize Vertex AI
    # The project ID and location can be set via environment variables:
    # GOOGLE_CLOUD_PROJECT or GCP_PROJECT for project ID
    # GOOGLE_CLOUD_REGION for location (defaults to us-central1)
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT') or os.environ.get('GCP_PROJECT')
    location = os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1')
    
    if project_id:
        vertexai.init(project=project_id, location=location)
        
        # Initialize the Gemini model
        vertex_model = GenerativeModel("gemini-2.5-pro")
        logger.info("Google Vertex AI client initialized successfully", 
                   project=project_id, location=location)
    else:
        logger.warning("Google Cloud project ID not found in environment variables")
        vertex_model = None
        
except Exception as e:
    logger.error("Failed to initialize Google Vertex AI client", error=str(e))
    vertex_model = None


def invoke_gemini_model(
    prompt: str, 
    model_name: str = "gemini-2.5-pro",
    response_mime_type: str = "application/json"
) -> str:
    """
    Invoke Gemini model via Google Vertex AI.
    
    This function sends prompts to the Gemini model and handles all error 
    scenarios gracefully. It's configured to return JSON responses by default.
    
    Args:
        prompt (str): The prompt to send to the Gemini model
        model_name (str): The Gemini model name to use (defaults to gemini-1.5-pro-001)
        response_mime_type (str): The expected response format (defaults to JSON)
        
    Returns:
        str: The model's response text, or empty string on failure
        
    Raises:
        RuntimeError: If Vertex AI client is not initialized
        ValueError: If prompt is empty or None
    """
    # Validate inputs
    if not prompt or not prompt.strip():
        logger.error("Empty or None prompt provided")
        raise ValueError("Prompt cannot be empty or None")
    
    # Check if client is initialized
    if vertex_model is None:
        logger.error("Vertex AI model is not initialized")
        raise RuntimeError("Google Vertex AI client is not available")
    
    try:
        # Configure generation parameters
        generation_config = GenerationConfig(
            max_output_tokens=4000,
            temperature=0.7,
            response_mime_type=response_mime_type
        )
        
        logger.info(
            "Invoking Gemini model",
            model_name=model_name,
            prompt_length=len(prompt)
        )
        
        # Generate content using the model
        response = vertex_model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Extract the text from the response
        if response and response.text:
            content = response.text
            logger.info(
                "Gemini model invocation successful",
                model_name=model_name,
                response_length=len(content)
            )
            return content
        else:
            logger.warning("No content in Gemini response")
            return ""
            
    except google_exceptions.InvalidArgument as e:
        # Handle invalid argument errors
        logger.error(
            "Invalid argument error",
            error=str(e),
            model_name=model_name
        )
        return ""
        
    except google_exceptions.ResourceExhausted as e:
        # Handle quota exceeded errors
        logger.error(
            "Resource exhausted (quota exceeded)",
            error=str(e),
            model_name=model_name
        )
        return ""
        
    except google_exceptions.PermissionDenied as e:
        # Handle permission errors
        logger.error(
            "Permission denied error",
            error=str(e),
            model_name=model_name
        )
        return ""
        
    except google_exceptions.GoogleAPIError as e:
        # Handle general Google API errors
        logger.error(
            "Google API error during model invocation",
            error=str(e),
            model_name=model_name
        )
        return ""
        
    except Exception as e:
        # Handle any other unexpected errors
        logger.error(
            "Unexpected error during model invocation",
            error=str(e),
            model_name=model_name
        )
        return ""


def get_available_models() -> List[str]:
    """
    Get list of available Gemini models from Google Vertex AI.
    
    Returns:
        list: List of available Gemini model names
    """
    # Common Gemini models available on Vertex AI
    gemini_models = [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.0-pro"
    ]
    
    if vertex_model is None:
        logger.warning("Vertex AI client not available, returning default models")
        return gemini_models
    
    try:
        # For now, we return the known Gemini models
        # In production, you might want to dynamically fetch available models
        logger.info("Returning available Gemini models", count=len(gemini_models))
        return gemini_models
        
    except Exception as e:
        logger.error("Failed to get available models", error=str(e))
        return gemini_models


def is_service_available() -> bool:
    """
    Check if the AI service is available and properly configured.
    
    Returns:
        bool: True if service is available, False otherwise
    """
    return vertex_model is not None


# For backward compatibility, maintain the same function name
# This allows the rest of the codebase to work without changes
def invoke_claude_model(prompt: str, model_id: str = None) -> str:
    """
    Backward compatibility wrapper for invoke_gemini_model.
    
    This function maintains the same interface as the old AWS Bedrock integration
    to minimize changes needed in the rest of the codebase.
    
    Args:
        prompt (str): The prompt to send to the model
        model_id (str): Ignored, uses default Gemini model
        
    Returns:
        str: The model's response text, or empty string on failure
    """
    return invoke_gemini_model(prompt, response_mime_type="application/json")