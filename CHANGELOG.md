# Changelog


## Version 3.0.9 - 2025-10-21

### Changes
- Implement RECOMMENDATIONS.md: Environment variables, retry logic, rate limiting, validation, exceptions, and comprehensive test suite (#52) by @Copilot

## Version 3.1.0 - 2025-10-21

### Added
- **Environment Variable Support**: Credentials can now be set via `PUSHOVER_TOKEN` and `PUSHOVER_USER` environment variables for better Docker/container security (#XX)
- **Retry Logic**: Automatic retry with exponential backoff for API requests (3 retries, backoff factor 1, handles HTTP 429, 500, 502, 503, 504) (#XX)
- **Rate Limiting**: API calls are now rate-limited (2s interval for NOAA, 1s for Pushover) to prevent quota violations (#XX)
- **Input Validation**: FIPS codes (6 digits) and UGC codes (2 letters + 3 digits) are validated on load to catch configuration errors early (#XX)
- **Custom Exception Hierarchy**: Added `NOAAAlertError`, `APIConnectionError`, `InvalidAlertDataError`, `ConfigurationError` for better error handling (#XX)
- **Testing Framework**: Pytest-based test suite with 13+ unit and integration tests (#XX)
  - Unit tests for Parser class methods
  - Integration tests with mocked API responses
  - Database fixtures for testing
  - CI/CD integration with GitHub Actions
- **Test Dependencies**: Added pytest (8.3.4), pytest-cov (6.0.0), responses (0.25.0) to requirements.txt (#XX)

### Changed
- **Error Handling**: Individual alert failures no longer stop processing of other alerts (#XX)
- **API Resilience**: Better handling of transient network failures with automatic retries (#XX)
- **Logging**: Module-level logger for better test compatibility (#XX)

### Improved
- **Documentation**: Updated README.md, INSTALL.md, SECURITY.md with new features (#XX)
- **CI/CD**: Added pytest execution to GitHub Actions workflow (#XX)
- **Security**: Environment variables take precedence over config.txt for credential management (#XX)

### Developer
- Created `tests/` directory with comprehensive test coverage
- Added pytest.ini for test configuration
- Updated .gitignore to exclude .pytest_cache/

## Version 3.0.8 - 2025-10-20

### Changes
- Code clean-up: Remove RUN_MODE, fix security issues, modernize code (#50) by @Copilot

## Version 3.0.7 - 2025-10-19

### Changes
- Stop tracking counties.json (#48) by @Copilot

## Version 3.0.6 - 2025-10-18

### Changes
- Fix incorrect FIPS and UGC code references in documentation (#47) by @Copilot

## Version 3.0.5 - 2025-10-18

### Changes
- [WIP] Ensure User-Agent compliance for weather.gov API (#46) by @Copilot

## Version 3.0.4 - 2025-10-18

### Changes
- Add configurable NOAA API URL in config.txt (#44) by @Copilot

## Version 3.0.3 - 2025-10-18

### Changes
- Add configurable Pushover API URL parameter to config.txt (#43) by @Copilot

## Version 3.0.2 - 2025-10-15

### Changes
- Bump requests from 2.32.3 to 2.32.4 (#36) by @dependabot[bot]

## Version 3.0.1 - 2025-10-15

### Changes
- Bump jinja2 from 3.1.4 to 3.1.6 (#35) by @dependabot[bot]

## Version 3.0.0 - 2025-10-07

### Changes
- Add Docker first-run auto-configuration and consolidate release documentation (#34) by @Copilot

## Version 2.3.5 - 2025-10-07

### 🚀 Improvements
- **Docker First-Run Auto-Configuration**: Container now automatically creates `config.txt` and `counties.json` from example files if they don't exist on first run
- **New File**: `counties.json.example` - Template file for county configuration
- **Enhanced Docker Experience**: Simplified first-time setup - no manual file creation required before running container

### 📝 Documentation Updates
- Updated `INSTALL.md` with auto-creation information for Docker setup
- Updated `docs/DOCKER_HUB_README.md` with two setup options (auto-creation vs manual)
- Updated `docker-compose.yml` with clarifying comment about auto-creation
- Updated `entrypoint.sh` to handle missing configuration files gracefully

### 🧹 Cleanup
- **Removed**: `create_tags.sh` script (no longer needed - use GitHub Actions workflow instead)
- **Removed**: `docs/TAGGING.md` and `docs/TAGGING_QUICKSTART.md` (consolidated into AUTO_VERSIONING.md)
- Updated all documentation to reference AUTO_VERSIONING.md for release creation

## Version 2.3.4 - 2025-10-07

### Changes
- Implement test_message config, migrate to main branch, and organize documentation (#32) by @Copilot

## Version 2.3.3 - 2025-10-07

### Changes
- Fix expires timestamp displaying as Unix timestamp instead of human-readable format (#31) by @Copilot

## Version 2.3.2 - 2025-10-06

### Changes
- Add GitHub Container Registry publishing workflow with auto-versioning integration (#30) by @Copilot

## Version 2.3.1 - 2025-10-06

### Changes
- Fix Docker Hub workflow to remove unwanted main tag (#29) by @Copilot

## Version 2.3.0 - 2025-10-06

### Changes
- Add automatic semantic versioning on PR merge with label-based version control (#28) by @Copilot
## Version 2.2.0 - 2024

### 📝 Documentation Improvements

#### Template Customization Guide
- **New file**: `templates/TEMPLATE_GUIDE.md` (300+ lines)
- **Content**: Comprehensive guide for customizing `detail.html` template
- **Includes**:
  - All available template variables (alert data, expires timestamp)
  - 7 practical customization examples
  - Jinja2 template syntax reference
  - Testing instructions
  - Best practices for accessibility
  - Mobile-friendly layout examples
  - Troubleshooting common issues

#### Enhanced Setup Validation Tool
- **New features** in `test_setup.py`:
  - `--fix` flag: Automatically create config.txt and initialize database
  - `--interactive` flag: Prompt before each fix for user control
- **Auto-fixes**:
  - Missing config.txt (creates from config.txt.example)
  - Uninitialized database (runs database setup)
- **Benefits**: One-command setup reduces friction for new users

#### Sample Data Format Update
- **Removed**: `templates/sample.xml` (outdated XML CAP format)
- **Added**: `templates/sample.json` (modern GeoJSON/CAP format)
- **Added**: `templates/README.md` (templates directory documentation)
- **Why**: Sample data now matches actual NOAA API response format

### 📚 Files Changed
- `templates/sample.xml` - Deleted (107 lines removed)
- `templates/sample.json` - Created (88 lines added)
- `templates/README.md` - Created (71 lines added)
- `templates/TEMPLATE_GUIDE.md` - Created (318 lines added, moved from root)
- `test_setup.py` - Enhanced (80 lines added)
- `README.md` - Updated (23 lines added for customization section)

### 🔄 Documentation Consolidation
- **Combined** INSTALL.md and QUICKSTART.md into comprehensive INSTALL.md
- **Combined** CHANGELOG.md and CHANGES_SUMMARY.md into single CHANGELOG.md
- **Incorporated** DOCKER_NONROOT.md content into INSTALL.md
- **Incorporated** SUMMARY.md modernization details into README.md
- **Removed** redundant documentation files to reduce maintenance burden
- **Updated** all cross-references between documentation files

**Total**: ~600 lines of new documentation, improved organization and accessibility

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
- **docs/CODE_EXPLANATION.md**: Technical deep dive into architecture and code flow
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
1. Python scheduler (default - recommended)
2. Docker Compose with scheduler mode
3. systemd service for scheduler (Linux)

The application includes a built-in scheduler using Python's `schedule` library for automated task execution.

See [INSTALL.md](INSTALL.md) for details.

### 📚 Documentation Structure

```
noaa-alerts-pushover/
├── README.md              # Overview and quick start
├── INSTALL.md             # Detailed installation guide
├── SECURITY.md            # Security best practices
├── CHANGELOG.md           # This file
├── config.txt.example     # Configuration template
└── docs/
    ├── CODE_EXPLANATION.md    # Technical architecture
    └── AUTO_VERSIONING.md     # Automatic versioning guide
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
- [CODE_EXPLANATION.md](docs/CODE_EXPLANATION.md) for understanding the codebase
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

For technical details, see [CODE_EXPLANATION.md](docs/CODE_EXPLANATION.md).
