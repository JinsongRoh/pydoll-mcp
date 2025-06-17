"""Test suite for PyDoll MCP Server.

This package contains comprehensive tests for the PyDoll MCP Server,
including unit tests, integration tests, and performance tests.

Test Structure:
- test_server.py: Unit tests for core server functionality
- test_integration.py: Integration tests with real browsers
- test_tools.py: Tests for individual tool handlers
- test_models.py: Tests for data models and validation
- test_cli.py: Tests for command-line interface
- conftest.py: Shared test configuration and fixtures

Test Categories:
- Unit Tests: Fast, isolated tests with mocks
- Integration Tests: Tests with real browser instances
- Performance Tests: Load and performance validation
- End-to-End Tests: Full workflow testing

Usage:
    # Run all tests
    pytest

    # Run only unit tests
    pytest -m "not integration"

    # Run with coverage
    pytest --cov=pydoll_mcp

    # Run integration tests
    pytest -m integration

    # Run performance tests
    pytest -m performance
"""

import sys
from pathlib import Path

# Ensure the package can be imported during testing
if __name__ == "__main__":
    # Add parent directory to path for direct execution
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

__version__ = "1.0.0"
__author__ = "Jinsong Roh"

# Test configuration
TEST_CONFIG = {
    "timeout": 30,
    "browser_timeout": 15,
    "integration_timeout": 60,
    "performance_timeout": 120,
    "max_concurrent_browsers": 3,
    "test_urls": {
        "base": "https://httpbin.org",
        "html": "https://httpbin.org/html",
        "json": "https://httpbin.org/json",
        "form": "https://httpbin.org/forms/post",
        "delay": "https://httpbin.org/delay/1"
    }
}

# Test utilities
def get_test_config():
    """Get test configuration."""
    return TEST_CONFIG.copy()


def setup_test_logging():
    """Setup logging for tests."""
    import logging
    logging.getLogger("pydoll_mcp").setLevel(logging.WARNING)
    logging.getLogger("mcp").setLevel(logging.WARNING)


# Auto-setup for test execution
setup_test_logging()
