# Hootsuite MCP Server

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

Create a `.env` file or set environment variables according to Hootsuite API requirements.

## Quick Start

```python
from hootsuite_mcp import HootsuiteMCPServer

# Initialize the server
server = HootsuiteMCPServer()

# Start the server
server.start()
```

## License

MIT License - see LICENSE file for details
