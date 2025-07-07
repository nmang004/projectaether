# Dummy Dockerfile for automatic Cloud Build triggers
# This exists only to prevent "Dockerfile not found" errors
# Actual deployment is handled by GitHub Actions

FROM alpine:latest
RUN echo "✅ Dummy build completed - actual deployment via GitHub Actions"
CMD ["echo", "This container should not be used in production"]