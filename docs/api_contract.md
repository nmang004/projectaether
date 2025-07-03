# Project Aether API Contract Standards

## Overview

This document defines the RESTful API contract standards for Project Aether. All API endpoints must adhere to these standards to ensure consistency, maintainability, and a predictable developer experience.

## Base URL Structure

```
https://api.projectaether.internal/v1
```

All API endpoints are versioned under `/v1` to allow for future breaking changes without affecting existing integrations.

## Authentication

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Request Standards

### Content Type

All POST, PUT, and PATCH requests must include:

```
Content-Type: application/json
```

### Request Body Validation

Request bodies are validated using Pydantic models. Invalid requests will return a 422 Unprocessable Entity status with detailed validation errors.

## Response Standards

### Success Response Format

All successful responses follow this structure:

```json
{
  "data": {
    // Response data here
  },
  "meta": {
    // Optional metadata
  }
}
```

### Error Response Format

All error responses follow a standardized format:

```json
{
  "detail": "Human-readable error message",
  "type": "error_type_identifier",
  "errors": [
    {
      "field": "field_name",
      "message": "Field-specific error message"
    }
  ]
}
```

### HTTP Status Codes

- `200 OK`: Successful GET, PUT, or PATCH request
- `201 Created`: Successful POST request that creates a resource
- `202 Accepted`: Request accepted for async processing
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid request format or parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `502 Bad Gateway`: External service error

## Pagination

All endpoints that return lists implement cursor-based pagination:

### Query Parameters

- `limit`: Number of items per page (default: 20, max: 100)
- `offset`: Number of items to skip (default: 0)

### Response Format

```json
{
  "data": [
    // Array of items
  ],
  "meta": {
    "pagination": {
      "total": 1234,
      "limit": 20,
      "offset": 0,
      "has_next": true,
      "has_previous": false
    }
  }
}
```

### Example Request

```
GET /v1/sites/123/pages?limit=50&offset=100
```

## Asynchronous Operations

Long-running operations return immediately with a task ID:

### Initial Response

```json
{
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "pending",
    "created_at": "2025-07-02T12:00:00Z"
  }
}
```

### Task Status Endpoint

```
GET /v1/tasks/{task_id}
```

### Task Status Response

```json
{
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "in_progress|completed|failed",
    "progress": 75,
    "created_at": "2025-07-02T12:00:00Z",
    "updated_at": "2025-07-02T12:05:00Z",
    "result": {
      // Task results when completed
    },
    "error": {
      // Error details if failed
    }
  }
}
```

## Resource Endpoints

### Standard CRUD Operations

Each resource follows RESTful conventions:

- `GET /v1/{resource}` - List resources
- `POST /v1/{resource}` - Create resource
- `GET /v1/{resource}/{id}` - Get specific resource
- `PUT /v1/{resource}/{id}` - Update entire resource
- `PATCH /v1/{resource}/{id}` - Partial update
- `DELETE /v1/{resource}/{id}` - Delete resource

### Nested Resources

For related resources:

```
GET /v1/sites/{site_id}/crawls
POST /v1/sites/{site_id}/crawls
GET /v1/sites/{site_id}/crawls/{crawl_id}
```

## Filtering and Sorting

### Filtering

Use query parameters for filtering:

```
GET /v1/sites/123/pages?status=error&has_missing_meta=true
```

### Sorting

Use the `sort` parameter with field names. Prefix with `-` for descending:

```
GET /v1/sites/123/pages?sort=-word_count,title
```

## Rate Limiting

Rate limit information is included in response headers:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1625097600
```

## Webhook Events (Future Enhancement)

For async task completion notifications:

```json
{
  "event": "task.completed",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-07-02T12:05:00Z",
  "data": {
    // Task-specific data
  }
}
```

## API Versioning Strategy

- Version in URL path: `/v1/`, `/v2/`
- Breaking changes require new version
- Deprecation notices via headers:
  ```
  X-API-Deprecation: true
  X-API-Deprecation-Date: 2026-01-01
  ```

## Example API Calls

### 1. Create Site Crawl

**Request:**
```http
POST /v1/sites/123/crawls
Authorization: Bearer <token>
Content-Type: application/json

{
  "max_pages": 1000,
  "follow_robots_txt": true,
  "javascript_rendering": true
}
```

**Response:**
```json
{
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "pending",
    "created_at": "2025-07-02T12:00:00Z"
  }
}
```

### 2. Get Crawl Results

**Request:**
```http
GET /v1/sites/123/crawls/latest/pages?limit=20&offset=0&status=error
Authorization: Bearer <token>
```

**Response:**
```json
{
  "data": [
    {
      "id": "page-001",
      "url": "https://example.com/page1",
      "status_code": 404,
      "title": "Page Not Found",
      "issues": ["broken_link", "missing_meta_description"]
    }
  ],
  "meta": {
    "pagination": {
      "total": 45,
      "limit": 20,
      "offset": 0,
      "has_next": true,
      "has_previous": false
    }
  }
}
```

### 3. Generate Content Brief

**Request:**
```http
POST /v1/content-briefs
Authorization: Bearer <token>
Content-Type: application/json

{
  "keyword": "best seo tools 2025",
  "target_audience": "digital marketers",
  "content_type": "blog_post"
}
```

**Response:**
```json
{
  "data": {
    "task_id": "660e8400-e29b-41d4-a716-446655440001",
    "status": "pending",
    "estimated_duration": 45
  }
}
```

## Security Considerations

1. **HTTPS Only**: All API communication must use TLS 1.2+
2. **CORS**: Configured to allow only the frontend domain
3. **Input Validation**: All inputs validated and sanitized
4. **SQL Injection**: Prevented via parameterized queries
5. **Rate Limiting**: Prevents abuse and ensures fair usage
6. **API Keys**: Never exposed in responses or logs