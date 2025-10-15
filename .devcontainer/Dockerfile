FROM mcr.microsoft.com/devcontainers/python:3.12

# Set working directory
WORKDIR /workspace

# Install any system-level dependencies (optional)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Default shell user (already set by the base image)
USER vscode