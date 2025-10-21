"""Integration tests for API interactions with mocking"""
import pytest
import responses
import json
import tempfile
import os
from fetch import Parser, APIConnectionError
from models import db, Alert


@pytest.fixture(autouse=True)
def setup_test_database():
    """Set up a temporary test database for each test"""
    # Use in-memory database for tests
    test_db = ':memory:'
    db.init(test_db)
    db.connect()
    db.create_tables([Alert])
    yield
    db.close()


class TestAPIIntegration:
    """Test cases for API integration"""
    
    @responses.activate
    def test_fetch_alerts_success(self):
        """Test successful fetch of alerts from NOAA API"""
        # Mock the NOAA API response
        mock_response = {
            'features': [
                {
                    'properties': {
                        'id': 'test-alert-1',
                        'headline': 'Test Alert',
                        'event': 'Test Warning',
                        'description': 'Test description',
                        'expires': '2025-10-21T15:00:00-05:00',
                        'uri': 'https://example.com/alert1',
                        '@id': 'https://api.weather.gov/alerts/1',
                        'geocode': {
                            'FIPS6': ['012057'],
                            'UGC': ['FLC057']
                        }
                    }
                }
            ]
        }
        
        responses.add(
            responses.GET,
            'https://api.weather.gov/alerts',
            json=mock_response,
            status=200
        )
        
        parser = Parser("token", "user", "https://api.pushover.net/1/messages.json", 
                       "https://api.weather.gov/alerts", ".", "TestApp/1.0")
        
        # This should not raise an exception
        parser.fetch(1234567890)
    
    @responses.activate
    def test_fetch_alerts_timeout(self):
        """Test handling of API timeout"""
        import requests
        
        def request_callback(request):
            raise requests.exceptions.Timeout("Connection timed out")
        
        responses.add_callback(
            responses.GET,
            'https://api.weather.gov/alerts',
            callback=request_callback
        )
        
        parser = Parser("token", "user", "https://api.pushover.net/1/messages.json",
                       "https://api.weather.gov/alerts", ".", "TestApp/1.0")
        
        with pytest.raises(APIConnectionError, match="timed out"):
            parser.fetch(1234567890)
    
    @responses.activate
    def test_fetch_alerts_invalid_json(self):
        """Test handling of invalid JSON response"""
        responses.add(
            responses.GET,
            'https://api.weather.gov/alerts',
            body='not valid json',
            status=200,
            content_type='application/json'
        )
        
        parser = Parser("token", "user", "https://api.pushover.net/1/messages.json",
                       "https://api.weather.gov/alerts", ".", "TestApp/1.0")
        
        # Should raise InvalidAlertDataError but we're catching it in fetch
        # So we just verify it doesn't crash the app
        from fetch import InvalidAlertDataError
        with pytest.raises(InvalidAlertDataError):
            parser.fetch(1234567890)
    
    @responses.activate
    def test_send_pushover_alert_success(self):
        """Test successful sending of Pushover alert"""
        responses.add(
            responses.POST,
            'https://api.pushover.net/1/messages.json',
            json={'status': 1},
            status=200
        )
        
        parser = Parser("token", "user", "https://api.pushover.net/1/messages.json",
                       "https://api.weather.gov/alerts", ".", "TestApp/1.0")
        
        # This should not raise an exception
        parser.send_pushover_alert("test123", "Test Title", "Test Message", "https://example.com")
    
    @responses.activate
    def test_send_pushover_alert_timeout(self):
        """Test handling of Pushover API timeout"""
        import requests
        
        def request_callback(request):
            raise requests.exceptions.Timeout("Connection timed out")
        
        responses.add_callback(
            responses.POST,
            'https://api.pushover.net/1/messages.json',
            callback=request_callback
        )
        
        parser = Parser("token", "user", "https://api.pushover.net/1/messages.json",
                       "https://api.weather.gov/alerts", ".", "TestApp/1.0")
        
        with pytest.raises(APIConnectionError, match="Pushover API request timed out"):
            parser.send_pushover_alert("test123", "Test Title", "Test Message", "https://example.com")
