"""Initial database schema

Revision ID: 8b1884919542
Revises: 
Create Date: 2025-07-02 22:16:40.436773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = '8b1884919542'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create custom enum types
    crawl_status_enum = sa.Enum('queued', 'in_progress', 'completed', 'failed', name='crawlstatus')
    crawl_status_enum.create(op.get_bind())
    
    link_suggestion_status_enum = sa.Enum('pending', 'completed', 'dismissed', name='linksuggestionstatus')
    link_suggestion_status_enum.create(op.get_bind())
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('root_url', sa.String(500), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('api_config', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)
    
    # Create crawls table
    op.create_table(
        'crawls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('status', crawl_status_enum, nullable=False),
        sa.Column('start_url', sa.String(500), nullable=False),
        sa.Column('max_pages', sa.Integer(), nullable=True),
        sa.Column('pages_crawled', sa.Integer(), nullable=False),
        sa.Column('pages_failed', sa.Integer(), nullable=False),
        sa.Column('celery_task_id', sa.String(255), nullable=True),
        sa.Column('crawl_config', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('error_log', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crawls_id'), 'crawls', ['id'], unique=False)
    op.create_index(op.f('ix_crawls_celery_task_id'), 'crawls', ['celery_task_id'], unique=False)
    
    # Create crawled_pages table
    op.create_table(
        'crawled_pages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crawl_id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(2000), nullable=False),
        sa.Column('http_status_code', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(500), nullable=True),
        sa.Column('title_length', sa.Integer(), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('meta_description_length', sa.Integer(), nullable=True),
        sa.Column('canonical_url', sa.String(2000), nullable=True),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('headers', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('internal_links', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('external_links', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('images', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('hreflang_attributes', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('issues', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('performance_data', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_response_data', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['crawl_id'], ['crawls.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crawled_pages_id'), 'crawled_pages', ['id'], unique=False)
    op.create_index(op.f('ix_crawled_pages_url'), 'crawled_pages', ['url'], unique=False)
    
    # Create content_briefs table
    op.create_table(
        'content_briefs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('target_keyword', sa.String(255), nullable=False),
        sa.Column('target_audience', sa.String(255), nullable=True),
        sa.Column('serp_data', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('competitor_analysis', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('brief_content', sa.Text(), nullable=True),
        sa.Column('title_suggestions', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_description_suggestion', sa.Text(), nullable=True),
        sa.Column('heading_structure', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('key_entities', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('faq_section', JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('model_used', sa.String(100), nullable=True),
        sa.Column('generation_cost', sa.Float(), nullable=True),
        sa.Column('celery_task_id', sa.String(255), nullable=True),
        sa.Column('generation_status', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_briefs_id'), 'content_briefs', ['id'], unique=False)
    op.create_index(op.f('ix_content_briefs_celery_task_id'), 'content_briefs', ['celery_task_id'], unique=False)
    
    # Create internal_link_suggestions table
    op.create_table(
        'internal_link_suggestions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crawl_id', sa.Integer(), nullable=False),
        sa.Column('source_page_id', sa.Integer(), nullable=False),
        sa.Column('target_page_id', sa.Integer(), nullable=False),
        sa.Column('suggested_anchor_text', sa.String(255), nullable=False),
        sa.Column('context_snippet', sa.Text(), nullable=False),
        sa.Column('relevance_score', sa.Float(), nullable=True),
        sa.Column('status', link_suggestion_status_enum, nullable=False),
        sa.Column('user_notes', sa.Text(), nullable=True),
        sa.Column('model_used', sa.String(100), nullable=True),
        sa.Column('generation_cost', sa.Float(), nullable=True),
        sa.Column('status_changed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['crawl_id'], ['crawls.id'], ),
        sa.ForeignKeyConstraint(['source_page_id'], ['crawled_pages.id'], ),
        sa.ForeignKeyConstraint(['target_page_id'], ['crawled_pages.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_internal_link_suggestions_id'), 'internal_link_suggestions', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order (respecting foreign key constraints)
    op.drop_table('internal_link_suggestions')
    op.drop_table('content_briefs')
    op.drop_table('crawled_pages')
    op.drop_table('crawls')
    op.drop_table('projects')
    op.drop_table('users')
    
    # Drop custom enum types
    sa.Enum(name='linksuggestionstatus').drop(op.get_bind())
    sa.Enum(name='crawlstatus').drop(op.get_bind())
