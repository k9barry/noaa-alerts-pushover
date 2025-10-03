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

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p /app/output /app/data

# Copy and set entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy and set healthcheck script
COPY healthcheck.sh /healthcheck.sh
RUN chmod +x /healthcheck.sh

# Create non-root user 'noaa' and set ownership
RUN useradd -m -u 1000 noaa && \
    chown -R noaa:noaa /app && \
    chown noaa:noaa /entrypoint.sh && \
    chown noaa:noaa /healthcheck.sh

# Switch to noaa user
USER noaa

# Initialize database
RUN python models.py

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV RUN_MODE=once
ENV CHECK_INTERVAL=300

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
CMD []
