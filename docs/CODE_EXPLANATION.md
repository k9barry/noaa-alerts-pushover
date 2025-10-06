# How the Code Works

This document provides a technical overview of the NOAA Alerts Pushover application, explaining the architecture, data flow, and key components.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Data Flow](#data-flow)
- [Core Components](#core-components)
- [Database Schema](#database-schema)
- [API Integration](#api-integration)
- [File Structure](#file-structure)

## Architecture Overview

```
┌─────────────────┐
│  NOAA Weather   │
│   Alerts API    │
└────────┬────────┘
         │ JSON Feed
         ▼
┌─────────────────┐
│   fetch.py      │◄──── Configuration (config.txt, counties.json)
│  (Main Script)  │
└────────┬────────┘
         │
         ├──► Parse JSON
         │
         ├──► Filter Counties
         │
         ├──► Check Database
         │         │
         │         ▼
         │    ┌─────────────┐
         │    │  SQLite DB  │
         │    │ (alerts.db) │
         │    └─────────────┘
         │
         ├──► Generate HTML
         │         │
         │         ▼
         │    ┌─────────────┐
         │    │   output/   │
         │    │  *.html     │
         │    └─────────────┘
         │
         └──► Send Push
                  │
                  ▼
            ┌─────────────┐
            │  Pushover   │
            │     API     │
            └─────────────┘
```

## Data Flow

### 1. Initialization Phase

```python
# Load configuration
config.txt → Parse pushover credentials
          → Parse ignored events

counties.json → Load monitored counties
             → Extract FIPS codes
             → Extract UGC codes
```

### 2. Fetch Phase

```python
# Request NOAA data
GET https://api.weather.gov/alerts
    → Receive GeoJSON feed
    → Parse all active alerts
    → Extract metadata for each alert:
        - Alert ID (SHA-224 hash of NOAA ID)
        - Title and event type
        - Expiration datetime
        - FIPS and UGC codes
        - URLs for details
```

### 3. Filter Phase

```python
# Match alerts to monitored counties
For each alert:
    Extract FIPS codes
    Extract UGC codes
    
    If FIPS/UGC matches monitored counties:
        Check if already in database
        If new: Insert into database
        If exists: Skip (no duplicate notifications)
```

### 4. Notification Phase

```python
# Process new alerts
For each new alert:
    If event type NOT in ignored list:
        Fetch detailed information from NOAA
        Generate HTML detail page
        Send Pushover notification
    Else:
        Log as ignored
```

## Core Components

### fetch.py

The main application script that orchestrates the entire process.

#### Key Functions:

**`Parser` Class:**
- Encapsulates all alert processing logic
- Manages Pushover credentials
- Handles county filtering

**`Parser.__init__(pushover_token, pushover_user, directory)`**
```python
# Initializes the Parser with:
# - Pushover API credentials
# - Working directory path
# - Empty lists for counties and codes
```

**`Parser.fetch(run_timestamp)`**
```python
# Main alert fetching logic:
1. Request NOAA JSON feed
2. Parse each alert entry
3. Calculate expiration timestamps
4. Extract FIPS/UGC codes
5. Check for special event keywords
6. Insert new alerts into database
7. Return statistics
```

**`Parser.check_new_alerts(created_ts)`**
```python
# Filter alerts for monitored counties:
1. Query database for alerts from this run
2. Extract FIPS/UGC codes from each alert
3. Compare against watched county codes
4. Match alerts to county names
5. Return list of matched Alert objects
```

**`Parser.details_for_alert(alert)`**
```python
# Fetch detailed information:
1. Request alert-specific JSON from NOAA
2. Parse GeoJSON response
3. Extract:
   - Headline
   - Event type
   - Issuer name
   - Description
   - Instructions
   - Area affected
4. Return dictionary of details
```

**`Parser.send_pushover_alert(id, title, message, url)`**
```python
# Send notification via Pushover:
1. Format request data
2. POST to Pushover API
3. Handle response
4. Log success/failure
```

**`Parser.create_alert_title(alert)`**
```python
# Format notification title:
"County Name (ST) Weather Alert"
```

**`Parser.create_alert_message(alert)`**
```python
# Format notification message:
"Alert Title (last 5 chars of ID)"
# Adds special event keywords if available
```

#### Main Execution Flow:

```python
if __name__ == '__main__':
    1. Parse command-line arguments
    2. Set up logging
    3. Initialize template engine (Jinja2)
    4. Create output directory if needed
    5. Load configuration files
    6. Initialize Parser object
    7. Clean up expired alerts (or purge all)
    8. Fetch current alerts from NOAA
    9. Check for new matching alerts
    10. For each match:
        - Fetch details
        - Generate HTML page
        - Send notification
    11. Exit
```

### models.py

Database ORM using Peewee for SQLite operations.

#### Database Schema:

```python
class Alert(BaseModel):
    alert_id      # VARCHAR: SHA-224 hash of NOAA ID
    title         # VARCHAR: Alert title
    event         # VARCHAR: Event type (e.g., "Tornado Warning")
    details       # VARCHAR: Optional keywords (e.g., "Thunderstorm, Wind")
    expires       # DATETIME: Expiration timestamp
    expires_utc_ts # DOUBLE: Unix timestamp for expiration
    url           # VARCHAR: Public alert URL
    api_url       # VARCHAR: NOAA API detail URL
    fips_codes    # TEXT: Comma-separated FIPS codes
    ugc_codes     # TEXT: Comma-separated UGC codes
    created       # DATETIME: When alert was inserted
```

#### Key Features:

- **WAL Mode:** Write-Ahead Logging for better concurrency
- **Data Directory:** Database stored in `data/` for easy volume mounting
- **Auto-create:** Database and directory created automatically

### cleanup.py

Utility script to remove expired HTML files from the output directory.

**Note:** When using scheduler.py (default), this script runs automatically on the configured schedule. It can also be run manually if needed.

#### Logic:

```python
1. List all HTML files in output/
2. For each file:
   - Parse HTML
   - Find <meta name="expires"> tag
   - Extract expiration timestamp
   - Compare to current time
   - Delete if expired
3. Log deletions
```

#### Automated Execution:

Cleanup runs automatically when using the scheduler (default mode). Configure the interval in `config.txt`:

```ini
[schedule]
cleanup_interval = 24  # hours (default: daily)
```

#### Manual Execution:

```bash
# Standard Python installation
python cleanup.py

# Docker installation
docker compose run --rm noaa-alerts python cleanup.py
```

### vacuum.py

Database maintenance utility to reclaim disk space.

**Note:** When using scheduler.py (default), this script runs automatically on the configured schedule. It can also be run manually if needed.

```python
# Runs SQLite VACUUM command
# Compacts database file
# Reduces fragmentation
```

#### Automated Execution:

Vacuum runs automatically when using the scheduler (default mode). Configure the interval in `config.txt`:

```ini
[schedule]
vacuum_interval = 168  # hours (default: weekly)
```

#### Manual Execution:

```bash
# Standard Python installation
python vacuum.py

# Docker installation
docker compose run --rm noaa-alerts python vacuum.py
```

### scheduler.py

Scheduler script that uses Python's `schedule` library to run fetch.py, cleanup.py, and vacuum.py on configurable intervals.

**Note:** This is the recommended way to run the application continuously.

#### Features:

- **Configurable Intervals:** Set check frequencies in `config.txt`
- **Automatic Maintenance:** Runs cleanup and vacuum automatically
- **Integrated Logging:** All operations logged to `scheduler.log`
- **Error Handling:** Continues running even if individual tasks fail

#### Configuration:

```ini
[schedule]
fetch_interval = 5        # Check for alerts every 5 minutes
cleanup_interval = 24     # Clean up HTML files every 24 hours
vacuum_interval = 168     # Vacuum database every 168 hours (weekly)
```

#### Running:

```bash
# Standard Python installation
python scheduler.py

# With debug logging
python scheduler.py --debug

# Disable push notifications (for testing)
python scheduler.py --nopush

# Docker (default mode)
docker compose up -d
```

#### Logs:

The scheduler maintains its own log file:
- `scheduler.log` - Scheduler operations and task execution
- `log.txt` - fetch.py operations (as usual)

## Database Schema

### Alert Table

| Field          | Type     | Description                          |
|----------------|----------|--------------------------------------|
| id             | INTEGER  | Primary key (auto-increment)         |
| alert_id       | VARCHAR  | Unique hash of NOAA alert ID         |
| title          | VARCHAR  | Alert title                          |
| event          | VARCHAR  | Event type                           |
| details        | VARCHAR  | Optional sub-event keywords          |
| expires        | DATETIME | Expiration date/time                 |
| expires_utc_ts | DOUBLE   | Unix timestamp of expiration         |
| url            | VARCHAR  | Public alert URL                     |
| api_url        | VARCHAR  | NOAA API URL for details             |
| fips_codes     | TEXT     | Comma-separated FIPS codes           |
| ugc_codes      | TEXT     | Comma-separated UGC codes            |
| created        | DATETIME | Timestamp when alert was inserted    |

### Indexes

The `alert_id` field should be indexed for faster lookups. The Peewee ORM handles this automatically.

## API Integration

### NOAA Weather Alerts API

**Base URL:** `https://api.weather.gov/alerts`

**Format:** GeoJSON with CAP (Common Alerting Protocol) properties

**Response Structure:**
```json
{
  "@context": [...],
  "type": "FeatureCollection",
  "features": [
    {
      "id": "https://api.weather.gov/alerts/urn:oid:...",
      "type": "Feature",
      "geometry": null,
      "properties": {
        "@id": "https://api.weather.gov/alerts/urn:oid:...",
        "id": "urn:oid:...",
        "areaDesc": "Jefferson County; Boulder County",
        "geocode": {
          "FIPS6": ["012057", "008005"],
          "UGC": ["FL057", "CO005"]
        },
        "sent": "2024-01-01T12:00:00-00:00",
        "effective": "2024-01-01T12:00:00-00:00",
        "expires": "2024-01-01T18:00:00-00:00",
        "status": "Actual",
        "messageType": "Alert",
        "category": "Met",
        "severity": "Severe",
        "event": "Tornado Warning",
        "headline": "Tornado Warning issued...",
        "description": "Full alert description",
        "instruction": "Safety instructions",
        "senderName": "NWS Office Name"
      }
    }
  ]
}
```

**Detail API:** Each alert has a unique API URL that provides the full GeoJSON feature with all properties.

### Pushover API

**Base URL:** `https://api.pushover.net/1/messages.json`

**Method:** POST

**Parameters:**
- `token`: Application API token
- `user`: User key
- `title`: Notification title
- `message`: Notification message
- `sound`: Notification sound (default: "falling")
- `url`: Optional URL to include

**Response:**
```json
{
  "status": 1,
  "request": "request-id"
}
```

## File Structure

```
noaa-alerts-pushover/
├── fetch.py              # Main alert checking application
├── scheduler.py          # Scheduler using Python schedule library
├── models.py             # Database models
├── cleanup.py            # HTML cleanup utility
├── vacuum.py             # Database maintenance
├── test_setup.py         # Setup validation script
├── requirements.txt      # Python dependencies
├── counties.json         # Counties to monitor
├── config.txt.example    # Configuration template
├── entrypoint.sh         # Docker entrypoint script
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose config
├── .dockerignore         # Docker build exclusions
├── .gitignore            # Git exclusions
├── README.md             # Project overview
├── INSTALL.md            # Installation guide
├── SECURITY.md           # Security documentation
├── CODE_EXPLANATION.md   # This file
├── LICENSE               # MIT license
├── templates/
│   └── detail.html       # Jinja2 template for alerts
├── output/               # Generated HTML files (gitignored)
├── data/                 # Database directory (gitignored)
│   └── alerts.db         # SQLite database
├── log.txt               # Application log (gitignored)
└── scheduler.log         # Scheduler log (gitignored)
```

## Key Algorithms

### Alert ID Generation

```python
# Use SHA-224 hash of NOAA's alert ID
# Ensures uniqueness and consistent length
alert_id = hashlib.sha224(noaa_id.encode()).hexdigest()
```

### County Matching

```python
# Extract codes from alert
alert_fips = ["012057", "008005"]
alert_ugc = ["FL057", "CO005"]

# Extract codes from configuration
watch_fips = ["012057", "029071"]
watch_ugc = ["FL057", "MO071"]

# Find intersection
fips_match = set(alert_fips) & set(watch_fips)  # {"012057"}
ugc_match = set(alert_ugc) & set(watch_ugc)      # {"FL057"}

# If any match, alert is relevant
if fips_match or ugc_match:
    # Look up county details
    for code in fips_match:
        county = find_county_by_fips(code)
    for code in ugc_match:
        county = find_county_by_ugc(code)
```

### Timestamp Handling

```python
# Parse NOAA timestamp
expires_dt = arrow.get("2024-01-01T18:00:00-05:00")

# Convert to UTC timestamp
expires_utc_ts = expires_dt.to('UTC').timestamp()

# Store both formats:
# - ISO string for readability
# - Unix timestamp for comparisons
```

### Special Event Detection

```python
# For generic event types, extract keywords
if event in ('Severe Weather Statement', 'Special Weather Statement'):
    summary = alert_summary.upper()
    keywords = []
    for term in ['THUNDERSTORM', 'TORNADO', 'FLOOD', 'WIND', 'HAIL']:
        if term in summary:
            keywords.append(term.title())
    details = ', '.join(keywords)
```

## Error Handling

The application includes comprehensive error handling to ensure stability even when NOAA APIs are experiencing issues.

### API Response Validation

#### HTTP Status Code Checking
```python
request = requests.get('https://api.weather.gov/alerts')
if request.status_code != 200:
    logger.error(f"Failed to fetch alerts feed: HTTP {request.status_code}")
    return
```

#### Content Type Detection
The application validates that responses contain expected data formats (JSON or XML) and not HTML error pages:

```python
# Check for HTML responses
if (
    'text/html' in request.headers.get('Content-Type', '')
    or request.text.strip().lower().startswith('<!doctype html')
    or request.text.strip().lower().startswith('<html')
):
    logger.error(f"Expected JSON but got HTML. Response was:\n{request.text[:1000]}")
    return
```

This prevents crashes when NOAA's API returns maintenance pages or error responses.

### JSON Parsing with Error Recovery

```python
try:
    data = request.json()
except Exception as e:
    logger.error(f"Failed to parse alerts feed JSON: {e}\nResponse was:\n{request.text[:1000]}")
    return
```

Malformed JSON is caught and logged with the first 1000 characters of the response for debugging.

### JSON Parsing with Safe Fallback

```python
try:
    data = request.json()
except Exception as e:
    logger.error(f"Failed to parse alert detail JSON: {e}\nResponse was:\n{request.text[:1000]}")
    return None
```

Invalid JSON returns `None` instead of crashing, allowing the application to continue processing other alerts.

### Network Errors
- Timeouts set to 30 seconds for all requests
- No automatic retries (cron/scheduler handles re-runs)
- All network errors logged to log.txt with context

### Database Errors
- WAL mode prevents most lock issues
- Peewee handles connection management
- Unique constraint on alert_id prevents duplicates

### Graceful Degradation
- Individual alert failures don't stop processing of other alerts
- Application exits gracefully if critical errors occur (e.g., configuration missing)
- Detailed error logging helps with troubleshooting

## Performance Considerations

### Scalability
- Single-threaded design (sufficient for personal use)
- Processes 100s of alerts in seconds
- Database queries are simple and fast
- Limited by NOAA API response time (~1-2 seconds)

### Resource Usage
- Memory: ~50MB typical usage
- Disk: Database grows slowly (~1KB per alert)
- Network: ~100KB per fetch
- CPU: Minimal (XML parsing)

### Optimization Opportunities
- Batch database inserts (currently one-by-one)
- Async HTTP requests (for multiple detail fetches)
- Database indexing on commonly queried fields
- Connection pooling for high-frequency runs

## Extension Points

### Adding New Notification Channels
1. Create new method in Parser class
2. Add configuration for new service
3. Call method alongside `send_pushover_alert()`

### Custom Filtering
1. Modify `check_new_alerts()` to add custom logic
2. Filter by additional criteria (severity, certainty, etc.)

### Alternative Storage
1. Replace Peewee models with different ORM
2. Or implement custom database layer
3. Keep Alert class interface compatible

### Web Interface
1. Serve HTML files from output/ directory
2. Add web framework (Flask, FastAPI)
3. Create API endpoints for alert history
4. Add web-based configuration

## Testing

The application doesn't include automated tests. For manual testing:

```bash
# Test with debug output
python fetch.py --debug

# Test without sending notifications
python fetch.py --nopush

# Test database cleanup
python fetch.py --purge

# Check logs
tail -f log.txt
```

## Dependencies Explained

- **arrow**: Modern Python datetime library with better API
- **beautifulsoup4**: HTML parsing for cleanup script
- **Jinja2**: Template engine for generating HTML alert pages
- **peewee**: Lightweight ORM for SQLite
- **requests**: HTTP library for API calls

## License

This code is released under the MIT License. See LICENSE file for details.
