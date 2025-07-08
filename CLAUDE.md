# Project Aether - Claude Assistant Guide

This document provides Claude with essential context for helping with Project Aether development and deployment tasks.

## Project Overview

Project Aether is a sophisticated SEO intelligence platform with:
- **Backend**: FastAPI + PostgreSQL + Redis + Celery (Python 3.11+)
- **Frontend**: React + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Infrastructure**: Google Cloud Platform with Terraform
- **AI**: AWS Bedrock integration for content generation
- **Status**: Production-ready with comprehensive test coverage

## Architecture Summary

### Current Deployment Infrastructure
- **Platform**: Google Cloud Platform (us-central1)
- **Frontend**: Cloud Run service with nginx
- **Backend API**: Cloud Run service with FastAPI
- **Database**: Cloud SQL PostgreSQL
- **Cache**: Memorystore Redis
- **Container Registry**: Artifact Registry
- **IaC**: Terraform with modular structure

### Technology Stack
```
Frontend: React 18 + TypeScript + Vite + Tailwind + shadcn/ui
Backend: FastAPI + SQLAlchemy + Alembic + Celery + Scrapy
Database: PostgreSQL 15+ with Redis cache
AI: AWS Bedrock (Claude models)
Infrastructure: Google Cloud Run + Terraform
```

## Directory Structure
```
projectaether/
├── frontend/                 # React SPA with sophisticated UI
│   ├── src/components/      # shadcn/ui + custom components
│   ├── src/pages/          # App pages (Dashboard, SiteAudit, etc.)
│   ├── src/stores/         # Zustand state management
│   ├── Dockerfile          # Multi-stage build for Cloud Run
│   └── package.json        # Dependencies and scripts
├── backend/                 # FastAPI application
│   ├── app/               # Application code
│   ├── tests/             # Test suite (80%+ coverage)
│   └── pyproject.toml     # Poetry dependencies
├── iac/                   # Infrastructure as Code
│   └── terraform/         # Terraform modules
├── .github/workflows/     # GitHub Actions CI/CD
└── docs/                  # Project documentation
```

## Key Development Commands

### Frontend Development
```bash
cd frontend
npm install              # Install dependencies
npm run dev             # Start dev server (localhost:5173)
npm run build           # Production build
npm run test            # Run tests
npm run lint            # Lint code
npm run type-check      # TypeScript checking
```

### Backend Development
```bash
cd backend
poetry install          # Install dependencies
poetry run uvicorn app.main:app --reload  # Start API server
poetry run pytest      # Run tests with coverage
poetry run celery -A app.tasks.crawler_tasks.celery_app worker  # Start worker
poetry run alembic upgrade head  # Run migrations
```

### Docker Development
```bash
docker-compose up -d    # Start all services
docker-compose logs -f  # View logs
docker-compose down     # Stop services
```

## Deployment Workflow

### Google Cloud Platform Deployment
```bash
# Build and deploy frontend
cd frontend
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/project-aether-465213/project-aether-prod-docker-repo/project-aether-frontend:latest .
docker push us-central1-docker.pkg.dev/project-aether-465213/project-aether-prod-docker-repo/project-aether-frontend:latest
gcloud run deploy project-aether-prod-frontend --image us-central1-docker.pkg.dev/project-aether-465213/project-aether-prod-docker-repo/project-aether-frontend:latest --region us-central1

# Infrastructure with Terraform
cd iac/terraform
terraform init
terraform plan -var="project_id=project-aether-465213" -var="environment=prod"
terraform apply -var="project_id=project-aether-465213" -var="environment=prod"
```

### GitHub Actions CI/CD
The project uses automated deployment via GitHub Actions:
- **Staging**: Deploys on push to `develop` branch
- **Production**: Deploys on push to `main` branch
- **Manual**: Workflow dispatch with environment selection

## Design System

### UI/UX Specifications
- **Design Language**: Modern glassmorphism with sophisticated gradients
- **Primary Gradient**: `linear-gradient(135deg, #6D28D9 0%, #BE185D 100%)`
- **Typography**: Inter font family from Google Fonts
- **Components**: shadcn/ui with custom styling
- **Effects**: Backdrop blur, soft shadows, hover animations
- **Layout**: Bento grid patterns for dashboard cards

### CSS Classes
```css
.glassmorphism {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
}
```

## Common Tasks

### Adding New Features
1. **Backend**: Add endpoints in `backend/app/api/v1/endpoints/`
2. **Frontend**: Create components in `frontend/src/components/`
3. **State**: Use Zustand stores in `frontend/src/stores/`
4. **API**: Integrate with TanStack Query hooks
5. **Tests**: Add tests for both frontend and backend

### Database Changes
```bash
cd backend
poetry run alembic revision --autogenerate -m "Description"
poetry run alembic upgrade head
```

### Environment Configuration
- **Development**: Use `.env` files and `docker-compose.yml`
- **Production**: Use Google Secret Manager via Terraform
- **Frontend**: Environment variables prefixed with `VITE_`

## Testing Strategy

### Backend Testing
```bash
poetry run pytest --cov=app --cov-report=term-missing  # Coverage report
poetry run pytest tests/unit/                          # Unit tests
poetry run pytest tests/integration/                   # Integration tests
```

### Frontend Testing
```bash
npm run test           # Vitest unit tests
npm run test:coverage  # Coverage report
npm run test -- --ui   # Interactive test UI
```

### E2E Testing
```bash
cd e2e-tests
npx playwright test           # Run all E2E tests
npx playwright test --ui      # Interactive mode
```

## Security & Quality

### Code Quality Checks
```bash
# Backend
poetry run black app/        # Code formatting
poetry run ruff app/         # Linting
poetry run mypy app/         # Type checking

# Frontend
npm run lint                 # ESLint
npm run type-check          # TypeScript
```

### Security Scanning
```bash
./run-security-scan.sh https://staging.project-aether.io
```

## API Reference

### Health & Status
- `GET /health` - API health check
- `GET /api/v1/ai/service-status` - AI services status

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Current user info

### Core Features
- `POST /api/v1/audits/start` - Start site audit
- `GET /api/v1/audits/status/{task_id}` - Check audit progress
- `POST /api/v1/ai/keyword-clusters` - Generate keyword clusters
- `POST /api/v1/ai/content-brief` - Generate content briefs

## Important Notes

### Development Environment
- Frontend runs on `http://localhost:5173`
- Backend API runs on `http://localhost:8000`
- API docs available at `http://localhost:8000/docs`
- Database: PostgreSQL on port 5432
- Redis: Cache/queue on port 6379

### Production Environment
- Frontend: Cloud Run service with custom domain
- Backend: Cloud Run service with VPC connector
- Database: Cloud SQL with private IP
- Cache: Memorystore Redis in VPC

### Recent UI Overhaul
The application recently underwent a comprehensive UI/UX transformation:
- Implemented sophisticated design system with glassmorphism effects
- Added Inter font family and custom Tailwind configuration
- Created comprehensive Site Audit page as flagship feature
- Applied Bento grid layouts and advanced micro-interactions
- All changes documented in `STYLE_GUIDE.md`

This guide provides Claude with the essential context needed to assist with Project Aether development, deployment, and maintenance tasks efficiently.