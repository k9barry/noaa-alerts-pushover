FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libxml2-dev \
    libxslt-dev \
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

# Switch to noaa user
USER noaa


# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV RUN_MODE=once
ENV CHECK_INTERVAL=300

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
CMD []
