"""Tests for MCP server."""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from hootsuite_mcp.server import HootsuiteMCPServer
from hootsuite_mcp.config import Settings


def test_server_initialization():
    """Test server initialization."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )
    
    server = HootsuiteMCPServer(settings)
    
    assert server.settings == settings
    assert server.server is not None
    assert server.client is not None


def test_server_initialization_without_settings():
    """Test server initialization without explicit settings."""
    # This will use environment variables or defaults
    # We need to set a token to avoid authentication error
    with patch.dict('os.environ', {'HOOTSUITE_ACCESS_TOKEN': 'test_token'}):
        server = HootsuiteMCPServer()
        assert server.settings is not None
        assert server.server is not None


@pytest.mark.asyncio
async def test_list_tools():
    """Test that server provides expected tools."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )
    
    server = HootsuiteMCPServer(settings)
    
    # Get the list_tools handler
    tools = await server.server._list_tools_handler()
    
    # Check that expected tools are present
    tool_names = [tool.name for tool in tools]
    
    assert "create_post" in tool_names
    assert "get_social_profiles" in tool_names
    assert "get_posts" in tool_names
    assert "delete_post" in tool_names
    assert "get_analytics" in tool_names


@pytest.mark.asyncio
async def test_create_post_tool():
    """Test create_post tool execution."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )
    
    server = HootsuiteMCPServer(settings)
    
    # Mock the client method
    expected_result = {"id": "123", "text": "Test post"}
    server.client.create_post = AsyncMock(return_value=expected_result)
    
    # Call the tool
    result = await server.server._call_tool_handler(
        "create_post",
        {
            "text": "Test post",
            "social_profile_ids": ["profile1"]
        }
    )
    
    assert len(result) == 1
    assert result[0].type == "text"
    assert "123" in result[0].text


@pytest.mark.asyncio
async def test_get_social_profiles_tool():
    """Test get_social_profiles tool execution."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )
    
    server = HootsuiteMCPServer(settings)
    
    # Mock the client method
    expected_result = {"data": [{"id": "1", "name": "Profile"}]}
    server.client.get_social_profiles = AsyncMock(return_value=expected_result)
    
    # Call the tool
    result = await server.server._call_tool_handler(
        "get_social_profiles",
        {}
    )
    
    assert len(result) == 1
    assert result[0].type == "text"
    assert "Profile" in result[0].text


@pytest.mark.asyncio
async def test_delete_post_tool():
    """Test delete_post tool execution."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )
    
    server = HootsuiteMCPServer(settings)
    
    # Mock the client method
    expected_result = {"success": True}
    server.client.delete_post = AsyncMock(return_value=expected_result)
    
    # Call the tool
    result = await server.server._call_tool_handler(
        "delete_post",
        {"post_id": "123"}
    )
    
    assert len(result) == 1
    assert result[0].type == "text"
    assert "success" in result[0].text.lower()


@pytest.mark.asyncio
async def test_unknown_tool_error():
    """Test error handling for unknown tool."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )
    
    server = HootsuiteMCPServer(settings)
    
    # Call unknown tool
    result = await server.server._call_tool_handler(
        "unknown_tool",
        {}
    )
    
    assert len(result) == 1
    assert result[0].type == "text"
    assert "error" in result[0].text.lower()


@pytest.mark.asyncio
async def test_tool_error_handling():
    """Test error handling in tool execution."""
    settings = Settings(
        hootsuite_access_token="test_token"
    )
    
    server = HootsuiteMCPServer(settings)
    
    # Mock client method to raise error
    server.client.create_post = AsyncMock(side_effect=Exception("Test error"))
    
    # Call the tool
    result = await server.server._call_tool_handler(
        "create_post",
        {
            "text": "Test",
            "social_profile_ids": ["profile1"]
        }
    )
    
    assert len(result) == 1
    assert result[0].type == "text"
    assert "error" in result[0].text.lower()
