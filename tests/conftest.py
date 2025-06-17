"""Test configuration and fixtures for PyDoll MCP Server.

This module provides shared test configuration, fixtures, and utilities
for all test modules in the PyDoll MCP Server test suite.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from unittest.mock import AsyncMock, MagicMock

# Add the parent directory to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydoll_mcp.browser_manager import BrowserManager
from pydoll_mcp.server import PyDollMCPServer


# Test Configuration
TEST_TIMEOUT = 30  # seconds
BROWSER_TIMEOUT = 15  # seconds
INTEGRATION_TIMEOUT = 60  # seconds

# Test environment variables
os.environ["PYDOLL_LOG_LEVEL"] = "WARNING"  # Reduce log noise during tests
os.environ["PYDOLL_TEST_MODE"] = "1"


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "browser_required: mark test as requiring real browser"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers and skip conditions."""
    # Skip integration tests if requested
    if config.getoption("--no-integration"):
        skip_integration = pytest.mark.skip(reason="Integration tests disabled")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)
    
    # Skip browser tests if no browser available
    if not _is_browser_available():
        skip_browser = pytest.mark.skip(reason="Browser not available")
        for item in items:
            if "browser_required" in item.keywords:
                item.add_marker(skip_browser)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--no-integration",
        action="store_true",
        default=False,
        help="Skip integration tests"
    )
    parser.addoption(
        "--browser-type",
        action="store",
        default="chrome",
        help="Browser type for testing (chrome, edge)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=True,
        help="Run browsers in headless mode"
    )


# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Basic fixtures
@pytest.fixture
def mock_browser():
    """Create a mock browser instance."""
    browser = AsyncMock()
    browser.new_page = AsyncMock()
    browser.close = AsyncMock()
    browser.pages = []
    return browser


@pytest.fixture
def mock_tab():
    """Create a mock tab/page instance."""
    tab = AsyncMock()
    tab.goto = AsyncMock()
    tab.title = AsyncMock(return_value="Test Page")
    tab.url = "https://example.com"
    tab.screenshot = AsyncMock(return_value=b"fake_screenshot_data")
    tab.evaluate = AsyncMock(return_value="test_result")
    tab.wait_for_selector = AsyncMock()
    tab.click = AsyncMock()
    tab.fill = AsyncMock()
    tab.select_option = AsyncMock()
    tab.check = AsyncMock()
    tab.get_attribute = AsyncMock(return_value="test_value")
    return tab


@pytest.fixture
def mock_browser_manager():
    """Create a mock browser manager."""
    manager = AsyncMock(spec=BrowserManager)
    manager.browsers = {}
    manager.start_browser = AsyncMock(return_value="test-browser-id")
    manager.stop_browser = AsyncMock(return_value=True)
    manager.new_tab = AsyncMock(return_value="test-tab-id")
    manager.close_tab = AsyncMock(return_value=True)
    manager.get_tab = AsyncMock()
    manager.list_browsers = AsyncMock(return_value=[])
    manager.list_tabs = AsyncMock(return_value=[])
    manager.cleanup_all = AsyncMock()
    return manager


# Server fixtures
@pytest.fixture
async def test_server():
    """Create a test PyDoll MCP Server instance."""
    server = PyDollMCPServer("test-server")
    
    # Mock the browser manager to avoid real browser instances
    with pytest.mock.patch('pydoll_mcp.server.get_browser_manager') as mock_get_manager:
        mock_manager = AsyncMock()
        mock_get_manager.return_value = mock_manager
        
        await server.initialize()
        yield server
        await server.cleanup()


# Browser fixtures for integration tests
@pytest.fixture
async def real_browser_manager() -> AsyncGenerator[BrowserManager, None]:
    """Create a real browser manager for integration tests."""
    if not _is_browser_available():
        pytest.skip("Browser not available for integration testing")
    
    manager = BrowserManager()
    yield manager
    await manager.cleanup_all()


@pytest.fixture
async def browser_session(real_browser_manager, request):
    """Create a browser session for testing."""
    browser_type = request.config.getoption("--browser-type")
    headless = request.config.getoption("--headless")
    
    browser_id = await real_browser_manager.start_browser(
        browser_type=browser_type,
        headless=headless,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    
    yield real_browser_manager, browser_id
    
    await real_browser_manager.stop_browser(browser_id)


@pytest.fixture
async def tab_session(browser_session):
    """Create a tab session for testing."""
    manager, browser_id = browser_session
    
    tab_id = await manager.new_tab(browser_id)
    tab = await manager.get_tab(browser_id, tab_id)
    
    yield manager, browser_id, tab_id, tab
    
    await manager.close_tab(browser_id, tab_id)


# Test data fixtures
@pytest.fixture
def test_urls():
    """Provide test URLs for various scenarios."""
    return {
        "html": "https://httpbin.org/html",
        "json": "https://httpbin.org/json",
        "xml": "https://httpbin.org/xml",
        "form": "https://httpbin.org/forms/post",
        "redirect": "https://httpbin.org/redirect/1",
        "delay": "https://httpbin.org/delay/1",
        "status_404": "https://httpbin.org/status/404",
        "status_500": "https://httpbin.org/status/500",
    }


@pytest.fixture
def test_scripts():
    """Provide test JavaScript code snippets."""
    return {
        "get_title": "document.title",
        "get_url": "window.location.href",
        "scroll_to_top": "window.scrollTo(0, 0)",
        "get_elements": "document.querySelectorAll('*').length",
        "invalid_syntax": "this.is.invalid.javascript.code();",
        "async_operation": """
            new Promise((resolve) => {
                setTimeout(() => resolve('async_result'), 100);
            });
        """,
        "dom_manipulation": """
            const div = document.createElement('div');
            div.id = 'test-element';
            div.textContent = 'Test content';
            document.body.appendChild(div);
            return div.id;
        """
    }


# Utility fixtures
@pytest.fixture
def temp_directory(tmp_path):
    """Provide a temporary directory for file operations."""
    test_dir = tmp_path / "pydoll_mcp_test"
    test_dir.mkdir()
    return test_dir


@pytest.fixture
def sample_config():
    """Provide sample configuration data."""
    return {
        "browser": {
            "type": "chrome",
            "headless": True,
            "args": ["--no-sandbox", "--disable-dev-shm-usage"],
            "viewport": {"width": 1920, "height": 1080}
        },
        "server": {
            "timeout": 30,
            "debug": False,
            "log_level": "INFO"
        },
        "tools": {
            "screenshot_format": "png",
            "navigation_timeout": 30000,
            "element_timeout": 5000
        }
    }


# Mock helpers
class MockResponse:
    """Mock HTTP response object."""
    
    def __init__(self, status=200, url="https://example.com"):
        self.status = status
        self.url = url
        self.ok = status < 400


class MockElement:
    """Mock page element object."""
    
    def __init__(self, tag_name="div", text_content="Test", attributes=None):
        self.tag_name = tag_name
        self.text_content = text_content
        self.attributes = attributes or {}
    
    async def click(self):
        """Mock click method."""
        pass
    
    async def fill(self, value):
        """Mock fill method."""
        self.attributes["value"] = value
    
    async def get_attribute(self, name):
        """Mock get_attribute method."""
        return self.attributes.get(name)


# Test utilities
def _is_browser_available() -> bool:
    """Check if a browser is available for testing."""
    try:
        import subprocess
        
        # Check for Chrome
        try:
            subprocess.run(
                ["google-chrome", "--version"],
                capture_output=True,
                check=True,
                timeout=5
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Check for Chromium
        try:
            subprocess.run(
                ["chromium-browser", "--version"],
                capture_output=True,
                check=True,
                timeout=5
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return False
        
    except Exception:
        return False


def create_mock_operation_result(success=True, data=None, error=None):
    """Create a mock OperationResult for testing."""
    from pydoll_mcp.models import OperationResult
    
    return OperationResult(
        success=success,
        message="Test operation",
        data=data or {"test": True},
        error=error
    )


def assert_operation_result(result, expected_success=True):
    """Assert that a result is a valid OperationResult with expected success."""
    import json
    
    assert len(result) == 1
    assert result[0].type == "text"
    
    data = json.loads(result[0].text)
    assert isinstance(data, dict)
    assert "success" in data
    assert data["success"] == expected_success
    
    if expected_success:
        assert "data" in data
    else:
        assert "error" in data
    
    return data


# Performance testing utilities
@pytest.fixture
def performance_monitor():
    """Monitor performance metrics during test execution."""
    import time
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.start_memory = None
            self.metrics = {}
        
        def start(self):
            self.start_time = time.time()
            self.start_memory = process.memory_info().rss
        
        def stop(self):
            if self.start_time:
                self.metrics["duration"] = time.time() - self.start_time
                self.metrics["memory_delta"] = process.memory_info().rss - self.start_memory
                self.metrics["memory_peak"] = process.memory_info().rss
        
        def assert_performance(self, max_duration=None, max_memory_mb=None):
            if max_duration and self.metrics.get("duration", 0) > max_duration:
                pytest.fail(f"Test took too long: {self.metrics['duration']:.2f}s > {max_duration}s")
            
            if max_memory_mb:
                memory_mb = self.metrics.get("memory_delta", 0) / (1024 * 1024)
                if memory_mb > max_memory_mb:
                    pytest.fail(f"Test used too much memory: {memory_mb:.2f}MB > {max_memory_mb}MB")
    
    return PerformanceMonitor()


# Async test helpers
async def wait_for_condition(condition_func, timeout=5.0, interval=0.1):
    """Wait for a condition to become true."""
    import time
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if await condition_func() if asyncio.iscoroutinefunction(condition_func) else condition_func():
            return True
        await asyncio.sleep(interval)
    
    return False


# Cleanup utilities
@pytest.fixture(autouse=True)
def cleanup_test_files(tmp_path):
    """Automatically cleanup test files after each test."""
    yield
    
    # Clean up any temporary files created during tests
    try:
        import shutil
        
        test_dirs = [
            tmp_path / "screenshots",
            tmp_path / "downloads",
            tmp_path / "profiles"
        ]
        
        for test_dir in test_dirs:
            if test_dir.exists():
                shutil.rmtree(test_dir)
                
    except Exception:
        pass  # Ignore cleanup errors


# Monkey patches for testing
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Setup test environment with necessary patches."""
    # Patch network requests to prevent external calls during unit tests
    if "PYDOLL_ALLOW_NETWORK" not in os.environ:
        monkeypatch.setenv("PYDOLL_TEST_MODE", "1")
        monkeypatch.setenv("PYDOLL_DISABLE_NETWORK", "1")
    
    # Set test-specific timeouts
    monkeypatch.setenv("PYDOLL_DEFAULT_TIMEOUT", "5000")
    monkeypatch.setenv("PYDOLL_NAVIGATION_TIMEOUT", "10000")
    
    yield
    
    # Any cleanup if needed
