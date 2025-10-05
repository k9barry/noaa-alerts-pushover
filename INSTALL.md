# Installation Guide

This comprehensive guide will help you get NOAA Alerts Pushover up and running. Choose between a quick 5-minute setup or detailed installation instructions.

## Table of Contents

- [Quick Start (5 Minutes)](#quick-start-5-minutes)
- [Docker Installation (Recommended)](#docker-installation-recommended)
- [Manual Installation](#manual-installation)
- [Configuration Details](#configuration-details)
- [Scheduling Options](#scheduling-options)
- [Command-Line Options](#command-line-options)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)
- [Security Notes](#security-notes)

## Quick Start (5 Minutes)

Get up and running with NOAA Alerts Pushover quickly!

### Prerequisites

Choose your preferred method:

**Docker (Easiest)**
- Docker 20.10+
- Docker Compose 2.0+

**Python (Manual)**
- Python 3.12+
- pip package manager

### Setup Steps

#### 1. Get the Code

```bash
git clone https://github.com/k9barry/noaa-alerts-pushover.git
cd noaa-alerts-pushover
```

#### 2. Configure

```bash
# Copy the example configuration
cp config.txt.example config.txt

# Edit with your Pushover credentials
nano config.txt  # or use your favorite editor
```

Add your [Pushover](https://pushover.net) credentials:
```ini
[pushover]
token = your_app_token_here
user = your_user_key_here

[events]
ignored = Red Flag Warning,Heat Advisory

[schedule]
# How often to check for new alerts (in minutes)
fetch_interval = 5
# How often to run cleanup.py to remove expired HTML files (in hours)
cleanup_interval = 24
# How often to run vacuum.py for database maintenance (in hours)
vacuum_interval = 168
```

#### 3. Select Counties

Edit `counties.json` to add the counties you want to monitor.

Find your county codes at: http://www.nws.noaa.gov/emwin/winugc.htm

Example:
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

#### 4. Validate Setup (Optional but Recommended)

```bash
python3 test_setup.py

# Auto-fix issues (create config.txt, initialize database)
python3 test_setup.py --fix

# Interactive mode (prompt before each fix)
python3 test_setup.py --interactive
```

#### 5. Run

**Docker (Recommended)**

Continuous monitoring (default):
```bash
docker compose up -d
```

This runs the scheduler which checks for alerts every 5 minutes by default.

Single check:
```bash
docker compose run -e RUN_MODE=once noaa-alerts
```

**Python (Manual)**

Initialize database:
```bash
python3 models.py
```

Continuous monitoring:
```bash
python3 scheduler.py
```

Single check:
```bash
python3 fetch.py
```

Test without sending notifications:
```bash
python3 fetch.py --nopush
```

Debug mode:
```bash
python3 fetch.py --debug
# or for scheduler
python3 scheduler.py --debug
```

---

## Docker Installation (Recommended)

Docker provides the easiest and most consistent way to run NOAA Alerts Pushover.

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/k9barry/noaa-alerts-pushover.git
   cd noaa-alerts-pushover
   ```

2. **Create your configuration file:**
   ```bash
   cp config.txt.example config.txt
   ```

3. **Edit `config.txt` with your Pushover credentials:**
   ```ini
   [pushover]
   token = YOUR_PUSHOVER_TOKEN
   user = YOUR_PUSHOVER_USER_KEY
   
   [events]
   ignored = Red Flag Warning,Heat Advisory
   ```

4. **Edit `counties.json` to monitor your desired counties:**
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

5. **Validate your setup (recommended):**
   ```bash
   python3 test_setup.py
   ```

6. **Set permissions for volume directories (if needed):**
   
   The container runs as user `noaa` (UID 1000). Ensure mounted directories are writable:
   ```bash
   # Option 1: Set ownership to UID 1000
   sudo chown -R 1000:1000 ./output ./data
   
   # Option 2: Use permissive permissions
   chmod 777 ./output ./data
   ```
   
   > **Note**: If your host user has UID 1000 (check with `id -u`), no changes are needed.
   > See the Docker Security section above for complete details.

7. **Build and run the container:**
   ```bash
   docker compose up -d
   ```

### Running on a Schedule

By default, the docker-compose.yml is configured for continuous monitoring using the Python schedule library.

#### Option 1: Use Scheduler Mode (Default)

The default docker-compose.yml runs in scheduler mode with configurable intervals:

```bash
docker compose up -d
```

The scheduler automatically runs:
- **fetch.py** - Check for new alerts (default: every 5 minutes)
- **cleanup.py** - Remove expired HTML files (default: every 24 hours)
- **vacuum.py** - Database maintenance (default: every 168 hours/weekly)

To customize intervals, edit your `config.txt` file:

```ini
[schedule]
fetch_interval = 5        # minutes
cleanup_interval = 24     # hours
vacuum_interval = 168     # hours (weekly)
```

#### Option 2: Use Single Run Mode

To run once and exit:

```bash
docker compose run -e RUN_MODE=once noaa-alerts
```

This runs fetch.py a single time, useful for testing or if you want to handle scheduling externally.

### Docker Commands

```bash
# View logs
docker compose logs -f

# Stop all containers
docker compose down

# Rebuild after changes
docker compose build

# Run with purge flag
docker compose run --rm noaa-alerts python fetch.py --purge

# Debug mode
docker compose run --rm noaa-alerts python fetch.py --debug
```

## Manual Installation

For systems without Docker or if you prefer a traditional Python installation.

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git
- Build tools (gcc, make) for some dependencies

#### Installing Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

**macOS:**
```bash
brew install python@3.12 git
```

**Windows:**
- Install Python 3.12+ from [python.org](https://www.python.org/downloads/)
- Install Git from [git-scm.com](https://git-scm.com/)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/k9barry/noaa-alerts-pushover.git
   cd noaa-alerts-pushover
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create your configuration file:**
   ```bash
   cp config.txt.example config.txt
   ```

5. **Edit `config.txt` with your credentials:**
   ```ini
   [pushover]
   token = YOUR_PUSHOVER_TOKEN
   user = YOUR_PUSHOVER_USER_KEY
   ```

6. **Edit `counties.json` to monitor your desired counties.**

7. **Initialize the database:**
   ```bash
   python models.py
   ```

8. **Validate your setup:**
   ```bash
   python test_setup.py
   ```

9. **Test the application:**
   ```bash
   python fetch.py --debug
   ```

### Running on a Schedule (Manual Installation)

#### Option 1: Use the Built-in Scheduler (Recommended)

The easiest way to run continuously is to use the built-in Python scheduler:

```bash
# Run the scheduler in the foreground
python scheduler.py

# Or run in the background (Linux/Mac)
nohup python scheduler.py > scheduler.log 2>&1 &

# Or use screen/tmux to keep it running
screen -dmS noaa-alerts python scheduler.py
```

Configure scheduling intervals in your `config.txt`:

```ini
[schedule]
fetch_interval = 5        # minutes
cleanup_interval = 24     # hours
vacuum_interval = 168     # hours
```

#### Option 2: Use systemd (Linux)

Create a service that runs the scheduler:

1. Create `/etc/systemd/system/noaa-alerts.service`:
   ```ini
   [Unit]
   Description=NOAA Alerts Pushover Scheduler
   After=network.target

   [Service]
   Type=simple
   User=youruser
   WorkingDirectory=/path/to/noaa-alerts-pushover
   ExecStart=/path/to/venv/bin/python scheduler.py
   Restart=always
   RestartSec=10
   StandardOutput=journal
   StandardError=journal

   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable noaa-alerts.service
   sudo systemctl start noaa-alerts.service
   ```

#### Option 3: Single-Run Mode

If you prefer to run fetch.py once per invocation, you can call it directly and handle scheduling externally. Note that you'll also need to separately schedule cleanup.py and vacuum.py for maintenance.

## Scheduling Options

### Recommended Check Intervals

- **Standard monitoring:** Every 5-10 minutes
- **Storm season:** Every 2-5 minutes
- **Low-risk areas:** Every 15-30 minutes

### Performance Considerations

- Each check makes one NOAA API call
- Processing time is typically < 5 seconds
- Database size grows slowly (old alerts are cleaned up)
- Network bandwidth usage is minimal

## Configuration Details

### Configuration File Structure

The `config.txt` file uses INI format with three main sections:

#### [pushover] Section

**Required** - Your Pushover API credentials:
```ini
[pushover]
token = YOUR_PUSHOVER_TOKEN
user = YOUR_PUSHOVER_USER_KEY
```

Get your credentials at: https://pushover.net

#### [events] Section

**Optional** - Filter out alert types you don't want to receive:
```ini
[events]
ignored = Red Flag Warning,Heat Advisory,Wind Advisory
```

Common events you might want to ignore:
- Red Flag Warning
- Heat Advisory
- Wind Advisory
- Small Craft Advisory
- Beach Hazards Statement
- Special Weather Statement

#### [schedule] Section

**Optional** - Configure how often tasks run (added in recent updates):
```ini
[schedule]
# How often to check for new alerts (in minutes)
fetch_interval = 5

# How often to remove expired HTML files (in hours)
cleanup_interval = 24

# How often to run database maintenance (in hours, default is weekly)
vacuum_interval = 168
```

**Default values** if not specified:
- `fetch_interval`: 5 minutes (checks for new alerts)
- `cleanup_interval`: 24 hours (daily cleanup of expired HTML files)
- `vacuum_interval`: 168 hours (weekly database optimization)

**Customization examples:**
- Check alerts every 2 minutes during storm season: `fetch_interval = 2`
- Run cleanup twice daily: `cleanup_interval = 12`
- Run database maintenance monthly: `vacuum_interval = 720`

### County Codes

County codes consist of:
- **FIPS:** Federal Information Processing Standard code (e.g., "012057")
- **UGC:** Universal Geographic Code (e.g., "FL057")
- **Name:** County name
- **State:** Two-letter state code

Find codes at: http://www.nws.noaa.gov/emwin/winugc.htm

Example `counties.json`:
```json
[
    {
        "fips": "012057",
        "name": "Hillsborough County",
        "state": "FL",
        "ugc": "FL057"
    },
    {
        "fips": "012103",
        "name": "Pinellas County",
        "state": "FL",
        "ugc": "FL103"
    }
]
```

## Command-Line Options

### fetch.py Options

```bash
# Standard run - check for alerts and send notifications
python3 fetch.py

# Test without sending push notifications
python3 fetch.py --nopush

# Clear all saved alerts from database
python3 fetch.py --purge

# Enable debug logging
python3 fetch.py --debug

# Combine options
python3 fetch.py --nopush --debug
```

### Docker Commands

```bash
# View logs
docker compose logs -f

# Stop all containers
docker compose down

# Rebuild after changes
docker compose build

# Run once and exit
docker compose run -e RUN_MODE=once noaa-alerts

# Run with purge flag
docker compose run --rm noaa-alerts python fetch.py --purge

# Debug mode
docker compose run --rm noaa-alerts python fetch.py --debug

# Rebuild from scratch
docker compose build --no-cache
```

### Quick Reference Table

| Task | Command |
|------|---------|
| Test setup | `python3 test_setup.py` |
| Auto-fix setup | `python3 test_setup.py --fix` |
| Single check | `python3 fetch.py` |
| Debug mode | `python3 fetch.py --debug` |
| No push | `python3 fetch.py --nopush` |
| Clear alerts | `python3 fetch.py --purge` |
| Run scheduler | `python3 scheduler.py` |
| Docker continuous | `docker compose up -d` |
| Docker once | `docker compose run -e RUN_MODE=once noaa-alerts` |
| View logs | `tail -f log.txt` |
| Docker logs | `docker compose logs -f` |

## Troubleshooting

### Common Issues

#### "Error! Output directory does not exist"
The output directory is now created automatically. Update to the latest version.

#### SSL Certificate Errors
Ensure your system has up-to-date SSL certificates:
```bash
pip install --upgrade certifi
```

#### Database Locked Errors
If using multiple instances, ensure only one is running at a time.

#### No Alerts Received
1. Check that your counties.json is formatted correctly
2. Verify your Pushover credentials in config.txt
3. Run with `--debug` flag to see detailed logs
4. Check log.txt for errors
5. Verify NOAA API is accessible: `curl https://api.weather.gov/alerts`

#### API Errors or HTML Responses
The application now automatically detects and handles cases where NOAA's API returns HTML error pages instead of JSON. If you see these errors in logs:
- The application will continue running and retry on the next scheduled check
- These are typically temporary NOAA API maintenance issues
- Check `log.txt` for detailed error messages with response previews

#### Permission Denied Errors (Linux)

**For Docker:**

The container runs as user `noaa` (UID 1000) for improved security. This follows Docker and Kubernetes security best practices by:
- Running as a non-root user
- Reducing attack surface
- Limiting potential damage from container escape vulnerabilities

If you see permission errors:
```bash
# Option 1: Set host directory owner to UID 1000
sudo chown -R 1000:1000 ./output ./data

# Option 2: Use permissive permissions
chmod 777 ./output ./data

# Option 3: If your host user is already UID 1000 (check with `id -u`), no changes are needed
```

**Verifying non-root execution:**
```bash
# Check the user inside the running container
docker compose exec noaa-alerts whoami
# Should output: noaa

# Check the UID
docker compose exec noaa-alerts id
# Should output: uid=1000(noaa) gid=1000(noaa) groups=1000(noaa)
```

**Additional Docker Security Measures:**

For enhanced security, consider these additional measures:
```bash
# Read-only root filesystem with writable volumes
docker run --read-only \
  --security-opt=no-new-privileges \
  --cap-drop=ALL \
  -v ./output:/app/output \
  -v ./data:/app/data \
  noaa-alerts
```

**Kubernetes deployment:**

When deploying to Kubernetes, set the security context:
```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
  - name: noaa-alerts
    image: your-image:latest
```

**For manual installation:**
Ensure the application has write permissions:
```bash
chmod +x fetch.py
chmod 644 config.txt
```

### Debugging

Enable debug mode:
```bash
python fetch.py --debug
```

Check the log file:
```bash
tail -f log.txt
```

For Docker:
```bash
docker compose logs -f
```

### Getting Help

If you encounter issues:
1. Check the log file (`log.txt`)
2. Run with `--debug` flag
3. Review [SECURITY.md](SECURITY.md) for security-related issues
4. Open an issue on GitHub with:
   - Your error message
   - Operating system and Python version
   - Steps to reproduce the issue

## Maintenance

### Database Maintenance

When using the scheduler (default), database maintenance and HTML cleanup run automatically on the configured schedule. If you need to run maintenance manually:

**Clear all alerts:**
```bash
python fetch.py --purge
```

**Vacuum database (reduce size):**
```bash
python vacuum.py
```

**Cleanup expired HTML files:**
```bash
python cleanup.py
```

**Note:** The scheduler automatically runs cleanup.py and vacuum.py on the intervals specified in config.txt, so manual execution is typically not needed.

### Updating

**Docker:**
```bash
git pull
docker compose build
docker compose up -d
```

**Manual:**
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## Security Notes

- Keep your `config.txt` private and never commit it to version control
- The `.gitignore` file is configured to exclude sensitive files
- Consider using environment variables for credentials in production
- See [SECURITY.md](SECURITY.md) for more information
