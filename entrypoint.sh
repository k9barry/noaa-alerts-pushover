#!/bin/sh
# Entrypoint script for Docker container
# This script provides flexible run modes for the container

set -e

# Fix ownership of /data and /output directories (handles mounted volumes)
# This runs as root before switching to noaa user
if [ "$(id -u)" = "0" ]; then
  echo "Fixing ownership of /app/data and /app/output..."
  chown -R noaa:noaa /app/data /app/output 2>/dev/null || true
  echo "Switching to noaa user..."
  echo "Initializing database..."
  gosu noaa python models.py || echo "Database initialization failed or already exists"
else
  echo "Initializing database..."
  python models.py || echo "Database initialization failed or already exists"
fi

# Default mode is single run
MODE="${RUN_MODE:-once}"

case "$MODE" in
  once)
    echo "Running in single-run mode..."
    if [ "$(id -u)" = "0" ]; then
      exec gosu noaa python fetch.py "$@"
    else
      exec python fetch.py "$@"
    fi
    ;;
  
  scheduler)
    echo "Running scheduler mode with Python schedule library..."
    if [ "$(id -u)" = "0" ]; then
      exec gosu noaa python scheduler.py "$@"
    else
      exec python scheduler.py "$@"
    fi
    ;;
  
  *)
    echo "Unknown mode: $MODE"
    echo "Valid modes: once, scheduler"
    exit 1
    ;;
esac
