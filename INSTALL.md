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

Add your [Pushover](https://pushover.net) credentials and User-Agent information:
```ini
[pushover]
token = your_app_token_here
user = your_user_key_here

[user_agent]
# Required by NWS API - provide your contact information
app_name = NOAA-Alerts-Pushover
version = 3.0
contact = your_email@example.com

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

**Important**: Replace `your_email@example.com` in the `[user_agent]` section with your actual email or website URL. The NWS API requires this to contact you about API changes or issues.

#### 3. Select Counties

Edit `counties.json` to add the counties you want to monitor.

**Finding County Codes:**

- **FIPS codes**: Visit https://www.weather.gov/pimar/FIPSCodes
- **UGC codes**: 
  1. Go to https://www.weather.gov/
  2. Find your state and click "County List" for county codes or "Zone List" for forecast zone codes
  3. County codes follow pattern `SSC###` (e.g., `INC095` for Madison County, Indiana)
  4. Zone codes follow pattern `SSZ###` (e.g., `INZ050` for a forecast zone)

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

Continuous monitoring (runs scheduler):
```bash
docker compose up -d
```

This runs the scheduler which checks for alerts every 5 minutes by default.

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

### Installation Methods

#### Option 1: Using Pre-built Docker Hub Image (Easiest)

The application is available as a pre-built image on Docker Hub:

```bash
# Pull the latest version
docker pull k9barry/noaa-alerts-pushover:latest

# Or pull a specific version
docker pull k9barry/noaa-alerts-pushover:v2.2.0
```

Then follow steps 2-7 below to set up your configuration and run the container.

#### Option 2: Build from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/k9barry/noaa-alerts-pushover.git
   cd noaa-alerts-pushover
   ```

### Installation Steps

2. **Create your configuration files (optional):**
   
   The container will automatically create `config.txt` and `counties.json` from example files if they don't exist. However, you can create them manually first:
   
   ```bash
   cp config.txt.example config.txt
   cp counties.json.example counties.json
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

7. **Run the container:**
   
   **If using Docker Hub image:**
   ```bash
   # Edit docker-compose.yml to use the pre-built image:
   # Replace "build: ." with "image: k9barry/noaa-alerts-pushover:latest"
   docker compose up -d
   ```
   
   **If building from source:**
   ```bash
   docker compose build
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

See the [Command-Line Options](#command-line-options) section below for all Docker commands and options.

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

The `config.txt` file uses INI format with the following sections:

- `[pushover]` - **Required** - Pushover API credentials and options
- `[user_agent]` - **Required** - User-Agent header for NOAA API compliance
- `[noaa]` - **Optional** - NOAA API endpoint URL (uses default if not specified)
- `[events]` - **Optional** - Event types to ignore/filter out
- `[schedule]` - **Optional** - Task scheduling intervals
- `[template]` - **Optional** - HTML template customization options

#### [pushover] Section

**Required** - Your Pushover API credentials:
```ini
[pushover]
token = YOUR_PUSHOVER_TOKEN
user = YOUR_PUSHOVER_USER_KEY

# Optional: Base URL for hosted HTML alert files
# If set, Pushover notifications will link to your hosted HTML files
# If not set, notifications will link to NOAA's official alert page
# base_url = https://example.com/alerts
```

Get your credentials at: https://pushover.net

**Base URL Configuration:**

The `base_url` option controls what URL is included in Pushover notifications:

- **Not set (default):** Notifications link to NOAA's official alert page
- **Set to your server:** Notifications link to your customized HTML files in the `output/` directory

Example: If you're hosting the HTML files on your own web server, set:
```ini
base_url = https://example.com/alerts
```

This generates notification URLs like: `https://example.com/alerts/abc123def.html`

You'll need to:
1. Set up a web server (Apache, Nginx, etc.)
2. Configure it to serve files from the `output/` directory
3. Ensure the server is accessible from the internet if you want to view alerts on mobile devices

**Docker Setup with Separate Web Server Container:**

If you're running NOAA Alerts Pushover in Docker and want to serve the HTML files with a separate web server container, you can use a shared volume. Here are complete examples:

##### Option 1: Using Nginx Container

Create a `docker-compose.yml` that includes both services:

```yaml
version: '3.8'

services:
  noaa-alerts:
    build: .
    container_name: noaa-alerts-pushover
    restart: unless-stopped
    volumes:
      - ./config.txt:/app/config.txt:ro
      - ./counties.json:/app/counties.json:ro
      - alert-output:/app/output      # Shared volume
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
      - TZ=UTC

  nginx-alerts:
    image: nginx:alpine
    container_name: nginx-alerts-server
    restart: unless-stopped
    ports:
      - "8080:80"  # Expose on port 8080
    volumes:
      - alert-output:/usr/share/nginx/html/alerts:ro  # Mount as read-only
      - ./nginx-alerts.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - noaa-alerts

volumes:
  alert-output:  # Shared named volume
```

Create `nginx-alerts.conf`:

```nginx
server {
    listen 80;
    server_name localhost;

    location /alerts {
        alias /usr/share/nginx/html/alerts;
        autoindex off;
        
        # Add cache headers for better performance
        expires 5m;
        add_header Cache-Control "public, must-revalidate";
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

Then set in your `config.txt`:
```ini
base_url = http://your-server-ip:8080/alerts
# Or with a domain: base_url = https://example.com/alerts
```

##### Option 2: Using Traefik (with automatic HTTPS)

For Traefik with automatic SSL certificates:

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik.yml:/traefik.yml:ro
      - ./acme.json:/acme.json
    networks:
      - web

  noaa-alerts:
    build: .
    container_name: noaa-alerts-pushover
    restart: unless-stopped
    volumes:
      - ./config.txt:/app/config.txt:ro
      - ./counties.json:/app/counties.json:ro
      - alert-output:/app/output
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
      - TZ=UTC
    networks:
      - web

  nginx-alerts:
    image: nginx:alpine
    container_name: nginx-alerts-server
    restart: unless-stopped
    volumes:
      - alert-output:/usr/share/nginx/html/alerts:ro
      - ./nginx-alerts.conf:/etc/nginx/conf.d/default.conf:ro
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.alerts.rule=Host(`alerts.example.com`)"
      - "traefik.http.routers.alerts.entrypoints=websecure"
      - "traefik.http.routers.alerts.tls.certresolver=letsencrypt"
      - "traefik.http.services.alerts.loadbalancer.server.port=80"
    depends_on:
      - noaa-alerts
      - traefik
    networks:
      - web

volumes:
  alert-output:

networks:
  web:
    external: true
```

Create `traefik.yml`:

```yaml
api:
  dashboard: true

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"

providers:
  docker:
    exposedByDefault: false

certificatesResolvers:
  letsencrypt:
    acme:
      email: your-email@example.com
      storage: /acme.json
      httpChallenge:
        entryPoint: web
```

Then set in your `config.txt`:
```ini
base_url = https://alerts.example.com/alerts
```

##### Option 3: Using Apache Container

```yaml
version: '3.8'

services:
  noaa-alerts:
    build: .
    container_name: noaa-alerts-pushover
    restart: unless-stopped
    volumes:
      - ./config.txt:/app/config.txt:ro
      - ./counties.json:/app/counties.json:ro
      - alert-output:/app/output
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
      - TZ=UTC

  apache-alerts:
    image: httpd:alpine
    container_name: apache-alerts-server
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - alert-output:/usr/local/apache2/htdocs/alerts:ro
      - ./apache-alerts.conf:/usr/local/apache2/conf/httpd.conf:ro
    depends_on:
      - noaa-alerts

volumes:
  alert-output:
```

Create `apache-alerts.conf`:

```apache
ServerRoot "/usr/local/apache2"
Listen 80

LoadModule mpm_event_module modules/mod_mpm_event.so
LoadModule authz_core_module modules/mod_authz_core.so
LoadModule dir_module modules/mod_dir.so
LoadModule mime_module modules/mod_mime.so
LoadModule log_config_module modules/mod_log_config.so
LoadModule alias_module modules/mod_alias.so
LoadModule unixd_module modules/mod_unixd.so

<IfModule unixd_module>
    User daemon
    Group daemon
</IfModule>

ServerAdmin webmaster@localhost
ServerName localhost

<Directory />
    AllowOverride none
    Require all denied
</Directory>

DocumentRoot "/usr/local/apache2/htdocs"

<Directory "/usr/local/apache2/htdocs/alerts">
    Options -Indexes +FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>

Alias /alerts "/usr/local/apache2/htdocs/alerts"

ErrorLog /proc/self/fd/2
TransferLog /proc/self/fd/1

TypesConfig conf/mime.types
AddType text/html .html
```

Then set in your `config.txt`:
```ini
base_url = http://your-server-ip:8080/alerts
```

**Starting the Multi-Container Setup:**

```bash
# Create the shared volume and network if needed
docker volume create alert-output  # Only if not using docker-compose volumes
docker network create web           # Only for Traefik setup

# For Traefik, create acme.json file for SSL certificates
touch acme.json && chmod 600 acme.json

# Start all services
docker compose up -d

# Verify both containers are running
docker compose ps

# Check logs
docker compose logs -f noaa-alerts
docker compose logs -f nginx-alerts  # or apache-alerts or traefik

# Test the web server
curl http://localhost:8080/alerts/
```

**Important Notes:**

1. **Volume Permissions**: The NOAA alerts container runs as user `noaa` (UID 1000). If you encounter permission issues, ensure the shared volume has appropriate permissions.

2. **Security**: 
   - The web server mounts the volume as read-only (`:ro`)
   - Directory listings are disabled (`autoindex off` or `Options -Indexes`)
   - Consider adding basic authentication if exposing publicly

3. **Port Conflicts**: Change the port mapping (`8080:80`) if port 8080 is already in use on your host.

4. **DNS/Domain**: For production with a domain name, update DNS records to point to your server's IP address.

5. **Firewall**: Ensure your firewall allows traffic on the exposed ports (80, 443, or 8080).

**Test Message Configuration:**

The `test_message` option enables receiving NOAA test messages and alerts. This is useful for:
- Testing your setup without waiting for real alerts
- Verifying notifications are working correctly
- Ensuring your configuration is correct

```ini
[pushover]
token = YOUR_PUSHOVER_TOKEN
user = YOUR_PUSHOVER_USER_KEY

# Enable test messages from NOAA (useful for testing)
test_message = false  # Set to true to enable, false to disable (default)
```

**When enabled (`test_message = true`):**
- Automatically monitors the MDC031 (Maryland Test Zone) for NOAA test messages
- Test alerts are sent to this zone by NOAA for testing purposes
- You'll receive notifications for any test alerts issued by NOAA

**When disabled (`test_message = false`):**
- Only monitors the counties you've specified in `counties.json`
- Recommended for production use to avoid test notifications

**Note:** You don't need to modify `counties.json` - the test zone is added automatically when enabled.

#### [user_agent] Section

**Required** - User-Agent header for NOAA API requests:

The National Weather Service (NWS) API requires a User-Agent header that identifies your application and provides contact information. This allows NWS to:
- Understand API usage patterns
- Contact you about API changes, outages, or potential issues
- Troubleshoot problems if needed

```ini
[user_agent]
# Required by NWS API - provide your contact information
app_name = NOAA-Alerts-Pushover
version = 3.0
contact = your_email@example.com  # or https://www.example.com/contact
```

**Configuration Options:**
- `app_name`: Your application name (default: `NOAA-Alerts-Pushover`)
- `version`: Application version (default: `3.0`)
- `contact`: Email address or website URL where NWS can reach you

**Important:** Replace `your_email@example.com` with your actual email address or a URL where you can be contacted.

**Examples of valid User-Agent formats:**
- `NOAA-Alerts-Pushover/3.0 (john.doe@example.com)`
- `MyWeatherApp/1.0 (https://www.example.com/contact)`
- `HomeWeatherMonitor/2.1 (homeowner@gmail.com)`

**If not configured:** The application will use a default User-Agent with the GitHub repository URL, but it's strongly recommended to provide your own contact information for NWS compliance.

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

**How to Find Your County Codes:**

**For FIPS codes:**
- Visit https://www.weather.gov/pimar/FIPSCodes

**For UGC codes:**
1. Access the NWS website at https://www.weather.gov/
2. Navigate to the correct list:
   - For county codes: Find your state and click the "County List" link
   - For zone codes: Find your state and click the "Zone List" link
3. Find your code:
   - UGC County codes follow the pattern `SSC###`, where:
     - `SS` is the two-letter state abbreviation (e.g., IN for Indiana)
     - `C` indicates it is a county code
     - `###` is the three-digit FIPS code for the county
   - UGC Zone codes follow the pattern `SSZ###`, where:
     - `SS` is the two-letter state abbreviation
     - `Z` indicates it is a forecast zone code
     - `###` is the three-digit forecast zone number

**Example: Finding codes for Pendleton, Indiana**
- Determine your county: Pendleton is in Madison County, Indiana
- Go to the NWS County Coverage page for Indiana: https://www.weather.gov/nwr/county_coverage?State=IN
- Find Madison County in the list
- The full UGC County code would be `INC095`

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
| Docker run | `docker compose up -d` |
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
