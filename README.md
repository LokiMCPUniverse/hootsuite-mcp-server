# Hootsuite MCP Server

<div align="center">

# Hootsuite Mcp Server

[![GitHub stars](https://img.shields.io/github/stars/LokiMCPUniverse/hootsuite-mcp-server?style=social)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/LokiMCPUniverse/hootsuite-mcp-server?style=social)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server/network)
[![GitHub watchers](https://img.shields.io/github/watchers/LokiMCPUniverse/hootsuite-mcp-server?style=social)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server/watchers)

[![License](https://img.shields.io/github/license/LokiMCPUniverse/hootsuite-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/LokiMCPUniverse/hootsuite-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/LokiMCPUniverse/hootsuite-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/LokiMCPUniverse/hootsuite-mcp-server?style=for-the-badge)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server/commits)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MCP](https://img.shields.io/badge/Model_Context_Protocol-DC143C?style=for-the-badge)](https://modelcontextprotocol.io)

[![Commit Activity](https://img.shields.io/github/commit-activity/m/LokiMCPUniverse/hootsuite-mcp-server?style=flat-square)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server/pulse)
[![Code Size](https://img.shields.io/github/languages/code-size/LokiMCPUniverse/hootsuite-mcp-server?style=flat-square)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server)
[![Contributors](https://img.shields.io/github/contributors/LokiMCPUniverse/hootsuite-mcp-server?style=flat-square)](https://github.com/LokiMCPUniverse/hootsuite-mcp-server/graphs/contributors)

</div>

A Model Context Protocol (MCP) server for integrating Hootsuite with GenAI applications.

## Overview

Social media management platform

## Features

- Comprehensive Hootsuite API coverage
- Multiple authentication methods
- Enterprise-ready with rate limiting
- Full error handling and retry logic
- Async support for better performance

## Installation

```bash
pip install hootsuite-mcp-server
```

Or install from source:

```bash
git clone https://github.com/asklokesh/hootsuite-mcp-server.git
cd hootsuite-mcp-server
pip install -e .
```

## Configuration

Create a `.env` file in your project root with your Hootsuite API credentials:

```env
# Option 1: OAuth Access Token (recommended)
HOOTSUITE_ACCESS_TOKEN=your_access_token_here

# Option 2: API Key and Secret
HOOTSUITE_API_KEY=your_api_key_here
HOOTSUITE_API_SECRET=your_api_secret_here
```

See `.env.example` for all available configuration options.

## Quick Start

### Running the MCP Server

```bash
# Using the command line entry point
hootsuite-mcp

# Or using Python
python -m hootsuite_mcp.server
```

### Using as a Library

```python
import asyncio
from hootsuite_mcp import HootsuiteMCPServer

async def main():
    server = HootsuiteMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

## Available Tools

The MCP server provides the following tools:

1. **create_post** - Create and schedule social media posts
2. **get_social_profiles** - Get connected social media profiles
3. **get_posts** - Retrieve scheduled and published posts
4. **delete_post** - Delete posts by ID
5. **get_analytics** - Get analytics data for profiles

## Development

See [DEVELOPER.md](DEVELOPER.md) for detailed development documentation.

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term
```

### Validation

Run the validation script to check the installation:

```bash
python validate.py
```

## CI/CD

The project uses GitHub Actions for continuous integration:
- **Quick Test** - Runs on every push/PR for fast feedback
- **Full CI** - Comprehensive testing across multiple Python versions and OSes

## License

MIT License - see LICENSE file for details
