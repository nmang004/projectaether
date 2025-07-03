#!/usr/bin/env python3
"""
Validation script for Project Aether database migrations
This script validates migration files without requiring a database connection
"""

import os
import sys
import importlib.util
from pathlib import Path

def validate_migration_syntax():
    """Validate that migration files have correct syntax"""
    print("🔍 Validating migration file syntax...")
    
    versions_dir = Path("alembic/versions")
    if not versions_dir.exists():
        print("❌ Alembic versions directory not found")
        return False
    
    migration_files = list(versions_dir.glob("*.py"))
    if not migration_files:
        print("❌ No migration files found")
        return False
    
    for migration_file in migration_files:
        try:
            # Load the migration module
            spec = importlib.util.spec_from_file_location("migration", migration_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check required attributes
            required_attrs = ['revision', 'down_revision', 'upgrade', 'downgrade']
            for attr in required_attrs:
                if not hasattr(module, attr):
                    print(f"❌ Migration {migration_file.name} missing required attribute: {attr}")
                    return False
            
            print(f"✅ Migration {migration_file.name} syntax valid")
            
            # Validate revision format
            if not module.revision or len(module.revision) < 8:
                print(f"❌ Migration {migration_file.name} has invalid revision ID")
                return False
                
        except Exception as e:
            print(f"❌ Migration {migration_file.name} syntax error: {e}")
            return False
    
    return True

def validate_models():
    """Validate that SQLAlchemy models can be imported"""
    print("\n🔍 Validating SQLAlchemy models...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        from app.models import Base, User, Project, Crawl, CrawledPage, ContentBrief, InternalLinkSuggestion
        
        # Check that Base has tables
        if not Base.metadata.tables:
            print("❌ No tables found in Base.metadata")
            return False
        
        print(f"✅ Found {len(Base.metadata.tables)} tables in metadata:")
        for table_name in Base.metadata.tables.keys():
            print(f"   - {table_name}")
        
        # Validate model relationships
        models = [User, Project, Crawl, CrawledPage, ContentBrief, InternalLinkSuggestion]
        for model in models:
            if not hasattr(model, '__tablename__'):
                print(f"❌ Model {model.__name__} missing __tablename__")
                return False
            print(f"✅ Model {model.__name__} -> table '{model.__tablename__}'")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import models: {e}")
        return False
    except Exception as e:
        print(f"❌ Model validation error: {e}")
        return False

def validate_alembic_config():
    """Validate Alembic configuration"""
    print("\n🔍 Validating Alembic configuration...")
    
    # Check alembic.ini exists
    if not os.path.exists("alembic.ini"):
        print("❌ alembic.ini not found")
        return False
    print("✅ alembic.ini found")
    
    # Check env.py exists
    if not os.path.exists("alembic/env.py"):
        print("❌ alembic/env.py not found")
        return False
    print("✅ alembic/env.py found")
    
    # Validate env.py imports our models
    with open("alembic/env.py", "r") as f:
        env_content = f.read()
        if "from app.models import Base" not in env_content:
            print("❌ alembic/env.py does not import our models")
            return False
        if "target_metadata = Base.metadata" not in env_content:
            print("❌ alembic/env.py does not set target_metadata")
            return False
    
    print("✅ alembic/env.py properly configured")
    return True

def check_dependencies():
    """Check that required dependencies are available"""
    print("\n🔍 Checking required dependencies...")
    
    required_packages = [
        'sqlalchemy',
        'alembic', 
        'psycopg2'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} not available")
            return False
    
    return True

def main():
    """Main validation function"""
    print("🔧 Project Aether Migration System Validation")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Run all validation checks
    checks = [
        ("Dependencies", check_dependencies),
        ("Alembic Configuration", validate_alembic_config), 
        ("SQLAlchemy Models", validate_models),
        ("Migration Syntax", validate_migration_syntax)
    ]
    
    for check_name, check_func in checks:
        if not check_func():
            all_checks_passed = False
            print(f"\n❌ {check_name} validation failed")
        else:
            print(f"\n✅ {check_name} validation passed")
    
    print("\n" + "=" * 50)
    
    if all_checks_passed:
        print("🎉 All validations passed!")
        print("\n📋 Migration system is ready:")
        print("   ✅ Dependencies installed")
        print("   ✅ Alembic properly configured")
        print("   ✅ SQLAlchemy models valid")
        print("   ✅ Migration files syntax correct")
        print("\n🚀 Ready to run migrations with PostgreSQL!")
        print("   Run: ./setup_database.sh")
        return True
    else:
        print("❌ Some validations failed!")
        print("   Please fix the issues above before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)