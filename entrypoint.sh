#!/bin/sh
# Entrypoint script for Docker container
# This script provides flexible run modes for the container

set -e

# Default mode is single run
MODE="${RUN_MODE:-once}"

case "$MODE" in
  once)
    echo "Running in single-run mode..."
    exec python fetch.py "$@"
    ;;
  
  loop)
    echo "Running in continuous mode with ${CHECK_INTERVAL:-300} second interval..."
    while true; do
      python fetch.py "$@" || echo "Check failed, will retry..."
      sleep "${CHECK_INTERVAL:-300}"
    done
    ;;
  
  cron)
    echo "Setting up cron job with schedule: ${CRON_SCHEDULE:-*/5 * * * *}"
    # Write cron job to crontab
    echo "${CRON_SCHEDULE:-*/5 * * * *} cd /app && python fetch.py $* >> /var/log/cron.log 2>&1" | crontab -
    # Start cron in foreground
    exec cron -f
    ;;
  
  *)
    echo "Unknown mode: $MODE"
    echo "Valid modes: once, loop, cron"
    exit 1
    ;;
esac
