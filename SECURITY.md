# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by opening a GitHub issue or contacting the maintainers directly. We take security seriously and will respond as quickly as possible.

**Please do not publicly disclose the vulnerability until we've had a chance to address it.**

## Security Best Practices

### Protecting Your Credentials

1. **Never commit `config.txt` to version control**
   - The `.gitignore` file excludes this by default
   - Always use `config.txt.example` as a template

2. **Use environment variables for sensitive data (Docker)** ✅ Implemented
   - The application supports `PUSHOVER_TOKEN` and `PUSHOVER_USER` environment variables
   - Environment variables take precedence over config.txt values
   - Store secrets in Docker secrets or your orchestration platform
   - Example:
   ```bash
   docker run -e PUSHOVER_TOKEN="..." -e PUSHOVER_USER="..." \
     k9barry/noaa-alerts-pushover:latest
   ```

3. **File permissions**
   ```bash
   chmod 600 config.txt  # Only owner can read/write
   ```

### Network Security

1. **HTTPS is used for all external API calls**
   - Pushover API: `https://api.pushover.net` (configurable via `api_url` in `[pushover]`)
   - NOAA API: `https://api.weather.gov` (configurable via `api_url` in `[noaa]`, see config.txt)

2. **Disable SSL warnings in production**
   - The code disables urllib3 warnings but maintains certificate verification
   - If you encounter certificate issues, update your system's CA certificates

3. **Timeout settings**
   - All HTTP requests have timeout values to prevent hanging connections
   - Default timeout is 30 seconds

### Docker Security

1. **Run as non-root user** ✅ Implemented
   - The Dockerfile includes a non-root user for enhanced security
   - Container runs as user `noaa` (UID 1000)
   - See [INSTALL.md](INSTALL.md) Docker Security section for volume mount permission details
   ```dockerfile
   RUN useradd -m -u 1000 noaa && chown -R noaa:noaa /app
   USER noaa
   ```
   
   **Volume mount permissions:**
   ```bash
   # Ensure mounted directories are writable by UID 1000
   sudo chown -R 1000:1000 ./output ./data
   # Or use permissive permissions
   chmod 777 ./output ./data
   ```

2. **Mount config files as read-only**
   - The docker-compose.yml already mounts config files as read-only
   ```yaml
   volumes:
     - ./config.txt:/app/config.txt:ro
   ```

3. **Keep base images updated**
   ```bash
   docker compose pull
   docker compose build --no-cache
   ```

### Database Security

1. **SQLite file permissions**
   - The database is stored in the `data/` directory
   - Ensure proper file permissions:
   ```bash
   chmod 700 data/
   chmod 600 data/alerts.db
   ```

2. **WAL mode enabled**
   - Write-Ahead Logging (WAL) mode is enabled for better concurrency
   - This prevents database lock issues

3. **No sensitive data in database**
   - Only alert metadata is stored
   - No personal information or credentials

### Application Security

1. **Input validation** ✅ Enhanced
   - County codes are validated against configured lists
   - **FIPS codes validated** with regex pattern `^\d{6}$` (6 digits)
   - **UGC codes validated** with regex pattern `^[A-Z]{2}\d{3}$` (2 letters + 3 digits)
   - JSON parsing uses Python's built-in json module for safety
   - API responses validated for correct content type before processing

2. **Error handling and resilience** ✅ Enhanced
   - **Custom exception hierarchy**: `NOAAAlertError`, `APIConnectionError`, `InvalidAlertDataError`, `ConfigurationError`
   - **Automatic retry logic**: 3 retries with exponential backoff for transient failures (HTTP 429, 500, 502, 503, 504)
   - **Rate limiting**: API calls limited to prevent quota violations (2s for NOAA, 1s for Pushover)
   - HTTP status codes validated before processing responses
   - HTML response detection prevents processing of error pages
   - JSON parsing errors caught and logged safely with specific exception types
   - Malformed API responses don't crash the application
   - Individual alert failures don't prevent processing of other alerts

3. **Dependency management**
   - All dependencies are pinned to specific versions
   - **Testing framework**: pytest with 13+ unit and integration tests
   - **Test coverage**: CI/CD pipeline runs tests on every commit
   - Regularly update dependencies:
   ```bash
   pip list --outdated
   pip install --upgrade -r requirements.txt
   ```

4. **Logging security**
   - Logs are stored in `log.txt`
   - No credentials are logged
   - Error responses truncated to first 1000 characters in logs
   - Consider log rotation for long-running deployments

### Known Security Considerations

#### 1. API Endpoints
- All external APIs use HTTPS (NOAA Weather API, Pushover API)
- Alert data from NOAA is public information
- All API responses are validated before processing (status codes, content types, JSON structure)
- See [docs/CODE_EXPLANATION.md](docs/CODE_EXPLANATION.md) for technical details on API integration

#### 2. HTML Output Files
- Alert detail pages are generated and stored in `output/`
- These files contain only public alert information
- If serving these files via web server, ensure proper access controls

#### 3. Third-Party Dependencies
- We use well-maintained, popular libraries
- Dependencies are kept up-to-date
- Current dependencies:
  - **requests**: HTTP library with retry support (industry standard)
  - **peewee**: ORM (SQL injection protection)
  - **Jinja2**: Template engine (XSS protection)
  - **arrow**: Date/time handling
  - **beautifulsoup4**: HTML parsing
  - **schedule**: Task scheduling
  - **pytest**: Testing framework (development)
  - **pytest-cov**: Test coverage (development)
  - **responses**: HTTP mocking for tests (development)

## Security Checklist for Deployment

- [ ] `config.txt` is not committed to version control
- [ ] `config.txt` has restrictive file permissions (600)
- [ ] **Consider using environment variables for credentials** (especially in Docker)
- [ ] Docker containers are kept up-to-date
- [ ] Dependencies are regularly updated
- [ ] **Run tests before deployment**: `python -m pytest tests/`
- [ ] Logs are reviewed periodically
- [ ] Database directory has proper permissions (700)
- [ ] Application runs with minimal required privileges
- [ ] Network access is restricted to required APIs only
- [ ] **County codes validated** (FIPS 6 digits, UGC 2 letters + 3 digits)

## Vulnerability Disclosure Timeline

1. **Day 0**: Vulnerability reported
2. **Day 1-2**: Acknowledgment and initial assessment
3. **Day 3-7**: Fix development and testing
4. **Day 7-14**: Release preparation and notification
5. **Day 14**: Public disclosure (if applicable)

We aim to address critical vulnerabilities within 7 days and other issues within 30 days.

## Updates and Patches

### Checking for Updates

```bash
git fetch
git status
```

### Applying Updates

**Docker:**
```bash
git pull
docker compose down
docker compose build --no-cache
docker compose up -d
```

**Manual:**
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
python fetch.py --debug  # Test the update
```

## Security Contact

For security-related inquiries, please:
1. Open a GitHub issue (for non-critical issues)
2. Contact the repository maintainers directly (for critical vulnerabilities)

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)

## Compliance

This application:
- Does not collect personal information beyond what you configure
- Does not transmit data except to configured APIs (Pushover, NOAA)
- Stores data locally in SQLite database
- Is provided as-is under MIT License

Users are responsible for:
- Securing their own Pushover credentials
- Compliance with Pushover's Terms of Service
- Compliance with NOAA data usage policies
- Securing their deployment environment

## License

This security policy is part of the NOAA Alerts Pushover project and is subject to the MIT License.
