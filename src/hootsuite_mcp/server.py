"""MCP Server implementation for Hootsuite API integration using FastMCP."""

from __future__ import annotations

import json
import logging
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from mcp.server.fastmcp import Context, FastMCP

from .client import HootsuiteClient
from .config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AppContext:
    """Application-level context shared with every tool call."""

    client: HootsuiteClient
    settings: Settings


def _build_lifespan(settings: Settings | None = None):
    """Create a lifespan manager bound to the given (or default) settings."""

    @asynccontextmanager
    async def lifespan(_server: FastMCP) -> AsyncIterator[AppContext]:
        cfg = settings or Settings()
        client = HootsuiteClient(cfg)
        try:
            yield AppContext(client=client, settings=cfg)
        finally:
            await client.close()

    return lifespan


# Module-level FastMCP instance - tools are registered against this
mcp: FastMCP = FastMCP("hootsuite-mcp-server", lifespan=_build_lifespan())


def _get_client(ctx: Context) -> HootsuiteClient:
    """Helper to grab the shared HootsuiteClient from the lifespan context."""
    app_ctx: AppContext = ctx.request_context.lifespan_context
    return app_ctx.client


def _format(payload: Any) -> str:
    """Serialize a response payload as pretty JSON text."""
    return json.dumps(payload, indent=2, default=str)


@mcp.tool()
async def create_post(
    text: str,
    social_profile_ids: list[str],
    scheduled_send_time: str | None = None,
    ctx: Context | None = None,
) -> str:
    """Create and schedule a social media post on Hootsuite.

    Args:
        text: The content of the post.
        social_profile_ids: List of social profile IDs to post to.
        scheduled_send_time: Optional ISO 8601 datetime for scheduling.
    """
    assert ctx is not None
    client = _get_client(ctx)
    try:
        result = await client.create_post(
            text=text,
            social_profile_ids=social_profile_ids,
            scheduled_send_time=scheduled_send_time,
        )
        return _format(result)
    except Exception as exc:  # noqa: BLE001
        logger.error("Error calling tool create_post: %s", exc)
        return f"Error: {exc}"


@mcp.tool()
async def get_social_profiles(ctx: Context | None = None) -> str:
    """Get the list of social media profiles connected to Hootsuite."""
    assert ctx is not None
    client = _get_client(ctx)
    try:
        result = await client.get_social_profiles()
        return _format(result)
    except Exception as exc:  # noqa: BLE001
        logger.error("Error calling tool get_social_profiles: %s", exc)
        return f"Error: {exc}"


@mcp.tool()
async def get_posts(
    limit: int = 20,
    state: str | None = None,
    ctx: Context | None = None,
) -> str:
    """Get scheduled and published posts from Hootsuite.

    Args:
        limit: Maximum number of posts to retrieve (default: 20).
        state: Optional filter by state (scheduled, published, draft).
    """
    assert ctx is not None
    client = _get_client(ctx)
    try:
        result = await client.get_posts(limit=limit, state=state)
        return _format(result)
    except Exception as exc:  # noqa: BLE001
        logger.error("Error calling tool get_posts: %s", exc)
        return f"Error: {exc}"


@mcp.tool()
async def delete_post(post_id: str, ctx: Context | None = None) -> str:
    """Delete a scheduled or draft post from Hootsuite.

    Args:
        post_id: The ID of the post to delete.
    """
    assert ctx is not None
    client = _get_client(ctx)
    try:
        result = await client.delete_post(post_id=post_id)
        return _format(result)
    except Exception as exc:  # noqa: BLE001
        logger.error("Error calling tool delete_post: %s", exc)
        return f"Error: {exc}"


@mcp.tool()
async def get_analytics(
    profile_ids: list[str],
    start_date: str,
    end_date: str,
    ctx: Context | None = None,
) -> str:
    """Get analytics data for social profiles.

    Args:
        profile_ids: List of profile IDs to get analytics for.
        start_date: Start date in ISO format (YYYY-MM-DD).
        end_date: End date in ISO format (YYYY-MM-DD).
    """
    assert ctx is not None
    client = _get_client(ctx)
    try:
        result = await client.get_analytics(
            profile_ids=profile_ids,
            start_date=start_date,
            end_date=end_date,
        )
        return _format(result)
    except Exception as exc:  # noqa: BLE001
        logger.error("Error calling tool get_analytics: %s", exc)
        return f"Error: {exc}"


def main() -> None:
    """Main entry point for the MCP server (stdio transport)."""
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001
        logger.error("Server error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
