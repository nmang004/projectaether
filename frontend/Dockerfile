# =============================================================================
# Multi-stage build for React frontend - Production optimized for Google Cloud Run
# =============================================================================

# Build stage: Install dependencies and build the React application
FROM node:18-alpine as builder

# Set working directory
WORKDIR /app

# Copy package files first for better Docker layer caching
COPY package*.json ./

# Install dependencies using npm ci for production builds
# This ensures reproducible builds and faster installation
RUN npm install --no-audit --no-fund

# Copy source code (excluding files in .dockerignore)
COPY . .

# Set production environment variable for build
ENV VITE_API_URL=https://project-aether-staging-api-271865958975.us-central1.run.app/api/v1

# Build the React application for production
RUN npm run build:docker

# =============================================================================
# Production stage: Lightweight nginx server for serving static assets
# =============================================================================
FROM nginx:alpine as production

# Install curl for health checks (wget is not always available)
RUN apk add --no-cache curl

# Create nginx user and group if not exists
RUN addgroup -g 1001 -S nginx || true
RUN adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx || true

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Set proper permissions for nginx files
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Create directory for nginx temp files
RUN mkdir -p /var/cache/nginx/client_temp && \
    chown -R nginx:nginx /var/cache/nginx/client_temp

# Switch to nginx user for security
USER nginx

# Expose port 80
EXPOSE 80

# Health check for load balancers and orchestration systems
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
