# PyDoll MCP Server - Production Docker Image
# Multi-stage build for optimized production deployment

# Build stage - install dependencies and prepare application
FROM python:3.11-slim as builder

# Set build arguments
ARG PYDOLL_VERSION="1.0.0"
ARG BUILD_DATE
ARG VCS_REF

# Set environment variables for build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app user and directories
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the application
RUN pip install --no-cache-dir -e .

# Runtime stage - minimal production image
FROM python:3.11-slim as runtime

# Set metadata labels
LABEL maintainer="Jinsong Roh <jinsongroh@gmail.com>" \
      version="$PYDOLL_VERSION" \
      description="PyDoll MCP Server - Revolutionary Browser Automation for AI" \
      org.opencontainers.image.title="PyDoll MCP Server" \
      org.opencontainers.image.description="Revolutionary Model Context Protocol server for PyDoll browser automation" \
      org.opencontainers.image.version="$PYDOLL_VERSION" \
      org.opencontainers.image.created="$BUILD_DATE" \
      org.opencontainers.image.revision="$VCS_REF" \
      org.opencontainers.image.source="https://github.com/JinsongRoh/pydoll-mcp" \
      org.opencontainers.image.url="https://github.com/JinsongRoh/pydoll-mcp" \
      org.opencontainers.image.documentation="https://github.com/JinsongRoh/pydoll-mcp/blob/main/README.md" \
      org.opencontainers.image.licenses="MIT"

# Set runtime environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYDOLL_LOG_LEVEL=INFO \
    PYDOLL_BROWSER_TYPE=chrome \
    PYDOLL_HEADLESS=true \
    PYDOLL_STEALTH_MODE=true \
    PYDOLL_AUTO_CAPTCHA_BYPASS=true \
    PYDOLL_WINDOW_WIDTH=1920 \
    PYDOLL_WINDOW_HEIGHT=1080 \
    PYDOLL_DOCKER=true

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Browser dependencies
    wget \
    gnupg \
    ca-certificates \
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
    lsb-release \
    xdg-utils \
    # Utilities
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* && \
    # Verify Chrome installation
    google-chrome --version

# Create app user and directories
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Create application directories
RUN mkdir -p /app /app/logs /app/config /app/data && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy Python environment from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Create configuration file
RUN echo '{\
  "browser": {\
    "type": "chrome",\
    "headless": true,\
    "window_size": [1920, 1080],\
    "stealth_mode": true\
  },\
  "automation": {\
    "timeout": 30,\
    "retry_attempts": 3,\
    "human_behavior": true\
  },\
  "captcha": {\
    "auto_solve": true,\
    "cloudflare_bypass": true,\
    "recaptcha_bypass": true\
  },\
  "network": {\
    "monitor_requests": true,\
    "block_ads": true,\
    "enable_cache": true\
  }\
}' > /app/config/default.json && \
    chown appuser:appuser /app/config/default.json

# Switch to non-root user
USER appuser

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Print banner\n\
echo "🤖 PyDoll MCP Server v$(python -c \"import pydoll_mcp; print(pydoll_mcp.__version__)\")"\n\
echo "Revolutionary Browser Automation for AI"\n\
echo "========================================"\n\
\n\
# Verify installation\n\
echo "Verifying installation..."\n\
python -m pydoll_mcp.server --test || {\n\
    echo "❌ Installation verification failed"\n\
    exit 1\n\
}\n\
echo "✅ Installation verified successfully"\n\
\n\
# Check browser availability\n\
echo "Checking browser availability..."\n\
google-chrome --version\n\
echo "✅ Google Chrome is available"\n\
\n\
# Start the server\n\
echo "Starting PyDoll MCP Server..."\n\
exec python -m pydoll_mcp.server "$@"\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -m pydoll_mcp.server --test || exit 1

# Expose port (if needed for future web interface)
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["--log-level", "INFO"]

# Build information
ARG BUILD_INFO="Built with Docker multi-stage build"
ENV BUILD_INFO="$BUILD_INFO"

# Add build information
RUN echo "Build Date: $BUILD_DATE" > /app/BUILD_INFO && \
    echo "VCS Ref: $VCS_REF" >> /app/BUILD_INFO && \
    echo "Version: $PYDOLL_VERSION" >> /app/BUILD_INFO && \
    echo "$BUILD_INFO" >> /app/BUILD_INFO
