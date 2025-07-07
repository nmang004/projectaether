#!/usr/bin/env python3
"""
Test script to verify Google Secret Manager integration.
This script tests the refactored secret fetching mechanism.

Before running this script:
1. Set the GCP_PROJECT_ID environment variable
2. Ensure Google Cloud credentials are configured (via gcloud auth or service account)
3. Create the secret in Google Secret Manager:
   - Secret name: projectaether-jwt-secret
   - Secret value: {"jwt_secret": "your-secret-key-here"}
"""

import os
import sys
import json

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set a dummy project ID for testing (replace with actual project ID)
os.environ["GCP_PROJECT_ID"] = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")

try:
    from app.auth.service import get_jwt_secret
    
    print("Testing Google Secret Manager integration...")
    print(f"GCP Project ID: {os.environ['GCP_PROJECT_ID']}")
    
    # Test fetching the secret
    secret = get_jwt_secret()
    print(f"✅ Successfully retrieved JWT secret (length: {len(secret)} characters)")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the backend directory with dependencies installed")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    print("\nTo fix this error:")
    print("1. Set GCP_PROJECT_ID environment variable")
    print("2. Configure Google Cloud credentials (gcloud auth application-default login)")
    print("3. Create the secret in Google Secret Manager:")
    print("   gcloud secrets create projectaether-jwt-secret --data-file=-")
    print("   Then paste: {\"jwt_secret\": \"your-secret-key-here\"}")