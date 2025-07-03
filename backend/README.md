# Project Aether Backend

SEO Intelligence Platform Backend Service

## Setup

```bash
poetry install
poetry run uvicorn main:app --reload
```

## Development

- **Framework:** FastAPI with Python 3.9+
- **Database:** PostgreSQL with SQLAlchemy 2.0
- **Task Queue:** Celery with Redis
- **Testing:** Pytest with coverage