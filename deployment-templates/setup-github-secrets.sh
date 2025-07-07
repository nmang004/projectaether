#!/bin/bash

# Project Aether - GitHub Secrets Setup Script
# This script helps set up the required GitHub secrets for CI/CD
#
# Prerequisites:
# - GitHub CLI (gh) installed and authenticated
# - Google Cloud CLI (gcloud) authenticated
# - Service account key file created

set -e

PROJECT_ID=${1:-$GCP_PROJECT_ID}
REPO=${2:-$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null)}

if [ -z "$PROJECT_ID" ]; then
    echo "Error: PROJECT_ID not provided and GCP_PROJECT_ID environment variable not set"
    echo "Usage: $0 [project-id] [repo-name]"
    exit 1
fi

if [ -z "$REPO" ]; then
    echo "Error: Could not determine repository name"
    echo "Usage: $0 [project-id] [repo-name]"
    echo "Example: $0 my-project-123 username/project-aether"
    exit 1
fi

echo "🔧 Setting up GitHub secrets for Project Aether CI/CD"
echo "📁 Project ID: ${PROJECT_ID}"
echo "📁 Repository: ${REPO}"
echo ""

# Check if GitHub CLI is authenticated
if ! gh auth status >/dev/null 2>&1; then
    echo "❌ GitHub CLI not authenticated. Please run 'gh auth login' first."
    exit 1
fi

# Check if user has access to the repository
if ! gh repo view "$REPO" >/dev/null 2>&1; then
    echo "❌ Cannot access repository ${REPO}. Please check the repository name and your permissions."
    exit 1
fi

# Function to set GitHub secret
set_github_secret() {
    local secret_name=$1
    local secret_value=$2
    local description=$3
    
    echo "🔑 Setting GitHub secret: ${secret_name}"
    echo "   ↳ ${description}"
    
    echo -n "${secret_value}" | gh secret set "${secret_name}" --repo="${REPO}"
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Successfully set ${secret_name}"
    else
        echo "   ❌ Failed to set ${secret_name}"
        return 1
    fi
}

# Set GCP Project ID
echo "📝 Setting basic configuration secrets..."
set_github_secret "GCP_PROJECT_ID" "${PROJECT_ID}" "Google Cloud Project ID"

# Service Account Key
SERVICE_ACCOUNT_KEY_FILE="github-actions-key.json"

if [ -f "$SERVICE_ACCOUNT_KEY_FILE" ]; then
    echo ""
    echo "🔐 Found service account key file: ${SERVICE_ACCOUNT_KEY_FILE}"
    SERVICE_ACCOUNT_KEY=$(cat "$SERVICE_ACCOUNT_KEY_FILE")
    set_github_secret "GCP_SA_KEY" "${SERVICE_ACCOUNT_KEY}" "Google Cloud Service Account Key for GitHub Actions"
    
    echo ""
    echo "⚠️  Security reminder: The service account key file contains sensitive information."
    echo "   Consider deleting it locally after setup: rm ${SERVICE_ACCOUNT_KEY_FILE}"
else
    echo ""
    echo "⚠️  Service account key file not found: ${SERVICE_ACCOUNT_KEY_FILE}"
    echo ""
    echo "To create the service account key file, run:"
    echo "gcloud iam service-accounts keys create ${SERVICE_ACCOUNT_KEY_FILE} \\"
    echo "  --iam-account=github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com"
    echo ""
    read -p "Create service account key now? (y/N): " create_key
    
    if [[ $create_key =~ ^[Yy]$ ]]; then
        echo "Creating service account key..."
        gcloud iam service-accounts keys create "$SERVICE_ACCOUNT_KEY_FILE" \
            --iam-account="github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com"
        
        if [ -f "$SERVICE_ACCOUNT_KEY_FILE" ]; then
            SERVICE_ACCOUNT_KEY=$(cat "$SERVICE_ACCOUNT_KEY_FILE")
            set_github_secret "GCP_SA_KEY" "${SERVICE_ACCOUNT_KEY}" "Google Cloud Service Account Key for GitHub Actions"
            
            echo ""
            echo "⚠️  Service account key created and uploaded to GitHub."
            echo "   Consider deleting the local file: rm ${SERVICE_ACCOUNT_KEY_FILE}"
        else
            echo "❌ Failed to create service account key file"
            exit 1
        fi
    else
        echo "❌ Cannot proceed without service account key. Exiting."
        exit 1
    fi
fi

# Verify secrets were set
echo ""
echo "🔍 Verifying GitHub secrets..."
SECRETS=$(gh secret list --repo="$REPO" --json name -q '.[].name' | tr '\n' ' ')

for required_secret in "GCP_PROJECT_ID" "GCP_SA_KEY"; do
    if echo "$SECRETS" | grep -q "$required_secret"; then
        echo "   ✅ ${required_secret} is set"
    else
        echo "   ❌ ${required_secret} is NOT set"
    fi
done

echo ""
echo "📋 GitHub Environments Setup"
echo "   You still need to create the following GitHub environments manually:"
echo "   1. Go to ${REPO} → Settings → Environments"
echo "   2. Create 'staging' environment"
echo "   3. Create 'production' environment"
echo "   4. (Optional) Add protection rules for production environment"

echo ""
echo "✅ GitHub secrets setup completed!"
echo ""
echo "📝 Next steps:"
echo "   1. Create GitHub environments (staging, production)"
echo "   2. Deploy infrastructure: cd iac/terraform && terraform apply"
echo "   3. Populate Secret Manager: ./deployment-templates/populate-secrets.sh staging"
echo "   4. Push code to trigger deployment"
echo ""
echo "🔗 Repository: https://github.com/${REPO}"
echo "🚀 Ready for CI/CD deployment!"