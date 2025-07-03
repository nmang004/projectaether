#!/bin/bash

# Security scan script for Project Aether
# Usage: ./run-security-scan.sh <target-url>

set -e

# Check if target URL is provided
if [ -z "$1" ]; then
    echo "Error: Target URL is required"
    echo "Usage: $0 <target-url>"
    echo "Example: $0 https://staging.project-aether.io"
    exit 1
fi

TARGET_URL="$1"

# Validate URL format
if ! echo "$TARGET_URL" | grep -E '^https?://' > /dev/null; then
    echo "Error: Invalid URL format. URL must start with http:// or https://"
    exit 1
fi

echo "Starting security scan for: $TARGET_URL"
echo "Timestamp: $(date)"

# Create reports directory if it doesn't exist
mkdir -p security-reports

# Run OWASP ZAP baseline scan
echo "Running OWASP ZAP baseline scan..."

docker run --rm \
    -v "$(pwd)/security-reports:/zap/wrk/:rw" \
    -t owasp/zap2docker-stable \
    zap-baseline.py \
    -t "$TARGET_URL" \
    -g gen.conf \
    -J baseline-report.json \
    -H baseline-report.html \
    -r baseline-report.md \
    || true

# Check if reports were generated
if [ -f "security-reports/baseline-report.html" ]; then
    echo "Security scan completed successfully!"
    echo "Reports generated in security-reports/ directory:"
    ls -la security-reports/
else
    echo "Warning: Security scan completed but reports may not have been generated"
fi

echo "Security scan finished at: $(date)"