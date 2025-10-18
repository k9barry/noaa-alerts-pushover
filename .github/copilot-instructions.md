# GitHub Copilot Instructions for NOAA Alerts Pushover

This file provides context and guidelines for GitHub Copilot when working with this repository.

## Project Overview

**NOAA Alerts Pushover** is a Python application that monitors NOAA (National Oceanic and Atmospheric Administration) severe weather alerts and sends real-time push notifications via the Pushover service. The application filters alerts by county, prevents duplicate notifications, and generates HTML detail pages.

### Key Features
- Real-time severe weather alerts from NOAA's public API
- Push notifications via Pushover API
- Multi-county monitoring across the US
- SQLite database for duplicate prevention
- Automatic cleanup of expired alerts
- Docker and Docker Compose support
- Configurable event filtering
- HTML detail page generation

## Architecture

### Core Components

1. **fetch.py** - Main application script
   - Fetches NOAA JSON feeds
   - Parses GeoJSON format with CAP properties
   - Filters alerts by county codes (FIPS/UGC)
   - Manages database operations
   - Sends Pushover notifications
   - Generates HTML detail pages

2. **models.py** - Database ORM layer
   - Uses Peewee ORM with SQLite
   - Alert model with fields: alert_id, title, event, details, expires, url, api_url, fips_codes, ugc_codes, created
   - Database stored in `data/alerts.db` with WAL mode enabled

3. **scheduler.py** - Task scheduler
   - Uses Python schedule library for automated task execution
   - Runs fetch.py, cleanup.py, and vacuum.py on configurable intervals
   - Configurable via config.txt [schedule] section

4. **cleanup.py** - HTML sanitization utility
   - Removes expired HTML alert files from output directory
   - Run automatically by scheduler or manually

5. **vacuum.py** - Database maintenance
   - SQLite VACUUM operations for database optimization
   - Run automatically by scheduler or manually

6. **test_setup.py** - Setup validation script
   - Validates Python version, dependencies, configuration, and database

### Data Flow

```
NOAA API → fetch.py → Parse JSON → Filter Counties → Check Database
                                                           ↓
                                                      Insert New
                                                           ↓
                                              Generate HTML + Send Push
```

## Coding Standards

### Python Style
- **Version**: Python 3.12+
- **Style Guide**: PEP 8 with 4-space indentation
- **Max Line Length**: 100 characters
- **Docstrings**: Required for classes and methods
- **Type Hints**: Optional but encouraged for new code

### Import Organization
```python
# Standard library imports
import os
import sys
import json

# Third-party imports
import arrow
import requests
import peewee

# Local imports
from models import Alert
```

### Key Dependencies
- **arrow**: Date/time handling (timezone-aware)
- **peewee**: SQLite ORM
- **requests**: HTTP client for API calls
- **jinja2**: Template engine for HTML generation
- **beautifulsoup4**: HTML cleaning
- **schedule**: Python job scheduling library

## Important Patterns and Conventions

### Alert ID Generation
Always use SHA-224 hash for consistent alert IDs:
```python
import hashlib
alert_id = hashlib.sha224(noaa_id.encode()).hexdigest()
```

### County Code Matching
The application uses two code systems:
- **FIPS6**: Federal Information Processing Standards (numeric)
- **UGC**: Universal Geographic Code (alphanumeric like "FL057")

Both must be checked for alert matching.

### Timestamp Handling
Use Arrow library for timezone-aware operations:
```python
import arrow
run_ts = arrow.utcnow().timestamp()
expires_ts = arrow.get(expires_str).timestamp()
```

### JSON Response Handling
NOAA API returns GeoJSON format with CAP properties:
```python
data = request.json()
properties = data.get('properties', {})
event = properties.get('event', '')
description = properties.get('description', '')
```

### Logging
Use Python's logging module (already configured in fetch.py):
```python
logger.info("Inserted %d new alerts." % insert_count)
logger.debug("Matched %d existing alerts." % existing_count)
```

## Configuration Files

### config.txt
INI format with sections:
- `[pushover]`: token, user (required); api_url, base_url, test_message (optional)
  - api_url: Pushover API endpoint URL (default: https://api.pushover.net/1/messages.json)
  - base_url: Base URL for hosted HTML alert files
  - test_message: Enable test messages from NOAA (true/false)
- `[noaa]`: api_url (optional)
  - api_url: NOAA Weather API endpoint URL (default: https://api.weather.gov/alerts)
- `[events]`: ignored (comma-separated list of event types to skip)
- `[schedule]`: fetch_interval (minutes), cleanup_interval (hours), vacuum_interval (hours)
  - fetch_interval: How often to check for new alerts (default: 5 minutes)
  - cleanup_interval: How often to remove expired HTML files (default: 24 hours)
  - vacuum_interval: How often to run database maintenance (default: 168 hours/weekly)

Example:
```ini
[pushover]
token = YOUR_PUSHOVER_TOKEN
user = YOUR_PUSHOVER_USER_KEY
api_url = https://api.pushover.net/1/messages.json

[noaa]
api_url = https://api.weather.gov/alerts

[events]
ignored = Red Flag Warning,Heat Advisory

[schedule]
fetch_interval = 5
cleanup_interval = 24
vacuum_interval = 168
```

### counties.json
JSON array of county objects:
```json
[
    {
        "fips": "012057",
        "name": "Hillsborough County",
        "state": "FL",
        "ugc": "FL057"
    }
]
```

## API Integrations

### NOAA Weather Alerts API
- **Base URL**: `https://api.weather.gov/alerts` (configurable via `api_url` in `[noaa]` section of config.txt)
- **Format**: GeoJSON with CAP properties
- **Rate Limiting**: Be respectful, implement delays if needed
- **SSL**: Verify certificates (currently disabled with urllib3 warning suppression)
- **Response**: JSON with GeoJSON features containing FIPS/UGC codes

### Pushover API
- **Endpoint**: `https://api.pushover.net/1/messages.json` (default, configurable via `api_url` in config.txt)
- **Method**: POST
- **Required Fields**: token, user, title, message
- **Optional Fields**: url, url_title, priority
- **Response**: JSON with status

## Database Schema

### Alert Table
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| alert_id | VARCHAR | Unique hash of NOAA alert ID |
| title | VARCHAR | Alert title |
| event | VARCHAR | Event type (e.g., "Tornado Warning") |
| details | VARCHAR | Optional sub-event keywords |
| expires | DATETIME | Expiration date/time |
| expires_utc_ts | DOUBLE | Unix timestamp of expiration |
| url | VARCHAR | Public alert URL |
| api_url | VARCHAR | NOAA API URL for details |
| fips_codes | TEXT | Comma-separated FIPS codes |
| ugc_codes | TEXT | Comma-separated UGC codes |
| created | DATETIME | Timestamp when alert was inserted |

**Important**: The database uses WAL (Write-Ahead Logging) mode for better concurrency.

## Testing Guidelines

### Manual Testing
```bash
# Test without sending notifications
python fetch.py --nopush

# Enable debug logging
python fetch.py --debug

# Clear database
python fetch.py --purge

# Validate setup
python test_setup.py
```

### Validation Script
The `test_setup.py` script validates:
- Python version (3.12+)
- Required module imports
- Configuration file existence and structure
- Counties file structure
- Database connectivity

**Enhanced with auto-fix capabilities:**
```bash
# Run validation checks only
python test_setup.py

# Auto-fix issues without prompting
python test_setup.py --fix

# Interactive mode - prompt before each fix
python test_setup.py --interactive
```

Auto-fixes include:
- Creating config.txt from config.txt.example
- Initializing database with proper schema
- Validating schedule section values in config.txt

### CI/CD
GitHub Actions workflow in `.github/workflows/ci.yml`:
- Python syntax checking
- Import validation
- Database initialization
- Docker image build

## Security Considerations

### Credentials
- Never hardcode Pushover tokens or user keys
- Use environment variables or config files (gitignored)
- config.txt should never be committed (only config.txt.example)

### API Security
- SSL verification should be enabled in production
- Implement timeouts for API requests
- Handle API rate limiting
- Validate and sanitize JSON input from NOAA

### Database
- Use parameterized queries (Peewee handles this)
- Regular backups recommended
- WAL mode prevents most lock issues

## Docker Support

### Files
- **Dockerfile**: Python 3.12-slim base
- **docker-compose.yml**: Uses scheduler mode by default
- **entrypoint.sh**: Flexible run modes (once, scheduler)
- **.dockerignore**: Excludes unnecessary files

### Volume Mounts
- `./data:/app/data` - Database persistence
- `./output:/app/output` - HTML files
- `./config.txt:/app/config.txt` - Configuration
- `./counties.json:/app/counties.json` - County list

## Common Tasks

### Adding New Features

When adding features, consider:
1. Backward compatibility with existing configurations
2. Impact on database schema (migrations not currently implemented)
3. Error handling for API failures
4. Logging for debugging
5. Documentation updates

### Modifying Alert Processing

The main processing flow in fetch.py:
1. `Parser.fetch()` - Fetches and inserts alerts
2. `Parser.check_new_alerts()` - Filters by county
3. `Parser.details_for_alert()` - Fetches detailed information
4. `Parser.send_pushover_alert()` - Sends notification

### Event Filtering

To ignore specific alert types, users add them to config.txt:
```ini
[events]
ignored = Red Flag Warning,Heat Advisory,Special Weather Statement
```

The main script reads this and skips matching events during notification.

## HTML Template

The `templates/detail.html` Jinja2 template generates alert detail pages with:
- Alert headline
- Event type and issuer
- Full description
- Safety instructions
- Affected area
- Expiration time

**Comprehensive customization guide**: See `templates/TEMPLATE_GUIDE.md` for:
- All available template variables (alert dictionary, expires timestamp)
- 7+ practical customization examples (styling, mobile layouts, conditional content)
- Jinja2 syntax reference and best practices
- Testing and troubleshooting instructions

## File Organization

```
noaa-alerts-pushover/
├── .github/
│   ├── workflows/ci.yml
│   └── copilot-instructions.md (this file)
├── templates/
│   ├── detail.html             # Jinja2 template for alert HTML pages
│   ├── sample.json             # Sample NOAA API GeoJSON response
│   ├── README.md               # Templates directory documentation
│   └── TEMPLATE_GUIDE.md       # Comprehensive template customization guide
├── data/              (gitignored, created at runtime)
│   └── alerts.db
├── output/            (gitignored, created at runtime)
│   └── *.html
├── fetch.py           (main alert checking application)
├── scheduler.py       (Python schedule-based task scheduler)
├── models.py          (database models)
├── cleanup.py         (HTML cleanup - run by scheduler)
├── vacuum.py          (DB maintenance - run by scheduler)
├── test_setup.py      (validation script with --fix and --interactive modes)
├── config.txt         (gitignored, user creates from example)
├── config.txt.example (template with [schedule] section)
├── counties.json      (user edits)
├── requirements.txt   (Python dependencies including schedule)
├── Dockerfile         (non-root user UID 1000)
├── docker-compose.yml (scheduler mode by default)
├── entrypoint.sh      (flexible run modes)
├── docs/                   # Documentation directory
│   ├── CODE_EXPLANATION.md    # Technical architecture
│   ├── TAGGING_QUICKSTART.md  # Quick guide for creating release tags
│   └── TAGGING.md             # Detailed tagging documentation
└── Documentation files:
    ├── README.md              # Project overview with modernization highlights
    ├── INSTALL.md             # Combined installation guide (includes quick start)
    ├── CHANGELOG.md           # Complete version history
    ├── CONTRIBUTING.md        # Contribution guidelines
    └── SECURITY.md            # Security best practices
```

## Error Handling

### Common Issues
1. **NOAA API failures**: Implement retries with exponential backoff
2. **Malformed JSON**: Wrap parsing in try-except blocks
3. **Database locks**: WAL mode helps, but still handle OperationalError
4. **Missing config**: Exit gracefully with clear error message
5. **Network timeouts**: Set reasonable timeout values on requests

### Graceful Degradation
- Individual alert failures shouldn't stop processing other alerts
- Log errors but continue operation when possible
- Provide clear error messages for configuration issues

## Documentation

Key documentation files (consolidated and updated):
- **README.md**: Project overview with modernization highlights, features, architecture, and quick start
- **INSTALL.md**: Comprehensive installation guide combining quick start (5-minute setup) and detailed instructions
- **templates/TEMPLATE_GUIDE.md**: Complete guide for customizing alert HTML templates (300+ lines, 7+ examples)
- **docs/CODE_EXPLANATION.md**: Technical architecture deep-dive
- **docs/TAGGING_QUICKSTART.md**: Quick guide for creating release tags
- **CONTRIBUTING.md**: Contribution guidelines
- **SECURITY.md**: Security best practices
- **CHANGELOG.md**: Complete version history including recent documentation improvements

**Removed files** (consolidated):
- QUICKSTART.md - merged into INSTALL.md
- CHANGES_SUMMARY.md - merged into CHANGELOG.md
- DOCKER_NONROOT.md - incorporated into INSTALL.md
- SUMMARY.md - incorporated into README.md
- TEMPLATE_GUIDE.md - moved to templates/TEMPLATE_GUIDE.md

## Tips for Copilot

### When Suggesting Code Changes
1. Maintain existing code style and patterns
2. Use the established logging conventions
3. Follow the existing error handling patterns
4. Preserve backward compatibility with config files
5. Consider both Docker and native Python environments
6. Remember that this runs on a schedule, not as a service

### When Adding Features
1. Check if configuration changes are needed
2. Update relevant documentation files
3. Add validation to test_setup.py if appropriate
4. Consider impact on both single-run and scheduler modes
5. Maintain minimal dependencies

### When Fixing Bugs
1. Preserve the existing database schema
2. Don't change the alert ID generation (breaks deduplication)
3. Test with both FIPS and UGC code matching
4. Verify timezone handling remains correct
5. Check that HTML generation still works

## Useful Resources

- NOAA API: https://www.weather.gov/documentation/services-web-api
- CAP Standard: http://docs.oasis-open.org/emergency/cap/v1.2/
- Pushover API: https://pushover.net/api
- FIPS Codes: https://www.weather.gov/pimar/FIPSCodes
- UGC Codes: https://www.weather.gov/ (find your state, then click "County List" or "Zone List")
- Peewee ORM: http://docs.peewee-orm.com/

## Version Information

- **Python**: 3.12+
- **Database**: SQLite 3 with WAL mode
- **Key Libraries**: See requirements.txt for specific versions

## License

MIT License - See LICENSE file for details.

---

**Last Updated**: 2024
**Maintained By**: k9barry
**Repository**: https://github.com/k9barry/noaa-alerts-pushover
