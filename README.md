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

## Quick Start with Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/k9barry/noaa-alerts-pushover.git
   cd noaa-alerts-pushover
   ```

2. **Configure your settings:**
   ```bash
   cp config.txt.example config.txt
   # Edit config.txt with your Pushover credentials
   ```

3. **Edit counties.json** to add the counties you want to monitor. Find county codes on the [NOAA website](http://www.nws.noaa.gov/emwin/winugc.htm).

4. **Validate your setup (optional but recommended):**
   ```bash
   python3 test_setup.py
   ```

5. **Run with Docker Compose:**
   ```bash
   docker compose up -d
   ```

The service will run continuously, checking for alerts every 5 minutes by default. For configuration options, see the [Installation Guide](INSTALL.md).

## Manual Installation (Python)

If you prefer to run without Docker:

1. **Install Python 3.12+ and dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your settings:**
   ```bash
   cp config.txt.example config.txt
   # Edit config.txt with your Pushover credentials
   ```

3. **Edit counties.json** to monitor your desired counties.

4. **Initialize the database:**
   ```bash
   python models.py
   ```

5. **Validate your setup:**
   ```bash
   python test_setup.py
   ```

6. **Run the application:**
   ```bash
   python fetch.py
   ```

## Configuration

### Pushover Credentials

Create a `config.txt` file with your Pushover API credentials:

```ini
[pushover]
token = YOUR_PUSHOVER_TOKEN
user = YOUR_PUSHOVER_USER_KEY
```

*Get your credentials at the [Pushover website](http://www.pushover.net).*

### Counties to Monitor

Edit the `counties.json` file to add counties you wish to monitor:

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

Find county codes at the [NOAA website](http://www.nws.noaa.gov/emwin/winugc.htm).

### Filtering Alerts (Optional)

To ignore specific alert types, add them to your `config.txt`:

```ini
[events]
ignored = Red Flag Warning,Heat Advisory
```

## Usage

### Command-Line Options

- **Standard run:** `python fetch.py`
- **Clear all alerts:** `python fetch.py --purge`
- **Disable push notifications:** `python fetch.py --nopush`
- **Debug mode:** `python fetch.py --debug`

### Running on a Schedule

The Docker Compose configuration uses Python's schedule library to run checks automatically. By default, it checks for alerts every 5 minutes, runs cleanup daily, and performs database maintenance weekly. You can customize these intervals in `config.txt` under the `[schedule]` section. See [INSTALL.md](INSTALL.md) for details.

## Customization

### Alert Template Customization

The HTML detail pages for alerts can be customized by editing `templates/detail.html`. This Jinja2 template controls how alerts are displayed.

For comprehensive customization instructions, see [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md), which includes:
- Available template variables
- 7+ practical customization examples
- Mobile-friendly layouts
- Conditional content display
- Styling tips and best practices

### Setup Validation Tool

The `test_setup.py` script helps validate and fix common setup issues:

```bash
# Run validation checks
python test_setup.py

# Auto-fix issues (create config.txt, initialize database)
python test_setup.py --fix

# Interactive mode (prompt before each fix)
python test_setup.py --interactive
```

## Documentation

- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [Installation Guide](INSTALL.md) - Detailed setup instructions
- [Template Customization Guide](TEMPLATE_GUIDE.md) - Customize alert HTML pages
- [How It Works](CODE_EXPLANATION.md) - Technical overview of the codebase
- [Security](SECURITY.md) - Security best practices and considerations
- [Changelog](CHANGELOG.md) - Version history and updates

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

## Notes

- The application saves alerts to a local SQLite database to prevent duplicate notifications
- Expired alerts are automatically cleaned up
- HTML detail pages are generated for each alert in the `output/` directory

## Contributing

Feedback and pull requests are welcome! Please read our [Security Policy](SECURITY.md) before contributing.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please open an issue on GitHub.
