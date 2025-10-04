# Installation Guide

This guide provides detailed instructions for installing and running NOAA Alerts Pushover.

## Table of Contents

- [Docker Installation (Recommended)](#docker-installation-recommended)
- [Manual Installation](#manual-installation)
- [Scheduling Options](#scheduling-options)
- [Troubleshooting](#troubleshooting)

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
   > See [DOCKER_NONROOT.md](DOCKER_NONROOT.md) for more details.

7. **Build and run the container:**
   ```bash
   docker compose up -d
   ```

8. **Access management tools:**
   
   The Docker Compose setup includes two additional services for monitoring and management:
   
   - **Dozzle (Log Viewer)**: http://localhost:8080
     - Real-time log viewing for all containers
     - Search and filter capabilities
     - Lightweight and fast
   
   - **SQLitebrowser (Database Viewer)**: http://localhost:8081
     - Browse the alerts database
     - View alert history
     - Run SQL queries
     - Export data
   
   Both services start automatically and require no configuration.

### Running on a Schedule

By default, the docker-compose.yml is configured for continuous monitoring using loop mode.

#### Option 1: Use Loop Mode (Default)

The default docker-compose.yml runs in loop mode with checks every 5 minutes:

```bash
docker compose up -d
```

To customize the interval, edit the `CHECK_INTERVAL` value in docker-compose.yml:

```yaml
services:
  noaa-alerts:
    environment:
      - RUN_MODE=loop
      - CHECK_INTERVAL=300  # Check every 5 minutes (300 seconds)
```

Or override it when running:
```bash
docker compose run -e CHECK_INTERVAL=120 noaa-alerts
```

#### Option 2: Use Single Run Mode

To run once and exit (for external schedulers):

```bash
docker compose run -e RUN_MODE=once noaa-alerts
```

#### Option 3: Use External Scheduler

Keep the default single-run behavior and schedule with:

**Cron (Linux/Mac):**
```bash
# Run every 5 minutes
*/5 * * * * cd /path/to/noaa-alerts-pushover && docker compose up
```

**Task Scheduler (Windows):**
Create a scheduled task that runs:
```
docker compose -f C:\path\to\noaa-alerts-pushover\docker-compose.yml up
```

### Docker Commands

```bash
# View logs (traditional method)
docker compose logs -f

# View logs with Dozzle (web interface)
# Open http://localhost:8080 in your browser

# Stop all containers
docker compose down

# Stop only the main application (keep management tools running)
docker compose stop noaa-alerts

# Rebuild after changes
docker compose build

# Run with purge flag
docker compose run --rm noaa-alerts python fetch.py --purge

# Debug mode
docker compose run --rm noaa-alerts python fetch.py --debug
```

### Management Tools Usage

#### Dozzle Log Viewer

Dozzle provides a web-based interface for viewing Docker container logs:

```bash
# Access at http://localhost:8080
```

Features:
- Real-time log streaming
- Search and filter logs
- Multi-container support
- Dark/light theme
- No authentication needed (localhost only)

#### SQLitebrowser Database Viewer

SQLitebrowser provides a web-based interface for the SQLite database:

```bash
# Access at http://localhost:8081
```

Features:
- Browse alert history
- View database schema and indexes
- Execute SQL queries
- Export data to CSV/JSON
- View statistics

The database file is located at `./data/alerts.db` and contains:
- Alert history
- FIPS and UGC codes
- Expiration timestamps
- URLs and metadata

**Security Note**: These management tools are intended for local development and monitoring. For production deployments, consider:
- Restricting access with firewall rules
- Using a reverse proxy with authentication
- Binding to localhost only (default configuration)

For detailed information about these tools, including advanced configuration, security considerations, and troubleshooting, see [MANAGEMENT_TOOLS.md](MANAGEMENT_TOOLS.md).

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

#### Linux/Mac - Using Cron

1. Edit your crontab:
   ```bash
   crontab -e
   ```

2. Add an entry to run every 5 minutes:
   ```
   */5 * * * * cd /path/to/noaa-alerts-pushover && /path/to/venv/bin/python fetch.py >> /path/to/cron.log 2>&1
   ```

#### Windows - Using Task Scheduler

1. Open Task Scheduler
2. Create a new Basic Task
3. Set the trigger to run every 5 minutes
4. Set the action to run:
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `fetch.py`
   - Start in: `C:\path\to\noaa-alerts-pushover`

#### Linux - Using systemd

1. Create `/etc/systemd/system/noaa-alerts.service`:
   ```ini
   [Unit]
   Description=NOAA Alerts Pushover
   After=network.target

   [Service]
   Type=oneshot
   User=youruser
   WorkingDirectory=/path/to/noaa-alerts-pushover
   ExecStart=/path/to/venv/bin/python fetch.py
   StandardOutput=journal
   StandardError=journal

   [Install]
   WantedBy=multi-user.target
   ```

2. Create `/etc/systemd/system/noaa-alerts.timer`:
   ```ini
   [Unit]
   Description=Run NOAA Alerts check every 5 minutes
   
   [Timer]
   OnBootSec=1min
   OnUnitActiveSec=5min
   
   [Install]
   WantedBy=timers.target
   ```

3. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable noaa-alerts.timer
   sudo systemctl start noaa-alerts.timer
   ```

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

### County Codes

County codes consist of:
- **FIPS:** Federal Information Processing Standard code (e.g., "012057")
- **UGC:** Universal Geographic Code (e.g., "FL057")
- **Name:** County name
- **State:** Two-letter state code

Find codes at: http://www.nws.noaa.gov/emwin/winugc.htm

### Ignored Events

Common events you might want to ignore:
- Red Flag Warning
- Heat Advisory
- Wind Advisory
- Small Craft Advisory
- Beach Hazards Statement

Add them comma-separated in `config.txt`:
```ini
[events]
ignored = Red Flag Warning,Heat Advisory,Wind Advisory
```

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
The container runs as user `noaa` (UID 1000). If you see permission errors:
```bash
# Ensure mounted directories are writable
sudo chown -R 1000:1000 ./output ./data
# Or use permissive permissions
chmod 777 ./output ./data
```

**For manual installation:**
Ensure the application has write permissions:
```bash
chmod +x fetch.py
chmod 644 config.txt
```

See [DOCKER_NONROOT.md](DOCKER_NONROOT.md) for more details on Docker permissions.

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

The database automatically cleans up old alerts, but you can manually maintain it:

**Clear all alerts:**
```bash
python fetch.py --purge
```

**Vacuum database (reduce size):**
```bash
python vacuum.py
```

### Cleanup HTML Files

Remove expired HTML alert files:
```bash
python cleanup.py
```

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
