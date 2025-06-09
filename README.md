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
