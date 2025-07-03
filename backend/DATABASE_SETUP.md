# Project Aether Database Setup Guide

This guide covers the complete setup of the Project Aether database system, including SQLAlchemy models, Alembic migrations, and PostgreSQL configuration.

## 📋 Overview

The Project Aether database system includes:
- **SQLAlchemy 2.0 Models**: Modern typed ORM models for all entities
- **Alembic Migrations**: Version-controlled database schema management
- **PostgreSQL Support**: JSONB fields for flexible data storage
- **Automated Testing**: Scripts to validate and test the migration system

## 🗄️ Database Schema

### Core Tables

1. **users** - User authentication and management
2. **projects** - Client website projects
3. **crawls** - Website crawl job tracking
4. **crawled_pages** - Individual page data from crawls
5. **content_briefs** - AI-generated content recommendations
6. **internal_link_suggestions** - AI-powered linking opportunities

### Key Features

- **JSONB Fields**: Flexible storage for API responses and structured data
- **Enum Types**: Status tracking with PostgreSQL native enums
- **Foreign Key Relationships**: Proper referential integrity
- **Automatic Timestamps**: Created/updated tracking on all tables
- **Indexes**: Optimized for common query patterns

## 🚀 Quick Start

### 1. Validate Setup
```bash
# Check that everything is configured correctly
python3 validate_migrations.py
```

### 2. Setup Database
```bash
# Automated setup with PostgreSQL detection
./setup_database.sh
```

### 3. Test Migrations
```bash
# Comprehensive migration testing
python3 test_migrations.py
```

## 🐘 PostgreSQL Setup Options

### Option 1: Docker (Recommended for Development)
```bash
docker run -d --name postgres-aether \
  -e POSTGRES_DB=projectaether \
  -e POSTGRES_USER=aether \
  -e POSTGRES_PASSWORD=aether123 \
  -p 5432:5432 \
  postgres:15
```

### Option 2: Homebrew (macOS)
```bash
brew install postgresql
brew services start postgresql
createdb projectaether
```

### Option 3: System Package (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb projectaether
```

## 🔧 Manual Migration Commands

### Initialize Alembic (Already Done)
```bash
alembic init alembic
```

### Generate New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade revision_id

# Downgrade to previous
alembic downgrade -1
```

### Check Status
```bash
# Current migration status
alembic current

# Migration history
alembic history

# Show pending migrations
alembic show head
```

## 🌍 Environment Configuration

### Database URL Format
```bash
# Development
export DATABASE_URL="postgresql://user:password@localhost/projectaether"

# Production (example)
export DATABASE_URL="postgresql://user:password@prod-host:5432/projectaether"
```

### Required Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- Optional: Individual components (parsed from DATABASE_URL)

## 📁 File Structure

```
backend/
├── alembic/
│   ├── versions/
│   │   └── 8b1884919542_initial_database_schema.py
│   ├── env.py              # Alembic environment config
│   └── script.py.mako      # Migration template
├── app/
│   └── models.py           # SQLAlchemy models
├── alembic.ini             # Alembic configuration
├── setup_database.sh       # Automated setup script
├── test_migrations.py      # Migration testing
├── validate_migrations.py  # Validation without DB
└── DATABASE_SETUP.md       # This file
```

## 🧪 Testing

### Validation (No Database Required)
```bash
# Validates configuration and syntax
python3 validate_migrations.py
```

### Full Migration Test (Requires PostgreSQL)
```bash
# Tests complete migration workflow
python3 test_migrations.py
```

### Manual Testing
```bash
# Connect to database
psql $DATABASE_URL

# List tables
\dt

# Describe a table
\d users

# Check data
SELECT * FROM alembic_version;
```

## 🔄 Migration Workflow

1. **Modify Models**: Update `app/models.py`
2. **Generate Migration**: `alembic revision --autogenerate -m "Description"`
3. **Review Migration**: Check generated file in `alembic/versions/`
4. **Test Migration**: Run on development database
5. **Apply to Production**: `alembic upgrade head`

## 📝 Model Definitions

### User Model
```python
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    # ... other fields
```

### Project Model
```python
class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    api_config: Mapped[Optional[dict]] = mapped_column(JSONB)
    # ... relationships and other fields
```

## 🚨 Common Issues

### Connection Refused
- **Problem**: `connection to server at "localhost" failed`
- **Solution**: Start PostgreSQL service or check connection string

### Permission Denied
- **Problem**: Cannot create database
- **Solution**: Check user permissions or use postgres superuser

### Migration Conflicts
- **Problem**: Alembic can't determine changes
- **Solution**: Review model changes and create manual migration

### Import Errors
- **Problem**: Cannot import models in migration
- **Solution**: Check PYTHONPATH and model imports in `alembic/env.py`

## 🔗 Next Steps

After successful database setup:

1. **Proceed to Phase 1**: Backend API development
2. **Configure Development Environment**: Set up FastAPI application
3. **Implement Business Logic**: Create service layers using these models
4. **Add Seed Data**: Create initial users and test projects

## 📞 Support

For issues with database setup:
1. Run `validate_migrations.py` to check configuration
2. Check PostgreSQL logs for connection issues
3. Verify environment variables are set correctly
4. Review Alembic documentation: https://alembic.sqlalchemy.org/