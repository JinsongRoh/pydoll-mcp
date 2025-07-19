# PyDoll MCP Server - Docker Image
# Provides a containerized environment for PyDoll browser automation

# Use official Python runtime as base image
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Jinsong Roh <jinsongroh@gmail.com>"
LABEL description="PyDoll MCP Server - Revolutionary Browser Automation for AI"
LABEL version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/JinsongRoh/pydoll-mcp"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYDOLL_HEADLESS=true
ENV PYDOLL_LOG_LEVEL=INFO
ENV PYDOLL_BROWSER_TYPE=chrome
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Essential system packages
    curl \
    wget \
    gnupg \
    unzip \
    xvfb \
    # Chrome dependencies
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgcc1 \
    libgconf-2-4 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    ca-certificates \
    # Additional utilities
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r pydoll && useradd -r -g pydoll -s /bin/bash pydoll \
    && mkdir -p /home/pydoll \
    && chown -R pydoll:pydoll /home/pydoll \
    && chown -R pydoll:pydoll /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install PyDoll MCP Server
RUN pip install --no-cache-dir -e .

# Create necessary directories
RUN mkdir -p /app/logs /app/screenshots /app/downloads /app/config \
    && chown -R pydoll:pydoll /app

# Create Chrome user data directory
RUN mkdir -p /home/pydoll/.config/google-chrome \
    && chown -R pydoll:pydoll /home/pydoll/.config

# Switch to non-root user
USER pydoll

# Set up Chrome for non-root user
RUN google-chrome --version

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Set up display for headless mode\n\
export DISPLAY=:99\n\
\n\
# Start Xvfb in background if not headless\n\
if [ "$PYDOLL_HEADLESS" != "true" ]; then\n\
    Xvfb :99 -screen 0 1920x1080x24 &\n\
    sleep 2\n\
fi\n\
\n\
# Run PyDoll MCP Server\n\
exec python -m pydoll_mcp.server "$@"\n\
' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import pydoll_mcp; print('OK')" || exit 1

# Expose port for HTTP communication (if needed)
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD []

# Build instructions and usage examples
# 
# Build the image:
#   docker build -t pydoll-mcp:latest .
#
# Run the container:
#   docker run -d --name pydoll-mcp-server \
#     -p 8080:8080 \
#     -v $(pwd)/config:/app/config \
#     -v $(pwd)/logs:/app/logs \
#     -v $(pwd)/screenshots:/app/screenshots \
#     -v $(pwd)/downloads:/app/downloads \
#     pydoll-mcp:latest
#
# Run with custom environment:
#   docker run -d --name pydoll-mcp-server \
#     -e PYDOLL_HEADLESS=false \
#     -e PYDOLL_LOG_LEVEL=DEBUG \
#     -e PYDOLL_BROWSER_TYPE=chrome \
#     --shm-size=2g \
#     pydoll-mcp:latest
#
# Run interactive test:
#   docker run -it --rm pydoll-mcp:latest python -m pydoll_mcp.cli test
#
# For GUI applications (Linux with X11):
#   docker run -d --name pydoll-mcp-server \
#     -e DISPLAY=$DISPLAY \
#     -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
#     -e PYDOLL_HEADLESS=false \
#     pydoll-mcp:latest