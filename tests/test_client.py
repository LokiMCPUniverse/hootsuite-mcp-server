"""Tests for Hootsuite API client."""

from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest

from hootsuite_mcp.client import (
    HootsuiteAuthenticationError,
    HootsuiteClient,
    RateLimiter,
)
from hootsuite_mcp.config import Settings


@pytest.mark.asyncio
async def test_rate_limiter_allows_requests():
    """Test that rate limiter allows requests within limit."""
    limiter = RateLimiter(max_requests=5, window_seconds=1)

    # Should allow 5 requests without delay
    for _ in range(5):
        await limiter.acquire()

    assert len(limiter.requests) == 5


@pytest.mark.asyncio
async def test_rate_limiter_blocks_excess_requests():
    """Test that rate limiter blocks requests exceeding limit."""
    limiter = RateLimiter(max_requests=2, window_seconds=1)

    # First 2 requests should be immediate
    start_time = datetime.now()
    await limiter.acquire()
    await limiter.acquire()

    # Third request should wait
    await limiter.acquire()
    elapsed = (datetime.now() - start_time).total_seconds()

    # Should have waited at least some time
    assert elapsed >= 0.9  # Allow some tolerance


def test_client_requires_credentials():
    """Test that client raises error without credentials."""
    settings = Settings()

    with pytest.raises(HootsuiteAuthenticationError):
        HootsuiteClient(settings)


def test_client_accepts_api_key():
    """Test that client accepts API key credentials."""
    settings = Settings(
        hootsuite_api_key="test_key",
        hootsuite_api_secret="test_secret"
    )

    client = HootsuiteClient(settings)
    assert client.settings.hootsuite_api_key == "test_key"


def test_client_accepts_access_token():
    """Test that client accepts access token."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )

    client = HootsuiteClient(settings)
    assert client.settings.hootsuite_access_token == "test_token"


def test_client_builds_headers_with_token():
    """Test header construction with access token."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )

    client = HootsuiteClient(settings)
    headers = client._build_headers()

    assert headers["Authorization"] == "Bearer test_token"
    assert headers["Content-Type"] == "application/json"


def test_client_builds_headers_with_api_key():
    """Test header construction with API key."""
    settings = Settings(
        hootsuite_api_key="test_key",
        hootsuite_api_secret="test_secret"
    )

    client = HootsuiteClient(settings)
    headers = client._build_headers()

    assert headers["X-API-Key"] == "test_key"
    assert headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_client_request_with_mock():
    """Test client request with mocked HTTP response."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )

    client = HootsuiteClient(settings)

    # Mock the HTTP client
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mock_response.raise_for_status = Mock()

    client.client.request = AsyncMock(return_value=mock_response)

    result = await client._request("GET", "/test")

    assert result == {"data": "test"}
    await client.close()


@pytest.mark.asyncio
async def test_client_handles_401_error():
    """Test that client raises authentication error on 401."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )

    client = HootsuiteClient(settings)

    # Mock 401 response
    mock_response = Mock()
    mock_response.status_code = 401

    client.client.request = AsyncMock(return_value=mock_response)

    with pytest.raises(HootsuiteAuthenticationError):
        await client._request("GET", "/test")

    await client.close()


@pytest.mark.asyncio
async def test_client_retries_on_500_error():
    """Test that client retries on server errors."""
    settings = Settings(
        hootsuite_access_token="test_token",
        max_retries=2,
        retry_delay=0.1
    )

    client = HootsuiteClient(settings)

    # Mock responses: first fails, second succeeds
    mock_fail = Mock()
    mock_fail.status_code = 500

    mock_success = Mock()
    mock_success.status_code = 200
    mock_success.json.return_value = {"data": "success"}
    mock_success.raise_for_status = Mock()

    client.client.request = AsyncMock(side_effect=[mock_fail, mock_success])

    result = await client._request("GET", "/test")

    assert result == {"data": "success"}
    assert client.client.request.call_count == 2

    await client.close()


@pytest.mark.asyncio
async def test_create_post():
    """Test create_post method."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )

    client = HootsuiteClient(settings)

    # Mock the request method
    expected_result = {"id": "123", "text": "Test post"}
    client._request = AsyncMock(return_value=expected_result)

    result = await client.create_post(
        text="Test post",
        social_profile_ids=["profile1", "profile2"]
    )

    assert result == expected_result
    client._request.assert_called_once()

    await client.close()


@pytest.mark.asyncio
async def test_get_social_profiles():
    """Test get_social_profiles method."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )

    client = HootsuiteClient(settings)

    expected_result = {"data": [{"id": "1", "name": "Profile 1"}]}
    client._request = AsyncMock(return_value=expected_result)

    result = await client.get_social_profiles()

    assert result == expected_result
    client._request.assert_called_once_with("GET", "/socialProfiles")

    await client.close()


@pytest.mark.asyncio
async def test_delete_post():
    """Test delete_post method."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )

    client = HootsuiteClient(settings)

    expected_result = {"success": True}
    client._request = AsyncMock(return_value=expected_result)

    result = await client.delete_post("post123")

    assert result == expected_result
    client._request.assert_called_once_with("DELETE", "/messages/post123")

    await client.close()


@pytest.mark.asyncio
async def test_client_context_manager():
    """Test client as async context manager."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )

    async with HootsuiteClient(settings) as client:
        assert client.client is not None

    # Client should be closed after context
    assert client.client.is_closed
