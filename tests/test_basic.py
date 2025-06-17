"""Basic tests for PyDoll MCP Server.

This module contains basic unit tests to ensure the core functionality
of the PyDoll MCP Server is working correctly.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from pydoll_mcp import __version__, health_check, get_package_info
from pydoll_mcp.server import PyDollMCPServer
from pydoll_mcp.browser_manager import BrowserManager
from pydoll_mcp.models import BrowserConfig, OperationResult


class TestPackageInfo:
    """Test package information and metadata."""
    
    def test_version_format(self):
        """Test version format is semantic versioning."""
        assert isinstance(__version__, str)
        version_parts = __version__.split('.')
        assert len(version_parts) == 3
        for part in version_parts:
            assert part.isdigit()
    
    def test_package_info(self):
        """Test package info contains required fields."""
        info = get_package_info()
        
        required_fields = [
            'version', 'author', 'description', 'url',
            'features', 'tool_categories', 'total_tools'
        ]
        
        for field in required_fields:
            assert field in info
            assert info[field] is not None
    
    def test_health_check(self):
        """Test health check returns proper structure."""
        health = health_check()
        
        required_keys = ['version_ok', 'dependencies_ok', 'overall_status', 'errors']
        for key in required_keys:
            assert key in health
        
        assert isinstance(health['errors'], list)
        assert isinstance(health['overall_status'], bool)


class TestBrowserManager:
    """Test browser manager functionality."""
    
    @pytest.fixture
    def browser_manager(self):
        """Create browser manager instance for testing."""
        return BrowserManager()
    
    @pytest.mark.asyncio
    async def test_browser_manager_initialization(self, browser_manager):
        """Test browser manager initializes correctly."""
        assert browser_manager is not None
        assert browser_manager.browsers == {}
        assert browser_manager.next_browser_id == 1
    
    @pytest.mark.asyncio
    async def test_browser_config_creation(self):
        """Test browser configuration creation."""
        config = BrowserConfig(
            browser_type="chrome",
            headless=True,
            args=["--no-sandbox"]
        )
        
        assert config.browser_type == "chrome"
        assert config.headless is True
        assert "--no-sandbox" in config.args
    
    @pytest.mark.asyncio
    @patch('pydoll_mcp.browser_manager.Chrome')
    async def test_start_browser_success(self, mock_chrome, browser_manager):
        """Test successful browser start."""
        # Mock PyDoll Chrome browser
        mock_browser_instance = AsyncMock()
        mock_chrome.return_value = mock_browser_instance
        
        browser_id = await browser_manager.start_browser("chrome", headless=True)
        
        assert browser_id is not None
        assert browser_id in browser_manager.browsers
        mock_chrome.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_start_browser_invalid_type(self, browser_manager):
        """Test starting browser with invalid type."""
        with pytest.raises(ValueError, match="Unsupported browser type"):
            await browser_manager.start_browser("firefox")


class TestOperationResult:
    """Test operation result model."""
    
    def test_success_result(self):
        """Test successful operation result."""
        result = OperationResult(
            success=True,
            message="Operation completed",
            data={"key": "value"}
        )
        
        assert result.success is True
        assert result.message == "Operation completed"
        assert result.data == {"key": "value"}
        assert result.error is None
    
    def test_error_result(self):
        """Test error operation result."""
        result = OperationResult(
            success=False,
            error="Something went wrong",
            message="Operation failed"
        )
        
        assert result.success is False
        assert result.error == "Something went wrong"
        assert result.message == "Operation failed"
        assert result.data is None
    
    def test_result_json_serialization(self):
        """Test operation result JSON serialization."""
        result = OperationResult(
            success=True,
            message="Test",
            data={"test": 123}
        )
        
        json_str = result.json()
        assert isinstance(json_str, str)
        assert "success" in json_str
        assert "message" in json_str


class TestMCPServer:
    """Test MCP server functionality."""
    
    @pytest.fixture
    def mcp_server(self):
        """Create MCP server instance for testing."""
        return PyDollMCPServer("test-server")
    
    def test_server_initialization(self, mcp_server):
        """Test MCP server initializes correctly."""
        assert mcp_server.server_name == "test-server"
        assert mcp_server.is_running is False
        assert mcp_server.browser_manager is None
        assert mcp_server.stats is not None
    
    @pytest.mark.asyncio
    async def test_server_cleanup(self, mcp_server):
        """Test server cleanup process."""
        # Mock browser manager
        mock_browser_manager = AsyncMock()
        mcp_server.browser_manager = mock_browser_manager
        
        await mcp_server.cleanup()
        
        assert mcp_server.is_running is False
        mock_browser_manager.cleanup_all.assert_called_once()


class TestToolSystem:
    """Test tool system functionality."""
    
    def test_tool_imports(self):
        """Test that all tool modules can be imported."""
        try:
            from pydoll_mcp.tools import (
                ALL_TOOLS, ALL_TOOL_HANDLERS,
                BROWSER_TOOLS, NAVIGATION_TOOLS,
                ELEMENT_TOOLS, SCREENSHOT_TOOLS,
                SCRIPT_TOOLS, ADVANCED_TOOLS
            )
            
            # Verify tools are lists
            assert isinstance(ALL_TOOLS, list)
            assert isinstance(BROWSER_TOOLS, list)
            assert isinstance(NAVIGATION_TOOLS, list)
            
            # Verify handlers are dictionaries
            assert isinstance(ALL_TOOL_HANDLERS, dict)
            
        except ImportError as e:
            pytest.skip(f"Tool modules not available: {e}")
    
    def test_tool_categories(self):
        """Test tool categories are properly defined."""
        try:
            from pydoll_mcp.tools import TOOL_CATEGORIES, TOTAL_TOOLS
            
            assert isinstance(TOOL_CATEGORIES, dict)
            assert isinstance(TOTAL_TOOLS, int)
            assert TOTAL_TOOLS > 0
            
            # Check category structure
            for category, info in TOOL_CATEGORIES.items():
                assert isinstance(category, str)
                assert isinstance(info, dict)
                assert "description" in info
                assert "tools" in info
                assert "count" in info
                
        except ImportError as e:
            pytest.skip(f"Tool categories not available: {e}")


class TestAsyncFunctionality:
    """Test async functionality and coroutines."""
    
    @pytest.mark.asyncio
    async def test_async_operation_simulation(self):
        """Test async operation simulation."""
        async def mock_async_operation():
            await asyncio.sleep(0.1)
            return {"result": "success"}
        
        result = await mock_async_operation()
        assert result["result"] == "success"
    
    @pytest.mark.asyncio
    async def test_async_error_handling(self):
        """Test async error handling."""
        async def failing_operation():
            await asyncio.sleep(0.1)
            raise ValueError("Simulated error")
        
        with pytest.raises(ValueError, match="Simulated error"):
            await failing_operation()


class TestConfigurationManagement:
    """Test configuration management."""
    
    def test_environment_variables(self):
        """Test environment variable handling."""
        import os
        
        # Test default values
        log_level = os.getenv("PYDOLL_LOG_LEVEL", "INFO")
        debug_mode = os.getenv("PYDOLL_DEBUG", "0")
        
        assert log_level in ["DEBUG", "INFO", "WARNING", "ERROR"]
        assert debug_mode in ["0", "1", "true", "false"]
    
    def test_browser_config_validation(self):
        """Test browser configuration validation."""
        # Valid config
        config = BrowserConfig(
            browser_type="chrome",
            headless=True
        )
        assert config.browser_type == "chrome"
        
        # Invalid browser type should raise error during validation
        with pytest.raises(ValueError):
            BrowserConfig(browser_type="invalid_browser")


@pytest.mark.integration
class TestIntegrationScenarios:
    """Integration test scenarios."""
    
    @pytest.mark.asyncio
    async def test_basic_server_lifecycle(self):
        """Test basic server lifecycle."""
        server = PyDollMCPServer("integration-test")
        
        # Test initialization
        await server.initialize()
        assert server.browser_manager is not None
        
        # Test cleanup
        await server.cleanup()
        assert server.is_running is False
    
    @pytest.mark.asyncio
    @patch('pydoll_mcp.browser_manager.Chrome')
    async def test_browser_automation_flow(self, mock_chrome):
        """Test basic browser automation flow."""
        # Mock browser and tab
        mock_browser = AsyncMock()
        mock_tab = AsyncMock()
        mock_tab.goto = AsyncMock()
        mock_tab.title = AsyncMock(return_value="Test Page")
        mock_browser.new_tab = AsyncMock(return_value=mock_tab)
        mock_chrome.return_value = mock_browser
        
        # Test the flow
        browser_manager = BrowserManager()
        browser_id = await browser_manager.start_browser("chrome")
        tab_id = await browser_manager.new_tab(browser_id)
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        await tab.goto("https://example.com")
        title = await tab.title()
        
        assert title == "Test Page"
        mock_tab.goto.assert_called_with("https://example.com")


# Test fixtures and utilities

@pytest.fixture
def mock_browser():
    """Create mock browser for testing."""
    browser = AsyncMock()
    browser.tabs = []
    browser.close = AsyncMock()
    return browser


@pytest.fixture
def mock_tab():
    """Create mock tab for testing."""
    tab = AsyncMock()
    tab.goto = AsyncMock()
    tab.title = AsyncMock(return_value="Mock Page")
    tab.url = "https://example.com"
    tab.evaluate = AsyncMock(return_value={"result": "success"})
    return tab


@pytest.fixture
def sample_operation_result():
    """Create sample operation result for testing."""
    return OperationResult(
        success=True,
        message="Test operation completed",
        data={
            "browser_id": "test-browser-1",
            "tab_id": "test-tab-1",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    )


# Parametrized tests

@pytest.mark.parametrize("browser_type,expected", [
    ("chrome", True),
    ("edge", True),
    ("firefox", False),
    ("safari", False),
])
def test_browser_type_support(browser_type, expected):
    """Test browser type support detection."""
    supported_browsers = ["chrome", "edge"]
    result = browser_type in supported_browsers
    assert result == expected


@pytest.mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR"])
def test_log_levels(log_level):
    """Test different log levels are valid."""
    import logging
    level = getattr(logging, log_level, None)
    assert level is not None
    assert isinstance(level, int)


# Performance tests

@pytest.mark.performance
def test_package_import_performance():
    """Test package import performance."""
    import time
    
    start_time = time.time()
    import pydoll_mcp
    import_time = time.time() - start_time
    
    # Import should complete within reasonable time
    assert import_time < 2.0, f"Package import took {import_time:.2f}s, too slow"


# Error handling tests

def test_error_handling_structure():
    """Test error handling provides proper structure."""
    result = OperationResult(
        success=False,
        error="TestError",
        message="This is a test error"
    )
    
    assert result.success is False
    assert result.error == "TestError"
    assert result.message == "This is a test error"
    assert result.data is None


# Configuration tests

def test_default_configuration():
    """Test default configuration values."""
    config = BrowserConfig()
    
    assert config.browser_type == "chrome"
    assert config.headless is False
    assert isinstance(config.args, list)
    assert config.viewport_size is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
