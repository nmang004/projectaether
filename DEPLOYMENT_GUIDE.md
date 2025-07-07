# Project Aether - Google Cloud Platform Deployment Guide

This guide provides step-by-step instructions for deploying Project Aether to Google Cloud Platform using the automated CI/CD pipeline.

## Prerequisites

### 1. Google Cloud Platform Setup
- Google Cloud Project with billing enabled
- Required APIs enabled:
  - Cloud Run API
  - Cloud SQL API
  - Cloud Build API
  - Artifact Registry API
  - Secret Manager API
  - VPC Access API
  - Service Networking API
  - Identity and Access Management (IAM) API

### 2. Required Tools
- `gcloud` CLI installed and configured
- `terraform` CLI (version 1.0.0 or later)
- GitHub repository with admin access

## Step-by-Step Deployment

### Phase 1: Infrastructure Provisioning

#### 1.1 Enable Required APIs
```bash
# Set your project ID
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"

# Enable required APIs
gcloud services enable run.googleapis.com \
  sqladmin.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  vpcaccess.googleapis.com \
  servicenetworking.googleapis.com \
  iam.googleapis.com \
  --project=$GCP_PROJECT_ID
```

#### 1.2 Create Service Account for GitHub Actions
```bash
# Create service account
gcloud iam service-accounts create github-actions-sa \
  --display-name="GitHub Actions Service Account" \
  --description="Service account for GitHub Actions CI/CD" \
  --project=$GCP_PROJECT_ID

# Grant necessary roles
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.editor"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Create and download service account key
gcloud iam service-accounts keys create github-actions-key.json \
  --iam-account=github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com
```

#### 1.3 Deploy Infrastructure with Terraform
```bash
# Navigate to terraform directory
cd iac/terraform

# Initialize Terraform
terraform init

# Plan deployment (staging environment)
terraform plan -var="project_id=$GCP_PROJECT_ID" -var="environment=staging"

# Apply infrastructure
terraform apply -var="project_id=$GCP_PROJECT_ID" -var="environment=staging"
```

### Phase 2: GitHub Repository Configuration

#### 2.1 Set GitHub Secrets
In your GitHub repository, go to Settings → Secrets and variables → Actions, and add:

| Secret Name | Value | Description |
|-------------|--------|-------------|
| `GCP_PROJECT_ID` | your-project-id | Google Cloud Project ID |
| `GCP_SA_KEY` | Contents of github-actions-key.json | Service account key for authentication |

#### 2.2 GitHub Environments
Create the following GitHub environments in your repository:
- `staging` (for develop branch deployments)
- `production` (for main branch deployments)

### Phase 3: Secret Manager Population

#### 3.1 Required Secrets
Populate the following secrets in Google Secret Manager:

```bash
# Application secrets
gcloud secrets versions add project-aether-staging-app-secret-key --data-file=- <<< "your-app-secret-key"
gcloud secrets versions add project-aether-staging-jwt-secret --data-file=- <<< "your-jwt-secret"

# External API secrets
gcloud secrets versions add project-aether-staging-google-api-key --data-file=- <<< "your-google-api-key"
gcloud secrets versions add project-aether-staging-dataforseo-login --data-file=- <<< "your-dataforseo-login"
gcloud secrets versions add project-aether-staging-dataforseo-password --data-file=- <<< "your-dataforseo-password"

# Database connection (will be auto-populated by Terraform outputs)
DATABASE_URL="postgresql://aether_user:$(terraform output -raw database_password)@$(terraform output -raw database_private_ip):5432/projectaether"
gcloud secrets versions add project-aether-staging-database-url --data-file=- <<< "$DATABASE_URL"

# Cloud SQL connection name
gcloud secrets versions add project-aether-staging-cloud-sql-connection-name --data-file=- <<< "$(terraform output -raw database_connection_name)"

# Redis connection
REDIS_URL="redis://$(terraform output -raw redis_host):$(terraform output -raw redis_port)"
gcloud secrets versions add project-aether-staging-redis-url --data-file=- <<< "$REDIS_URL"

# Celery configuration (same as Redis URL)
gcloud secrets versions add project-aether-staging-celery-broker-url --data-file=- <<< "$REDIS_URL"
```

### Phase 4: Pipeline Execution

#### 4.1 Trigger Deployment
Push code to the `develop` branch to trigger staging deployment:
```bash
git checkout develop
git push origin develop
```

#### 4.2 Monitor Deployment
- Go to GitHub Actions tab in your repository
- Monitor the "Deploy to Google Cloud Platform" workflow
- Check logs for any deployment issues

#### 4.3 Verify Deployment
```bash
# Get service URLs
API_URL=$(gcloud run services describe project-aether-staging-api --region=$GCP_REGION --format="value(status.url)")
FRONTEND_URL=$(gcloud run services describe project-aether-staging-frontend --region=$GCP_REGION --format="value(status.url)")

# Test API health endpoint
curl -f "$API_URL/health"

# Test frontend
curl -f "$FRONTEND_URL/health"

echo "API URL: $API_URL"
echo "Frontend URL: $FRONTEND_URL"
```

### Phase 5: Database Migration

Database migrations are automatically triggered during deployment. If you need to run them manually:

```bash
# Trigger migration build
gcloud builds submit --config ./iac/cloudbuild-migrate.yaml \
  --substitutions=_ENVIRONMENT=staging,_IMAGE_TAG=latest \
  --project=$GCP_PROJECT_ID
```

## Production Deployment

### 1. Prepare Production Infrastructure
```bash
# Deploy production infrastructure
terraform apply -var="project_id=$GCP_PROJECT_ID" -var="environment=production"
```

### 2. Populate Production Secrets
Repeat the secret population process for production environment, replacing `staging` with `production` in secret names.

### 3. Deploy to Production
Push to the `main` branch:
```bash
git checkout main
git merge develop  # Merge staging changes
git push origin main
```

## Troubleshooting

### Common Issues

#### 1. Permission Denied Errors
Ensure the GitHub Actions service account has all required roles:
```bash
# Verify service account roles
gcloud projects get-iam-policy $GCP_PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com"
```

#### 2. Cloud SQL Connection Issues
Verify VPC connector and private service connection:
```bash
# Check VPC connector status
gcloud compute networks vpc-access connectors list --region=$GCP_REGION

# Check private service connection
gcloud services vpc-peerings list --network=project-aether-staging-vpc
```

#### 3. Container Registry Issues
Ensure Artifact Registry repositories exist:
```bash
# List repositories
gcloud artifacts repositories list --location=$GCP_REGION
```

#### 4. Secret Manager Issues
Verify secrets exist and have values:
```bash
# List secrets
gcloud secrets list --filter="name:project-aether-staging"

# Check secret value (be careful with sensitive data)
gcloud secrets versions access latest --secret="project-aether-staging-app-secret-key"
```

## Monitoring and Maintenance

### 1. View Logs
```bash
# API service logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=project-aether-staging-api" --limit=50 --format=table

# Worker service logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=project-aether-staging-worker" --limit=50 --format=table
```

### 2. Monitor Resources
```bash
# Check Cloud Run services
gcloud run services list --region=$GCP_REGION

# Check Cloud SQL instance
gcloud sql instances list

# Check Redis instance
gcloud redis instances list --region=$GCP_REGION
```

### 3. Scale Services
```bash
# Update Cloud Run service scaling
gcloud run services update project-aether-staging-api \
  --min-instances=2 \
  --max-instances=20 \
  --region=$GCP_REGION
```

## Security Considerations

1. **Service Account Keys**: Store GitHub service account keys securely and rotate regularly
2. **Secret Manager**: Use Secret Manager for all sensitive configuration
3. **Network Security**: Services run in private VPC with controlled egress
4. **IAM**: Follow principle of least privilege for all service accounts
5. **Container Security**: Use non-root users in Docker containers

## Cost Optimization

1. **Auto-scaling**: Configure appropriate min/max instances for Cloud Run
2. **Resource Limits**: Set CPU and memory limits appropriately
3. **Database**: Use appropriate instance sizes for Cloud SQL
4. **Monitoring**: Set up billing alerts and resource monitoring

For additional support, refer to the Google Cloud documentation or create an issue in this repository.