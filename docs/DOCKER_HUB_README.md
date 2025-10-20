# NOAA Alerts Pushover - Docker Image

Real-time NOAA severe weather alerts delivered via Pushover push notifications to your devices.

## Quick Start

```bash
# Pull the image
docker pull k9barry/noaa-alerts-pushover:latest

# Create directories
mkdir -p data output

# Option 1: Let the container auto-create config files (recommended for first-time users)
# The container will automatically create config.txt and counties.json from example files
docker run -d \
  --name noaa-alerts \
  -v $(pwd)/config.txt:/app/config.txt \
  -v $(pwd)/counties.json:/app/counties.json \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/data:/app/data \
  -e TZ=UTC \
  --restart unless-stopped \
  k9barry/noaa-alerts-pushover:latest

# Option 2: Pre-create configuration files manually
wget https://raw.githubusercontent.com/k9barry/noaa-alerts-pushover/main/config.txt.example -O config.txt
wget https://raw.githubusercontent.com/k9barry/noaa-alerts-pushover/main/counties.json.example -O counties.json

# Edit config.txt with your Pushover credentials
# Edit counties.json with your monitored counties

# Then run the container
docker run -d \
  --name noaa-alerts \
  -v $(pwd)/config.txt:/app/config.txt:ro \
  -v $(pwd)/counties.json:/app/counties.json:ro \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/data:/app/data \
  -e TZ=UTC \
  --restart unless-stopped \
  k9barry/noaa-alerts-pushover:latest
```

**Important**: After first run, edit `config.txt` to add your Pushover credentials and `counties.json` to select your counties!

## Features

- 🌪️ Real-time severe weather alerts from NOAA
- 📱 Push notifications via Pushover API
- 🗺️ Monitor multiple counties across the US
- 🔕 Filter out unwanted alert types
- 💾 SQLite database prevents duplicate notifications
- 🔄 Automatic cleanup of expired alerts
- 🛡️ Robust error handling and security

## Configuration

### Required Files

1. **config.txt** - Pushover API credentials and settings
2. **counties.json** - List of counties to monitor

**Auto-Creation**: The container automatically creates these files from example templates if they don't exist on first run.

Download templates manually (optional):
- [config.txt.example](https://raw.githubusercontent.com/k9barry/noaa-alerts-pushover/main/config.txt.example)
- [counties.json.example](https://raw.githubusercontent.com/k9barry/noaa-alerts-pushover/main/counties.json.example)

### Environment Variables

- `TZ`: Timezone for logs (default: UTC)

**Note**: Container runs in scheduler mode only for continuous monitoring.

### Volumes

- `/app/config.txt` - Configuration file (mount as read-only)
- `/app/counties.json` - Counties list (mount as read-only)
- `/app/output` - Generated HTML alert files
- `/app/data` - SQLite database

### Scheduler Intervals

Configure check intervals in `config.txt`:

```ini
[schedule]
fetch_interval = 5        # Check for new alerts (minutes)
cleanup_interval = 24     # Remove expired HTML files (hours)
vacuum_interval = 168     # Database maintenance (hours/weekly)
```

## Docker Compose

Example `docker-compose.yml`:

```yaml
services:
  noaa-alerts:
    image: k9barry/noaa-alerts-pushover:latest
    container_name: noaa-alerts-pushover
    restart: unless-stopped
    volumes:
      - ./config.txt:/app/config.txt:ro
      - ./counties.json:/app/counties.json:ro
      - ./output:/app/output
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
      - TZ=UTC
    healthcheck:
      test: ["CMD", "/healthcheck.sh"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

## Security

- Container runs as non-root user `noaa` (UID 1000)
- Configuration files can be mounted read-only
- No secrets embedded in the image
- All API calls use HTTPS

### Volume Permissions

The container runs as UID 1000. Ensure mounted directories are writable:

```bash
# If your user is UID 1000 (check with: id -u)
chmod 755 ./output ./data

# Otherwise, set ownership
sudo chown -R 1000:1000 ./output ./data
```

## Tags

- `latest` - Latest stable release from main branch
- `v2.2.0`, `v2.1.0`, etc. - Specific version tags
- `2.2`, `2` - Major/minor version shortcuts

## Requirements

- Docker Engine 20.10+
- Active [Pushover](https://pushover.net) account (for notifications)
- Internet connection to NOAA API

## Usage Examples

### Debug Mode

Enable debug logging with the scheduler:

```bash
docker run --rm \
  -v $(pwd)/config.txt:/app/config.txt:ro \
  -v $(pwd)/counties.json:/app/counties.json:ro \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/data:/app/data \
  k9barry/noaa-alerts-pushover:latest \
  --debug --nopush
```

**Note**: For single-run testing without the Docker container, use the Python scripts directly:
```bash
python3 fetch.py --nopush --debug
```

## Support and Documentation

- **GitHub Repository**: https://github.com/k9barry/noaa-alerts-pushover
- **Installation Guide**: [INSTALL.md](https://github.com/k9barry/noaa-alerts-pushover/blob/main/INSTALL.md)
- **Security**: [SECURITY.md](https://github.com/k9barry/noaa-alerts-pushover/blob/main/SECURITY.md)
- **Issues**: https://github.com/k9barry/noaa-alerts-pushover/issues

## License

MIT License - See [LICENSE](https://github.com/k9barry/noaa-alerts-pushover/blob/main/LICENSE)
