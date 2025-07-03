#!/bin/bash

# Project Aether Database Setup Script
# Comprehensive setup and testing of the database migration system

set -e

echo "🚀 Project Aether Database Migration System Setup"
echo "=================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Check if PostgreSQL is running
check_postgresql() {
    print_info "Checking PostgreSQL availability..."
    
    if command -v pg_isready &> /dev/null; then
        if pg_isready -h localhost -p 5432 &> /dev/null; then
            print_status "PostgreSQL is running on localhost:5432"
            return 0
        else
            print_warning "PostgreSQL is installed but not running"
            return 1
        fi
    else
        print_warning "PostgreSQL is not installed or not in PATH"
        return 1
    fi
}

# Install PostgreSQL if needed
install_postgresql() {
    print_info "PostgreSQL setup options:"
    echo ""
    echo "1️⃣  Install with Homebrew (macOS):"
    echo "   brew install postgresql"
    echo "   brew services start postgresql"
    echo ""
    echo "2️⃣  Install with Docker:"
    echo "   docker run -d --name postgres-aether \\"
    echo "     -e POSTGRES_DB=projectaether \\"
    echo "     -e POSTGRES_USER=aether \\"
    echo "     -e POSTGRES_PASSWORD=aether123 \\"
    echo "     -p 5432:5432 postgres:15"
    echo ""
    echo "3️⃣  Install natively (Ubuntu/Debian):"
    echo "   sudo apt update && sudo apt install postgresql postgresql-contrib"
    echo "   sudo systemctl start postgresql"
    echo ""
    
    read -p "Would you like to try Docker setup now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_docker_postgres
    else
        print_info "Please install PostgreSQL manually and run this script again"
        exit 1
    fi
}

# Setup PostgreSQL with Docker
setup_docker_postgres() {
    print_info "Setting up PostgreSQL with Docker..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Stop existing container if running
    docker stop postgres-aether 2>/dev/null || true
    docker rm postgres-aether 2>/dev/null || true
    
    # Start new PostgreSQL container
    docker run -d --name postgres-aether \
        -e POSTGRES_DB=projectaether \
        -e POSTGRES_USER=aether \
        -e POSTGRES_PASSWORD=aether123 \
        -p 5432:5432 \
        postgres:15
    
    print_info "Waiting for PostgreSQL to start..."
    sleep 10
    
    # Set database URL for this session
    export DATABASE_URL="postgresql://aether:aether123@localhost/projectaether"
    print_status "PostgreSQL container started successfully"
    print_info "Database URL: $DATABASE_URL"
}

# Create database if it doesn't exist
create_database() {
    print_info "Creating database if it doesn't exist..."
    
    # Extract components from DATABASE_URL
    DB_URL=${DATABASE_URL:-"postgresql://aether:aether123@localhost/projectaether"}
    
    # Use Python to create database
    python3 -c "
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse
import sys

url = '$DB_URL'
parsed = urlparse(url)

# Connect to postgres database first
try:
    conn = psycopg2.connect(
        host=parsed.hostname or 'localhost',
        port=parsed.port or 5432,
        database='postgres',
        user=parsed.username or 'postgres',
        password=parsed.password or ''
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    db_name = parsed.path.lstrip('/') if parsed.path else 'projectaether'
    
    # Check if database exists
    cur.execute('SELECT 1 FROM pg_database WHERE datname = %s', (db_name,))
    exists = cur.fetchone()
    
    if not exists:
        cur.execute('CREATE DATABASE {}'.format(db_name))
        print(f'Database {db_name} created successfully')
    else:
        print(f'Database {db_name} already exists')
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_status "Database ready"
    else
        print_error "Failed to create database"
        exit 1
    fi
}

# Run Alembic migration
run_migration() {
    print_info "Running database migration..."
    
    # Find alembic executable
    ALEMBIC_PATH="/Users/nickmangubat/Library/Python/3.9/bin/alembic"
    if [ ! -f "$ALEMBIC_PATH" ]; then
        ALEMBIC_PATH="alembic"
    fi
    
    # Check current migration status
    print_info "Checking current migration status..."
    $ALEMBIC_PATH current || print_warning "No migration history (expected for first run)"
    
    # Run the migration
    print_info "Applying database schema..."
    if $ALEMBIC_PATH upgrade head; then
        print_status "Database migration completed successfully"
    else
        print_error "Migration failed"
        return 1
    fi
    
    # Verify migration
    print_info "Verifying migration..."
    $ALEMBIC_PATH current
    
    return 0
}

# Main execution
main() {
    echo ""
    print_info "Step 1: Checking PostgreSQL..."
    
    if ! check_postgresql; then
        print_warning "PostgreSQL is not available"
        install_postgresql
    fi
    
    echo ""
    print_info "Step 2: Setting up database..."
    
    # Set default DATABASE_URL if not set
    if [ -z "$DATABASE_URL" ]; then
        export DATABASE_URL="postgresql://aether:aether123@localhost/projectaether"
        print_info "Using default DATABASE_URL: $DATABASE_URL"
    else
        print_info "Using DATABASE_URL: $DATABASE_URL"
    fi
    
    create_database
    
    echo ""
    print_info "Step 3: Running migrations..."
    
    if run_migration; then
        echo ""
        print_status "🎉 Database setup completed successfully!"
        echo ""
        print_info "Summary:"
        echo "  ✅ PostgreSQL is running"
        echo "  ✅ Database 'projectaether' created"
        echo "  ✅ All tables created with migration"
        echo "  ✅ Ready for Phase 1 development"
        echo ""
        print_info "Environment variable for development:"
        echo "  export DATABASE_URL=\"$DATABASE_URL\""
        echo ""
        print_info "To test the setup, run:"
        echo "  python3 test_migrations.py"
    else
        print_error "Database setup failed"
        exit 1
    fi
}

# Run main function
main