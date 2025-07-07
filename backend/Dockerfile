# =============================================================================
# Multi-stage build for Python backend - Production optimized for Google Cloud Run
# =============================================================================

# Build stage: Install dependencies and build virtual environment
FROM python:3.11-slim as builder

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Poetry for dependency management
RUN pip install --no-cache-dir poetry

# Configure Poetry for production builds
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml poetry.lock ./

# Install production dependencies only
RUN poetry install --only=main --no-root && \
    mv $(poetry env info --path) /app/.venv && \
    find /app/.venv/bin -type f -exec sed -i '1s|^#!.*python.*|#!/app/.venv/bin/python|' {} + && \
    rm -rf $POETRY_CACHE_DIR

# =============================================================================
# Production stage: Lightweight runtime environment
# =============================================================================
FROM python:3.11-slim as production

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r aether && useradd -r -g aether aether

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code (excluding files listed in .dockerignore)
COPY . .

# Change ownership to aether user
RUN chown -R aether:aether /app

# Switch to non-root user for security
USER aether

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set Python environment variables for production
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose port 8000 for the application
EXPOSE 8000

# Health check for load balancers and orchestration systems
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command using gunicorn with uvicorn workers
# This provides better performance and stability for production workloads
CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "1", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--keep-alive", "5", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
