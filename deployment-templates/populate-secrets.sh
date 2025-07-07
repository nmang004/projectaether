#!/bin/bash

# Project Aether - Secret Population Script
# This script populates Google Secret Manager with required application secrets
# 
# Usage: ./populate-secrets.sh [staging|production] [project-id]
#
# Prerequisites:
# - gcloud CLI authenticated and configured
# - Terraform infrastructure already deployed
# - Required permissions to access Secret Manager

set -e

ENVIRONMENT=${1:-staging}
PROJECT_ID=${2:-$GCP_PROJECT_ID}

if [ -z "$PROJECT_ID" ]; then
    echo "Error: PROJECT_ID not provided and GCP_PROJECT_ID environment variable not set"
    echo "Usage: $0 [staging|production] [project-id]"
    exit 1
fi

PREFIX="project-aether-${ENVIRONMENT}"

echo "🔐 Populating secrets for Project Aether - ${ENVIRONMENT} environment"
echo "📁 Project ID: ${PROJECT_ID}"
echo "🏷️  Secret prefix: ${PREFIX}"
echo ""

# Function to create or update secret
create_or_update_secret() {
    local secret_name=$1
    local secret_value=$2
    local description=$3
    
    echo "📝 Setting secret: ${secret_name}"
    
    # Check if secret exists
    if gcloud secrets describe "${secret_name}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
        echo "   ↳ Updating existing secret"
        echo -n "${secret_value}" | gcloud secrets versions add "${secret_name}" --data-file=- --project="${PROJECT_ID}"
    else
        echo "   ↳ Creating new secret"
        gcloud secrets create "${secret_name}" --replication-policy="automatic" --project="${PROJECT_ID}"
        echo -n "${secret_value}" | gcloud secrets versions add "${secret_name}" --data-file=- --project="${PROJECT_ID}"
    fi
}

# Function to prompt for secret value
prompt_for_secret() {
    local secret_name=$1
    local description=$2
    local secret_value
    
    echo ""
    echo "🔑 ${description}"
    echo "Secret name: ${secret_name}"
    read -s -p "Enter value: " secret_value
    echo ""
    
    if [ -z "$secret_value" ]; then
        echo "⚠️  Warning: Empty value provided for ${secret_name}"
        read -p "Continue anyway? (y/N): " confirm
        if [[ ! $confirm =~ ^[Yy]$ ]]; then
            echo "Skipping ${secret_name}"
            return
        fi
    fi
    
    create_or_update_secret "${secret_name}" "${secret_value}" "${description}"
}

# Function to get Terraform output
get_terraform_output() {
    local output_name=$1
    cd iac/terraform
    terraform output -raw "${output_name}" 2>/dev/null || echo ""
    cd - >/dev/null
}

echo "🏗️  Retrieving infrastructure information from Terraform..."

# Get infrastructure details from Terraform
DATABASE_CONNECTION_NAME=$(get_terraform_output "database_connection_name")
DATABASE_PRIVATE_IP=$(get_terraform_output "database_private_ip")
DATABASE_NAME=$(get_terraform_output "database_name")
DATABASE_USER=$(get_terraform_output "database_user")
REDIS_HOST=$(get_terraform_output "redis_host")
REDIS_PORT=$(get_terraform_output "redis_port")

echo "   ↳ Database connection: ${DATABASE_CONNECTION_NAME}"
echo "   ↳ Redis host: ${REDIS_HOST}:${REDIS_PORT}"

# Application secrets that need manual input
echo ""
echo "📋 The following secrets require manual input:"

prompt_for_secret "${PREFIX}-app-secret-key" "Application secret key for session management (generate a random 32-character string)"

prompt_for_secret "${PREFIX}-jwt-secret" "JWT signing secret for authentication tokens (generate a random 64-character string)"

prompt_for_secret "${PREFIX}-google-api-key" "Google API key for Vertex AI and other Google services"

prompt_for_secret "${PREFIX}-dataforseo-login" "DataForSEO API login credentials"

prompt_for_secret "${PREFIX}-dataforseo-password" "DataForSEO API password credentials"

# Infrastructure-derived secrets
echo ""
echo "🔧 Setting infrastructure-derived secrets..."

if [ -n "$DATABASE_CONNECTION_NAME" ]; then
    create_or_update_secret "${PREFIX}-cloud-sql-connection-name" "${DATABASE_CONNECTION_NAME}" "Cloud SQL connection name"
else
    echo "⚠️  Warning: Could not retrieve database connection name from Terraform"
fi

# For database URL, we need the password which should be manually provided or retrieved
echo ""
echo "🗄️  Database Configuration"
if [ -n "$DATABASE_PRIVATE_IP" ] && [ -n "$DATABASE_NAME" ] && [ -n "$DATABASE_USER" ]; then
    echo "Database details retrieved from Terraform:"
    echo "   ↳ Host: ${DATABASE_PRIVATE_IP}"
    echo "   ↳ Database: ${DATABASE_NAME}"
    echo "   ↳ User: ${DATABASE_USER}"
    echo ""
    
    read -s -p "Enter database password: " DATABASE_PASSWORD
    echo ""
    
    if [ -n "$DATABASE_PASSWORD" ]; then
        DATABASE_URL="postgresql://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_PRIVATE_IP}:5432/${DATABASE_NAME}"
        create_or_update_secret "${PREFIX}-database-url" "${DATABASE_URL}" "Complete database connection URL"
        create_or_update_secret "${PREFIX}-database-password" "${DATABASE_PASSWORD}" "Database password"
    else
        echo "⚠️  Warning: Database password not provided, skipping database URL"
    fi
else
    echo "⚠️  Warning: Could not retrieve complete database information from Terraform"
    prompt_for_secret "${PREFIX}-database-url" "Complete database connection URL (postgresql://user:pass@host:port/db)"
fi

# Redis configuration
echo ""
echo "📨 Redis Configuration"
if [ -n "$REDIS_HOST" ] && [ -n "$REDIS_PORT" ]; then
    REDIS_URL="redis://${REDIS_HOST}:${REDIS_PORT}"
    create_or_update_secret "${PREFIX}-redis-url" "${REDIS_URL}" "Complete Redis connection URL"
    create_or_update_secret "${PREFIX}-celery-broker-url" "${REDIS_URL}" "Celery broker URL (Redis)"
    create_or_update_secret "${PREFIX}-celery-result-backend" "${REDIS_URL}" "Celery result backend URL (Redis)"
    create_or_update_secret "${PREFIX}-memorystore-ip" "${REDIS_HOST}" "Memorystore Redis IP address"
    create_or_update_secret "${PREFIX}-memorystore-port" "${REDIS_PORT}" "Memorystore Redis port"
else
    echo "⚠️  Warning: Could not retrieve Redis information from Terraform"
    prompt_for_secret "${PREFIX}-redis-url" "Complete Redis connection URL (redis://host:port)"
    prompt_for_secret "${PREFIX}-celery-broker-url" "Celery broker URL (usually same as Redis URL)"
fi

# Application configuration secrets
echo ""
echo "⚙️  Application Configuration"
create_or_update_secret "${PREFIX}-gcp-project-id" "${PROJECT_ID}" "Google Cloud Project ID"
create_or_update_secret "${PREFIX}-gcp-region" "us-central1" "Google Cloud Region"
create_or_update_secret "${PREFIX}-environment" "${ENVIRONMENT}" "Application environment"
create_or_update_secret "${PREFIX}-debug-mode" "false" "Debug mode setting"

# Frontend configuration
if [ "$ENVIRONMENT" = "production" ]; then
    FRONTEND_URL="https://project-aether-production-frontend-us-central1.a.run.app"
else
    FRONTEND_URL="https://project-aether-staging-frontend-us-central1.a.run.app"
fi

create_or_update_secret "${PREFIX}-frontend-origin" "${FRONTEND_URL}" "Frontend origin URL for CORS configuration"

echo ""
echo "✅ Secret population completed for ${ENVIRONMENT} environment!"
echo ""
echo "📝 Next steps:"
echo "   1. Verify all secrets are properly set:"
echo "      gcloud secrets list --filter='name:${PREFIX}' --project=${PROJECT_ID}"
echo ""
echo "   2. Test secret access from a Cloud Run service:"
echo "      gcloud secrets versions access latest --secret='${PREFIX}-app-secret-key' --project=${PROJECT_ID}"
echo ""
echo "   3. Trigger the CI/CD pipeline by pushing to the appropriate branch"
echo ""
echo "🔒 Security reminder: The secret values are now stored securely in Google Secret Manager"
echo "    and will be automatically injected into your Cloud Run services."