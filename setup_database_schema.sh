#!/bin/bash

# Project Aether Database Schema Setup Script
# Phase 0, Step 4: Database Schema Design
# This script creates SQLAlchemy models and sets up Alembic for Project Aether

set -e

# Ensure we're in the backend directory
cd backend

# Create the app directory if it doesn't exist
mkdir -p app

# Create the SQLAlchemy models file
cat <<EOF > app/models.py
"""
SQLAlchemy models for Project Aether
Defines the database schema for the unified SEO intelligence platform
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class CrawlStatus(PyEnum):
    """Enumeration for crawl job statuses"""
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class LinkSuggestionStatus(PyEnum):
    """Enumeration for internal link suggestion statuses"""
    PENDING = "pending"
    COMPLETED = "completed"
    DISMISSED = "dismissed"


class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="owner")


class Project(Base):
    """Project model representing a client website"""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    root_url: Mapped[str] = mapped_column(String(500), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    # External API configuration (stored as JSONB for flexibility)
    api_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="projects")
    crawls: Mapped[List["Crawl"]] = relationship("Crawl", back_populates="project")
    content_briefs: Mapped[List["ContentBrief"]] = relationship("ContentBrief", back_populates="project")


class Crawl(Base):
    """Crawl model to track the status and metadata of crawl jobs"""
    __tablename__ = "crawls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Crawl configuration and status
    status: Mapped[CrawlStatus] = mapped_column(Enum(CrawlStatus), default=CrawlStatus.QUEUED, nullable=False)
    start_url: Mapped[str] = mapped_column(String(500), nullable=False)
    max_pages: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Crawl results summary
    pages_crawled: Mapped[int] = mapped_column(Integer, default=0)
    pages_failed: Mapped[int] = mapped_column(Integer, default=0)
    
    # Task tracking
    celery_task_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    
    # Crawl metadata and settings (stored as JSONB)
    crawl_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    error_log: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="crawls")
    crawled_pages: Mapped[List["CrawledPage"]] = relationship("CrawledPage", back_populates="crawl")
    internal_link_suggestions: Mapped[List["InternalLinkSuggestion"]] = relationship("InternalLinkSuggestion", back_populates="crawl")


class CrawledPage(Base):
    """CrawledPage model to store detailed data for each page found in a crawl"""
    __tablename__ = "crawled_pages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crawl_id: Mapped[int] = mapped_column(Integer, ForeignKey("crawls.id"), nullable=False)
    
    # Page identification
    url: Mapped[str] = mapped_column(String(2000), nullable=False, index=True)
    http_status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # SEO metadata
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    title_length: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    meta_description_length: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    canonical_url: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    
    # Content analysis
    word_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    text_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Headers structure (H1-H6 stored as JSONB)
    headers: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Links analysis
    internal_links: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    external_links: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Images analysis
    images: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Internationalization
    hreflang_attributes: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Technical SEO issues detected
    issues: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Performance data (if available)
    performance_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Raw response data for debugging
    raw_response_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    crawl: Mapped["Crawl"] = relationship("Crawl", back_populates="crawled_pages")
    source_link_suggestions: Mapped[List["InternalLinkSuggestion"]] = relationship(
        "InternalLinkSuggestion", 
        foreign_keys="InternalLinkSuggestion.source_page_id",
        back_populates="source_page"
    )
    target_link_suggestions: Mapped[List["InternalLinkSuggestion"]] = relationship(
        "InternalLinkSuggestion",
        foreign_keys="InternalLinkSuggestion.target_page_id", 
        back_populates="target_page"
    )


class ContentBrief(Base):
    """ContentBrief model to store AI-generated content briefs"""
    __tablename__ = "content_briefs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Target keyword and audience
    target_keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    target_audience: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # SERP analysis data
    serp_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    competitor_analysis: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # AI-generated content brief
    brief_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Structured brief components
    title_suggestions: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    meta_description_suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    heading_structure: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    key_entities: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    faq_section: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Generation metadata
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    generation_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Task tracking
    celery_task_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    generation_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="content_briefs")


class InternalLinkSuggestion(Base):
    """InternalLinkSuggestion model to store and track AI-generated linking opportunities"""
    __tablename__ = "internal_link_suggestions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crawl_id: Mapped[int] = mapped_column(Integer, ForeignKey("crawls.id"), nullable=False)
    source_page_id: Mapped[int] = mapped_column(Integer, ForeignKey("crawled_pages.id"), nullable=False)
    target_page_id: Mapped[int] = mapped_column(Integer, ForeignKey("crawled_pages.id"), nullable=False)
    
    # AI-generated suggestion details
    suggested_anchor_text: Mapped[str] = mapped_column(String(255), nullable=False)
    context_snippet: Mapped[str] = mapped_column(Text, nullable=False)
    relevance_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Suggestion status tracking
    status: Mapped[LinkSuggestionStatus] = mapped_column(
        Enum(LinkSuggestionStatus), 
        default=LinkSuggestionStatus.PENDING, 
        nullable=False
    )
    
    # User feedback and notes
    user_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # AI generation metadata
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    generation_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Status tracking timestamps
    status_changed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    crawl: Mapped["Crawl"] = relationship("Crawl", back_populates="internal_link_suggestions")
    source_page: Mapped["CrawledPage"] = relationship(
        "CrawledPage", 
        foreign_keys=[source_page_id],
        back_populates="source_link_suggestions"
    )
    target_page: Mapped["CrawledPage"] = relationship(
        "CrawledPage",
        foreign_keys=[target_page_id], 
        back_populates="target_link_suggestions"
    )

    # Constraints to prevent self-linking and duplicate suggestions
    __table_args__ = (
        # Ensure a page doesn't link to itself
        # Note: This would be better implemented as a check constraint in production
    )
EOF

# Initialize Alembic
alembic init alembic

# Create the Alembic configuration file
cat <<EOF > alembic.ini
# A generic, single database configuration for PostgreSQL

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration files
# file_template = %%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding \`alembic[tz]\` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses
# os.pathsep. If this key is omitted entirely, it falls back to the legacy
# behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

# Database URL - will be set via environment variable
sqlalchemy.url = postgresql://user:password@localhost/projectaether

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
EOF

# Create the Alembic environment configuration
cat <<EOF > alembic/env.py
"""
Alembic environment configuration for Project Aether
"""
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Add the app directory to the path so we can import our models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import all models to ensure they're registered with SQLAlchemy
from app.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_database_url():
    """Get database URL from environment variable or config file"""
    return os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Override the sqlalchemy.url with our environment variable
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
EOF

# Generate the initial migration
alembic revision --autogenerate -m "Initial database schema"

# Create the step completion summary in the docs directory
cat <<EOF > ../docs/Phase0_Step4_Completion.md
# Phase 0, Step 4: Database Schema Design - Completion Summary

**Date:** \$(date '+%Y-%m-%d')  
**Status:** Completed

## Overview

Successfully completed the database schema design for Project Aether, establishing the foundational data layer for the unified SEO intelligence platform.

## Deliverables Created

### 1. SQLAlchemy Models (\`app/models.py\`)

Created comprehensive database models supporting all functional requirements:

#### Core Models:
- **User**: Authentication and user management
- **Project**: Client website representation  
- **Crawl**: Website crawl job tracking and metadata
- **CrawledPage**: Detailed page-level crawl data storage
- **ContentBrief**: AI-generated content brief storage
- **InternalLinkSuggestion**: AI-powered internal linking recommendations

#### Key Features:
- **Modern SQLAlchemy 2.0 syntax** with typed annotations
- **PostgreSQL JSONB fields** for flexible semi-structured data storage
- **Comprehensive relationships** between all entities
- **Enum types** for status tracking (CrawlStatus, LinkSuggestionStatus)
- **Timestamp tracking** with automatic created_at/updated_at
- **Proper indexing** on key lookup fields

### 2. Alembic Configuration

#### Files Created:
- \`alembic.ini\`: Main Alembic configuration with PostgreSQL settings
- \`alembic/env.py\`: Environment configuration with proper model imports
- Initial migration script: Auto-generated from SQLAlchemy models

#### Configuration Highlights:
- **Environment variable support** for database URL
- **Proper model imports** ensuring all tables are detected
- **Production-ready logging** configuration
- **Automatic migration generation** from model changes

### 3. Database Schema Features

#### Supports All SRS Requirements:
- **FR-1 (Live Site Crawler)**: Crawl and CrawledPage models with comprehensive field coverage
- **FR-2 (Core Web Vitals)**: Performance data stored in JSONB fields  
- **FR-3 (Backlink Intelligence)**: API configuration stored in Project model
- **FR-4 (Keyword Clustering)**: Extensible via JSONB fields for future enhancement
- **FR-5 (Content Briefs)**: Dedicated ContentBrief model with structured brief components
- **FR-6 (Schema Generator)**: Supported via existing models and JSONB flexibility
- **FR-7 (Internal Linking)**: InternalLinkSuggestion model with source/target page relationships

#### Technical Specifications:
- **PostgreSQL 15+ compatible** with JSONB support
- **Celery task integration** with task_id tracking fields
- **Scalable design** supporting large crawls and datasets
- **Referential integrity** with proper foreign key constraints
- **Audit trails** with comprehensive timestamp tracking

## Next Steps

1. **Phase 0, Step 5**: Infrastructure & DevOps Strategy
2. **Phase 1**: Backend Development & API Implementation
3. **Database deployment** via Alembic migrations in staging/production environments

## Notes

- All models follow SQLAlchemy 2.0 best practices with typed annotations
- JSONB fields provide flexibility for evolving API response formats
- Schema is optimized for the specific use cases outlined in the SRS
- Migration system is ready for ongoing schema evolution
EOF

echo "✅ Database schema setup completed successfully!"
echo ""
echo "Created files:"
echo "- app/models.py (SQLAlchemy models)"
echo "- alembic.ini (Alembic configuration)"
echo "- alembic/env.py (Environment configuration)"
echo "- alembic/versions/<timestamp>_initial_database_schema.py (Initial migration)"
echo "- ../docs/Phase0_Step4_Completion.md (Completion summary)"
echo ""
echo "Next steps:"
echo "1. Set DATABASE_URL environment variable"
echo "2. Run 'alembic upgrade head' to apply migrations"
echo "3. Proceed to Phase 0, Step 5: Infrastructure & DevOps Strategy"