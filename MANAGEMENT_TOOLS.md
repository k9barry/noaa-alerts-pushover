# Management Tools Guide

This guide covers the management tools included with the Docker Compose setup for monitoring and maintaining your NOAA Alerts Pushover installation.

## Overview

When running NOAA Alerts Pushover with Docker Compose, two additional services are automatically included:

1. **Dozzle** - Real-time log viewer
2. **SQLitebrowser** - Database management tool

Both services require no configuration and start automatically with `docker compose up -d`.

## Dozzle - Log Viewer

### Description
Dozzle is a lightweight, real-time log viewer for Docker containers. It provides a clean web interface to view, search, and filter container logs.

### Access
- **URL**: http://localhost:8080
- **Container Name**: `noaa-alerts-dozzle`
- **Image**: `amir20/dozzle:latest`

### Features
- ✅ Real-time log streaming
- ✅ Search and filter logs
- ✅ Multi-container support
- ✅ Auto-refresh
- ✅ Dark/light theme
- ✅ Download logs
- ✅ No authentication required (localhost only)

### Usage

#### Viewing Logs
1. Open http://localhost:8080 in your browser
2. You'll see a list of running containers
3. Click on `noaa-alerts-pushover` to view its logs
4. Logs update in real-time as new entries are written

#### Searching Logs
- Use the search box at the top to filter log messages
- Search is case-insensitive
- Results highlight matching terms

#### Downloading Logs
- Click the download icon to save logs to a file
- Useful for troubleshooting or sharing with support

#### Configuration
The service is pre-configured with optimal settings:
- `DOZZLE_LEVEL=info` - Show info and above
- `DOZZLE_TAILSIZE=300` - Show last 300 lines
- `DOZZLE_FILTER=name=noaa-alerts-pushover` - Filter to main app

### Advanced Configuration

To customize Dozzle settings, edit the docker-compose.yml file:

```yaml
dozzle:
  image: amir20/dozzle:latest
  environment:
    - DOZZLE_LEVEL=debug  # Change log level
    - DOZZLE_TAILSIZE=500  # Show more lines
    # Add authentication (optional)
    - DOZZLE_USERNAME=admin
    - DOZZLE_PASSWORD=secure_password
```

For more options, see: https://dozzle.dev/guide/

### Troubleshooting Dozzle

#### Can't Access Port 8080
If port 8080 is already in use, change it in docker-compose.yml:
```yaml
ports:
  - "8888:8080"  # Access on port 8888 instead
```

#### Dozzle Shows No Containers
Ensure the Docker socket is mounted:
```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock:ro
```

#### Permission Denied
On some systems, you may need to add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```

## SQLitebrowser - Database Viewer

### Description
SQLitebrowser provides a web-based interface to view, query, and manage the SQLite database that stores alert history.

### Access
- **URL**: http://localhost:8081
- **Container Name**: `noaa-alerts-sqlitebrowser`
- **Image**: `lscr.io/linuxserver/sqlitebrowser:latest`

### Features
- ✅ Browse database tables
- ✅ View alert history
- ✅ Execute SQL queries
- ✅ Export data (CSV, JSON)
- ✅ View database schema
- ✅ Statistics and indexes
- ✅ No authentication required (localhost only)

### Usage

#### Opening the Database
1. Open http://localhost:8081 in your browser
2. Click "Open Database"
3. Navigate to `/data/alerts.db`
4. Click "Open"

#### Browsing Data
1. Select the "Browse Data" tab
2. Choose the "alert" table from the dropdown
3. View all stored alerts with pagination
4. Sort by clicking column headers

#### Running Queries
1. Select the "Execute SQL" tab
2. Enter your SQL query, for example:
   ```sql
   SELECT * FROM alert WHERE event = 'Tornado Warning';
   ```
3. Click "Execute" to run the query
4. Results appear in the table below

#### Viewing Schema
1. Select the "Database Structure" tab
2. View all tables, columns, and data types
3. See indexes and constraints

#### Exporting Data
1. Browse to the data you want to export
2. Click "Export" button
3. Choose format (CSV, JSON, SQL)
4. Save the file

### Common Queries

#### Recent Alerts (Last 7 Days)
```sql
SELECT title, event, expires, created 
FROM alert 
WHERE created >= datetime('now', '-7 days')
ORDER BY created DESC;
```

#### Alerts by Event Type
```sql
SELECT event, COUNT(*) as count 
FROM alert 
GROUP BY event 
ORDER BY count DESC;
```

#### Expired Alerts
```sql
SELECT * FROM alert 
WHERE expires_utc_ts < strftime('%s', 'now');
```

#### Alerts for Specific County (FIPS Code)
```sql
SELECT * FROM alert 
WHERE fips_codes LIKE '%012057%'
ORDER BY created DESC;
```

#### Database Statistics
```sql
SELECT 
  COUNT(*) as total_alerts,
  COUNT(DISTINCT event) as unique_event_types,
  MIN(created) as oldest_alert,
  MAX(created) as newest_alert
FROM alert;
```

### Database Schema

The `alert` table contains the following columns:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| alert_id | VARCHAR | Unique hash of NOAA alert ID |
| title | VARCHAR | Alert title/headline |
| event | VARCHAR | Event type (e.g., "Tornado Warning") |
| details | VARCHAR | Optional sub-event keywords |
| expires | DATETIME | Expiration date/time |
| expires_utc_ts | DOUBLE | Unix timestamp of expiration |
| url | VARCHAR | Public alert URL |
| api_url | VARCHAR | NOAA API detail URL |
| fips_codes | TEXT | Comma-separated FIPS codes |
| ugc_codes | TEXT | Comma-separated UGC codes |
| created | DATETIME | When alert was inserted |

### Advanced Configuration

To customize SQLitebrowser settings, edit docker-compose.yml:

```yaml
sqlitebrowser:
  image: lscr.io/linuxserver/sqlitebrowser:latest
  ports:
    - "8888:3000"  # Change port
  environment:
    - PUID=1000    # User ID (should match host)
    - PGID=1000    # Group ID (should match host)
    - TZ=America/New_York  # Change timezone
```

### Troubleshooting SQLitebrowser

#### Can't Access Port 8081
If port 8081 is already in use, change it in docker-compose.yml:
```yaml
ports:
  - "8082:3000"  # Access on port 8082 instead
```

#### Database Not Found
Ensure the data volume is correctly mounted:
```yaml
volumes:
  - ./data:/data  # Local ./data maps to /data in container
```

#### Permission Denied
Ensure the data directory is writable:
```bash
chmod 777 ./data
# Or match container UID
sudo chown -R 1000:1000 ./data
```

#### Database Locked
If you see "database is locked" errors:
1. Ensure only one SQLitebrowser instance is open
2. Close any other connections to the database
3. The main application uses WAL mode, which should prevent most locks

## Security Considerations

### Local Development vs. Production

The default configuration is suitable for **local development only**. Both services:
- ❌ Have no authentication
- ❌ Are accessible from localhost only
- ❌ Should not be exposed to the internet

### Securing for Production

If you need to access these tools remotely:

#### Option 1: SSH Tunnel (Recommended)
```bash
# From your local machine
ssh -L 8080:localhost:8080 -L 8081:localhost:8081 user@server
```

Then access http://localhost:8080 and http://localhost:8081 on your local machine.

#### Option 2: Reverse Proxy with Authentication

Use nginx or Traefik with basic auth:

```nginx
# nginx example
location /logs/ {
    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://localhost:8080/;
}
```

#### Option 3: VPN Access
Place the server behind a VPN and access through the VPN connection.

#### Option 4: Firewall Rules
Restrict access to specific IP addresses:
```bash
# Allow only from specific IP
sudo ufw allow from 203.0.113.0/24 to any port 8080
sudo ufw allow from 203.0.113.0/24 to any port 8081
```

#### Option 5: Disable External Access
Bind to localhost only (already default):
```yaml
ports:
  - "127.0.0.1:8080:8080"  # Only accessible from localhost
  - "127.0.0.1:8081:3000"
```

### Authentication Options

#### Adding Authentication to Dozzle
```yaml
dozzle:
  environment:
    - DOZZLE_USERNAME=admin
    - DOZZLE_PASSWORD=secure_password
```

#### Adding Authentication to SQLitebrowser
SQLitebrowser doesn't have built-in authentication. Use a reverse proxy with auth.

## Port Configuration

### Default Ports
- **Dozzle**: 8080
- **SQLitebrowser**: 8081
- **NOAA Alerts**: No exposed ports (scheduled task)

### Changing Ports

If the default ports conflict with other services:

```yaml
services:
  dozzle:
    ports:
      - "9080:8080"  # Access on port 9080
  
  sqlitebrowser:
    ports:
      - "9081:3000"  # Access on port 9081
```

## Disabling Management Tools

If you don't need the management tools:

### Option 1: Comment Out Services
Edit docker-compose.yml and comment out the services:
```yaml
#  dozzle:
#    image: amir20/dozzle:latest
#    ...
#
#  sqlitebrowser:
#    image: lscr.io/linuxserver/sqlitebrowser:latest
#    ...
```

### Option 2: Start Specific Service
Only start the main application:
```bash
docker compose up -d noaa-alerts
```

### Option 3: Create Minimal Compose File
Create `docker-compose.minimal.yml` with only the main service:
```yaml
services:
  noaa-alerts:
    build: .
    # ... rest of configuration
```

Then use:
```bash
docker compose -f docker-compose.minimal.yml up -d
```

## Performance Impact

### Resource Usage

Both management tools are lightweight:

**Dozzle**:
- Memory: ~20MB
- CPU: Minimal (only when viewing logs)
- Disk: None (no persistent storage)

**SQLitebrowser**:
- Memory: ~100MB
- CPU: Minimal (only when browsing)
- Disk: None (reads existing database)

**Total overhead**: ~120MB RAM, negligible CPU

### Network Usage
- Local access only (no external traffic)
- Minimal bandwidth (only UI assets)

## Alternatives

If you prefer not to use the included management tools:

### Log Viewing Alternatives
- `docker compose logs -f` (command line)
- Portainer (full Docker management)
- Lazydocker (terminal UI)
- Docker Desktop (native app)

### Database Viewing Alternatives
- `sqlite3` command-line tool
- DB Browser for SQLite (desktop app)
- DBeaver (universal database tool)
- DataGrip (JetBrains IDE)

### Accessing Without Docker
If not using Docker, access directly:
```bash
# View logs
tail -f log.txt

# View database
sqlite3 data/alerts.db
```

## Maintenance

### Updating Management Tools

To update to the latest versions:

```bash
# Pull latest images
docker compose pull dozzle sqlitebrowser

# Restart services
docker compose up -d
```

### Removing Management Tools

To completely remove:

```bash
# Stop containers
docker compose down

# Remove images (optional)
docker rmi amir20/dozzle:latest
docker rmi lscr.io/linuxserver/sqlitebrowser:latest
```

## FAQ

### Q: Do I need to configure anything?
**A**: No, both services work out of the box with Docker Compose.

### Q: Can I access these tools from another computer?
**A**: Not by default. Use SSH tunneling or a reverse proxy for remote access.

### Q: Do these tools slow down the main application?
**A**: No, they run independently and have minimal resource impact.

### Q: Can I use these with the Python installation (non-Docker)?
**A**: Dozzle and SQLitebrowser are Docker-specific. For Python installations, use command-line tools.

### Q: What if ports 8080 or 8081 are already in use?
**A**: Change the port mapping in docker-compose.yml (see Port Configuration section).

### Q: Are my logs and database data secure?
**A**: Yes, by default services are only accessible from localhost. See Security section for production use.

### Q: Can I use different tools instead?
**A**: Yes, see the Alternatives section for other options.

### Q: How do I backup my data?
**A**: The database is in `./data/alerts.db`. Copy this file to backup:
```bash
cp ./data/alerts.db ./backup/alerts-$(date +%Y%m%d).db
```

## Troubleshooting

### Service Won't Start
Check logs:
```bash
docker compose logs dozzle
docker compose logs sqlitebrowser
```

### Can't Access Web Interface
1. Verify service is running:
   ```bash
   docker compose ps
   ```
2. Check port isn't blocked by firewall
3. Try accessing from localhost: http://127.0.0.1:8080

### Browser Shows "Connection Refused"
Service may still be starting. Wait 30 seconds and refresh.

### Database Changes Not Showing
Click refresh in SQLitebrowser or re-run your query.

## Additional Resources

- **Dozzle Documentation**: https://dozzle.dev/
- **SQLitebrowser Project**: https://github.com/linuxserver/docker-sqlitebrowser
- **Docker Compose Docs**: https://docs.docker.com/compose/
- **SQLite Documentation**: https://www.sqlite.org/docs.html

## Support

For issues with:
- **Dozzle**: https://github.com/amir20/dozzle/issues
- **SQLitebrowser**: https://github.com/linuxserver/docker-sqlitebrowser/issues
- **NOAA Alerts Pushover**: Open an issue on the main repository

---

**Last Updated**: 2024
**Maintained By**: k9barry
**Repository**: https://github.com/k9barry/noaa-alerts-pushover
