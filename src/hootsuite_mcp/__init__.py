"""Hootsuite MCP Server - Model Context Protocol server for Hootsuite integration."""

__version__ = "0.1.0"

from .server import HootsuiteMCPServer, main
from .client import HootsuiteClient, HootsuiteAPIError, HootsuiteAuthenticationError
from .config import Settings

__all__ = [
    "HootsuiteMCPServer",
    "HootsuiteClient",
    "HootsuiteAPIError",
    "HootsuiteAuthenticationError",
    "Settings",
    "main"
]
