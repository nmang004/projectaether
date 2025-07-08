# Project Aether - Unified SEO Intelligence Platform

🚀 **Status**: Production-ready with sophisticated UI/UX and fully automated deployment pipeline

[![Backend Tests](https://img.shields.io/badge/backend%20tests-passing-brightgreen)](./backend/tests/)
[![Frontend Tests](https://img.shields.io/badge/frontend%20tests-passing-brightgreen)](./frontend/src/)
[![E2E Tests](https://img.shields.io/badge/e2e%20tests-configured-brightgreen)](./e2e-tests/)
[![CI/CD](https://img.shields.io/badge/ci%2Fcd-automated-brightgreen)](./.github/workflows/ci-cd.yml)
[![Security](https://img.shields.io/badge/security%20scan-automated-brightgreen)](./run-security-scan.sh)
[![Phase 1](https://img.shields.io/badge/phase%201-complete-success)](./docs/Phase1_QA_Readiness_Report.md)
[![Phase 2](https://img.shields.io/badge/phase%202-complete-success)](./docs/Phase2_QA_Audit_Report.md)
[![Phase 3](https://img.shields.io/badge/phase%203-complete-success)](./QA_Audit_Report.md)
[![Production Ready](https://img.shields.io/badge/production-ready-success)](./QA_Audit_Report.md)
[![Code Coverage](https://img.shields.io/badge/coverage-80%25%2B-brightgreen)](./docs/Phase1_Step5_Completion.md)

## Overview

**Project Aether** is a cutting-edge, internal SEO intelligence platform featuring a sophisticated glassmorphism UI that unifies three critical pillars of SEO data:

1. **Live Site Data** - Acquired via sophisticated, JavaScript-aware web crawler with comprehensive audit capabilities
2. **Real-Time Market Data** - Sourced from industry-leading external APIs with intelligent caching
3. **Generative AI Insights** - Powered by Amazon Bedrock's Foundation Models with contextual understanding

The platform combines modern design principles with robust technical architecture, delivering an exceptional user experience while standardizing best practices, automating high-effort tasks, and scaling the agency's ability to deliver consistent, data-driven SEO outcomes.

### Key Features

- 🎨 **Sophisticated Design System** - Modern glassmorphism UI with Inter typography and gradient aesthetics
- 🕷️ **Live Site Audit & Technical Crawler** - Comprehensive website analysis with detailed issue tracking
- 📊 **Performance & Core Web Vitals** - Real-time performance monitoring with visual dashboards
- 🔗 **Backlink Intelligence** - Advanced off-page SEO analysis with competitive insights
- 🤖 **AI-Powered Keyword Clustering** - Semantic keyword generation with market intelligence
- 📝 **SERP-Driven Content Briefs** - AI-powered content planning with optimization recommendations
- 🏷️ **Schema Markup Generator** - Automated JSON-LD generation with validation
- 🔗 **AI-Assisted Internal Linking** - Contextual linking opportunities with anchor text optimization
- 📈 **Interactive Data Visualization** - Advanced charts and metrics with Recharts integration
- 🎯 **Bento Grid Dashboards** - Modern card-based layouts with responsive design

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

**Frontend (✅ COMPLETE - SOPHISTICATED UI/UX)**
- **Framework:** React 18+ with TypeScript and modern hooks
- **Build Tool:** Vite with optimized bundling and hot reload
- **State Management:** Zustand + TanStack Query for server state
- **UI Components:** Shadcn/UI + Tailwind CSS with custom design system
- **Design Language:** Glassmorphism with Inter typography and gradient aesthetics
- **Styling:** Custom Tailwind configuration with design tokens and utilities
- **Charts:** Recharts for advanced data visualization and interactive dashboards
- **Animations:** Smooth micro-interactions with CSS transforms and transitions
- **Layout:** Bento Grid patterns and responsive design principles
- **Testing:** Vitest with React Testing Library and comprehensive coverage
- **E2E Testing:** Playwright with data-testid instrumentation across browsers

**DevOps & Infrastructure (✅ COMPLETE - GOOGLE CLOUD PLATFORM)**
- **CI/CD:** GitHub Actions with automated testing, security, and deployment
- **E2E Testing:** Playwright multi-browser testing with comprehensive coverage
- **Security:** OWASP ZAP automated security scanning and vulnerability assessment
- **Performance:** Bundle size monitoring, optimization, and Core Web Vitals tracking
- **Cloud Platform:** Google Cloud Platform (us-central1) - Production deployed
- **IaC:** Terraform with modular infrastructure components
- **Frontend Hosting:** Google Cloud Run with nginx and custom domains
- **API Hosting:** Google Cloud Run with auto-scaling and VPC integration
- **Workers:** Celery background tasks with Redis queue management
- **Database:** Google Cloud SQL (PostgreSQL) with automated backups
- **Cache:** Google Memorystore (Redis) with VPC connectivity
- **Container Registry:** Google Artifact Registry with multi-architecture support
- **Monitoring:** Google Cloud Monitoring with logging and alerting

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

# Rebuild services after code changes
docker-compose up -d --build

# View specific service logs
docker-compose logs -f api
docker-compose logs -f worker
```

### Full-Stack Development

```bash
# Terminal 1: Start backend services
docker-compose up -d

# Terminal 2: Start frontend development server with sophisticated UI
cd frontend && npm run dev

# Terminal 3: Start Storybook for component development (optional)
cd frontend && npm run storybook

# Access the application
# Frontend (Sophisticated UI): http://localhost:5173
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
# Storybook Component Library: http://localhost:6006
# Database Admin (if running): http://localhost:8080
```

### API Documentation

Once running, access interactive documentation:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## API Endpoints

### Health & Status
- `GET /health` - API health check with service status
- `GET /api/v1/ai/service-status` - Check AI service availability

### Authentication
- `POST /api/v1/auth/register` - User registration with validation
- `POST /api/v1/auth/login` - User login with JWT token generation
- `GET /api/v1/auth/me` - Get current user profile and permissions
- `POST /api/v1/auth/refresh` - Refresh JWT access token
- `POST /api/v1/auth/logout` - Logout and invalidate token

### Site Audits (Core Feature)
- `POST /api/v1/audits/start` - Start comprehensive site audit with crawling
- `GET /api/v1/audits/status/{task_id}` - Check audit progress and results
- `GET /api/v1/audits/history` - Get audit history with pagination
- `GET /api/v1/audits/{audit_id}` - Get detailed audit results
- `DELETE /api/v1/audits/{audit_id}` - Delete audit record
- `POST /api/v1/audits/{audit_id}/export` - Export audit results (PDF/CSV)

### AI Services (Bedrock Integration)
- `POST /api/v1/ai/keyword-clusters` - Generate semantic keyword clusters
- `POST /api/v1/ai/schema-markup` - Generate structured JSON-LD schema
- `POST /api/v1/ai/content-brief` - Generate SERP-driven content briefs
- `POST /api/v1/ai/internal-links` - AI-assisted internal linking suggestions
- `POST /api/v1/ai/optimize-content` - Content optimization recommendations

### Sites Management
- `GET /api/v1/sites/` - List managed sites with metadata
- `POST /api/v1/sites/` - Add new site for monitoring
- `GET /api/v1/sites/{site_id}` - Get site details and analytics
- `PUT /api/v1/sites/{site_id}` - Update site configuration
- `DELETE /api/v1/sites/{site_id}` - Remove site from monitoring
- `GET /api/v1/sites/{site_id}/metrics` - Get site performance metrics

### Analytics & Reporting
- `GET /api/v1/analytics/dashboard` - Dashboard metrics and KPIs
- `GET /api/v1/analytics/trends` - Historical trends and insights
- `POST /api/v1/reports/generate` - Generate custom reports
- `GET /api/v1/reports/` - List available reports

## Project Structure

```
projectaether/
├── backend/                          # ✅ COMPLETE - Backend API & Services
│   ├── app/
│   │   ├── api/v1/endpoints/        # API route handlers
│   │   │   ├── audits.py           # Site audit endpoints with progress tracking
│   │   │   ├── ai.py               # AI-powered features (Bedrock integration)
│   │   │   ├── auth.py             # JWT authentication endpoints
│   │   │   ├── sites.py            # Site management and analytics
│   │   │   └── analytics.py        # Dashboard metrics and reporting
│   │   ├── auth/                   # Authentication system
│   │   │   ├── dependencies.py     # Auth middleware and dependencies
│   │   │   ├── router.py           # Auth routes with JWT handling
│   │   │   ├── schemas.py          # Pydantic auth data models
│   │   │   └── service.py          # Auth business logic
│   │   ├── models/                 # SQLAlchemy database models
│   │   │   ├── user.py            # User model with relationships
│   │   │   ├── site.py            # Site model with audit history
│   │   │   └── audit.py           # Audit results and metadata
│   │   ├── services/               # Business logic services
│   │   │   ├── ai_service.py       # AWS Bedrock integration
│   │   │   ├── external_api_service.py  # Third-party API integrations
│   │   │   └── crawler_service.py  # Web crawling and analysis
│   │   ├── tasks/                  # Celery background tasks
│   │   │   ├── crawler_tasks.py    # Site crawling tasks
│   │   │   └── ai_tasks.py         # AI processing tasks
│   │   ├── config.py               # Application configuration
│   │   └── main.py                 # FastAPI application with middleware
│   ├── tests/                      # ✅ COMPLETE - Test suite (80%+ coverage)
│   │   ├── unit/                   # Unit tests for services and models
│   │   ├── integration/            # Integration tests for APIs
│   │   └── fixtures/               # Test data and fixtures
│   ├── alembic/                    # Database migrations with version control
│   ├── pyproject.toml              # Poetry dependencies and configuration
│   └── docker-compose.yml          # Local development environment
├── frontend/                       # ✅ COMPLETE - Sophisticated React SPA
│   ├── src/
│   │   ├── components/             # React components with design system
│   │   │   ├── ui/                 # Shadcn/UI component library (customized)
│   │   │   ├── layout/             # Layout components with glassmorphism
│   │   │   ├── auth/               # Authentication components
│   │   │   ├── charts/             # Advanced data visualization (Recharts)
│   │   │   └── dashboard/          # Dashboard widgets and Bento Grid layouts
│   │   ├── pages/                  # Page components with sophisticated design
│   │   │   ├── LoginPage.tsx       # Authentication page with gradient design
│   │   │   ├── DashboardPage.tsx   # Main dashboard with interactive widgets
│   │   │   ├── SiteAuditPage.tsx   # Flagship audit interface with filtering
│   │   │   └── AnalyticsPage.tsx   # Advanced analytics and reporting
│   │   ├── hooks/                  # Custom hooks for API integration
│   │   ├── stores/                 # Zustand state management
│   │   ├── lib/                    # Utilities, API client, and helpers
│   │   ├── styles/                 # Global styles and design tokens
│   │   └── test/                   # Test utilities and setup
│   ├── public/                     # Static assets and favicons
│   ├── .storybook/                 # Storybook configuration for components
│   ├── tailwind.config.js          # Custom Tailwind with design system
│   ├── package.json                # Dependencies including design packages
│   ├── vite.config.ts              # Vite configuration with optimizations
│   ├── Dockerfile                  # Multi-stage build for production
│   └── nginx.conf                  # Nginx configuration for Cloud Run
├── e2e-tests/                      # ✅ COMPLETE - End-to-End Testing
│   ├── playwright.config.ts        # Multi-browser configuration
│   ├── global.setup.ts             # Authentication and test setup
│   ├── tests/
│   │   ├── critical-paths.spec.ts  # Core user journey tests
│   │   ├── audit-workflow.spec.ts  # Site audit workflow testing
│   │   └── ui-interactions.spec.ts # UI component interaction tests
│   └── playwright/                 # Test artifacts and auth state
├── iac/                            # ✅ COMPLETE - Infrastructure as Code
│   └── terraform/                  # Terraform modules for GCP
│       ├── modules/               # Reusable infrastructure modules
│       │   ├── networking/        # VPC and network configuration
│       │   ├── database/          # Cloud SQL setup
│       │   ├── redis/             # Memorystore configuration
│       │   ├── cloud_run/         # Cloud Run services
│       │   └── artifact_registry/ # Container registry setup
│       ├── main.tf                # Main infrastructure definition
│       ├── variables.tf           # Terraform variables
│       └── outputs.tf             # Infrastructure outputs
├── .github/workflows/              # ✅ COMPLETE - Advanced CI/CD Pipeline
│   └── deploy.yml                 # Multi-environment deployment automation
├── docs/                           # ✅ COMPLETE - Comprehensive documentation
│   ├── Phase*_Reports/            # QA certification documents
│   ├── architecture.md            # System architecture and design
│   ├── api_contract.md            # API standards and conventions
│   └── authentication_security.md # Security implementation details
├── STYLE_GUIDE.md                  # ✅ NEW - Comprehensive design system
├── CLAUDE.md                       # ✅ NEW - Claude assistant context guide
├── QA_Audit_Report.md              # ✅ COMPLETE - Production readiness
├── UAT_Plan.md                     # ✅ COMPLETE - User acceptance testing
├── Deployment_Checklist.md        # ✅ COMPLETE - Production deployment
├── run-security-scan.sh            # ✅ COMPLETE - OWASP ZAP security
├── cloudbuild.yaml                 # ✅ COMPLETE - GCP Cloud Build config
├── Project Aether _ SRS.md         # Software Requirements Specification
├── Project Aether _ Dev Roadmap.md # Complete development roadmap
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

### ✅ Phase 3: Full-Stack Integration & Testing (COMPLETE)
- [x] **Step 1:** End-to-end testing with Playwright (multi-browser support)
- [x] **Step 2:** User Acceptance Testing (UAT) plan with Alex/Sarah personas
- [x] **Step 3:** Performance optimization and security hardening (OWASP ZAP)
- [x] **Step 4:** Production deployment automation and procedures

**🎉 All phases complete - Production deployment ready!**

### 🚧 Phase 4: Post-Launch & Iteration (NEXT)
- [ ] **Step 1:** Execute production deployment via Deployment_Checklist.md
- [ ] **Step 2:** Monitoring and maintenance setup
- [ ] **Step 3:** User feedback system implementation
- [ ] **Step 4:** Version 2.0 roadmap planning

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

### End-to-End Testing (✅ COMPLETE)

```bash
# Navigate to e2e-tests directory
cd e2e-tests

# Install dependencies (if needed)
npm install

# Install Playwright browsers
npx playwright install

# Run E2E tests
npx playwright test

# Run tests with UI mode
npx playwright test --ui

# Run specific test file
npx playwright test critical-paths.spec.ts

# Generate HTML report
npx playwright show-report
```

**Test Coverage:** Authentication flows, keyword clustering, core user journeys

### CI/CD & Automation (✅ COMPLETE)

```bash
# Run security scan
./run-security-scan.sh https://staging.project-aether.io

# Check CI/CD pipeline status
# View at: https://github.com/[username]/projectaether/actions

# Manual CI/CD pipeline trigger (if needed)
git push origin main  # Triggers automated pipeline
```

**Pipeline Includes:** Backend tests, frontend tests, E2E tests, security scan, performance checks

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
- **OWASP Compliance:** Automated security scanning with OWASP ZAP
- **Security Pipeline:** Integrated security checks in CI/CD

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
- ✅ **[Final QA Audit](./QA_Audit_Report.md)** - Production readiness certification
- 🧪 **[UAT Plan](./UAT_Plan.md)** - User acceptance testing procedures
- 🚀 **[Deployment Checklist](./Deployment_Checklist.md)** - Production deployment guide
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

## Deployment to Google Cloud Platform

### Production Deployment Commands

```bash
# Build and deploy frontend with sophisticated UI
cd frontend
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/project-aether-465213/project-aether-prod-docker-repo/project-aether-frontend:latest .
docker push us-central1-docker.pkg.dev/project-aether-465213/project-aether-prod-docker-repo/project-aether-frontend:latest

# Deploy to Cloud Run
gcloud run deploy project-aether-prod-frontend \
  --image us-central1-docker.pkg.dev/project-aether-465213/project-aether-prod-docker-repo/project-aether-frontend:latest \
  --region us-central1 \
  --allow-unauthenticated \
  --port 80

# Deploy infrastructure with Terraform
cd iac/terraform
terraform init
terraform plan -var="project_id=project-aether-465213" -var="environment=prod"
terraform apply -var="project_id=project-aether-465213" -var="environment=prod"
```

### GitHub Actions Automated Deployment

```bash
# Trigger production deployment
git push origin main  # Automatically deploys to production

# Trigger staging deployment
git push origin develop  # Automatically deploys to staging

# Manual deployment trigger
# Use GitHub Actions workflow_dispatch with environment selection
```

## Design System & UI/UX

### Sophisticated Glassmorphism Design

Project Aether features a cutting-edge design system with:

- **Glassmorphism Effects**: Backdrop blur with semi-transparent backgrounds
- **Gradient Aesthetics**: Primary gradient from #6D28D9 to #BE185D
- **Inter Typography**: Google Fonts integration with multiple weights
- **Micro-interactions**: Smooth hover effects and animations
- **Bento Grid Layouts**: Modern card-based dashboard designs
- **Responsive Design**: Mobile-first approach with fluid typography

### Key Design Components

```css
/* Glassmorphism Effect */
.glassmorphism {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
}

/* Primary Gradient */
.bg-gradient-primary {
  background: linear-gradient(135deg, #6D28D9 0%, #BE185D 100%);
}
```

See [STYLE_GUIDE.md](./STYLE_GUIDE.md) for complete design system documentation.

## Quick Commands Reference

```bash
# Development Environment
docker-compose up -d                    # Start all backend services
cd frontend && npm run dev               # Start frontend with sophisticated UI
cd frontend && npm run storybook         # Start component library

# Testing & Quality
cd backend && poetry run pytest --cov=app --cov-report=term-missing  # Backend tests with coverage
cd frontend && npm run test              # Frontend tests with Vitest
cd e2e-tests && npx playwright test      # End-to-end tests
./run-security-scan.sh                  # OWASP security scan

# Code Quality
cd backend && poetry run black app/ && poetry run ruff app/  # Format and lint Python
cd frontend && npm run lint && npm run type-check             # Lint and type-check TypeScript

# Application Access
open http://localhost:5173               # Frontend application (sophisticated UI)
open http://localhost:8000/docs          # API documentation (Swagger)
open http://localhost:6006               # Storybook component library
curl http://localhost:8000/health        # API health check

# Database Management
cd backend && poetry run alembic upgrade head  # Run database migrations
cd backend && poetry run alembic revision --autogenerate -m "Description"  # Create migration

# Production Deployment
git add . && git commit -m "Deploy to production" && git push origin main  # Trigger production deployment
docker-compose logs -f                   # View application logs

# Google Cloud Platform
gcloud run services list --region us-central1  # List deployed services
gcloud sql instances list                       # List database instances
gcloud redis instances list --region us-central1  # List Redis instances
```

## Troubleshooting & Support

### Common Development Issues

```bash
# Frontend build issues
cd frontend && rm -rf node_modules && npm install  # Clean install
cd frontend && npm run build                       # Check build errors

# Backend dependency issues
cd backend && poetry install --no-dev             # Install production dependencies
cd backend && poetry run pip check                # Check dependency conflicts

# Docker issues
docker-compose down && docker-compose up -d --build  # Rebuild containers
docker system prune -a                               # Clean up Docker resources

# Database connection issues
docker-compose logs postgres                      # Check database logs
psql $DATABASE_URL -c "SELECT 1;"                 # Test database connection

# Google Cloud deployment issues
gcloud auth list                                  # Check authentication
gcloud config get-value project                  # Verify project ID
gcloud run services list --region us-central1    # Check service status
```

### Performance Monitoring

```bash
# Frontend performance
cd frontend && npm run build && npx lighthouse http://localhost:5173  # Lighthouse audit
cd frontend && npm run analyze                                         # Bundle analysis

# Backend performance
cd backend && poetry run pytest --benchmark-only                      # Performance benchmarks
curl -w "@curl-format.txt" http://localhost:8000/health               # Response time analysis
```

### Production Health Checks

```bash
# Check all services
curl https://project-aether-prod-frontend-271865958975.us-central1.run.app/
curl https://project-aether-prod-api-271865958975.us-central1.run.app/health

# Monitor logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

---

**Current Status:** Phase 1 ✅ | Phase 2 ✅ | Phase 3 ✅ | **PRODUCTION DEPLOYED** 🚀

## 🎉 Production Achievement

Project Aether is **live in production** with all development phases complete:

- ✅ **Sophisticated UI/UX** - Modern glassmorphism design with Inter typography
- ✅ **Backend Development** - FastAPI with 80%+ test coverage and comprehensive APIs
- ✅ **Frontend Development** - React with advanced components and interactive dashboards
- ✅ **Google Cloud Deployment** - Cloud Run services with Terraform infrastructure
- ✅ **Testing Infrastructure** - Unit, integration, and E2E tests with Playwright
- ✅ **CI/CD Pipeline** - Automated GitHub Actions deployment pipeline
- ✅ **Security Validation** - OWASP ZAP integration and security scanning
- ✅ **Quality Assurance** - Comprehensive QA audit with production certification

**Live Application:** [https://project-aether-prod-frontend-271865958975.us-central1.run.app](https://project-aether-prod-frontend-271865958975.us-central1.run.app)

**API Documentation:** [https://project-aether-prod-api-271865958975.us-central1.run.app/docs](https://project-aether-prod-api-271865958975.us-central1.run.app/docs)

---

## Contributing & Development

For development contributions, see [CLAUDE.md](./CLAUDE.md) for comprehensive development context and [STYLE_GUIDE.md](./STYLE_GUIDE.md) for design system guidelines.

## License

**Internal Proprietary Software** - Not for public distribution.