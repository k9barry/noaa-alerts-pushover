#!/bin/sh
# Entrypoint script for Docker container
# This container runs in scheduler mode only

set -e

# Check if config.txt exists, if not create it from config.txt.example
if [ ! -f /app/config.txt ]; then
  echo "config.txt not found, creating from config.txt.example..."
  if [ -f /app/config.txt.example ]; then
    cp /app/config.txt.example /app/config.txt
    echo "✓ Created config.txt from config.txt.example"
    echo "⚠️  IMPORTANT: Edit config.txt and add your Pushover credentials!"
  else
    echo "❌ ERROR: config.txt.example not found, cannot auto-create config.txt"
    exit 1
  fi
fi

# Check if counties.json exists, if not create it from counties.json.example
if [ ! -f /app/counties.json ]; then
  echo "counties.json not found, creating from counties.json.example..."
  if [ -f /app/counties.json.example ]; then
    cp /app/counties.json.example /app/counties.json
    echo "✓ Created counties.json from counties.json.example"
    echo "⚠️  IMPORTANT: Edit counties.json to monitor your desired counties!"
  else
    echo "❌ ERROR: counties.json.example not found, cannot auto-create counties.json"
    exit 1
  fi
fi

# Fix ownership of /data and /output directories (handles mounted volumes)
# This runs as root before switching to noaa user
if [ "$(id -u)" = "0" ]; then
  echo "Fixing ownership of /app/data and /app/output..."
  chown -R noaa:noaa /app/data /app/output 2>/dev/null || true
  echo "Switching to noaa user..."
  echo "Initializing database..."
  gosu noaa python models.py || echo "Database initialization failed or already exists"
  
  # Run setup validation
  echo ""
  echo "=" * 60
  echo "Running setup validation..."
  echo "=" * 60
  gosu noaa python test_setup.py || echo "⚠️  Setup validation completed with warnings"
  echo ""
else
  echo "Initializing database..."
  python models.py || echo "Database initialization failed or already exists"
  
  # Run setup validation
  echo ""
  echo "=" * 60
  echo "Running setup validation..."
  echo "=" * 60
  python test_setup.py || echo "⚠️  Setup validation completed with warnings"
  echo ""
fi

# Run scheduler mode
echo "Starting scheduler mode with Python schedule library..."
if [ "$(id -u)" = "0" ]; then
  exec gosu noaa python scheduler.py "$@"
else
  exec python scheduler.py "$@"
fi
