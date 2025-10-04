# Changelog

## Version 2.1.0 - 2024

### 🔧 API Changes

#### Removed XML Dependencies
- **Removed lxml dependency**: No longer needed as NOAA API returns JSON
- **Updated to JSON parsing**: All API responses are now parsed as JSON/GeoJSON
- **Simplified code**: Removed XML namespace handling and etree parsing
- **Modern API usage**: Using current NOAA Weather API v1 format

The NOAA Weather API returns JSON/GeoJSON format, not XML. Updated code to parse JSON responses directly:
- Main alerts feed: GeoJSON FeatureCollection
- Individual alert details: GeoJSON Feature with properties
- All needed fields (headline, event, description, instruction, senderName, areaDesc) are available in JSON

**Breaking Change**: If you have lxml installed, you can remove it. The application no longer uses it.

### 📦 Dependency Changes

- **Removed**: lxml (XML parsing library)
- All other dependencies remain the same

## Version 2.0.0 - 2024

This is a major update that modernizes the entire codebase and adds Docker support.

### 🚀 Major Changes

#### Python 3 Migration
- **Updated to Python 3.12+**: All code migrated from Python 2 to Python 3
- **Modern syntax**: Updated all deprecated Python 2 syntax
- **Latest libraries**: All dependencies updated to latest stable versions

#### Docker Support
- **Full containerization**: Added Dockerfile and docker-compose.yml
- **Easy deployment**: Run the entire application with `docker compose up`
- **Volume management**: Proper data persistence with Docker volumes
- **Optimized builds**: Efficient Docker image with .dockerignore

#### Security Improvements
- **SSL verification**: Fixed insecure `verify=False` in API calls
- **Request timeouts**: Added 30-second timeouts to prevent hanging
- **Robust error handling**: HTML response detection, status code validation, and safe parsing
- **API response validation**: Prevents processing of unexpected content types
- **Security documentation**: Comprehensive SECURITY.md with best practices

#### Code Quality
- **Automatic directory creation**: No more manual output directory setup
- **WAL mode**: Database uses Write-Ahead Logging for better concurrency
- **Better structure**: Organized data into `data/` directory
- **Type safety**: Cleaner, more maintainable code

#### Documentation
- **README.md**: Completely rewritten with modern features
- **INSTALL.md**: Detailed installation guide for Docker and manual setup
- **SECURITY.md**: Security best practices and vulnerability reporting
- **CODE_EXPLANATION.md**: Technical deep dive into architecture and code flow
- **config.txt.example**: Template configuration file

### 📦 Dependency Updates

| Package | Old Version | New Version |
|---------|-------------|-------------|
| arrow | 0.5.4 | 1.3.0 |
| beautifulsoup4 | 4.4.1 | 4.12.3 |
| Jinja2 | 2.8 | 3.1.4 |
| lxml | 3.4.4 | 5.2.2 |
| peewee | 2.6.1 | 3.17.6 |
| requests | 2.7.0 | 2.32.3 |

**Removed obsolete dependencies:**
- backports.ssl-match-hostname
- certifi (now part of system)
- MarkupSafe (Jinja2 dependency)
- python-dateutil (arrow dependency)
- PyYAML (not used)
- six (Python 2/3 compatibility)
- wheel (build tool)

### 🔧 Breaking Changes

#### Configuration
- No breaking changes to `config.txt` format
- No changes to `counties.json` format
- Database schema unchanged (backward compatible)

#### File Locations
- Database moved from `alerts.db` to `data/alerts.db`
- Old database files will need to be moved manually if you want to preserve history

#### Python Version
- **Python 2 is no longer supported**
- Minimum Python version: 3.12
- Recommended: Python 3.12 or later

### 🐛 Bug Fixes

- Fixed output directory error - now creates automatically
- Fixed SSL warnings with proper urllib3 handling
- Fixed timestamp methods (`.timestamp` → `.timestamp()`)
- Fixed arrow replace method (`.replace` → `.shift` for date math)
- Fixed exception syntax (`Exception, e` → `Exception as e`)
- Fixed print statements (Python 2 → Python 3 syntax)

### 🛡️ Enhanced Error Handling

The application now includes robust error handling for NOAA API interactions:

#### API Response Validation
- **HTTP Status Code Checking**: Validates successful responses before processing
- **Content Type Detection**: Detects when APIs return HTML instead of expected JSON/XML
- **HTML Response Protection**: Prevents crashes when NOAA APIs return error pages

#### JSON Parsing Improvements
- **Try/Catch Blocks**: Graceful handling of malformed JSON responses
- **Error Logging**: Detailed error messages with response previews for debugging
- **Graceful Degradation**: Application continues running even if one alert fails to parse

#### XML Parsing Improvements
- **XMLSyntaxError Handling**: Catches and logs XML parsing failures
- **Safe Fallback**: Returns None for unparseable alerts instead of crashing
- **Debug Information**: Logs first 1000 characters of problematic responses

These improvements ensure the application remains stable even when NOAA's APIs are experiencing issues or maintenance.

### 🆕 New Features

#### Docker Compose
```yaml
services:
  noaa-alerts:
    build: .
    volumes:
      - ./config.txt:/app/config.txt:ro
      - ./counties.json:/app/counties.json:ro
      - ./output:/app/output
      - ./data:/app/data
```

#### Scheduled Running
Options for continuous monitoring:
1. Docker Compose with loop command
2. Cron job scheduling
3. systemd timers (Linux)
4. Task Scheduler (Windows)

See [INSTALL.md](INSTALL.md) for details.

### 📚 Documentation Structure

```
noaa-alerts-pushover/
├── README.md              # Overview and quick start
├── INSTALL.md             # Detailed installation guide
├── SECURITY.md            # Security best practices
├── CODE_EXPLANATION.md    # Technical architecture
├── CHANGELOG.md           # This file
└── config.txt.example     # Configuration template
```

### 🔒 Security Updates

1. **SSL/TLS**: Removed `verify=False`, now uses system certificates
2. **Timeouts**: All HTTP requests have 30-second timeouts
3. **Input validation**: Proper XML parsing with namespace validation
4. **Dependency security**: All libraries updated to latest secure versions
5. **Docker security**: Best practices for container security documented

### 🚦 Migration Guide

#### From Python 2 Version

1. **Update Python:**
   ```bash
   python3 --version  # Should be 3.12 or higher
   ```

2. **Update dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Move database (optional):**
   ```bash
   mkdir -p data
   mv alerts.db data/
   ```

4. **Test:**
   ```bash
   python3 fetch.py --nopush --debug
   ```

#### Using Docker (Recommended)

1. **Install Docker and Docker Compose**

2. **Pull and build:**
   ```bash
   git pull
   docker compose build
   ```

3. **Run:**
   ```bash
   docker compose up
   ```

### 🎯 Compatibility

- **Operating Systems**: Linux, macOS, Windows
- **Python**: 3.12+
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### 🤝 Contributing

This version includes comprehensive documentation making it easier to contribute:
- [CODE_EXPLANATION.md](CODE_EXPLANATION.md) for understanding the codebase
- [SECURITY.md](SECURITY.md) for security guidelines
- [INSTALL.md](INSTALL.md) for development setup

### 📝 Notes

- All changes are backward compatible in terms of functionality
- Configuration files use the same format
- Alert notification behavior unchanged
- Database schema compatible (just location changed)

### 🔮 Future Improvements

Potential enhancements for future versions:
- Web interface for configuration and history
- Additional notification channels (email, SMS, etc.)
- Alert severity filtering
- Geographic radius monitoring
- REST API for integration
- Automated testing suite

### 🙏 Credits

This modernization was performed to:
- Update to Python 3 (Python 2 EOL January 2020)
- Fix security vulnerabilities in old dependencies
- Add Docker support for easier deployment
- Improve documentation for better user experience
- Make the codebase more maintainable

---

For detailed installation and usage instructions, see [INSTALL.md](INSTALL.md).

For security information, see [SECURITY.md](SECURITY.md).

For technical details, see [CODE_EXPLANATION.md](CODE_EXPLANATION.md).
