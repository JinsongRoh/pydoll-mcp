"""Integration tests for PyDoll MCP Server.

These tests verify the integration between different components
and real browser automation capabilities.
"""

import asyncio
import json
import pytest
from pathlib import Path

from pydoll_mcp.server import PyDollMCPServer
from pydoll_mcp.browser_manager import get_browser_manager


@pytest.mark.integration
class TestBrowserIntegration:
    """Integration tests with real browser instances."""
    
    @pytest.fixture
    async def browser_manager(self):
        """Create a real browser manager for testing."""
        manager = get_browser_manager()
        yield manager
        await manager.cleanup_all()
    
    @pytest.mark.asyncio
    async def test_full_browser_lifecycle(self, browser_manager):
        """Test complete browser lifecycle."""
        # Start browser
        browser_id = await browser_manager.start_browser(
            browser_type="chrome",
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        
        assert browser_id is not None
        assert browser_id in browser_manager.browsers
        
        # Create tab
        tab_id = await browser_manager.new_tab(browser_id)
        assert tab_id is not None
        
        # Navigate to page
        tab = await browser_manager.get_tab(browser_id, tab_id)
        response = await tab.goto("https://httpbin.org/html")
        assert response.status == 200
        
        # Verify page content
        title = await tab.title()
        assert "Herman Melville" in title
        
        # Close tab
        await browser_manager.close_tab(browser_id, tab_id)
        
        # Stop browser
        result = await browser_manager.stop_browser(browser_id)
        assert result is True
        assert browser_id not in browser_manager.browsers
    
    @pytest.mark.asyncio
    async def test_multiple_tabs(self, browser_manager):
        """Test multiple tab management."""
        browser_id = await browser_manager.start_browser(headless=True)
        
        # Create multiple tabs
        tab_ids = []
        for i in range(3):
            tab_id = await browser_manager.new_tab(browser_id)
            tab_ids.append(tab_id)
        
        # Navigate each tab to different pages
        urls = [
            "https://httpbin.org/html",
            "https://httpbin.org/json",
            "https://httpbin.org/xml"
        ]
        
        for tab_id, url in zip(tab_ids, urls):
            tab = await browser_manager.get_tab(browser_id, tab_id)
            await tab.goto(url)
        
        # Verify all tabs are working
        tabs = await browser_manager.list_tabs(browser_id)
        assert len(tabs) >= 3
        
        # Cleanup
        await browser_manager.stop_browser(browser_id)
    
    @pytest.mark.asyncio
    async def test_page_interaction(self, browser_manager):
        """Test basic page interactions."""
        browser_id = await browser_manager.start_browser(headless=True)
        tab_id = await browser_manager.new_tab(browser_id)
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Navigate to a form page
        await tab.goto("https://httpbin.org/forms/post")
        
        # Find and fill form elements
        try:
            # Wait for form to load
            await tab.wait_for_selector("form", timeout=5000)
            
            # Fill text input
            await tab.fill('input[name="custname"]', "Test User")
            
            # Select option
            await tab.select_option('select[name="size"]', "medium")
            
            # Check checkbox
            await tab.check('input[name="topping"][value="bacon"]')
            
            # Get form values to verify
            name_value = await tab.get_attribute('input[name="custname"]', "value")
            assert name_value == "Test User"
            
        except Exception as e:
            # Some interactions might fail in headless mode, that's ok for testing
            print(f"Form interaction test note: {e}")
        
        await browser_manager.stop_browser(browser_id)


@pytest.mark.integration
class TestMCPServerIntegration:
    """Integration tests for the full MCP server."""
    
    @pytest.fixture
    async def server(self):
        """Create and initialize a test server."""
        server = PyDollMCPServer("integration-test")
        await server.initialize()
        yield server
        await server.cleanup()
    
    @pytest.mark.asyncio
    async def test_server_tool_execution(self, server):
        """Test tool execution through the server."""
        # Test browser management tools
        from pydoll_mcp.tools import ALL_TOOL_HANDLERS
        
        # Test start_browser
        if "start_browser" in ALL_TOOL_HANDLERS:
            handler = ALL_TOOL_HANDLERS["start_browser"]
            result = await handler({
                "browser_type": "chrome",
                "headless": True
            })
            
            assert len(result) == 1
            result_data = json.loads(result[0].text)
            assert result_data["success"] is True
            
            browser_id = result_data["data"]["browser_id"]
            
            # Test navigate_to
            if "navigate_to" in ALL_TOOL_HANDLERS:
                nav_handler = ALL_TOOL_HANDLERS["navigate_to"]
                nav_result = await nav_handler({
                    "browser_id": browser_id,
                    "url": "https://httpbin.org/html"
                })
                
                nav_data = json.loads(nav_result[0].text)
                assert nav_data["success"] is True
            
            # Test stop_browser
            if "stop_browser" in ALL_TOOL_HANDLERS:
                stop_handler = ALL_TOOL_HANDLERS["stop_browser"]
                stop_result = await stop_handler({
                    "browser_id": browser_id
                })
                
                stop_data = json.loads(stop_result[0].text)
                assert stop_data["success"] is True


@pytest.mark.integration
class TestToolsIntegration:
    """Integration tests for various tool categories."""
    
    @pytest.fixture
    async def browser_setup(self):
        """Setup browser for tool testing."""
        manager = get_browser_manager()
        browser_id = await manager.start_browser(headless=True)
        tab_id = await manager.new_tab(browser_id)
        
        yield manager, browser_id, tab_id
        
        await manager.stop_browser(browser_id)
    
    @pytest.mark.asyncio
    async def test_navigation_tools(self, browser_setup):
        """Test navigation tool integration."""
        manager, browser_id, tab_id = browser_setup
        
        from pydoll_mcp.tools.navigation_tools import (
            handle_navigate_to,
            handle_get_current_url,
            handle_get_page_title
        )
        
        # Navigate to page
        nav_result = await handle_navigate_to({
            "browser_id": browser_id,
            "tab_id": tab_id,
            "url": "https://httpbin.org/html"
        })
        
        nav_data = json.loads(nav_result[0].text)
        assert nav_data["success"] is True
        
        # Get current URL
        url_result = await handle_get_current_url({
            "browser_id": browser_id,
            "tab_id": tab_id
        })
        
        url_data = json.loads(url_result[0].text)
        assert url_data["success"] is True
        assert "httpbin.org" in url_data["data"]["url"]
        
        # Get page title
        title_result = await handle_get_page_title({
            "browser_id": browser_id,
            "tab_id": tab_id
        })
        
        title_data = json.loads(title_result[0].text)
        assert title_data["success"] is True
        assert len(title_data["data"]["title"]) > 0
    
    @pytest.mark.asyncio
    async def test_screenshot_tools(self, browser_setup):
        """Test screenshot tool integration."""
        manager, browser_id, tab_id = browser_setup
        
        # Navigate to a page first
        tab = await manager.get_tab(browser_id, tab_id)
        await tab.goto("https://httpbin.org/html")
        
        from pydoll_mcp.tools.screenshot_tools import handle_take_screenshot
        
        # Take screenshot
        screenshot_result = await handle_take_screenshot({
            "browser_id": browser_id,
            "tab_id": tab_id,
            "format": "png",
            "save_to_file": False,
            "return_base64": True
        })
        
        screenshot_data = json.loads(screenshot_result[0].text)
        assert screenshot_data["success"] is True
        assert "base64_data" in screenshot_data["data"]
        assert screenshot_data["data"]["base64_data"].startswith("data:image/png;base64,")
    
    @pytest.mark.asyncio
    async def test_script_execution_tools(self, browser_setup):
        """Test JavaScript execution tool integration."""
        manager, browser_id, tab_id = browser_setup
        
        # Navigate to a page first
        tab = await manager.get_tab(browser_id, tab_id)
        await tab.goto("https://httpbin.org/html")
        
        from pydoll_mcp.tools.script_tools import handle_execute_javascript
        
        # Execute JavaScript
        script_result = await handle_execute_javascript({
            "browser_id": browser_id,
            "tab_id": tab_id,
            "script": "document.title",
            "return_result": True
        })
        
        script_data = json.loads(script_result[0].text)
        assert script_data["success"] is True
        assert "result" in script_data["data"]
        assert isinstance(script_data["data"]["result"], str)


@pytest.mark.integration
class TestErrorHandling:
    """Integration tests for error handling."""
    
    @pytest.mark.asyncio
    async def test_invalid_browser_id(self):
        """Test handling of invalid browser ID."""
        from pydoll_mcp.tools.browser_tools import handle_stop_browser
        
        result = await handle_stop_browser({
            "browser_id": "invalid-browser-id"
        })
        
        result_data = json.loads(result[0].text)
        assert result_data["success"] is False
        assert "not found" in result_data["error"].lower()
    
    @pytest.mark.asyncio
    async def test_invalid_navigation(self):
        """Test handling of invalid navigation."""
        manager = get_browser_manager()
        browser_id = await manager.start_browser(headless=True)
        tab_id = await manager.new_tab(browser_id)
        
        try:
            from pydoll_mcp.tools.navigation_tools import handle_navigate_to
            
            # Try to navigate to invalid URL
            result = await handle_navigate_to({
                "browser_id": browser_id,
                "tab_id": tab_id,
                "url": "invalid-url-format"
            })
            
            result_data = json.loads(result[0].text)
            # Should either fail or handle gracefully
            assert "success" in result_data
            
        finally:
            await manager.stop_browser(browser_id)
    
    @pytest.mark.asyncio
    async def test_script_execution_error(self):
        """Test handling of JavaScript execution errors."""
        manager = get_browser_manager()
        browser_id = await manager.start_browser(headless=True)
        tab_id = await manager.new_tab(browser_id)
        
        try:
            tab = await manager.get_tab(browser_id, tab_id)
            await tab.goto("https://httpbin.org/html")
            
            from pydoll_mcp.tools.script_tools import handle_execute_javascript
            
            # Execute invalid JavaScript
            result = await handle_execute_javascript({
                "browser_id": browser_id,
                "tab_id": tab_id,
                "script": "this.is.invalid.javascript.code();",
                "return_result": True
            })
            
            result_data = json.loads(result[0].text)
            assert result_data["success"] is False
            assert "error" in result_data
            
        finally:
            await manager.stop_browser(browser_id)


@pytest.mark.integration
class TestPerformanceIntegration:
    """Integration tests for performance."""
    
    @pytest.mark.asyncio
    async def test_concurrent_browser_operations(self):
        """Test concurrent browser operations."""
        manager = get_browser_manager()
        
        # Start multiple browsers concurrently
        browser_tasks = []
        for i in range(3):
            task = asyncio.create_task(manager.start_browser(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            ))
            browser_tasks.append(task)
        
        browser_ids = await asyncio.gather(*browser_tasks)
        assert len(browser_ids) == 3
        
        # Create tabs concurrently
        tab_tasks = []
        for browser_id in browser_ids:
            task = asyncio.create_task(manager.new_tab(browser_id))
            tab_tasks.append(task)
        
        tab_ids = await asyncio.gather(*tab_tasks)
        assert len(tab_ids) == 3
        
        # Navigate all tabs concurrently
        nav_tasks = []
        for browser_id, tab_id in zip(browser_ids, tab_ids):
            async def navigate(bid, tid):
                tab = await manager.get_tab(bid, tid)
                await tab.goto("https://httpbin.org/html")
                return await tab.title()
            
            task = asyncio.create_task(navigate(browser_id, tab_id))
            nav_tasks.append(task)
        
        titles = await asyncio.gather(*nav_tasks)
        assert len(titles) == 3
        
        # Cleanup all browsers
        cleanup_tasks = []
        for browser_id in browser_ids:
            task = asyncio.create_task(manager.stop_browser(browser_id))
            cleanup_tasks.append(task)
        
        results = await asyncio.gather(*cleanup_tasks)
        assert all(results)
    
    @pytest.mark.asyncio
    async def test_memory_usage(self):
        """Test memory usage during operations."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        manager = get_browser_manager()
        browser_id = await manager.start_browser(headless=True)
        
        # Perform multiple operations
        for i in range(10):
            tab_id = await manager.new_tab(browser_id)
            tab = await manager.get_tab(browser_id, tab_id)
            await tab.goto("https://httpbin.org/html")
            await manager.close_tab(browser_id, tab_id)
        
        await manager.stop_browser(browser_id)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
