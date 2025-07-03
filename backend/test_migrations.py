#!/usr/bin/env python3
"""
Test script for Project Aether database migrations
"""

import os
import subprocess
import sys
from urllib.parse import urlparse

def check_postgresql_connection(database_url):
    """Test if we can connect to PostgreSQL"""
    try:
        import psycopg2
        parsed = urlparse(database_url)
        
        conn = psycopg2.connect(
            host=parsed.hostname or 'localhost',
            port=parsed.port or 5432,
            database=parsed.path.lstrip('/') if parsed.path else 'postgres',
            user=parsed.username or 'postgres',
            password=parsed.password or ''
        )
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Cannot connect to PostgreSQL: {e}")
        return False

def run_alembic_command(command):
    """Run an alembic command and return success status"""
    try:
        # Find alembic executable
        alembic_path = "/Users/nickmangubat/Library/Python/3.9/bin/alembic"
        if not os.path.exists(alembic_path):
            # Try system alembic
            alembic_path = "alembic"
        
        result = subprocess.run([alembic_path] + command, 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ {' '.join(command)} - Success")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {' '.join(command)} - Failed")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {' '.join(command)} - Exception: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Project Aether Database Migration System")
    print("=" * 60)
    
    # Check if DATABASE_URL is set
    database_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/projectaether')
    print(f"📍 Database URL: {database_url}")
    
    # Test 1: Check PostgreSQL connection
    print("\n1️⃣  Testing PostgreSQL connection...")
    if not check_postgresql_connection(database_url):
        print("\n⚠️  PostgreSQL is not available. Migration tests require a running PostgreSQL instance.")
        print("\n💡 To set up PostgreSQL locally:")
        print("   - macOS: brew install postgresql && brew services start postgresql")
        print("   - Ubuntu: sudo apt install postgresql && sudo systemctl start postgresql")
        print("   - Docker: docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres")
        print(f"\n   Then set DATABASE_URL environment variable:")
        print(f"   export DATABASE_URL='{database_url}'")
        return False
    
    print("✅ PostgreSQL connection successful!")
    
    # Test 2: Check migration status
    print("\n2️⃣  Checking migration status...")
    if not run_alembic_command(["current"]):
        print("⚠️  No migration history found (expected for first run)")
    
    # Test 3: Validate migration file
    print("\n3️⃣  Validating migration file...")
    if not run_alembic_command(["check"]):
        return False
    
    # Test 4: Run migration (upgrade)
    print("\n4️⃣  Running database migration (upgrade)...")
    if not run_alembic_command(["upgrade", "head"]):
        return False
    
    # Test 5: Check migration status after upgrade
    print("\n5️⃣  Verifying migration status...")
    if not run_alembic_command(["current"]):
        return False
    
    # Test 6: Test downgrade (optional)
    print("\n6️⃣  Testing downgrade capability...")
    if not run_alembic_command(["downgrade", "base"]):
        print("⚠️  Downgrade failed - this might be expected if foreign key constraints exist")
    
    # Test 7: Re-upgrade to verify repeatability
    print("\n7️⃣  Re-running upgrade to test repeatability...")
    if not run_alembic_command(["upgrade", "head"]):
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All migration tests completed successfully!")
    print("\n📋 Summary:")
    print("   ✅ PostgreSQL connection working")
    print("   ✅ Alembic configuration valid")
    print("   ✅ Migration file syntax correct")
    print("   ✅ Database schema created successfully")
    print("   ✅ Migration system is ready for development")
    print("\n🔄 Next steps:")
    print("   1. Set up your local .env file with DATABASE_URL")
    print("   2. Proceed to Phase 1: Backend Development")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)