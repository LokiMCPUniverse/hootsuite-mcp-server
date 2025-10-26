"""Tests for configuration management."""

import pytest
from hootsuite_mcp.config import Settings


def test_settings_default_values():
    """Test default settings values."""
    settings = Settings()
    
    assert settings.hootsuite_api_base_url == "https://platform.hootsuite.com/v1"
    assert settings.rate_limit_requests == 100
    assert settings.rate_limit_window == 60
    assert settings.max_retries == 3
    assert settings.retry_delay == 1.0
    assert settings.request_timeout == 30


def test_settings_with_api_key():
    """Test settings validation with API key."""
    settings = Settings(
        hootsuite_api_key="test_key",
        hootsuite_api_secret="test_secret"
    )
    
    assert settings.validate_credentials() is True


def test_settings_with_access_token():
    """Test settings validation with access token."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )
    
    assert settings.validate_credentials() is True


def test_settings_without_credentials():
    """Test settings validation without credentials."""
    settings = Settings()
    
    assert settings.validate_credentials() is False


def test_settings_custom_values():
    """Test custom settings values."""
    settings = Settings(
        hootsuite_api_key="custom_key",
        hootsuite_api_secret="custom_secret",
        rate_limit_requests=50,
        max_retries=5,
        request_timeout=60
    )
    
    assert settings.hootsuite_api_key == "custom_key"
    assert settings.hootsuite_api_secret == "custom_secret"
    assert settings.rate_limit_requests == 50
    assert settings.max_retries == 5
    assert settings.request_timeout == 60
