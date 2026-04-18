"""Tests for MCP server (FastMCP-based)."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from hootsuite_mcp import server as server_module
from hootsuite_mcp.config import Settings
from hootsuite_mcp.server import (
    create_post,
    delete_post,
    get_analytics,
    get_posts,
    get_social_profiles,
    mcp,
)


def _make_ctx(client) -> SimpleNamespace:
    """Build a minimal stand-in for mcp.server.fastmcp.Context."""
    settings = Settings(hootsuite_access_token="test_token")
    app_ctx = server_module.AppContext(client=client, settings=settings)
    request_context = SimpleNamespace(lifespan_context=app_ctx)
    return SimpleNamespace(request_context=request_context)


def test_server_module_exposes_mcp():
    """Module should expose a FastMCP instance named correctly."""
    assert mcp is not None
    assert mcp.name == "hootsuite-mcp-server"


@pytest.mark.asyncio
async def test_registered_tools():
    """Check expected tools are registered with FastMCP."""
    tools = await mcp.list_tools()
    names = {tool.name for tool in tools}

    assert {
        "create_post",
        "get_social_profiles",
        "get_posts",
        "delete_post",
        "get_analytics",
    }.issubset(names)


@pytest.mark.asyncio
async def test_create_post_tool():
    """Test create_post tool execution."""
    client = AsyncMock()
    client.create_post = AsyncMock(return_value={"id": "123", "text": "Test post"})
    ctx = _make_ctx(client)

    result = await create_post(
        text="Test post",
        social_profile_ids=["profile1"],
        ctx=ctx,
    )

    assert "123" in result
    client.create_post.assert_awaited_once_with(
        text="Test post",
        social_profile_ids=["profile1"],
        scheduled_send_time=None,
    )


@pytest.mark.asyncio
async def test_get_social_profiles_tool():
    """Test get_social_profiles tool execution."""
    client = AsyncMock()
    client.get_social_profiles = AsyncMock(
        return_value={"data": [{"id": "1", "name": "Profile"}]}
    )
    ctx = _make_ctx(client)

    result = await get_social_profiles(ctx=ctx)

    assert "Profile" in result
    client.get_social_profiles.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_posts_tool():
    """Test get_posts tool execution."""
    client = AsyncMock()
    client.get_posts = AsyncMock(return_value={"data": []})
    ctx = _make_ctx(client)

    result = await get_posts(limit=5, state="scheduled", ctx=ctx)

    assert "data" in result
    client.get_posts.assert_awaited_once_with(limit=5, state="scheduled")


@pytest.mark.asyncio
async def test_delete_post_tool():
    """Test delete_post tool execution."""
    client = AsyncMock()
    client.delete_post = AsyncMock(return_value={"success": True})
    ctx = _make_ctx(client)

    result = await delete_post(post_id="123", ctx=ctx)

    assert "success" in result.lower()
    client.delete_post.assert_awaited_once_with(post_id="123")


@pytest.mark.asyncio
async def test_get_analytics_tool():
    """Test get_analytics tool execution."""
    client = AsyncMock()
    client.get_analytics = AsyncMock(return_value={"impressions": 100})
    ctx = _make_ctx(client)

    result = await get_analytics(
        profile_ids=["1"],
        start_date="2026-01-01",
        end_date="2026-01-31",
        ctx=ctx,
    )

    assert "impressions" in result
    client.get_analytics.assert_awaited_once_with(
        profile_ids=["1"],
        start_date="2026-01-01",
        end_date="2026-01-31",
    )


@pytest.mark.asyncio
async def test_tool_error_handling():
    """Test that tool errors are surfaced as text rather than raising."""
    client = AsyncMock()
    client.create_post = AsyncMock(side_effect=Exception("Test error"))
    ctx = _make_ctx(client)

    result = await create_post(
        text="Test",
        social_profile_ids=["profile1"],
        ctx=ctx,
    )

    assert "error" in result.lower()
    assert "test error" in result.lower()
