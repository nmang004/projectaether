#!/bin/bash

# Project Aether - Deployment Verification Script
# This script verifies that the deployment was successful and all services are running
#
# Usage: ./verify-deployment.sh [staging|production] [project-id]

set -e

ENVIRONMENT=${1:-staging}
PROJECT_ID=${2:-$GCP_PROJECT_ID}
REGION=${3:-us-central1}

if [ -z "$PROJECT_ID" ]; then
    echo "Error: PROJECT_ID not provided and GCP_PROJECT_ID environment variable not set"
    echo "Usage: $0 [staging|production] [project-id] [region]"
    exit 1
fi

PREFIX="project-aether-${ENVIRONMENT}"

echo "🔍 Verifying Project Aether deployment - ${ENVIRONMENT} environment"
echo "📁 Project ID: ${PROJECT_ID}"
echo "🌍 Region: ${REGION}"
echo "🏷️  Service prefix: ${PREFIX}"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    local status=$1
    local message=$2
    case $status in
        "success")
            echo -e "${GREEN}✅ ${message}${NC}"
            ;;
        "warning")
            echo -e "${YELLOW}⚠️  ${message}${NC}"
            ;;
        "error")
            echo -e "${RED}❌ ${message}${NC}"
            ;;
        "info")
            echo -e "${BLUE}ℹ️  ${message}${NC}"
            ;;
    esac
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔧 Checking prerequisites..."
if ! command_exists gcloud; then
    print_status "error" "gcloud CLI not found. Please install it first."
    exit 1
fi

if ! command_exists curl; then
    print_status "error" "curl not found. Please install it first."
    exit 1
fi

# Verify authentication
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1 >/dev/null 2>&1; then
    print_status "error" "Not authenticated with gcloud. Run 'gcloud auth login' first."
    exit 1
fi

print_status "success" "Prerequisites check passed"
echo ""

# Set the project
gcloud config set project "$PROJECT_ID" >/dev/null 2>&1

# 1. Check Cloud Run Services
echo "🚀 Checking Cloud Run services..."

# API Service
API_SERVICE="${PREFIX}-api"
if gcloud run services describe "$API_SERVICE" --region="$REGION" >/dev/null 2>&1; then
    API_URL=$(gcloud run services describe "$API_SERVICE" --region="$REGION" --format="value(status.url)")
    API_STATUS=$(gcloud run services describe "$API_SERVICE" --region="$REGION" --format="value(status.conditions[0].status)")
    
    if [ "$API_STATUS" = "True" ]; then
        print_status "success" "API service is running at: $API_URL"
    else
        print_status "warning" "API service exists but may not be ready"
    fi
else
    print_status "error" "API service not found"
    API_URL=""
fi

# Frontend Service
FRONTEND_SERVICE="${PREFIX}-frontend"
if gcloud run services describe "$FRONTEND_SERVICE" --region="$REGION" >/dev/null 2>&1; then
    FRONTEND_URL=$(gcloud run services describe "$FRONTEND_SERVICE" --region="$REGION" --format="value(status.url)")
    FRONTEND_STATUS=$(gcloud run services describe "$FRONTEND_SERVICE" --region="$REGION" --format="value(status.conditions[0].status)")
    
    if [ "$FRONTEND_STATUS" = "True" ]; then
        print_status "success" "Frontend service is running at: $FRONTEND_URL"
    else
        print_status "warning" "Frontend service exists but may not be ready"
    fi
else
    print_status "error" "Frontend service not found"
    FRONTEND_URL=""
fi

# Worker Service
WORKER_SERVICE="${PREFIX}-worker"
if gcloud run services describe "$WORKER_SERVICE" --region="$REGION" >/dev/null 2>&1; then
    WORKER_URL=$(gcloud run services describe "$WORKER_SERVICE" --region="$REGION" --format="value(status.url)")
    WORKER_STATUS=$(gcloud run services describe "$WORKER_SERVICE" --region="$REGION" --format="value(status.conditions[0].status)")
    
    if [ "$WORKER_STATUS" = "True" ]; then
        print_status "success" "Worker service is deployed (no public traffic)"
    else
        print_status "warning" "Worker service exists but may not be ready"
    fi
else
    print_status "error" "Worker service not found"
fi

echo ""

# 2. Test Service Health Endpoints
echo "🏥 Testing service health endpoints..."

if [ -n "$API_URL" ]; then
    echo "Testing API health endpoint..."
    if curl -f -s "$API_URL/health" >/dev/null; then
        print_status "success" "API health check passed"
    else
        print_status "error" "API health check failed"
        echo "   Trying to get more details:"
        curl -s "$API_URL/health" || echo "   Could not reach endpoint"
    fi
else
    print_status "warning" "Skipping API health check (service not found)"
fi

if [ -n "$FRONTEND_URL" ]; then
    echo "Testing Frontend health endpoint..."
    if curl -f -s "$FRONTEND_URL/health" >/dev/null; then
        print_status "success" "Frontend health check passed"
    else
        print_status "error" "Frontend health check failed"
        echo "   Trying to get more details:"
        curl -s "$FRONTEND_URL/health" || echo "   Could not reach endpoint"
    fi
else
    print_status "warning" "Skipping Frontend health check (service not found)"
fi

echo ""

# 3. Check Database and Redis
echo "🗄️  Checking database and Redis..."

# Cloud SQL
CLOUDSQL_INSTANCE="${PREFIX}-postgres"
if gcloud sql instances describe "$CLOUDSQL_INSTANCE" >/dev/null 2>&1; then
    CLOUDSQL_STATUS=$(gcloud sql instances describe "$CLOUDSQL_INSTANCE" --format="value(state)")
    if [ "$CLOUDSQL_STATUS" = "RUNNING" ]; then
        print_status "success" "Cloud SQL instance is running"
    else
        print_status "warning" "Cloud SQL instance state: $CLOUDSQL_STATUS"
    fi
else
    print_status "error" "Cloud SQL instance not found"
fi

# Redis (Memorystore)
REDIS_INSTANCE="${PREFIX}-redis"
if gcloud redis instances describe "$REDIS_INSTANCE" --region="$REGION" >/dev/null 2>&1; then
    REDIS_STATUS=$(gcloud redis instances describe "$REDIS_INSTANCE" --region="$REGION" --format="value(state)")
    if [ "$REDIS_STATUS" = "READY" ]; then
        print_status "success" "Redis instance is ready"
    else
        print_status "warning" "Redis instance state: $REDIS_STATUS"
    fi
else
    print_status "error" "Redis instance not found"
fi

echo ""

# 4. Check Secrets
echo "🔐 Checking Secret Manager secrets..."

SECRETS_COUNT=$(gcloud secrets list --filter="name:${PREFIX}" --format="value(name)" | wc -l)
if [ "$SECRETS_COUNT" -gt 0 ]; then
    print_status "success" "Found $SECRETS_COUNT secrets in Secret Manager"
    
    # Check critical secrets
    CRITICAL_SECRETS=(
        "${PREFIX}-database-url"
        "${PREFIX}-redis-url"
        "${PREFIX}-app-secret-key"
        "${PREFIX}-jwt-secret"
    )
    
    for secret in "${CRITICAL_SECRETS[@]}"; do
        if gcloud secrets describe "$secret" >/dev/null 2>&1; then
            print_status "success" "Secret exists: $secret"
        else
            print_status "error" "Missing critical secret: $secret"
        fi
    done
else
    print_status "error" "No secrets found in Secret Manager with prefix: $PREFIX"
fi

echo ""

# 5. Check VPC and Networking
echo "🌐 Checking VPC and networking..."

VPC_NAME="${PREFIX}-vpc"
if gcloud compute networks describe "$VPC_NAME" >/dev/null 2>&1; then
    print_status "success" "VPC network exists: $VPC_NAME"
else
    print_status "error" "VPC network not found: $VPC_NAME"
fi

VPC_CONNECTOR="${PREFIX}-vpc-connector"
if gcloud compute networks vpc-access connectors describe "$VPC_CONNECTOR" --region="$REGION" >/dev/null 2>&1; then
    CONNECTOR_STATUS=$(gcloud compute networks vpc-access connectors describe "$VPC_CONNECTOR" --region="$REGION" --format="value(state)")
    if [ "$CONNECTOR_STATUS" = "READY" ]; then
        print_status "success" "VPC connector is ready"
    else
        print_status "warning" "VPC connector state: $CONNECTOR_STATUS"
    fi
else
    print_status "error" "VPC connector not found"
fi

echo ""

# 6. Check Artifact Registry
echo "📦 Checking Artifact Registry..."

REPO_NAME="${PREFIX}-docker-repo"
if gcloud artifacts repositories describe "$REPO_NAME" --location="$REGION" >/dev/null 2>&1; then
    print_status "success" "Artifact Registry repository exists: $REPO_NAME"
    
    # Check if images exist
    IMAGES=$(gcloud artifacts docker images list "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME" --format="value(package)" 2>/dev/null | wc -l)
    if [ "$IMAGES" -gt 0 ]; then
        print_status "success" "Found $IMAGES Docker images in registry"
    else
        print_status "warning" "No Docker images found in registry"
    fi
else
    print_status "error" "Artifact Registry repository not found: $REPO_NAME"
fi

echo ""

# 7. Summary
echo "📊 Deployment Summary"
echo "════════════════════════════════════════════════════════════════"

if [ -n "$API_URL" ]; then
    echo "🔗 API URL: $API_URL"
fi

if [ -n "$FRONTEND_URL" ]; then
    echo "🔗 Frontend URL: $FRONTEND_URL"
fi

echo ""
echo "🔧 Useful commands for monitoring:"
echo ""
echo "View API logs:"
echo "gcloud logging read \"resource.type=cloud_run_revision AND resource.labels.service_name=${PREFIX}-api\" --limit=50 --format=table"
echo ""
echo "View Worker logs:"
echo "gcloud logging read \"resource.type=cloud_run_revision AND resource.labels.service_name=${PREFIX}-worker\" --limit=50 --format=table"
echo ""
echo "Monitor Cloud Run services:"
echo "gcloud run services list --region=$REGION --filter=\"metadata.name ~ ${PREFIX}\""
echo ""
echo "Check database connections:"
echo "gcloud sql operations list --instance=$CLOUDSQL_INSTANCE"
echo ""

# Final status
echo "════════════════════════════════════════════════════════════════"
print_status "info" "Deployment verification completed for ${ENVIRONMENT} environment"

if [ -n "$API_URL" ] && [ -n "$FRONTEND_URL" ]; then
    print_status "success" "Core services are deployed and accessible"
    echo ""
    echo "🎉 Project Aether is successfully deployed to Google Cloud Platform!"
    echo "   You can now test the application using the URLs above."
else
    print_status "warning" "Some services may need attention"
    echo ""
    echo "💡 Check the deployment logs and ensure all steps were completed successfully."
fi