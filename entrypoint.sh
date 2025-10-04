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
  
  loop)
    echo "Running in continuous mode with ${CHECK_INTERVAL:-300} second interval..."
    if [ "$(id -u)" = "0" ]; then
      exec gosu noaa sh -c "while true; do python fetch.py $* || echo 'Check failed, will retry...'; sleep ${CHECK_INTERVAL:-300}; done"
    else
      while true; do
        python fetch.py "$@" || echo "Check failed, will retry..."
        sleep "${CHECK_INTERVAL:-300}"
      done
    fi
    ;;
  
  cron)
    echo "Setting up cron job with schedule: ${CRON_SCHEDULE:-*/5 * * * *}"
    if [ "$(id -u)" = "0" ]; then
      # Write cron job to crontab as noaa user - log to /app for non-root user write access
      gosu noaa sh -c "echo '${CRON_SCHEDULE:-*/5 * * * *} cd /app && python fetch.py $* >> /app/cron.log 2>&1' | crontab -"
    else
      # Write cron job to crontab - log to /app for non-root user write access
      echo "${CRON_SCHEDULE:-*/5 * * * *} cd /app && python fetch.py $* >> /app/cron.log 2>&1" | crontab -
    fi
    # Start cron in foreground
    exec cron -f
    ;;
  
  *)
    echo "Unknown mode: $MODE"
    echo "Valid modes: once, loop, cron"
    exit 1
    ;;
esac
