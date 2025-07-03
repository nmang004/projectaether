# Project Aether API Endpoints Guide

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Site Audit Endpoints](#site-audit-endpoints)
4. [AI Feature Endpoints](#ai-feature-endpoints)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Examples](#examples)

## Overview

The Project Aether API provides a comprehensive suite of endpoints for SEO intelligence and website analysis. All endpoints follow RESTful conventions and return JSON responses. The API is versioned with the current version being v1.

**Base URL:** `https://api.projectaether.com/api/v1`  
**Documentation:** `https://api.projectaether.com/docs`

## Authentication

All protected endpoints require JWT Bearer token authentication. Tokens are obtained through the authentication endpoints and must be included in the Authorization header.

### Authentication Header Format
```
Authorization: Bearer <your-jwt-token>
```

### Authentication Endpoints

#### POST /api/v1/auth/login
Login with email and password to obtain JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### POST /api/v1/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "your-password",
  "full_name": "John Doe"
}
```

## Site Audit Endpoints

The site audit endpoints provide comprehensive website analysis capabilities, including SEO audits, performance analysis, and technical issue detection.

### POST /api/v1/audits/start
🔐 **Authentication Required**

Start a comprehensive site audit that analyzes SEO issues, performance metrics, and technical problems.

**Request Body:**
```json
{
  "root_url": "https://example.com",
  "max_depth": 3,
  "max_pages": 100
}
```

**Parameters:**
- `root_url` (required): The website URL to audit
- `max_depth` (optional): Maximum crawl depth (default: 3)
- `max_pages` (optional): Maximum pages to crawl (default: 100)

**Response:**
```json
{
  "task_id": "12345678-1234-1234-1234-123456789012",
  "status": "pending",
  "message": "Site audit task started successfully",
  "root_url": "https://example.com"
}
```

**HTTP Status Codes:**
- `200 OK`: Audit started successfully
- `400 Bad Request`: Invalid URL or parameters
- `401 Unauthorized`: Authentication required
- `500 Internal Server Error`: Server error

### GET /api/v1/audits/status/{task_id}
🔐 **Authentication Required**

Check the status and progress of a site audit task.

**URL Parameters:**
- `task_id`: The unique task identifier returned by the start endpoint

**Response States:**

**PENDING:**
```json
{
  "task_id": "12345678-1234-1234-1234-123456789012",
  "status": "PENDING",
  "message": "Task is waiting to be processed",
  "result": null,
  "progress": null,
  "error": null
}
```

**PROGRESS:**
```json
{
  "task_id": "12345678-1234-1234-1234-123456789012",
  "status": "PROGRESS",
  "message": "Task is being processed",
  "progress": {
    "phase": "crawling",
    "progress": 45,
    "total": 100,
    "crawled": 45,
    "current_url": "https://example.com/page-45"
  },
  "result": null,
  "error": null
}
```

**SUCCESS:**
```json
{
  "task_id": "12345678-1234-1234-1234-123456789012",
  "status": "SUCCESS",
  "message": "Task completed successfully",
  "result": {
    "project_id": 1,
    "root_url": "https://example.com",
    "crawl_summary": {
      "total_pages_crawled": 50,
      "total_pages_discovered": 65,
      "crawl_depth_reached": 3,
      "crawl_duration_seconds": 180,
      "crawl_status": "completed"
    },
    "seo_metrics": {
      "pages_with_missing_titles": 5,
      "pages_with_missing_descriptions": 8,
      "pages_with_duplicate_titles": 3,
      "pages_with_duplicate_descriptions": 4,
      "pages_with_missing_h1": 2,
      "pages_with_broken_links": 7,
      "average_page_load_time": 2.3,
      "pages_with_images_missing_alt": 12
    },
    "technical_issues": {
      "pages_with_4xx_errors": 3,
      "pages_with_5xx_errors": 1,
      "pages_with_redirect_chains": 4,
      "pages_with_large_dom": 6,
      "pages_with_render_blocking_resources": 15
    },
    "performance_metrics": {
      "average_first_contentful_paint": 1.4,
      "average_largest_contentful_paint": 2.8,
      "average_cumulative_layout_shift": 0.06,
      "pages_failing_core_web_vitals": 12
    }
  },
  "progress": null,
  "error": null
}
```

**FAILURE:**
```json
{
  "task_id": "12345678-1234-1234-1234-123456789012",
  "status": "FAILURE",
  "message": "Task failed to complete",
  "result": null,
  "progress": null,
  "error": "Connection timeout: Unable to connect to https://example.com"
}
```

### GET /api/v1/audits/history
🔐 **Authentication Required**

Retrieve the audit history for the authenticated user with pagination support.

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 10, max: 100)
- `offset` (optional): Number of records to skip (default: 0)

**Response:**
```json
{
  "audits": [
    {
      "task_id": "12345678-1234-1234-1234-123456789012",
      "root_url": "https://example.com",
      "status": "SUCCESS",
      "created_at": "2025-07-03T10:30:00Z",
      "completed_at": "2025-07-03T10:35:00Z",
      "pages_crawled": 50,
      "issues_found": 25
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

## AI Feature Endpoints

The AI endpoints provide advanced SEO capabilities powered by Claude AI, including keyword research, content optimization, and schema generation.

### POST /api/v1/ai/keyword-clusters
🔐 **Authentication Required**

Generate keyword clusters for a given head term using AI analysis.

**Request Body:**
```json
{
  "head_term": "SEO audit"
}
```

**Response:**
```json
{
  "head_term": "SEO audit",
  "clusters": {
    "Informational": [
      "what is SEO audit",
      "SEO audit checklist",
      "how to do SEO audit",
      "SEO audit guide",
      "SEO audit tutorial"
    ],
    "Commercial": [
      "SEO audit service",
      "SEO audit tool",
      "best SEO audit software",
      "SEO audit agency",
      "professional SEO audit"
    ],
    "Navigational": [
      "Google SEO audit",
      "Semrush SEO audit",
      "Ahrefs SEO audit",
      "Screaming Frog SEO audit"
    ]
  },
  "generated_by": "Claude AI via AWS Bedrock",
  "user": "user@example.com"
}
```

### POST /api/v1/ai/schema-markup
🔐 **Authentication Required**

Generate JSON-LD schema markup for content using AI analysis.

**Request Body:**
```json
{
  "content": "Best practices for SEO auditing and website optimization",
  "schema_type": "Article"
}
```

**Response:**
```json
{
  "schema_type": "Article",
  "content_length": 54,
  "schema_markup": {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Best practices for SEO auditing and website optimization",
    "description": "Comprehensive guide to SEO auditing best practices",
    "author": {
      "@type": "Organization",
      "name": "Project Aether"
    },
    "datePublished": "2025-07-03",
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": "https://example.com/seo-audit-guide"
    }
  },
  "generated_by": "Claude AI via AWS Bedrock",
  "user": "user@example.com"
}
```

### POST /api/v1/ai/content-brief
🔐 **Authentication Required**

Generate comprehensive content briefs using AI analysis.

**Request Body:**
```json
{
  "keyword": "technical SEO"
}
```

**Response:**
```json
{
  "keyword": "technical SEO",
  "content_brief": {
    "target_audience": "SEO professionals, web developers, and digital marketers",
    "content_angle": "Comprehensive technical guide with actionable strategies",
    "key_points": [
      "Website crawlability and indexation",
      "Site speed optimization",
      "Mobile-first indexing",
      "Core Web Vitals",
      "Structured data implementation"
    ],
    "suggested_word_count": 2500,
    "internal_linking_opportunities": [
      "Link to SEO audit tools",
      "Reference page speed guides",
      "Connect to schema markup articles"
    ]
  },
  "generated_by": "Claude AI via AWS Bedrock",
  "user": "user@example.com"
}
```

### GET /api/v1/ai/service-status
🔐 **Authentication Required**

Check the availability and status of AI services.

**Response:**
```json
{
  "service_available": true,
  "available_models": [
    "anthropic.claude-3-haiku-20240307-v1:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0"
  ],
  "service_provider": "AWS Bedrock",
  "default_model": "anthropic.claude-3-haiku-20240307-v1:0",
  "prompts_loaded": true,
  "user": "user@example.com"
}
```

## Error Handling

All API endpoints return standardized error responses with appropriate HTTP status codes.

### Error Response Format
```json
{
  "detail": "Error message description",
  "status_code": 400,
  "error_type": "validation_error"
}
```

### Common HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request parameters or body
- **401 Unauthorized**: Authentication required or invalid token
- **403 Forbidden**: Access denied
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Service temporarily unavailable

### Validation Errors
```json
{
  "detail": [
    {
      "loc": ["body", "root_url"],
      "msg": "invalid or missing URL scheme",
      "type": "value_error.url.scheme"
    }
  ]
}
```

## Rate Limiting

Rate limiting is implemented to ensure fair usage and prevent abuse.

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1641024000
```

### Rate Limit Exceeded Response
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds.",
  "status_code": 429,
  "retry_after": 60
}
```

## Examples

### Complete Site Audit Workflow

1. **Start Audit**
```bash
curl -X POST "https://api.projectaether.com/api/v1/audits/start" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "root_url": "https://example.com",
    "max_depth": 3,
    "max_pages": 100
  }'
```

2. **Check Status**
```bash
curl -X GET "https://api.projectaether.com/api/v1/audits/status/12345678-1234-1234-1234-123456789012" \
  -H "Authorization: Bearer <your-token>"
```

3. **Get History**
```bash
curl -X GET "https://api.projectaether.com/api/v1/audits/history?limit=10&offset=0" \
  -H "Authorization: Bearer <your-token>"
```

### AI-Powered Keyword Research

```bash
curl -X POST "https://api.projectaether.com/api/v1/ai/keyword-clusters" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "head_term": "SEO audit"
  }'
```

### Schema Markup Generation

```bash
curl -X POST "https://api.projectaether.com/api/v1/ai/schema-markup" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Best practices for SEO auditing",
    "schema_type": "Article"
  }'
```

---

For more detailed information, please refer to the interactive API documentation available at `/docs` when the API is running.