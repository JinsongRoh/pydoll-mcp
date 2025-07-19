"""Test suite for browser manager functionality."""

import asyncio
import pytest
import os
from unittest.mock import Mock, AsyncMock, patch

from pydoll_mcp.browser_manager import (
    BrowserManager,
    BrowserInstance,
    BrowserPool,
    BrowserMetrics,
    get_browser_manager,
    cleanup_browser_manager,
)


class TestBrowserMetrics:
    """Test browser metrics functionality."""
    
    def test_init(self):
        """Test metrics initialization."""
        metrics = BrowserMetrics(max_history=50)
        assert metrics.max_history == 50
        assert metrics.error_count == 0
        assert metrics.total_operations == 0
        assert len(metrics.navigation_times) == 0
    
    def test_record_navigation(self):
        """Test navigation recording."""
        metrics = BrowserMetrics()
        metrics.record_navigation(1.5)
        metrics.record_navigation(2.0)
        
        assert metrics.total_operations == 2
        assert len(metrics.navigation_times) == 2
        assert metrics.get_avg_navigation_time() == 1.75
    
    def test_error_tracking(self):
        """Test error tracking and rate calculation."""
        metrics = BrowserMetrics()
        
        # Record some operations
        for _ in range(10):
            metrics.record_navigation(1.0)
        
        # Record some errors
        metrics.record_error()
        metrics.record_error()
        
        assert metrics.error_count == 2
        assert metrics.get_error_rate() == 20.0  # 2/10 * 100
    
    def test_max_history(self):
        """Test that history is limited by max_history."""
        metrics = BrowserMetrics(max_history=3)
        
        # Record more than max_history
        for i in range(5):
            metrics.record_navigation(float(i))
        
        # Should only keep last 3
        assert len(metrics.navigation_times) == 3
        assert list(metrics.navigation_times) == [2.0, 3.0, 4.0]


class TestBrowserInstance:
    """Test browser instance functionality."""
    
    @pytest.fixture
    def mock_browser(self):
        """Create a mock browser."""
        browser = Mock()
        browser.stop = AsyncMock()
        return browser
    
    @pytest.fixture
    def browser_instance(self, mock_browser):
        """Create a browser instance."""
        return BrowserInstance(mock_browser, "chrome", "test_123")
    
    def test_init(self, browser_instance):
        """Test instance initialization."""
        assert browser_instance.browser_type == "chrome"
        assert browser_instance.instance_id == "test_123"
        assert browser_instance.is_active
        assert len(browser_instance.tabs) == 0
        assert isinstance(browser_instance.metrics, BrowserMetrics)
    
    def test_activity_tracking(self, browser_instance):
        """Test activity tracking."""
        import time
        
        initial_time = browser_instance.last_activity
        time.sleep(0.1)
        browser_instance.update_activity()
        
        assert browser_instance.last_activity > initial_time
        assert browser_instance.get_idle_time() < 0.1
    
    def test_uptime(self, browser_instance):
        """Test uptime calculation."""
        import time
        
        time.sleep(0.1)
        uptime = browser_instance.get_uptime()
        
        assert uptime >= 0.1
        assert uptime < 0.2
    
    @pytest.mark.asyncio
    async def test_tab_context(self, browser_instance):
        """Test tab context manager."""
        # Add a mock tab
        mock_tab = Mock()
        browser_instance.tabs["tab1"] = mock_tab
        
        # Test successful context
        async with browser_instance.tab_context("tab1") as tab:
            assert tab == mock_tab
        
        # Test missing tab
        with pytest.raises(ValueError):
            async with browser_instance.tab_context("missing"):
                pass
    
    @pytest.mark.asyncio
    async def test_cleanup(self, browser_instance, mock_browser):
        """Test cleanup functionality."""
        # Add some mock tabs
        mock_tab1 = Mock()
        mock_tab1.close = AsyncMock()
        mock_tab2 = Mock()
        mock_tab2.close = AsyncMock()
        
        browser_instance.tabs["tab1"] = mock_tab1
        browser_instance.tabs["tab2"] = mock_tab2
        
        await browser_instance.cleanup()
        
        # Check tabs were closed
        mock_tab1.close.assert_called_once()
        mock_tab2.close.assert_called_once()
        
        # Check browser was stopped
        mock_browser.stop.assert_called_once()
        
        # Check instance is inactive
        assert not browser_instance.is_active
        assert len(browser_instance.tabs) == 0


class TestBrowserPool:
    """Test browser pool functionality."""
    
    @pytest.fixture
    def browser_pool(self):
        """Create a browser pool."""
        return BrowserPool(max_size=2)
    
    @pytest.fixture
    def mock_instance(self):
        """Create a mock browser instance."""
        instance = Mock(spec=BrowserInstance)
        instance.is_active = True
        instance.cleanup = AsyncMock()
        return instance
    
    @pytest.mark.asyncio
    async def test_acquire_empty(self, browser_pool):
        """Test acquiring from empty pool."""
        instance = await browser_pool.acquire()
        assert instance is None
    
    @pytest.mark.asyncio
    async def test_acquire_release(self, browser_pool, mock_instance):
        """Test acquire and release cycle."""
        # Add instance to available
        browser_pool.available.append(mock_instance)
        
        # Acquire
        acquired = await browser_pool.acquire()
        assert acquired == mock_instance
        assert len(browser_pool.available) == 0
        assert mock_instance in browser_pool.in_use
        
        # Release
        await browser_pool.release(mock_instance)
        assert len(browser_pool.available) == 1
        assert mock_instance not in browser_pool.in_use
    
    @pytest.mark.asyncio
    async def test_pool_size_limit(self, browser_pool):
        """Test pool size limit enforcement."""
        instances = []
        for i in range(3):
            instance = Mock(spec=BrowserInstance)
            instance.is_active = True
            instance.cleanup = AsyncMock()
            instances.append(instance)
        
        # Release all instances
        for instance in instances:
            browser_pool.in_use.add(instance)
            await browser_pool.release(instance)
        
        # Pool should only keep max_size instances
        assert len(browser_pool.available) == 2
        
        # The extra instance should be cleaned up
        instances[2].cleanup.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_clear(self, browser_pool):
        """Test clearing the pool."""
        # Add some instances
        for i in range(2):
            instance = Mock(spec=BrowserInstance)
            instance.cleanup = AsyncMock()
            browser_pool.available.append(instance)
        
        # Add in-use instance
        in_use = Mock(spec=BrowserInstance)
        in_use.cleanup = AsyncMock()
        browser_pool.in_use.add(in_use)
        
        await browser_pool.clear()
        
        # All instances should be cleaned up
        assert len(browser_pool.available) == 0
        assert len(browser_pool.in_use) == 0
        
        for instance in [*browser_pool.available, in_use]:
            instance.cleanup.assert_called()


class TestBrowserManager:
    """Test browser manager functionality."""
    
    @pytest.fixture
    def browser_manager(self):
        """Create a browser manager."""
        return BrowserManager()
    
    @pytest.fixture
    def mock_chrome_class(self):
        """Mock Chrome class."""
        with patch('pydoll_mcp.browser_manager.Chrome') as mock:
            instance = Mock()
            instance.start = AsyncMock()
            instance.stop = AsyncMock()
            mock.return_value = instance
            yield mock
    
    def test_init(self, browser_manager):
        """Test manager initialization."""
        assert browser_manager.max_browsers == 3
        assert browser_manager.max_tabs_per_browser == 10
        assert browser_manager.cleanup_interval == 300
        assert browser_manager.idle_timeout == 1800
        assert not browser_manager._is_running
    
    @pytest.mark.asyncio
    async def test_start_stop(self, browser_manager):
        """Test starting and stopping manager."""
        await browser_manager.start()
        assert browser_manager._is_running
        assert browser_manager._cleanup_task is not None
        
        await browser_manager.stop()
        assert not browser_manager._is_running
        assert browser_manager._cleanup_task.cancelled()
    
    def test_generate_browser_id(self, browser_manager):
        """Test browser ID generation."""
        id1 = browser_manager._generate_browser_id()
        id2 = browser_manager._generate_browser_id()
        
        assert id1.startswith("browser_")
        assert id2.startswith("browser_")
        assert id1 != id2
    
    def test_get_browser_options_caching(self, browser_manager):
        """Test browser options caching."""
        with patch('pydoll_mcp.browser_manager.ChromiumOptions') as mock_options:
            mock_options.return_value = Mock()
            
            # First call - cache miss
            options1 = browser_manager._get_browser_options(headless=True)
            assert browser_manager.global_stats["cache_misses"] == 1
            assert browser_manager.global_stats["cache_hits"] == 0
            
            # Second call with same params - cache hit
            options2 = browser_manager._get_browser_options(headless=True)
            assert browser_manager.global_stats["cache_misses"] == 1
            assert browser_manager.global_stats["cache_hits"] == 1
            
            # Options should be the same object
            assert options1 is options2
    
    @pytest.mark.asyncio
    async def test_create_browser(self, browser_manager, mock_chrome_class):
        """Test browser creation."""
        with patch('pydoll_mcp.browser_manager.PYDOLL_AVAILABLE', True):
            instance = await browser_manager.create_browser("chrome")
            
            assert instance.browser_type == "chrome"
            assert instance.instance_id in browser_manager.browsers
            assert browser_manager.global_stats["total_browsers_created"] == 1
    
    @pytest.mark.asyncio
    async def test_create_browser_pool_reuse(self, browser_manager):
        """Test browser creation with pool reuse."""
        # Create a mock pooled instance
        pooled = Mock(spec=BrowserInstance)
        pooled.instance_id = "pooled_123"
        
        browser_manager.browser_pool.available.append(pooled)
        
        with patch('pydoll_mcp.browser_manager.PYDOLL_AVAILABLE', True):
            instance = await browser_manager.create_browser()
            
            assert instance == pooled
            assert browser_manager.global_stats["total_browsers_created"] == 0
    
    @pytest.mark.asyncio
    async def test_destroy_browser(self, browser_manager):
        """Test browser destruction."""
        # Create a mock instance
        instance = Mock(spec=BrowserInstance)
        instance.cleanup = AsyncMock()
        browser_manager.browsers["test_123"] = instance
        
        await browser_manager.destroy_browser("test_123")
        
        assert "test_123" not in browser_manager.browsers
        assert browser_manager.global_stats["total_browsers_destroyed"] == 1
    
    @pytest.mark.asyncio
    async def test_cleanup_idle_browsers(self, browser_manager):
        """Test idle browser cleanup."""
        # Create mock instances
        active = Mock(spec=BrowserInstance)
        active.get_idle_time = Mock(return_value=100)  # Not idle
        
        idle = Mock(spec=BrowserInstance)
        idle.get_idle_time = Mock(return_value=3600)  # Idle
        idle.cleanup = AsyncMock()
        
        browser_manager.browsers = {
            "active": active,
            "idle": idle,
        }
        
        await browser_manager._cleanup_idle_browsers()
        
        # Only idle browser should be removed
        assert "active" in browser_manager.browsers
        assert "idle" not in browser_manager.browsers
    
    def test_get_statistics(self, browser_manager):
        """Test statistics retrieval."""
        # Add a mock instance
        instance = Mock(spec=BrowserInstance)
        instance.browser_type = "chrome"
        instance.get_uptime = Mock(return_value=100.0)
        instance.get_idle_time = Mock(return_value=10.0)
        instance.tabs = {}
        instance.stats = {"total_navigations": 5}
        instance.metrics = Mock()
        instance.metrics.get_avg_navigation_time = Mock(return_value=1.5)
        instance.metrics.get_error_rate = Mock(return_value=5.0)
        
        browser_manager.browsers["test_123"] = instance
        
        stats = browser_manager.get_statistics()
        
        assert stats["active_browsers"] == 1
        assert stats["max_browsers"] == 3
        assert len(stats["browser_details"]) == 1
        
        detail = stats["browser_details"][0]
        assert detail["id"] == "test_123"
        assert detail["type"] == "chrome"
        assert detail["uptime"] == 100.0
        assert detail["idle_time"] == 10.0
        assert detail["avg_navigation_time"] == 1.5
        assert detail["error_rate"] == 5.0
    
    @pytest.mark.asyncio
    async def test_ensure_tab_methods(self, browser_manager):
        """Test backward compatibility tab method injection."""
        mock_tab = Mock()
        
        # Tab without methods
        assert not hasattr(mock_tab, 'fetch_domain_commands')
        assert not hasattr(mock_tab, 'get_parent_element')
        
        # Ensure methods
        await browser_manager.ensure_tab_methods(mock_tab)
        
        # Methods should be added
        assert hasattr(mock_tab, 'fetch_domain_commands')
        assert hasattr(mock_tab, 'get_parent_element')
        
        # Test the stub methods
        result = await mock_tab.fetch_domain_commands()
        assert "error" in result
        
        result = await mock_tab.get_parent_element("test")
        assert "error" in result


class TestGlobalFunctions:
    """Test global browser manager functions."""
    
    def test_get_browser_manager(self):
        """Test getting global browser manager."""
        manager1 = get_browser_manager()
        manager2 = get_browser_manager()
        
        # Should be the same instance
        assert manager1 is manager2
        assert isinstance(manager1, BrowserManager)
    
    @pytest.mark.asyncio
    async def test_cleanup_browser_manager(self):
        """Test cleaning up global browser manager."""
        # Get manager first
        manager = get_browser_manager()
        await manager.start()
        
        # Cleanup
        await cleanup_browser_manager()
        
        # Should create new instance
        new_manager = get_browser_manager()
        assert new_manager is not manager