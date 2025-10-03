#!/bin/sh
# Healthcheck script for Docker container
# This script performs basic validation that the application can run

set -e

# Check if Python is available
python --version > /dev/null 2>&1 || exit 1

# Check if required files exist
[ -f /app/fetch.py ] || exit 1
[ -f /app/models.py ] || exit 1
[ -f /app/config.txt ] || exit 1
[ -f /app/counties.json ] || exit 1

# Check if database directory exists
[ -d /app/data ] || exit 1

# Try to import the database module to ensure it's accessible
python -c "from models import db; db.connect(); db.close()" || exit 1

# All checks passed
exit 0
