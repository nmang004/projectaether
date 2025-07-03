# Project Aether - Unified SEO Intelligence Platform

[![Backend Tests](https://img.shields.io/badge/backend%20tests-passing-brightgreen)](./backend/tests/)
[![Phase 1](https://img.shields.io/badge/phase%201-complete-success)](./docs/Phase1_QA_Readiness_Report.md)
[![Phase 2](https://img.shields.io/badge/phase%202-complete-success)](./docs/Phase2_QA_Audit_Report.md)
[![Code Coverage](https://img.shields.io/badge/coverage-80%25%2B-brightgreen)](./docs/Phase1_Step5_Completion.md)
[![Frontend Tests](https://img.shields.io/badge/frontend%20tests-passing-brightgreen)](./frontend/src/)

## Overview

**Project Aether** is a proprietary, internal SEO intelligence platform that unifies three critical pillars of SEO data:

1. **Live Site Data** - Acquired via sophisticated, JavaScript-aware web crawler
2. **Real-Time Market Data** - Sourced from industry-leading external APIs
3. **Generative AI Insights** - Powered by Amazon Bedrock's Foundation Models

The platform standardizes best practices, automates high-effort tasks, and scales the agency's ability to deliver consistent, data-driven SEO outcomes grounded in both technical reality and current market dynamics.

### Key Features

- 🕷️ **Live Site Audit & Technical Crawler** - Comprehensive website analysis
- 📊 **Performance & Core Web Vitals** - Real-time performance monitoring
- 🔗 **Backlink Intelligence** - Off-page SEO analysis
- 🤖 **AI-Powered Keyword Clustering** - Semantic keyword generation
- 📝 **SERP-Driven Content Briefs** - AI-powered content planning
- 🏷️ **Schema Markup Generator** - Automated JSON-LD generation
- 🔗 **AI-Assisted Internal Linking** - Contextual linking opportunities

## Architecture

### Technology Stack

**Backend (✅ COMPLETE)**
- **Language:** Python 3.11+
- **Framework:** FastAPI with Pydantic V2
- **Database:** PostgreSQL 15+ with SQLAlchemy 2.0 + Alembic
- **Cache/Queue:** Redis with Celery for background tasks
- **Crawler:** Scrapy with scrapy-playwright
- **AI Service:** AWS Bedrock (Claude models)
- **Authentication:** JWT with AWS Secrets Manager
- **Testing:** Pytest with 80%+ coverage

**Frontend (✅ COMPLETE)**
- **Framework:** React 18+ with TypeScript
- **Build Tool:** Vite
- **State Management:** Zustand + TanStack Query
- **UI Components:** Shadcn/UI + Tailwind CSS
- **Charts:** Recharts for data visualization
- **Testing:** Vitest with React Testing Library

**Infrastructure (🚧 PLANNED - Phase 3)**
- **Cloud:** AWS (us-east-1)
- **IaC:** AWS CDK with TypeScript
- **API Hosting:** AWS App Runner
- **Workers:** AWS ECS Fargate
- **Database:** AWS RDS (PostgreSQL)
- **Cache:** AWS ElastiCache (Redis)
- **Monitoring:** AWS CloudWatch

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- PostgreSQL (for database)
- Redis (for caching and task queue)
- Node.js 18+ (for frontend)
- npm or yarn (for frontend dependencies)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies with Poetry
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Set up database
./setup_database.sh

# Run database migrations
poetry run alembic upgrade head

# Start the FastAPI server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start Celery worker (in another terminal)
poetry run celery -A app.tasks.crawler_tasks.celery_app worker --loglevel=info
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev

# Run tests
npm run test

# Run tests with coverage
npm run test:coverage

# Build for production
npm run build

# Start Storybook (for component development)
npm run storybook
```

### Using Docker (Recommended for Development)

```bash
# Start all services (API, Worker, Database, Redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Full-Stack Development

```bash
# Terminal 1: Start backend services
docker-compose up -d

# Terminal 2: Start frontend development server
cd frontend && npm run dev

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Storybook: http://localhost:6006
```

### API Documentation

Once running, access interactive documentation:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Site Audits
- `POST /api/v1/audits/start` - Start comprehensive site audit
- `GET /api/v1/audits/status/{task_id}` - Check audit progress
- `GET /api/v1/audits/history` - Get audit history

### AI Services
- `POST /api/v1/ai/keyword-clusters` - Generate keyword clusters
- `POST /api/v1/ai/schema-markup` - Generate JSON-LD schema
- `POST /api/v1/ai/content-brief` - Generate content briefs
- `GET /api/v1/ai/service-status` - Check AI service availability

### Sites Management
- `GET /api/v1/sites/` - List managed sites
- `POST /api/v1/sites/` - Add new site
- `GET /api/v1/sites/{site_id}` - Get site details

## Project Structure

```
projectaether/
├── backend/                          # ✅ COMPLETE - Backend API & Services
│   ├── app/
│   │   ├── api/v1/endpoints/        # API route handlers
│   │   │   ├── audits.py           # Site audit endpoints
│   │   │   ├── ai.py               # AI-powered features
│   │   │   ├── auth.py             # Authentication endpoints
│   │   │   └── sites.py            # Site management
│   │   ├── auth/                   # Authentication system
│   │   │   ├── dependencies.py     # Auth dependencies
│   │   │   ├── router.py           # Auth routes
│   │   │   ├── schemas.py          # Auth data models
│   │   │   └── service.py          # Auth business logic
│   │   ├── models/                 # Database models
│   │   │   └── user.py            # User model
│   │   ├── services/               # Business logic services
│   │   │   ├── ai_service.py       # AWS Bedrock integration
│   │   │   └── external_api_service.py  # Third-party APIs
│   │   ├── tasks/                  # Celery background tasks
│   │   │   └── crawler_tasks.py    # Site crawling tasks
│   │   ├── config.py               # Application configuration
│   │   └── main.py                 # FastAPI application
│   ├── tests/                      # ✅ COMPLETE - Test suite (80%+ coverage)
│   │   ├── unit/                   # Unit tests
│   │   └── integration/            # Integration tests
│   ├── alembic/                    # Database migrations
│   ├── pyproject.toml              # Python dependencies
│   └── docker-compose.yml          # Local development environment
├── frontend/                       # ✅ COMPLETE - React SPA
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── ui/                 # Shadcn/UI component library
│   │   │   ├── layout/             # Layout components
│   │   │   ├── auth/               # Authentication components
│   │   │   └── charts/             # Data visualization components
│   │   ├── pages/                  # Page components
│   │   ├── hooks/                  # Custom hooks for API integration
│   │   ├── stores/                 # Zustand state management
│   │   ├── lib/                    # Utilities and API client
│   │   └── test/                   # Test utilities
│   ├── .storybook/                 # Storybook configuration
│   ├── package.json                # Frontend dependencies
│   └── vite.config.ts              # Vite configuration
├── docs/                           # ✅ COMPLETE - Comprehensive documentation
│   ├── Phase1_QA_Readiness_Report.md      # Phase 1 QA certification
│   ├── Phase2_QA_Audit_Report.md          # Phase 2 QA certification
│   ├── Phase1_Step*_Completion.md         # Phase 1 progress reports
│   ├── Phase2_Step*_Completion.md         # Phase 2 progress reports
│   ├── architecture.md                    # System architecture
│   ├── api_contract.md                    # API standards
│   └── authentication_security.md        # Security guidelines
├── iac/                            # 🚧 PLANNED - Infrastructure as Code (Phase 3)
│   └── lib/iac-stack.ts           # AWS CDK definitions
├── prompts/                        # ✅ COMPLETE - AI prompt library
│   └── prompts.json               # Structured prompts for AI
├── Project Aether _ SRS.md         # Software Requirements Specification
├── Project Aether _ Dev Roadmap.md # Complete development plan
└── docker-compose.yml             # Full-stack development environment
```

## Development Status

### ✅ Phase 0: Foundation & Architecture (COMPLETE)
- [x] SRS requirements analysis and clarification
- [x] Technology stack finalization
- [x] System architecture design
- [x] Database schema design
- [x] Infrastructure and DevOps strategy

### ✅ Phase 1: Backend Development & API (COMPLETE)
- [x] **Step 1:** Core scaffolding with FastAPI, logging, and configuration
- [x] **Step 2:** JWT authentication with AWS Secrets Manager integration
- [x] **Step 3:** Business logic services (AI, external APIs, crawler tasks)
- [x] **Step 4:** Complete API endpoint development with validation
- [x] **Step 5:** Comprehensive testing suite (80%+ coverage)

**🎉 Backend is production-ready and QA-certified!**

### ✅ Phase 2: Frontend Development (COMPLETE)
- [x] **Step 1:** UI/UX scaffolding with React + TypeScript + Vite
- [x] **Step 2:** Client-side architecture (routing, state, API integration)
- [x] **Step 3:** Component and view development with Shadcn/UI
- [x] **Step 4:** API integration with TanStack Query
- [x] **Step 5:** Frontend testing suite with Vitest

**🎉 Frontend is production-ready and QA-certified!**

### 🚧 Phase 3: Full-Stack Integration & Deployment (NEXT)
- [ ] **Step 1:** End-to-end testing with Playwright
- [ ] **Step 2:** User Acceptance Testing (UAT)
- [ ] **Step 3:** Performance optimization and security hardening
- [ ] **Step 4:** Production deployment to AWS

### 🚧 Phase 4: Post-Launch & Iteration (PLANNED)
- [ ] **Step 1:** Monitoring and maintenance setup
- [ ] **Step 2:** User feedback system implementation
- [ ] **Step 3:** Version 2.0 roadmap planning

## Testing

### Backend Testing (✅ COMPLETE)

```bash
# Run all tests with coverage
poetry run pytest --cov=app --cov-report=term-missing

# Run only unit tests
poetry run pytest tests/unit/

# Run only integration tests
poetry run pytest tests/integration/

# Generate HTML coverage report
poetry run pytest --cov=app --cov-report=html
```

**Current Coverage:** 80%+ (exceeds SRS requirements)

### Frontend Testing (✅ COMPLETE)

```bash
# Navigate to frontend directory
cd frontend

# Run all tests
npm run test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test -- --watch

# Run specific test file
npm run test Button.test.tsx

# Type checking
npm run type-check

# Lint frontend code
npm run lint
```

**Test Coverage:** Comprehensive unit and integration tests with Vitest

### Code Quality

```bash
# Format code
poetry run black app/

# Lint code
poetry run ruff app/

# Type checking
poetry run mypy app/

# Run all quality checks
poetry run pre-commit run --all-files
```

## Security

### Authentication & Authorization
- **JWT Tokens:** Secure token-based authentication
- **AWS Secrets Manager:** Secure storage of sensitive credentials
- **Protected Endpoints:** All business endpoints require authentication
- **CORS:** Properly configured for frontend integration

### Data Security
- **No Hardcoded Secrets:** All sensitive data stored in AWS Secrets Manager
- **Input Validation:** Comprehensive request validation with Pydantic
- **SQL Injection Protection:** SQLAlchemy ORM with parameterized queries
- **OWASP Compliance:** Following security best practices

## Environment Configuration

### Required Environment Variables

```bash
# Application
APP_NAME="Project Aether"
APP_VERSION="0.1.0"
LOG_LEVEL="INFO"

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/projectaether"

# Cache & Queue
REDIS_URL="redis://localhost:6379/0"

# CORS
FRONTEND_ORIGIN="http://localhost:3000"

# AWS (for production)
AWS_ACCESS_KEY_ID="your-access-key"
AWS_SECRET_ACCESS_KEY="your-secret-key"
AWS_DEFAULT_REGION="us-east-1"
```

## Contributing

### Development Workflow
1. Create feature branch from `develop`
2. Implement changes with tests
3. Run quality checks: `pre-commit run --all-files`
4. Submit PR to `develop` branch
5. After review, merge to `develop`
6. Deploy to staging for testing
7. Merge to `main` for production

### Code Standards
- **Python:** Black formatting, Ruff linting, MyPy type checking
- **Testing:** Minimum 80% coverage required
- **Documentation:** All public functions documented
- **Security:** No secrets in code, input validation required

## Documentation

### Key Documents
- 📋 **[SRS](./Project%20Aether%20_%20SRS.md)** - Complete requirements specification
- 🗺️ **[Dev Roadmap](./Project%20Aether%20_%20Dev%20Roadmap.md)** - Full development plan
- ✅ **[Phase 1 QA Report](./docs/Phase1_QA_Readiness_Report.md)** - Backend quality certification
- ✅ **[Phase 2 QA Report](./docs/Phase2_QA_Audit_Report.md)** - Frontend quality certification
- 🏗️ **[Architecture](./docs/architecture.md)** - System design and patterns
- 🔐 **[Security](./docs/authentication_security.md)** - Security implementation details

### API Documentation
- **Interactive Docs:** Available at `/docs` endpoint when running
- **API Contract:** Standardized in [api_contract.md](./docs/api_contract.md)
- **Integration Guide:** Frontend integration instructions

## Monitoring & Observability

### Logging
- **Structured Logging:** JSON format with structured data
- **Log Levels:** Configurable via `LOG_LEVEL` environment variable
- **Request Tracking:** Unique request IDs for tracing

### Health Checks
- **API Health:** `GET /health` endpoint
- **Service Status:** `GET /api/v1/ai/service-status` for AI services
- **Database:** Connection health monitoring

## Performance

### Current Benchmarks
- **API Response Time:** < 250ms for synchronous endpoints
- **AI Processing:** < 15 seconds for AI-powered endpoints
- **Database Queries:** Optimized with proper indexing
- **Caching:** Redis caching for external API responses

### Scalability
- **Async Processing:** Celery for background tasks
- **Database:** PostgreSQL with connection pooling
- **Horizontal Scaling:** Stateless API design for multi-instance deployment

## License

**Internal Proprietary Software** - Not for public distribution.

---

## Quick Commands Reference

```bash
# Start development environment
docker-compose up -d

# Start frontend development server
cd frontend && npm run dev

# Run backend tests
cd backend && poetry run pytest

# Run frontend tests
cd frontend && npm run test

# Format and lint code
cd backend && poetry run black app/ && poetry run ruff app/
cd frontend && npm run lint

# View API documentation
open http://localhost:8000/docs

# View frontend application
open http://localhost:5173

# View Storybook component library
open http://localhost:6006

# Check service health
curl http://localhost:8000/health

# View application logs
docker-compose logs -f api
```

**Current Status:** Phase 1 ✅ | Phase 2 ✅ | Ready for Phase 3 Full-Stack Integration 🚀