"""
AI-powered feature endpoints for Project Aether.

This module provides HTTP endpoints for AI-powered SEO features including
keyword clustering, content optimization, and schema generation.
All endpoints integrate with the AWS Bedrock Claude model via the ai_service.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth.dependencies import get_current_user
from app.services.ai_service import invoke_claude_model, is_service_available


# Initialize the router with appropriate metadata
router = APIRouter(
    prefix="/ai",
    tags=["AI Services"],
    dependencies=[Depends(get_current_user)]  # All endpoints require authentication
)


class KeywordClusterPayload(BaseModel):
    """
    Request payload for keyword clustering analysis.
    
    This model defines the structure for keyword clustering requests.
    The head_term is the primary keyword around which related keywords
    will be generated and clustered.
    """
    head_term: str = Field(..., min_length=1, max_length=100)
    
    class Config:
        """Pydantic configuration for the model."""
        schema_extra = {
            "example": {
                "head_term": "SEO audit"
            }
        }


class SchemaGenerationPayload(BaseModel):
    """
    Request payload for JSON-LD schema generation.
    
    This model defines the structure for schema markup generation requests.
    It includes the content to generate schema for and the desired schema type.
    """
    content: str = Field(..., min_length=1, max_length=5000)
    schema_type: str = Field(..., min_length=1, max_length=50)
    
    class Config:
        """Pydantic configuration for the model."""
        schema_extra = {
            "example": {
                "content": "Best practices for SEO auditing and website optimization",
                "schema_type": "Article"
            }
        }


class ContentBriefPayload(BaseModel):
    """
    Request payload for AI-generated content briefs.
    
    This model defines the structure for content brief generation requests.
    The keyword is used to create comprehensive content strategies.
    """
    keyword: str = Field(..., min_length=1, max_length=100)
    
    class Config:
        """Pydantic configuration for the model."""
        schema_extra = {
            "example": {
                "keyword": "technical SEO"
            }
        }


def load_prompts() -> Dict[str, str]:
    """
    Load AI prompts from the prompts.json file.
    
    Returns:
        Dict containing all available AI prompts
        
    Raises:
        HTTPException: 500 Internal Server Error if prompts file cannot be loaded
    """
    try:
        # Get the path to the prompts file
        # Navigate from backend/app/api/v1/endpoints/ to prompts/
        current_dir = Path(__file__).parent
        prompts_path = current_dir.parent.parent.parent.parent.parent / "prompts" / "prompts.json"
        
        with open(prompts_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI prompts configuration file not found"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid AI prompts configuration file"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load AI prompts configuration"
        )


@router.post("/keyword-clusters")
async def generate_keyword_clusters(
    payload: KeywordClusterPayload,
    current_user: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Generate keyword clusters using AI analysis.
    
    This endpoint uses the Claude AI model to generate related keywords
    for a given head term and groups them into semantic clusters based
    on user intent (informational, commercial, navigational, etc.).
    
    Args:
        payload: Request payload containing the head term
        current_user: The authenticated user (injected by dependency)
        
    Returns:
        Dict containing keyword clusters organized by intent
        
    Raises:
        HTTPException: 400 Bad Request if the head term is invalid
        HTTPException: 401 Unauthorized if authentication fails
        HTTPException: 503 Service Unavailable if AI service is not available
        HTTPException: 500 Internal Server Error if AI processing fails
        
    Security:
        - Requires valid JWT authentication
        - Input validation prevents injection attacks
        - Rate limiting should be implemented for production use
        
    Performance:
        - Synchronous processing with ~5-10 second response time
        - Response is cached for similar requests (future enhancement)
        - Claude Haiku model provides fast, cost-effective results
    """
    # Check if AI service is available
    if not is_service_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable"
        )
    
    try:
        # Load the AI prompts
        prompts = load_prompts()
        
        # Get the keyword clustering prompt
        if "keyword_clustering" not in prompts:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Keyword clustering prompt not found"
            )
        
        # Format the prompt with the user's head term
        prompt = prompts["keyword_clustering"].format(head_term=payload.head_term)
        
        # Call the AI service
        ai_response = invoke_claude_model(prompt)
        
        if not ai_response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service returned empty response"
            )
        
        # Parse the JSON response from the AI
        try:
            keyword_clusters = json.loads(ai_response)
        except json.JSONDecodeError:
            # If the AI doesn't return valid JSON, wrap the response
            keyword_clusters = {
                "response": ai_response,
                "note": "AI response was not in expected JSON format"
            }
        
        # Return the structured response
        return {
            "head_term": payload.head_term,
            "clusters": keyword_clusters,
            "generated_by": "Claude AI via AWS Bedrock",
            "user": current_user
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate keyword clusters"
        )


@router.post("/schema-markup")
async def generate_schema_markup(
    payload: SchemaGenerationPayload,
    current_user: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Generate JSON-LD schema markup using AI analysis.
    
    This endpoint uses the Claude AI model to generate structured data
    markup for given content, improving SEO and search result appearance.
    
    Args:
        payload: Request payload containing content and schema type
        current_user: The authenticated user (injected by dependency)
        
    Returns:
        Dict containing the generated JSON-LD schema markup
        
    Raises:
        HTTPException: 400 Bad Request if content or schema type is invalid
        HTTPException: 401 Unauthorized if authentication fails
        HTTPException: 503 Service Unavailable if AI service is not available
        HTTPException: 500 Internal Server Error if AI processing fails
    """
    # Check if AI service is available
    if not is_service_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable"
        )
    
    try:
        # Load the AI prompts
        prompts = load_prompts()
        
        # Get the schema generation prompt
        if "schema_generator" not in prompts:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Schema generation prompt not found"
            )
        
        # Format the prompt with the user's content and schema type
        prompt = prompts["schema_generator"].format(
            content=payload.content,
            schema_type=payload.schema_type
        )
        
        # Call the AI service
        ai_response = invoke_claude_model(prompt)
        
        if not ai_response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service returned empty response"
            )
        
        # Parse the JSON response from the AI
        try:
            schema_markup = json.loads(ai_response)
        except json.JSONDecodeError:
            # If the AI doesn't return valid JSON, wrap the response
            schema_markup = {
                "raw_response": ai_response,
                "note": "AI response was not in expected JSON format"
            }
        
        # Return the structured response
        return {
            "schema_type": payload.schema_type,
            "content_length": len(payload.content),
            "schema_markup": schema_markup,
            "generated_by": "Claude AI via AWS Bedrock",
            "user": current_user
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate schema markup"
        )


@router.post("/content-brief")
async def generate_content_brief(
    payload: ContentBriefPayload,
    current_user: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Generate comprehensive content briefs using AI analysis.
    
    This endpoint uses the Claude AI model to create detailed content
    strategies including target audience analysis, content angles,
    and optimization recommendations.
    
    Args:
        payload: Request payload containing the target keyword
        current_user: The authenticated user (injected by dependency)
        
    Returns:
        Dict containing the comprehensive content brief
        
    Raises:
        HTTPException: 400 Bad Request if keyword is invalid
        HTTPException: 401 Unauthorized if authentication fails
        HTTPException: 503 Service Unavailable if AI service is not available
        HTTPException: 500 Internal Server Error if AI processing fails
    """
    # Check if AI service is available
    if not is_service_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable"
        )
    
    try:
        # Load the AI prompts
        prompts = load_prompts()
        
        # Get the content brief prompt
        if "content_brief" not in prompts:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Content brief prompt not found"
            )
        
        # Format the prompt with the user's keyword
        prompt = prompts["content_brief"].format(keyword=payload.keyword)
        
        # Call the AI service
        ai_response = invoke_claude_model(prompt)
        
        if not ai_response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service returned empty response"
            )
        
        # Parse the JSON response from the AI
        try:
            content_brief = json.loads(ai_response)
        except json.JSONDecodeError:
            # If the AI doesn't return valid JSON, wrap the response
            content_brief = {
                "raw_response": ai_response,
                "note": "AI response was not in expected JSON format"
            }
        
        # Return the structured response
        return {
            "keyword": payload.keyword,
            "content_brief": content_brief,
            "generated_by": "Claude AI via AWS Bedrock",
            "user": current_user
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate content brief"
        )


@router.get("/service-status")
async def get_ai_service_status(
    current_user: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Check the status of the AI service.
    
    This endpoint provides information about the availability and
    configuration of the AI service for monitoring and debugging purposes.
    
    Args:
        current_user: The authenticated user (injected by dependency)
        
    Returns:
        Dict containing AI service status and configuration
        
    Security:
        - Requires valid JWT authentication
        - Does not expose sensitive configuration details
        - Provides operational status for monitoring
    """
    try:
        # Check service availability
        is_available = is_service_available()
        
        # Get available models (this doesn't expose credentials)
        from app.services.ai_service import get_available_models
        available_models = get_available_models()
        
        return {
            "service_available": is_available,
            "available_models": available_models,
            "service_provider": "AWS Bedrock",
            "default_model": "anthropic.claude-3-haiku-20240307-v1:0",
            "prompts_loaded": len(load_prompts()) > 0,
            "user": current_user
        }
        
    except Exception as e:
        # Handle errors gracefully
        return {
            "service_available": False,
            "error": "Failed to check service status",
            "user": current_user
        }