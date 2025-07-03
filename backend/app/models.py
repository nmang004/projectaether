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
