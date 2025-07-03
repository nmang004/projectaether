"""
External API Service for third-party integrations.

This module handles all non-AI third-party API calls and implements mandatory
Redis caching to minimize costs and improve performance. It serves as the
centralized gateway for external data sources.
"""

import json
import hashlib
import redis
import structlog
from typing import Dict, Any, Optional
from app.config import Settings


# Initialize structured logger
logger = structlog.get_logger(__name__)

# Initialize settings
settings = Settings()

# Initialize Redis client with error handling
redis_client = None

try:
    # Parse Redis URL and create client
    redis_client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,  # Automatically decode bytes to strings
        socket_connect_timeout=5,
        socket_timeout=5
    )
    # Test connection
    redis_client.ping()
    logger.info("Redis client initialized successfully", redis_url=settings.REDIS_URL)
except redis.ConnectionError as e:
    logger.error("Failed to connect to Redis", error=str(e), redis_url=settings.REDIS_URL)
    redis_client = None
except Exception as e:
    logger.error("Failed to initialize Redis client", error=str(e))
    redis_client = None


def _generate_cache_key(prefix: str, **kwargs) -> str:
    """
    Generate a consistent cache key from function parameters.
    
    Args:
        prefix (str): The cache key prefix (usually function name)
        **kwargs: Parameters to include in the key
        
    Returns:
        str: SHA256 hash-based cache key
    """
    # Create a sorted string representation of all parameters
    key_data = f"{prefix}:" + ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
    
    # Generate SHA256 hash to ensure consistent key length
    key_hash = hashlib.sha256(key_data.encode()).hexdigest()
    
    return f"{prefix}:{key_hash}"


def _get_cached_result(cache_key: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve cached result from Redis.
    
    Args:
        cache_key (str): The cache key to look up
        
    Returns:
        Optional[Dict[str, Any]]: Cached result or None if not found
    """
    if redis_client is None:
        logger.warning("Redis client not available, cache miss")
        return None
    
    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.debug("Cache hit", cache_key=cache_key)
            return json.loads(cached_data)
        else:
            logger.debug("Cache miss", cache_key=cache_key)
            return None
    except (redis.RedisError, json.JSONDecodeError) as e:
        logger.error("Failed to retrieve cached result", error=str(e), cache_key=cache_key)
        return None


def _set_cached_result(cache_key: str, result: Dict[str, Any], ttl: int = 86400) -> None:
    """
    Store result in Redis cache.
    
    Args:
        cache_key (str): The cache key to store under
        result (Dict[str, Any]): The result to cache
        ttl (int): Time to live in seconds (default: 24 hours)
    """
    if redis_client is None:
        logger.warning("Redis client not available, skipping cache")
        return
    
    try:
        cached_data = json.dumps(result)
        redis_client.setex(cache_key, ttl, cached_data)
        logger.debug("Result cached", cache_key=cache_key, ttl=ttl)
    except (redis.RedisError, json.JSONEncodeError) as e:
        logger.error("Failed to cache result", error=str(e), cache_key=cache_key)


def get_pagespeed_insights(url: str) -> Dict[str, Any]:
    """
    Get PageSpeed Insights data for a given URL.
    
    This function will eventually integrate with Google PageSpeed Insights API.
    For now, it returns realistic mock data with full caching implementation.
    
    Args:
        url (str): The URL to analyze
        
    Returns:
        Dict[str, Any]: PageSpeed Insights data
    """
    # Generate cache key
    cache_key = _generate_cache_key("pagespeed", url=url)
    
    # Check cache first
    cached_result = _get_cached_result(cache_key)
    if cached_result:
        logger.info("Returning cached PageSpeed data", url=url)
        return cached_result
    
    # Mock realistic PageSpeed Insights data
    # In production, this would be replaced with actual Google API call
    logger.info("Fetching PageSpeed Insights data", url=url)
    
    mock_data = {
        "url": url,
        "performance_score": 85,
        "metrics": {
            "first_contentful_paint": 1.2,
            "largest_contentful_paint": 2.1,
            "cumulative_layout_shift": 0.05,
            "first_input_delay": 15,
            "speed_index": 1.8,
            "time_to_interactive": 2.3
        },
        "opportunities": [
            {
                "id": "unused-css-rules",
                "title": "Remove unused CSS",
                "description": "Remove dead rules from stylesheets to reduce bytes",
                "savings": 150
            },
            {
                "id": "optimize-images",
                "title": "Properly size images",
                "description": "Serve images that are appropriately-sized",
                "savings": 250
            }
        ],
        "diagnostics": [
            {
                "id": "dom-size",
                "title": "Avoid an excessive DOM size",
                "description": "A large DOM will increase memory usage",
                "score": 0.8
            }
        ],
        "timestamp": "2024-01-01T00:00:00Z",
        "lighthouse_version": "10.0.0"
    }
    
    # Cache the result for 24 hours
    _set_cached_result(cache_key, mock_data, ttl=86400)
    
    logger.info("PageSpeed Insights data retrieved", url=url, score=mock_data["performance_score"])
    return mock_data


def get_serp_data(keyword: str, location: str = "US", language: str = "en") -> Dict[str, Any]:
    """
    Get SERP (Search Engine Results Page) data for a given keyword.
    
    This function will eventually integrate with SERP APIs like DataForSEO or SEMrush.
    For now, it returns realistic mock data with full caching implementation.
    
    Args:
        keyword (str): The keyword to analyze
        location (str): Geographic location for results (default: US)
        language (str): Language for results (default: en)
        
    Returns:
        Dict[str, Any]: SERP analysis data
    """
    # Generate cache key
    cache_key = _generate_cache_key("serp", keyword=keyword, location=location, language=language)
    
    # Check cache first
    cached_result = _get_cached_result(cache_key)
    if cached_result:
        logger.info("Returning cached SERP data", keyword=keyword)
        return cached_result
    
    # Mock realistic SERP data
    # In production, this would be replaced with actual SERP API call
    logger.info("Fetching SERP data", keyword=keyword, location=location)
    
    mock_data = {
        "keyword": keyword,
        "location": location,
        "language": language,
        "search_volume": 12000,
        "competition": "Medium",
        "cpc": 2.45,
        "results": [
            {
                "position": 1,
                "title": f"Ultimate Guide to {keyword}",
                "url": "https://example.com/guide",
                "description": f"Comprehensive guide covering everything about {keyword}",
                "domain": "example.com",
                "word_count": 2500
            },
            {
                "position": 2,
                "title": f"Best {keyword} Practices",
                "url": "https://another-site.com/best-practices",
                "description": f"Learn the best practices for {keyword}",
                "domain": "another-site.com",
                "word_count": 1800
            },
            {
                "position": 3,
                "title": f"{keyword} Tutorial",
                "url": "https://tutorial-site.com/tutorial",
                "description": f"Step-by-step tutorial for {keyword}",
                "domain": "tutorial-site.com",
                "word_count": 3200
            }
        ],
        "related_keywords": [
            f"{keyword} guide",
            f"{keyword} tutorial",
            f"{keyword} tips",
            f"best {keyword}",
            f"{keyword} examples"
        ],
        "questions": [
            f"What is {keyword}?",
            f"How to use {keyword}?",
            f"Why is {keyword} important?",
            f"When to use {keyword}?"
        ],
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    # Cache the result for 24 hours
    _set_cached_result(cache_key, mock_data, ttl=86400)
    
    logger.info("SERP data retrieved", keyword=keyword, search_volume=mock_data["search_volume"])
    return mock_data


def get_backlink_data(domain: str) -> Dict[str, Any]:
    """
    Get backlink analysis data for a given domain.
    
    This function will eventually integrate with backlink APIs like Ahrefs or Majestic.
    For now, it returns realistic mock data with full caching implementation.
    
    Args:
        domain (str): The domain to analyze
        
    Returns:
        Dict[str, Any]: Backlink analysis data
    """
    # Generate cache key
    cache_key = _generate_cache_key("backlinks", domain=domain)
    
    # Check cache first
    cached_result = _get_cached_result(cache_key)
    if cached_result:
        logger.info("Returning cached backlink data", domain=domain)
        return cached_result
    
    # Mock realistic backlink data
    logger.info("Fetching backlink data", domain=domain)
    
    mock_data = {
        "domain": domain,
        "total_backlinks": 15420,
        "referring_domains": 2340,
        "domain_rating": 45,
        "top_backlinks": [
            {
                "source_domain": "authoritative-site.com",
                "source_url": "https://authoritative-site.com/resources",
                "target_url": f"https://{domain}/page",
                "anchor_text": "quality resource",
                "domain_rating": 78,
                "first_seen": "2024-01-01"
            },
            {
                "source_domain": "blog-site.com",
                "source_url": "https://blog-site.com/article",
                "target_url": f"https://{domain}/guide",
                "anchor_text": "comprehensive guide",
                "domain_rating": 52,
                "first_seen": "2024-01-15"
            }
        ],
        "anchor_text_distribution": {
            "branded": 35,
            "exact_match": 15,
            "partial_match": 25,
            "generic": 25
        },
        "referring_domains_by_dr": {
            "0-10": 45,
            "11-30": 35,
            "31-50": 15,
            "51-70": 4,
            "71-100": 1
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    # Cache the result for 24 hours
    _set_cached_result(cache_key, mock_data, ttl=86400)
    
    logger.info("Backlink data retrieved", domain=domain, total_backlinks=mock_data["total_backlinks"])
    return mock_data


def clear_cache(pattern: str = "*") -> int:
    """
    Clear cached results matching a pattern.
    
    Args:
        pattern (str): Redis key pattern to match (default: all keys)
        
    Returns:
        int: Number of keys deleted
    """
    if redis_client is None:
        logger.warning("Redis client not available, cannot clear cache")
        return 0
    
    try:
        keys = redis_client.keys(pattern)
        if keys:
            deleted = redis_client.delete(*keys)
            logger.info("Cache cleared", pattern=pattern, deleted_keys=deleted)
            return deleted
        else:
            logger.info("No keys found matching pattern", pattern=pattern)
            return 0
    except redis.RedisError as e:
        logger.error("Failed to clear cache", error=str(e), pattern=pattern)
        return 0


def get_cache_stats() -> Dict[str, Any]:
    """
    Get Redis cache statistics.
    
    Returns:
        Dict[str, Any]: Cache statistics
    """
    if redis_client is None:
        return {"available": False, "error": "Redis client not available"}
    
    try:
        info = redis_client.info()
        return {
            "available": True,
            "used_memory": info.get("used_memory_human", "N/A"),
            "connected_clients": info.get("connected_clients", 0),
            "total_commands_processed": info.get("total_commands_processed", 0),
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0)
        }
    except redis.RedisError as e:
        return {"available": False, "error": str(e)}


def is_service_available() -> bool:
    """
    Check if the external API service is available and properly configured.
    
    Returns:
        bool: True if service is available, False otherwise
    """
    return redis_client is not None