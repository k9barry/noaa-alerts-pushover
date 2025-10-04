# Quick Start Guide

Get up and running with NOAA Alerts Pushover in 5 minutes!

## Prerequisites

Choose your preferred method:

### Docker (Easiest)
- Docker 20.10+
- Docker Compose 2.0+

### Python (Manual)
- Python 3.12+
- pip package manager

## Setup Steps

### 1. Get the Code

```bash
git clone https://github.com/k9barry/noaa-alerts-pushover.git
cd noaa-alerts-pushover
```

### 2. Configure

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
```

### 3. Select Counties

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

### 4. Validate Setup (Optional)

```bash
python3 test_setup.py
```

This checks that everything is configured correctly.

### 5. Run

#### Docker (Recommended)

**Continuous monitoring (default, every 5 minutes):**
```bash
docker compose up -d
```

**Single check:**
```bash
docker compose run -e RUN_MODE=once noaa-alerts
```

**Custom interval:**
```bash
# Check every 2 minutes (120 seconds)
docker compose run -e RUN_MODE=loop -e CHECK_INTERVAL=120 noaa-alerts
```

#### Python (Manual)

**Initialize database:**
```bash
python3 models.py
```

**Single check:**
```bash
python3 fetch.py
```

**Test without sending notifications:**
```bash
python3 fetch.py --nopush
```

**Debug mode:**
```bash
python3 fetch.py --debug
```

## Usage Modes

### Run Once
Check for alerts once and exit:
```bash
docker compose run -e RUN_MODE=once noaa-alerts
# or
python3 fetch.py
```

### Continuous Monitoring
Check every N seconds continuously (default):
```bash
docker compose up -d
# or setup a cron job
```

### Scheduled (Cron)
Run on a schedule via cron:
```bash
# Every 5 minutes
*/5 * * * * cd /path/to/noaa-alerts-pushover && python3 fetch.py
```

## Command-Line Options

```bash
# Test without sending push notifications
python3 fetch.py --nopush

# Clear all saved alerts from database
python3 fetch.py --purge

# Enable debug logging
python3 fetch.py --debug

# Combine options
python3 fetch.py --nopush --debug
```

## Docker Tips

### View Logs
```bash
docker compose logs -f
```

### Stop Container
```bash
docker compose down
```

### Run One-Time Check
```bash
docker compose run --rm noaa-alerts
```

### Debug Container
```bash
docker compose run --rm noaa-alerts --debug
```

## Troubleshooting

### No Alerts Received?
1. Check your Pushover credentials in `config.txt`
2. Verify counties in `counties.json` are correct
3. Run with `--debug` flag to see detailed logs
4. Check `log.txt` for errors

### Permission Errors?

**Docker:**
```bash
# Container runs as UID 1000, ensure directories are writable
sudo chown -R 1000:1000 ./output ./data
```

**Manual installation:**
```bash
chmod 600 config.txt
chmod 755 *.py
```

### Database Issues?
```bash
# Recreate database
python3 models.py

# Or purge all alerts
python3 fetch.py --purge
```

### Docker Build Errors?
```bash
# Rebuild from scratch
docker compose build --no-cache
```

## What's Next?

- **Automation**: Set up continuous monitoring with cron or Docker loop mode
- **Customization**: Add ignored events to `config.txt`
- **Monitoring**: Check `log.txt` regularly for any issues

## Documentation

- [README.md](README.md) - Project overview
- [INSTALL.md](INSTALL.md) - Detailed installation guide
- [SECURITY.md](SECURITY.md) - Security best practices
- [CODE_EXPLANATION.md](CODE_EXPLANATION.md) - Technical details
- [CHANGELOG.md](CHANGELOG.md) - Version history

## Getting Help

1. Run the validation script: `python3 test_setup.py`
2. Check logs: `tail -f log.txt`
3. Enable debug mode: `python3 fetch.py --debug`
4. Review [INSTALL.md](INSTALL.md) for detailed troubleshooting

## Quick Reference

| Task | Command |
|------|---------|
| Test setup | `python3 test_setup.py` |
| Single check | `python3 fetch.py` |
| Debug mode | `python3 fetch.py --debug` |
| No push | `python3 fetch.py --nopush` |
| Clear alerts | `python3 fetch.py --purge` |
| Docker loop | `docker compose up -d` |
| Docker once | `docker compose run -e RUN_MODE=once noaa-alerts` |
| View logs | `tail -f log.txt` |
| Docker logs | `docker compose logs -f` |

---

**Ready to go?** Your NOAA weather alerts will start arriving on your Pushover-enabled devices!
