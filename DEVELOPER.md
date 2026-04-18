# Developer Guide

## Setup

### Installation

```bash
# Clone the repository
git clone https://github.com/LokiMCPUniverse/hootsuite-mcp-server.git
cd hootsuite-mcp-server

# Install the package in development mode
pip install -e ".[dev]"
```

### Configuration

Create a `.env` file in the project root with your Hootsuite API credentials:

```env
HOOTSUITE_ACCESS_TOKEN=your_access_token_here
# OR
HOOTSUITE_API_KEY=your_api_key_here
HOOTSUITE_API_SECRET=your_api_secret_here
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term

# Run specific test file
pytest tests/test_config.py -v
```

## Linting

```bash
# Check code style
ruff check src tests

# Format code
ruff format src tests
```

## Project Structure

```
hootsuite-mcp-server/
├── src/
│   └── hootsuite_mcp/
│       ├── __init__.py      # Package initialization
│       ├── server.py         # MCP server implementation
│       ├── client.py         # Hootsuite API client
│       └── config.py         # Configuration management
├── tests/
│   ├── test_server.py        # Server tests
│   ├── test_client.py        # Client tests
│   └── test_config.py        # Config tests
├── .github/
│   └── workflows/
│       ├── ci.yml            # Full CI pipeline
│       └── quick-test.yml    # Quick test workflow
├── pyproject.toml            # Project configuration
└── README.md                 # User documentation
```

## Architecture

### MCP Server (`server.py`)
- Implements the Model Context Protocol server
- Provides 5 main tools:
  - `create_post`: Create and schedule social media posts
  - `get_social_profiles`: Get connected social profiles
  - `get_posts`: Retrieve scheduled/published posts
  - `delete_post`: Delete posts
  - `get_analytics`: Get analytics data

### Hootsuite Client (`client.py`)
- Async HTTP client for Hootsuite API
- Features:
  - Rate limiting (100 requests/minute by default)
  - Automatic retry with exponential backoff
  - Comprehensive error handling
  - Support for multiple authentication methods

### Configuration (`config.py`)
- Pydantic-based settings management
- Environment variable support
- Validation for credentials and settings

## Testing

The test suite includes:
- **Unit tests** for all components
- **Mock-based tests** to avoid external dependencies
- **Async test support** via pytest-asyncio
- **Coverage reporting** to ensure code quality

## Continuous Integration

GitHub Actions workflows automatically:
- Run tests on Python 3.10-3.13
- Test on Ubuntu, Windows, and macOS
- Check code style with ruff
- Generate coverage reports
- Build and verify the package

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Known Issues and Limitations

- The MCP protocol requires the `mcp` package which provides the server infrastructure
- Hootsuite API endpoints used are based on common patterns and may need adjustment
- Rate limiting is implemented client-side; server-side limits may differ
