"""Hootsuite MCP Server - Model Context Protocol server for Hootsuite integration."""

__version__ = "0.2.0"

from .client import HootsuiteAPIError, HootsuiteAuthenticationError, HootsuiteClient
from .config import Settings
from .server import main, mcp

__all__ = [
    "HootsuiteAPIError",
    "HootsuiteAuthenticationError",
    "HootsuiteClient",
    "Settings",
    "main",
    "mcp",
]
