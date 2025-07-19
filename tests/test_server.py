"""Unit tests for PyDoll MCP Server.

This module contains unit tests for the core functionality of the PyDoll MCP Server.
"""

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from pydoll_mcp import __version__
from pydoll_mcp.server import PyDollMCPServer
from pydoll_mcp.browser_manager import BrowserManager
from pydoll_mcp.models import BrowserConfig, OperationResult


class TestPyDollMCPServer:
    """Test cases for the main PyDollMCPServer class."""
    
    @pytest.fixture
    def server(self):
        """Create a test server instance."""
        return PyDollMCPServer("test-server")
    
    def test_server_initialization(self, server):
        """Test server initialization."""
        assert server.server_name == "test-server"
        assert server.is_running is False
        assert server.browser_manager is None
        assert "total_requests" in server.stats
    
    @pytest.mark.asyncio
    async def test_server_initialize(self, server):
        """Test server component initialization."""
        with patch('pydoll_mcp.server.get_browser_manager') as mock_browser_manager:
            mock_browser_manager.return_value = MagicMock()
            
            await server.initialize()
            
            assert server.browser_manager is not None
            assert server.stats["uptime_start"] is not None
    
    @pytest.mark.asyncio
    async def test_server_cleanup(self, server):
        """Test server cleanup."""
        # Setup mock browser manager
        mock_browser_manager = AsyncMock()
        server.browser_manager = mock_browser_manager
        
        await server.cleanup()
        
        mock_browser_manager.cleanup_all.assert_called_once()
        assert server.is_running is False


class TestBrowserManager:
    """Test cases for the BrowserManager class."""
    
    @pytest.fixture
    def browser_manager(self):
        """Create a test browser manager instance."""
        return BrowserManager()
    
    def test_browser_manager_initialization(self, browser_manager):
        """Test browser manager initialization."""
        assert len(browser_manager.browsers) == 0
        assert browser_manager.default_config is not None
    
    @pytest.mark.asyncio
    async def test_start_browser(self, browser_manager):
        """Test browser startup."""
        with patch('pydoll_mcp.browser_manager.Chrome') as mock_chrome:
            mock_browser = AsyncMock()
            mock_chrome.return_value = mock_browser
            
            browser_id = await browser_manager.start_browser()
            
            assert browser_id in browser_manager.browsers
            mock_chrome.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_stop_browser(self, browser_manager):
        """Test browser shutdown."""
        # Add a mock browser
        mock_browser = AsyncMock()
        browser_id = "test-browser"
        browser_manager.browsers[browser_id] = mock_browser
        
        result = await browser_manager.stop_browser(browser_id)
        
        assert result is True
        assert browser_id not in browser_manager.browsers
        mock_browser.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_new_tab(self, browser_manager):
        """Test tab creation."""
        # Setup mock browser
        mock_browser = AsyncMock()
        mock_tab = AsyncMock()
        mock_browser.new_page.return_value = mock_tab
        
        browser_id = "test-browser"
        browser_manager.browsers[browser_id] = mock_browser
        
        tab_id = await browser_manager.new_tab(browser_id)
        
        assert tab_id is not None
        mock_browser.new_page.assert_called_once()


class TestModels:
    """Test cases for data models."""
    
    def test_browser_config_creation(self):
        """Test BrowserConfig model creation."""
        config = BrowserConfig(
            headless=True,
            width=1920,
            height=1080
        )
        
        assert config.headless is True
        assert config.width == 1920
        assert config.height == 1080
    
    def test_operation_result_success(self):
        """Test OperationResult success case."""
        result = OperationResult(
            success=True,
            message="Operation completed",
            data={"key": "value"}
        )
        
        assert result.success is True
        assert result.message == "Operation completed"
        assert result.data["key"] == "value"
        assert result.error is None
    
    def test_operation_result_failure(self):
        """Test OperationResult failure case."""
        result = OperationResult(
            success=False,
            message="Operation failed",
            error="Test error"
        )
        
        assert result.success is False
        assert result.message == "Operation failed"
        assert result.error == "Test error"
    
    def test_operation_result_json_serialization(self):
        """Test OperationResult JSON serialization."""
        result = OperationResult(
            success=True,
            message="Test",
            data={"test": True}
        )
        
        json_str = result.json()
        parsed = json.loads(json_str)
        
        assert parsed["success"] is True
        assert parsed["message"] == "Test"
        assert parsed["data"]["test"] is True


class TestToolHandlers:
    """Test cases for tool handlers."""
    
    @pytest.mark.asyncio
    async def test_browser_tool_handlers(self):
        """Test browser tool handlers."""
        with patch('pydoll_mcp.tools.browser_tools.get_browser_manager') as mock_manager:
            mock_browser_manager = AsyncMock()
            mock_manager.return_value = mock_browser_manager
            mock_browser_manager.start_browser.return_value = "browser-123"
            
            from pydoll_mcp.tools.browser_tools import handle_start_browser
            
            result = await handle_start_browser({
                "browser_type": "chrome",
                "headless": True
            })
            
            assert len(result) == 1
            assert result[0].type == "text"
            
            # Parse the result
            result_data = json.loads(result[0].text)
            assert result_data["success"] is True
            assert "browser_id" in result_data["data"]
    
    @pytest.mark.asyncio
    async def test_navigation_tool_handlers(self):
        """Test navigation tool handlers."""
        with patch('pydoll_mcp.tools.navigation_tools.get_browser_manager') as mock_manager:
            mock_browser_manager = AsyncMock()
            mock_tab = AsyncMock()
            mock_manager.return_value = mock_browser_manager
            mock_browser_manager.get_tab.return_value = mock_tab
            
            from pydoll_mcp.tools.navigation_tools import handle_navigate_to
            
            result = await handle_navigate_to({
                "browser_id": "browser-123",
                "url": "https://example.com"
            })
            
            assert len(result) == 1
            result_data = json.loads(result[0].text)
            assert result_data["success"] is True
    
    @pytest.mark.asyncio
    async def test_element_tool_handlers(self):
        """Test element tool handlers."""
        with patch('pydoll_mcp.tools.element_tools.get_browser_manager') as mock_manager:
            mock_browser_manager = AsyncMock()
            mock_tab = AsyncMock()
            mock_manager.return_value = mock_browser_manager
            mock_browser_manager.get_tab.return_value = mock_tab
            
            from pydoll_mcp.tools.element_tools import handle_find_element
            
            result = await handle_find_element({
                "browser_id": "browser-123",
                "selector": {"css": "button"}
            })
            
            assert len(result) == 1
            result_data = json.loads(result[0].text)
            assert result_data["success"] is True


class TestHealthCheck:
    """Test cases for health check functionality."""
    
    def test_health_check_basic(self):
        """Test basic health check."""
        from pydoll_mcp import health_check
        
        health_info = health_check()
        
        assert "version_ok" in health_info
        assert "dependencies_ok" in health_info
        assert "browser_available" in health_info
        assert "overall_status" in health_info
        assert "errors" in health_info
    
    @patch('pydoll_mcp.check_version')
    def test_health_check_version_failure(self, mock_check_version):
        """Test health check with version failure."""
        mock_check_version.side_effect = RuntimeError("Python version too old")
        
        from pydoll_mcp import health_check
        
        health_info = health_check()
        
        assert health_info["version_ok"] is False
        assert len(health_info["errors"]) > 0
        assert health_info["overall_status"] is False


class TestCLI:
    """Test cases for CLI functionality."""
    
    def test_cli_import(self):
        """Test CLI module import."""
        from pydoll_mcp.cli import cli
        
        assert cli is not None
    
    @patch('pydoll_mcp.cli.health_check')
    def test_test_installation_command(self, mock_health_check):
        """Test the test-installation CLI command."""
        mock_health_check.return_value = {
            "version_ok": True,
            "dependencies_ok": True,
            "browser_available": True,
            "overall_status": True,
            "errors": []
        }
        
        from click.testing import CliRunner
        from pydoll_mcp.cli import test_installation
        
        runner = CliRunner()
        result = runner.invoke(test_installation, ['--json-output'])
        
        assert result.exit_code == 0
        assert "overall_status" in result.output


class TestPackageInfo:
    """Test cases for package information."""
    
    def test_version_import(self):
        """Test version import."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert len(__version__.split('.')) >= 2
    
    def test_package_info(self):
        """Test package info function."""
        from pydoll_mcp import get_package_info
        
        info = get_package_info()
        
        assert "version" in info
        assert "author" in info
        assert "features" in info
        assert "total_tools" in info
        assert info["version"] == __version__


class TestAsyncUtils:
    """Test cases for async utilities."""
    
    @pytest.mark.asyncio
    async def test_async_timeout(self):
        """Test async timeout handling."""
        async def slow_function():
            await asyncio.sleep(2)
            return "done"
        
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(slow_function(), timeout=0.5)
    
    @pytest.mark.asyncio
    async def test_async_cancellation(self):
        """Test async task cancellation."""
        async def cancellable_task():
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                return "cancelled"
            return "completed"
        
        task = asyncio.create_task(cancellable_task())
        await asyncio.sleep(0.1)
        task.cancel()
        
        result = await task
        assert result == "cancelled"


# Fixtures and test configuration

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_browser():
    """Create a mock browser instance."""
    browser = AsyncMock()
    browser.new_page = AsyncMock()
    browser.close = AsyncMock()
    return browser


@pytest.fixture
def mock_tab():
    """Create a mock tab instance."""
    tab = AsyncMock()
    tab.goto = AsyncMock()
    tab.title = AsyncMock(return_value="Test Page")
    tab.url = "https://example.com"
    tab.screenshot = AsyncMock(return_value=b"fake_screenshot_data")
    return tab


# Test utilities

def create_test_operation_result(success: bool = True, data: dict = None):
    """Create a test OperationResult."""
    return OperationResult(
        success=success,
        message="Test operation",
        data=data or {"test": True},
        error=None if success else "Test error"
    )


def assert_valid_json_response(text_content):
    """Assert that a text content contains valid JSON."""
    try:
        data = json.loads(text_content.text)
        assert isinstance(data, dict)
        assert "success" in data
        return data
    except (json.JSONDecodeError, KeyError) as e:
        pytest.fail(f"Invalid JSON response: {e}")


# Performance tests

@pytest.mark.performance
class TestPerformance:
    """Performance test cases."""
    
    @pytest.mark.asyncio
    async def test_server_startup_time(self):
        """Test server startup performance."""
        import time
        
        start_time = time.time()
        server = PyDollMCPServer("perf-test")
        
        with patch('pydoll_mcp.server.get_browser_manager'):
            await server.initialize()
        
        startup_time = time.time() - start_time
        
        # Server should start in less than 5 seconds
        assert startup_time < 5.0
    
    @pytest.mark.asyncio
    async def test_tool_execution_time(self):
        """Test tool execution performance."""
        import time
        
        with patch('pydoll_mcp.tools.browser_tools.get_browser_manager') as mock_manager:
            mock_browser_manager = AsyncMock()
            mock_manager.return_value = mock_browser_manager
            mock_browser_manager.start_browser.return_value = "browser-123"
            
            from pydoll_mcp.tools.browser_tools import handle_start_browser
            
            start_time = time.time()
            await handle_start_browser({"browser_type": "chrome"})
            execution_time = time.time() - start_time
            
            # Tool should execute in less than 1 second
            assert execution_time < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
