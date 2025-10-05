# NOAA Alerts Pushover

Sends out NOAA Severe Weather Alerts via [Pushover](http://www.pushover.net). Any time a new alert is created for your monitored counties, you'll receive a push notification on your devices.

## Features

- 🌪️ Real-time severe weather alerts from NOAA
- 📱 Push notifications via Pushover
- 🗺️ Monitor multiple counties across the US
- 🔕 Filter out unwanted alert types
- 🐳 Docker and Docker Compose support
- 💾 SQLite database to prevent duplicate notifications
- 🔄 Automatic cleanup of expired alerts
- 🛡️ Robust error handling for API failures and malformed responses

## Quick Start

Get up and running in 5 minutes:

```bash
# Clone and configure
git clone https://github.com/k9barry/noaa-alerts-pushover.git
cd noaa-alerts-pushover
cp config.txt.example config.txt
# Edit config.txt with your Pushover credentials

# Edit counties.json to add counties you want to monitor

# Run with Docker (recommended)
docker compose up -d

# Or run with Python
pip install -r requirements.txt
python3 models.py
python3 fetch.py
```

For detailed installation instructions, configuration options, and troubleshooting, see the [Installation Guide](INSTALL.md)

## Configuration

The application uses two configuration files:

**`config.txt`** - Your Pushover API credentials and settings:
```ini
[pushover]
token = YOUR_PUSHOVER_TOKEN     # Get from pushover.net
user = YOUR_PUSHOVER_USER_KEY

[events]
ignored = Red Flag Warning,Heat Advisory  # Optional: filter unwanted alerts

[schedule]
fetch_interval = 5      # Check for alerts every 5 minutes
cleanup_interval = 24   # Clean expired files daily
vacuum_interval = 168   # Database maintenance weekly
```

**`counties.json`** - Counties to monitor (find codes at [NOAA website](http://www.nws.noaa.gov/emwin/winugc.htm)):
```json
[
    {"fips": "012057", "name": "Hillsborough County", "state": "FL", "ugc": "FL057"}
]
```

See [INSTALL.md](INSTALL.md) for complete configuration details

## Usage

```bash
# Standard run
python fetch.py

# Test without notifications    # Debug mode
python fetch.py --nopush         python fetch.py --debug

# Clear all alerts               # Continuous monitoring
python fetch.py --purge          python scheduler.py
```

The built-in scheduler runs checks automatically (default: every 5 minutes). Customize intervals in the `[schedule]` section of `config.txt`. See [INSTALL.md](INSTALL.md) for all options.

## Customization

**Alert Templates**: Customize `templates/detail.html` to change how alert HTML pages look. See [templates/TEMPLATE_GUIDE.md](templates/TEMPLATE_GUIDE.md) for 7+ examples and complete guide.

**Setup Validation**: Run `python test_setup.py --fix` to automatically create config.txt and initialize the database

## Project Status

This project has been fully modernized to Python 3.12+ with comprehensive documentation and Docker support:

### ✅ Modernization Highlights
- **Python 3 Migration**: Updated from Python 2 to Python 3.12+ with modern syntax
- **Security Improvements**: SSL verification, request timeouts, robust error handling
- **Docker Support**: Full containerization with non-root user (UID 1000) for enhanced security
- **Built-in Scheduler**: Python schedule library for automated task execution
- **Comprehensive Documentation**: 2,000+ lines across 7 detailed guides
- **CI/CD Pipeline**: Automated testing with GitHub Actions
- **Auto-fix Tools**: Setup validation script with automatic configuration repair

### 🔒 Docker Security
The Docker container runs as non-root user `noaa` (UID 1000) following security best practices:
- Reduced attack surface
- Limits container escape vulnerability impact
- Follows Docker and Kubernetes security recommendations
- Compatible with read-only root filesystems

See [INSTALL.md](INSTALL.md) for permission setup details.

## Documentation

- [Installation Guide](INSTALL.md) - Complete setup instructions with quick start section
- [Template Customization Guide](templates/TEMPLATE_GUIDE.md) - Customize alert HTML pages
- [How It Works](CODE_EXPLANATION.md) - Technical overview of the codebase
- [Security](SECURITY.md) - Security best practices and considerations
- [Changelog](CHANGELOG.md) - Version history and updates
- [Contributing](CONTRIBUTING.md) - Contribution guidelines
- [Creating Tags and Releases](docs/TAGGING.md) - Guide for maintainers on tagging versions

## Requirements

- Python 3.12+
- SQLite3
- Active Pushover account
- Internet connection

## Dependencies

- **arrow** - Date/time handling
- **beautifulsoup4** - HTML parsing for cleanup tasks
- **Jinja2** - Template engine for alert pages
- **peewee** - ORM for SQLite database
- **requests** - HTTP client for API calls

See [requirements.txt](requirements.txt) for specific versions.

## How It Works

### Architecture

The application consists of several key components:

1. **fetch.py** - Main application that fetches alerts from NOAA and sends notifications
2. **scheduler.py** - Automated task scheduler with configurable intervals
3. **models.py** - Database ORM layer using Peewee with SQLite
4. **cleanup.py** - Removes expired HTML alert files
5. **vacuum.py** - Database maintenance and optimization
6. **test_setup.py** - Setup validation with auto-fix capabilities

### Data Flow

```
NOAA API (GeoJSON) → fetch.py → Filter by Counties → Check Database
                                                           ↓
                                                      New Alert?
                                                           ↓
                                        Generate HTML + Send Pushover Notification
```

### Scheduling

The built-in scheduler (Python `schedule` library) automatically runs:
- **fetch.py** - Check for new alerts (default: every 5 minutes)
- **cleanup.py** - Remove expired HTML files (default: every 24 hours)
- **vacuum.py** - Database maintenance (default: weekly)

All intervals are configurable in `config.txt` under the `[schedule]` section.

### Database

- **Engine**: SQLite with WAL (Write-Ahead Logging) mode
- **Location**: `data/alerts.db`
- **Purpose**: Prevents duplicate notifications by tracking sent alerts
- **Maintenance**: Automatic cleanup and vacuum operations via scheduler

### Alert Processing

1. Fetches latest alerts from NOAA Weather API (JSON/GeoJSON format)
2. Filters alerts matching your monitored counties (FIPS/UGC codes)
3. Checks database to prevent duplicate notifications
4. Generates HTML detail page in `output/` directory
5. Sends Pushover notification with link to detail page
6. Stores alert in database with expiration timestamp

## Notes

- The application saves alerts to a local SQLite database to prevent duplicate notifications
- Expired alerts are automatically cleaned up by the scheduler
- HTML detail pages are generated for each alert in the `output/` directory
- County matching uses both FIPS6 and UGC code systems for comprehensive coverage

## Performance & Requirements

### System Requirements
- **CPU**: Minimal (typically <1% during checks)
- **Memory**: ~50-100 MB RAM
- **Storage**: <100 MB (depends on alert history)
- **Network**: Minimal bandwidth usage

### API Usage
- One NOAA API call per check (default: every 5 minutes)
- One Pushover API call per new alert
- Typical processing time: <5 seconds per check

## Contributing

Feedback and pull requests are welcome! Please read our [Security Policy](SECURITY.md) before contributing.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please open an issue on GitHub.
