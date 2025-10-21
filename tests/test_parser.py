"""Unit tests for Parser class"""
import pytest
from fetch import Parser, validate_county, ConfigurationError


class TestParser:
    """Test cases for Parser class"""
    
    def test_create_alert_title(self):
        """Test alert title formatting"""
        parser = Parser("token", "user", "api_url", "noaa_url", ".", None)
        
        class MockAlert:
            county = "Test County"
            state = "TX"
        
        alert = MockAlert()
        title = parser.create_alert_title(alert)
        
        assert title == "Test County (TX) Weather Alert"
    
    def test_create_alert_message_without_details(self):
        """Test alert message formatting without details"""
        parser = Parser("token", "user", "api_url", "noaa_url", ".", None)
        
        class MockAlert:
            title = "Tornado Warning issued"
            details = None
            alert_id = "abc123def456"
        
        alert = MockAlert()
        message = parser.create_alert_message(alert)
        
        assert "Tornado Warning issued" in message
        assert "56" in message  # Last 5 chars of alert_id
    
    def test_create_alert_message_with_details(self):
        """Test alert message formatting with details"""
        parser = Parser("token", "user", "api_url", "noaa_url", ".", None)
        
        class MockAlert:
            title = "Special Weather Statement issued"
            details = "Thunderstorm, Wind"
            alert_id = "xyz789uvw012"
        
        alert = MockAlert()
        message = parser.create_alert_message(alert)
        
        assert "Thunderstorm, Wind" in message
        assert "w012" in message  # Last 5 chars of alert_id


class TestValidation:
    """Test cases for validation functions"""
    
    def test_validate_county_valid_fips_and_ugc(self):
        """Test validation with valid FIPS and UGC codes"""
        county = {
            'fips': '012057',
            'name': 'Hillsborough County',
            'state': 'FL',
            'ugc': 'FLC057'
        }
        assert validate_county(county) is True
    
    def test_validate_county_valid_ugc_empty_fips(self):
        """Test validation with valid UGC and empty FIPS"""
        county = {
            'fips': '',
            'name': 'Test County',
            'state': 'TX',
            'ugc': 'TXC123'
        }
        assert validate_county(county) is True
    
    def test_validate_county_invalid_fips(self):
        """Test validation with invalid FIPS code"""
        county = {
            'fips': '12057',  # Only 5 digits, should be 6
            'name': 'Test County',
            'state': 'FL',
            'ugc': 'FLC057'
        }
        with pytest.raises(ConfigurationError, match="Invalid FIPS code"):
            validate_county(county)
    
    def test_validate_county_invalid_ugc(self):
        """Test validation with invalid UGC code"""
        county = {
            'fips': '012057',
            'name': 'Test County',
            'state': 'FL',
            'ugc': 'FL57'  # Only 2 digits after state code
        }
        with pytest.raises(ConfigurationError, match="Invalid UGC code"):
            validate_county(county)
    
    def test_validate_county_missing_ugc(self):
        """Test validation with missing UGC code"""
        county = {
            'fips': '012057',
            'name': 'Test County',
            'state': 'FL',
            'ugc': ''
        }
        with pytest.raises(ConfigurationError, match="Invalid UGC code"):
            validate_county(county)
