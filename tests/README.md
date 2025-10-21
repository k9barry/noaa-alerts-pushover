# Test Suite

This directory contains the test suite for NOAA Alerts Pushover.

## Running Tests

### Run all tests
```bash
python -m pytest tests/
```

### Run with verbose output
```bash
python -m pytest tests/ -v
```

### Run with coverage report
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

### Run specific test file
```bash
python -m pytest tests/test_parser.py -v
```

### Run specific test
```bash
python -m pytest tests/test_parser.py::TestParser::test_create_alert_title -v
```

## Test Structure

- **`test_parser.py`** - Unit tests for Parser class methods and validation functions
  - Tests for alert title formatting
  - Tests for alert message creation
  - Tests for county code validation (FIPS/UGC)

- **`test_api_integration.py`** - Integration tests with mocked API calls
  - Tests for NOAA API fetching with mocked responses
  - Tests for Pushover notification sending
  - Tests for error handling (timeouts, invalid JSON)

- **`fixtures/`** - Test data fixtures
  - `test_config.txt` - Sample configuration file for testing
  - `sample_alert.json` - Sample NOAA alert in GeoJSON format

## Test Configuration

Tests use pytest with the following configuration (see `pytest.ini`):
- Verbose output (`-v`)
- Short traceback format (`--tb=short`)
- Strict markers
- Warnings disabled

## Database Testing

Integration tests use an in-memory SQLite database that is created and destroyed for each test. This ensures tests don't interfere with each other and don't affect the production database.

## Continuous Integration

Tests are automatically run on every push and pull request via GitHub Actions (see `.github/workflows/ci.yml`).

## Writing New Tests

When adding new tests:

1. Follow the existing naming convention (`test_*.py`)
2. Use descriptive test names that explain what is being tested
3. Group related tests in classes (e.g., `TestParser`, `TestValidation`)
4. Add docstrings to explain the purpose of each test
5. Use pytest fixtures for setup/teardown when needed
6. Mock external API calls using the `responses` library

Example:
```python
import pytest
from fetch import Parser

class TestNewFeature:
    """Test cases for new feature"""
    
    def test_feature_works_correctly(self):
        """Test that new feature behaves as expected"""
        # Arrange
        parser = Parser("token", "user", "api_url", "noaa_url", ".", None)
        
        # Act
        result = parser.some_method()
        
        # Assert
        assert result == expected_value
```

## Test Coverage

Current test coverage includes:
- Parser class initialization
- Alert title and message formatting
- County code validation (FIPS and UGC)
- API request handling with retries
- Error handling and exception raising
- Rate limiting functionality

## Dependencies

Testing requires the following additional packages (included in `requirements.txt`):
- **pytest** (8.3.4) - Testing framework
- **pytest-cov** (6.0.0) - Coverage reporting
- **responses** (0.25.0) - HTTP request mocking

## Troubleshooting

### Database Errors
If you see database errors, ensure the test database fixture is properly set up. The `setup_test_database` fixture should create a fresh in-memory database for each test.

### Import Errors
Make sure you're running tests from the project root directory:
```bash
cd /path/to/noaa-alerts-pushover
python -m pytest tests/
```

### Mock Not Working
Ensure the `@responses.activate` decorator is present on tests that mock HTTP requests.
