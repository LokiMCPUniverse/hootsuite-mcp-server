"""Hootsuite API client with authentication, rate limiting, and retry logic."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

import httpx

from .config import Settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for API requests."""

    def __init__(self, max_requests: int, window_seconds: int):
        """Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed in the window.
            window_seconds: Time window in seconds.
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: list[datetime] = []
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire permission to make a request, waiting if necessary."""
        while True:
            sleep_time = 0.0
            async with self._lock:
                now = datetime.now()
                # Remove old requests outside the window
                cutoff = now - timedelta(seconds=self.window_seconds)
                self.requests = [req_time for req_time in self.requests if req_time > cutoff]

                # Check if we're at the limit
                if len(self.requests) >= self.max_requests:
                    # Wait until the oldest request expires
                    sleep_time = (self.requests[0] - cutoff).total_seconds()
                else:
                    # Record this request and exit
                    self.requests.append(now)
                    return

            if sleep_time > 0:
                logger.info("Rate limit reached, waiting %.2f seconds", sleep_time)
                await asyncio.sleep(sleep_time)


class HootsuiteAPIError(Exception):
    """Base exception for Hootsuite API errors."""


class HootsuiteAuthenticationError(HootsuiteAPIError):
    """Authentication error."""


class HootsuiteRateLimitError(HootsuiteAPIError):
    """Rate limit exceeded error."""


class HootsuiteClient:
    """Async HTTP client for Hootsuite API."""

    def __init__(self, settings: Settings):
        """Initialize the Hootsuite client.

        Args:
            settings: Configuration settings.
        """
        self.settings = settings
        self.base_url = settings.hootsuite_api_base_url
        self.rate_limiter = RateLimiter(
            max_requests=settings.rate_limit_requests,
            window_seconds=settings.rate_limit_window,
        )

        # Validate credentials
        if not settings.validate_credentials():
            raise HootsuiteAuthenticationError(
                "Missing credentials. Please provide either API key/secret or access token."
            )

        # Initialize HTTP client
        headers = self._build_headers()
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=settings.request_timeout,
        )

    def _build_headers(self) -> dict[str, str]:
        """Build HTTP headers for API requests.

        Returns:
            Dictionary of headers.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.settings.hootsuite_access_token:
            headers["Authorization"] = f"Bearer {self.settings.hootsuite_access_token}"
        elif self.settings.hootsuite_api_key:
            # Some APIs use API key in header
            headers["X-API-Key"] = self.settings.hootsuite_api_key

        return headers

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        retry_count: int = 0,
    ) -> dict[str, Any]:
        """Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.).
            endpoint: API endpoint.
            data: Request body data.
            params: Query parameters.
            retry_count: Current retry attempt.

        Returns:
            Response data as dictionary.

        Raises:
            HootsuiteAPIError: On API errors.
        """
        # Apply rate limiting
        await self.rate_limiter.acquire()

        try:
            response = await self.client.request(
                method=method,
                url=endpoint,
                json=data,
                params=params,
            )

            # Handle different status codes
            if response.status_code == 401:
                raise HootsuiteAuthenticationError(
                    "Authentication failed. Check your credentials."
                )
            if response.status_code == 429:
                # Rate limit exceeded
                if retry_count < self.settings.max_retries:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    logger.warning(
                        "Rate limit exceeded. Retrying after %s seconds", retry_after
                    )
                    await asyncio.sleep(retry_after)
                    return await self._request(method, endpoint, data, params, retry_count + 1)
                raise HootsuiteRateLimitError("Rate limit exceeded and max retries reached")
            if response.status_code >= 500:
                # Server error - retry
                if retry_count < self.settings.max_retries:
                    delay = self.settings.retry_delay * (2**retry_count)  # Exponential backoff
                    logger.warning(
                        "Server error %s. Retrying in %s seconds", response.status_code, delay
                    )
                    await asyncio.sleep(delay)
                    return await self._request(method, endpoint, data, params, retry_count + 1)
                raise HootsuiteAPIError(f"Server error: {response.status_code}")

            response.raise_for_status()

            # Return JSON response or empty dict
            try:
                return response.json()
            except Exception:  # noqa: BLE001
                return {"success": True, "status_code": response.status_code}

        except httpx.HTTPError as e:
            if retry_count < self.settings.max_retries:
                delay = self.settings.retry_delay * (2**retry_count)
                logger.warning("Request error: %s. Retrying in %s seconds", e, delay)
                await asyncio.sleep(delay)
                return await self._request(method, endpoint, data, params, retry_count + 1)
            raise HootsuiteAPIError(f"Request failed: {e}") from e

    async def create_post(
        self,
        text: str,
        social_profile_ids: list[str],
        scheduled_send_time: str | None = None,
    ) -> dict[str, Any]:
        """Create a social media post.

        Args:
            text: Post content.
            social_profile_ids: List of profile IDs to post to.
            scheduled_send_time: Optional ISO 8601 datetime for scheduling.

        Returns:
            Created post data.
        """
        data: dict[str, Any] = {
            "text": text,
            "socialProfileIds": social_profile_ids,
        }

        if scheduled_send_time:
            data["scheduledSendTime"] = scheduled_send_time

        return await self._request("POST", "/messages", data=data)

    async def get_social_profiles(self) -> dict[str, Any]:
        """Get connected social media profiles.

        Returns:
            List of social profiles.
        """
        return await self._request("GET", "/socialProfiles")

    async def get_posts(
        self,
        limit: int = 20,
        state: str | None = None,
    ) -> dict[str, Any]:
        """Get posts from Hootsuite.

        Args:
            limit: Maximum number of posts to retrieve.
            state: Filter by state (scheduled, published, draft).

        Returns:
            List of posts.
        """
        params: dict[str, Any] = {"limit": limit}
        if state:
            params["state"] = state

        return await self._request("GET", "/messages", params=params)

    async def delete_post(self, post_id: str) -> dict[str, Any]:
        """Delete a post.

        Args:
            post_id: ID of the post to delete.

        Returns:
            Deletion confirmation.
        """
        return await self._request("DELETE", f"/messages/{post_id}")

    async def get_analytics(
        self,
        profile_ids: list[str],
        start_date: str,
        end_date: str,
    ) -> dict[str, Any]:
        """Get analytics data for profiles.

        Args:
            profile_ids: List of profile IDs.
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).

        Returns:
            Analytics data.
        """
        params = {
            "profileIds": ",".join(profile_ids),
            "startDate": start_date,
            "endDate": end_date,
        }

        return await self._request("GET", "/analytics", params=params)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self) -> HootsuiteClient:
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
