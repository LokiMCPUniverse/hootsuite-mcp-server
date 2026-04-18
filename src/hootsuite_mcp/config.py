"""Configuration management for Hootsuite MCP Server."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for Hootsuite MCP Server."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Hootsuite API credentials
    hootsuite_api_key: str = Field(
        default="",
        description="Hootsuite API key",
    )
    hootsuite_api_secret: str = Field(
        default="",
        description="Hootsuite API secret",
    )
    hootsuite_access_token: str | None = Field(
        default=None,
        description="Hootsuite OAuth access token",
    )
    hootsuite_refresh_token: str | None = Field(
        default=None,
        description="Hootsuite OAuth refresh token",
    )

    # API Configuration
    hootsuite_api_base_url: str = Field(
        default="https://platform.hootsuite.com/v1",
        description="Hootsuite API base URL",
    )

    # Rate limiting
    rate_limit_requests: int = Field(
        default=100,
        description="Maximum requests per minute",
    )
    rate_limit_window: int = Field(
        default=60,
        description="Rate limit window in seconds",
    )

    # Retry configuration
    max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts",
    )
    retry_delay: float = Field(
        default=1.0,
        description="Initial retry delay in seconds",
    )

    # Timeout
    request_timeout: int = Field(
        default=30,
        description="Request timeout in seconds",
    )

    def validate_credentials(self) -> bool:
        """Validate that necessary credentials are present.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        # Either API key/secret or access token must be present
        has_api_key = bool(self.hootsuite_api_key and self.hootsuite_api_secret)
        has_access_token = bool(self.hootsuite_access_token)

        return has_api_key or has_access_token
