"""MCP Server implementation for Hootsuite API integration."""

import asyncio
import logging
from typing import Any, Dict, List, Optional
import json

from mcp.server import Server
from mcp.types import Tool, TextContent, Resource, Prompt

from .client import HootsuiteClient
from .config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HootsuiteMCPServer:
    """MCP Server for Hootsuite API integration."""

    def __init__(self, settings: Optional[Settings] = None):
        """Initialize the Hootsuite MCP server.
        
        Args:
            settings: Configuration settings. If None, will load from environment.
        """
        self.settings = settings or Settings()
        self.server = Server("hootsuite-mcp-server")
        self.client = HootsuiteClient(self.settings)
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available Hootsuite tools."""
            return [
                Tool(
                    name="create_post",
                    description="Create and schedule a social media post on Hootsuite",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "The content of the post"
                            },
                            "social_profile_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of social profile IDs to post to"
                            },
                            "scheduled_send_time": {
                                "type": "string",
                                "description": "ISO 8601 formatted datetime for scheduling (optional)"
                            }
                        },
                        "required": ["text", "social_profile_ids"]
                    }
                ),
                Tool(
                    name="get_social_profiles",
                    description="Get list of social media profiles connected to Hootsuite",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_posts",
                    description="Get scheduled and published posts from Hootsuite",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of posts to retrieve (default: 20)",
                                "default": 20
                            },
                            "state": {
                                "type": "string",
                                "description": "Filter by post state (scheduled, published, draft)",
                                "enum": ["scheduled", "published", "draft"]
                            }
                        }
                    }
                ),
                Tool(
                    name="delete_post",
                    description="Delete a scheduled or draft post from Hootsuite",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "string",
                                "description": "The ID of the post to delete"
                            }
                        },
                        "required": ["post_id"]
                    }
                ),
                Tool(
                    name="get_analytics",
                    description="Get analytics data for social profiles",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "profile_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of profile IDs to get analytics for"
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Start date in ISO format (YYYY-MM-DD)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date in ISO format (YYYY-MM-DD)"
                            }
                        },
                        "required": ["profile_ids", "start_date", "end_date"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            try:
                if name == "create_post":
                    result = await self.client.create_post(
                        text=arguments["text"],
                        social_profile_ids=arguments["social_profile_ids"],
                        scheduled_send_time=arguments.get("scheduled_send_time")
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "get_social_profiles":
                    result = await self.client.get_social_profiles()
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "get_posts":
                    result = await self.client.get_posts(
                        limit=arguments.get("limit", 20),
                        state=arguments.get("state")
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "delete_post":
                    result = await self.client.delete_post(
                        post_id=arguments["post_id"]
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "get_analytics":
                    result = await self.client.get_analytics(
                        profile_ids=arguments["profile_ids"],
                        start_date=arguments["start_date"],
                        end_date=arguments["end_date"]
                    )
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                else:
                    raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                logger.error(f"Error calling tool {name}: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List available resources."""
            return []

        @self.server.list_prompts()
        async def list_prompts() -> List[Prompt]:
            """List available prompts."""
            return []

    async def run(self):
        """Run the MCP server."""
        from mcp.server.stdio import stdio_server
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point for the MCP server."""
    import sys
    
    try:
        server = HootsuiteMCPServer()
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
