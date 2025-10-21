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
- 🔐 Environment variable support for credentials (Docker-friendly)
- 🔁 Automatic retry logic with exponential backoff
- ⏱️ Rate limiting to respect API quotas
- ✅ Input validation for county codes (FIPS/UGC)
- 🧪 Comprehensive test suite with pytest

## Quick Start

**Docker (recommended):**
```bash
# From Docker Hub
docker pull k9barry/noaa-alerts-pushover:latest

# Or from GitHub Container Registry
docker pull ghcr.io/k9barry/noaa-alerts-pushover:latest

# Then configure and run - see INSTALL.md
```

See the [Installation Guide](INSTALL.md) for a 5-minute quick start or detailed installation instructions.

## Configuration

The application uses two configuration files:
- **`config.txt`** - Pushover API credentials, NOAA User-Agent (required by NWS), event filtering, test message options, and scheduling intervals
- **`counties.json`** - Counties to monitor (find FIPS codes at [NOAA FIPS Codes](https://www.weather.gov/pimar/FIPSCodes) and UGC codes at [NWS State Pages](https://www.weather.gov/) - click your state, then "County List" or "Zone List")

**New in 2.3+**: Enable `test_message = true` in config.txt to receive NOAA test alerts for validating your setup.

**Important**: The NWS API requires a User-Agent header with contact information. Configure the `[user_agent]` section in config.txt with your application name, version, and contact email or URL.

See [INSTALL.md](INSTALL.md) for complete configuration details and examples.

## Usage

**Continuous monitoring (recommended):**
```bash
python scheduler.py              # or: docker compose up -d
```

**Single check:**
```bash
python fetch.py                  # Standard run
python fetch.py --nopush         # Test without notifications
python fetch.py --debug          # Debug mode
```

See [INSTALL.md](INSTALL.md) for all command-line options and scheduling configuration.

## Customization

**Alert Templates**: Customize `templates/detail.html` to change how alert HTML pages look. See [templates/TEMPLATE_GUIDE.md](templates/TEMPLATE_GUIDE.md) for 7+ examples and complete guide.

**Custom URLs**: Configure `base_url` in `config.txt` to link Pushover notifications to your own hosted HTML files instead of NOAA's pages. See [INSTALL.md](INSTALL.md) for details.

**Setup Validation**: Run `python test_setup.py --fix` to automatically create config.txt and initialize the database

## Project Status

This project has been fully modernized to Python 3.12+ with comprehensive documentation and Docker support:

### ✅ Modernization Highlights
- **Python 3 Migration**: Updated from Python 2 to Python 3.12+ with modern syntax
- **Security Improvements**: SSL verification, request timeouts, robust error handling, environment variable support
- **Docker Support**: Full containerization with non-root user (UID 1000) for enhanced security
- **Built-in Scheduler**: Python schedule library for automated task execution
- **API Resilience**: Retry logic with exponential backoff, rate limiting, custom exception hierarchy
- **Input Validation**: FIPS/UGC code format validation to catch configuration errors early
- **Testing Framework**: Pytest-based test suite with 13+ unit and integration tests
- **Comprehensive Documentation**: 2,000+ lines across 7 detailed guides
- **CI/CD Pipeline**: Automated testing with GitHub Actions
- **Auto-fix Tools**: Setup validation script with automatic configuration repair

### 🔒 Docker Security
The Docker container runs as non-root user `noaa` (UID 1000) for enhanced security. See [INSTALL.md](INSTALL.md) for permission setup and [SECURITY.md](SECURITY.md) for security best practices.

## Documentation

- [Installation Guide](INSTALL.md) - Complete setup instructions with quick start section
- [Template Customization Guide](templates/TEMPLATE_GUIDE.md) - Customize alert HTML pages
- [How It Works](docs/CODE_EXPLANATION.md) - Technical overview of the codebase
- [Security](SECURITY.md) - Security best practices and considerations
- [Changelog](CHANGELOG.md) - Version history and updates
- [Contributing](CONTRIBUTING.md) - Contribution guidelines
- [Automatic Versioning](docs/AUTO_VERSIONING.md) - How PR merges automatically create releases
- [Versioning Quick Reference](docs/VERSIONING_QUICK_REFERENCE.md) - Quick guide for version labels
- [Workflow Diagram](docs/WORKFLOW_DIAGRAM.md) - Visual guide to automatic versioning

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
- **requests** - HTTP client for API calls with retry support
- **schedule** - Task scheduling for automated runs
- **pytest** - Testing framework (development)
- **pytest-cov** - Test coverage reporting (development)
- **responses** - HTTP request mocking for tests (development)

See [requirements.txt](requirements.txt) for specific versions.

## How It Works

1. **Fetch** - Downloads alerts from NOAA Weather API (JSON/GeoJSON format)
2. **Filter** - Matches alerts to your monitored counties (FIPS/UGC codes)
3. **Check** - Verifies against SQLite database to prevent duplicate notifications
4. **Generate** - Creates HTML detail page in `output/` directory
5. **Notify** - Sends Pushover notification with link to detail page
6. **Store** - Saves alert to database with expiration timestamp

The built-in scheduler automatically runs:
- **fetch.py** - Check for new alerts (default: every 5 minutes)
- **cleanup.py** - Remove expired HTML files (default: every 24 hours)
- **vacuum.py** - Database maintenance (default: weekly)

For technical details and architecture diagrams, see [docs/CODE_EXPLANATION.md](docs/CODE_EXPLANATION.md).

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

Feedback and pull requests are welcome! 

**Automatic Versioning**: When your PR is merged, a new version is automatically created based on labels you add (`major`, `minor`, or `patch`). See [docs/AUTO_VERSIONING.md](docs/AUTO_VERSIONING.md) for details.

Please read our [Security Policy](SECURITY.md) before contributing.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please open an issue on GitHub.
