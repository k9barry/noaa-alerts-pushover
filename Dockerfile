FROM python:3.12-slim

# Metadata labels for better Docker Hub display
LABEL org.opencontainers.image.title="NOAA Alerts Pushover"
LABEL org.opencontainers.image.description="Real-time NOAA severe weather alerts via Pushover push notifications"
LABEL org.opencontainers.image.url="https://github.com/k9barry/noaa-alerts-pushover"
LABEL org.opencontainers.image.source="https://github.com/k9barry/noaa-alerts-pushover"
LABEL org.opencontainers.image.documentation="https://github.com/k9barry/noaa-alerts-pushover/blob/master/README.md"
LABEL org.opencontainers.image.licenses="MIT"
LABEL maintainer="k9barry"

# Set working directory
WORKDIR /app

# Install system dependencies including gosu for user switching
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libxml2-dev \
    libxslt-dev \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user 'noaa'
RUN useradd -m -u 1000 noaa

# Copy application files (excluding entrypoint and healthcheck scripts)
COPY . .

# Copy entrypoint and healthcheck scripts explicitly
COPY entrypoint.sh /entrypoint.sh
COPY healthcheck.sh /healthcheck.sh

# Create necessary directories, set permissions, and ensure ownership for 'noaa' user
RUN mkdir -p /app/output /app/data

# Set permissions and ownership for entrypoint and healthcheck scripts
RUN chmod +x /entrypoint.sh /healthcheck.sh && \
    chown noaa:noaa /entrypoint.sh /healthcheck.sh

# Force ownership of /app/data and /app/output to noaa (fixes volume or root-owned dir issues)
RUN chown -R noaa:noaa /app/data /app/output && chmod 775 /app/data /app/output

# Set ownership for all app files (optional, but ensures noaa can write)
RUN chown -R noaa:noaa /app

# Note: We intentionally do NOT switch to noaa user here.
# The entrypoint script will handle ownership fixes and then switch to noaa user.
# This allows the entrypoint to fix permissions on mounted volumes.

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
CMD []
