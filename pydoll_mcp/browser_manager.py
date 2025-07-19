"""Browser Manager for PyDoll MCP Server.

This module provides centralized browser instance management, including:
- Browser lifecycle management
- Resource cleanup and monitoring
- Configuration management
- Performance optimization
"""

import asyncio
import logging
import os
import time
import weakref
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

try:
    from pydoll.browser import Chrome, Edge
    from pydoll.browser.options import ChromiumOptions
    from pydoll.browser.tab import Tab
    PYDOLL_AVAILABLE = True
except ImportError:
    PYDOLL_AVAILABLE = False
    Chrome = None
    Edge = None
    ChromiumOptions = None
    Tab = None

logger = logging.getLogger(__name__)


class BrowserInstance:
    """Represents a managed browser instance with metadata."""
    
    def __init__(self, browser, browser_type: str, instance_id: str):
        self.browser = browser
        self.browser_type = browser_type
        self.instance_id = instance_id
        self.created_at = time.time()
        self.tabs: Dict[str, Tab] = {}
        self.is_active = True
        self.last_activity = time.time()
        
        # Performance metrics
        self.stats = {
            "total_tabs_created": 0,
            "total_navigations": 0,
            "total_screenshots": 0,
            "total_scripts_executed": 0,
        }
    
    def update_activity(self):
        """Update the last activity timestamp."""
        self.last_activity = time.time()
    
    def get_uptime(self) -> float:
        """Get browser instance uptime in seconds."""
        return time.time() - self.created_at
    
    def get_idle_time(self) -> float:
        """Get time since last activity in seconds."""
        return time.time() - self.last_activity
    
    async def cleanup(self):
        """Clean up browser instance and all associated resources."""
        try:
            logger.info(f"Cleaning up browser instance {self.instance_id}")
            
            # Close all tabs
            for tab_id, tab in list(self.tabs.items()):
                try:
                    await tab.close()
                except Exception as e:
                    logger.warning(f"Error closing tab {tab_id}: {e}")
            
            self.tabs.clear()
            
            # Stop browser
            if self.browser and hasattr(self.browser, 'stop'):
                await self.browser.stop()
            
            self.is_active = False
            logger.info(f"Browser instance {self.instance_id} cleaned up successfully")
            
        except Exception as e:
            logger.error(f"Error during browser cleanup: {e}")


class BrowserManager:
    """Centralized browser management for PyDoll MCP Server."""
    
    def __init__(self):
        self.browsers: Dict[str, BrowserInstance] = {}
        self.default_browser_type = os.getenv("PYDOLL_BROWSER_TYPE", "chrome").lower()
        self.max_browsers = int(os.getenv("PYDOLL_MAX_BROWSERS", "3"))
        self.max_tabs_per_browser = int(os.getenv("PYDOLL_MAX_TABS_PER_BROWSER", "10"))
        self.cleanup_interval = int(os.getenv("PYDOLL_CLEANUP_INTERVAL", "300"))  # 5 minutes
        self.idle_timeout = int(os.getenv("PYDOLL_IDLE_TIMEOUT", "1800"))  # 30 minutes
        
        # Global statistics
        self.global_stats = {
            "total_browsers_created": 0,
            "total_browsers_destroyed": 0,
            "total_errors": 0,
        }
        
        # Cleanup task
        self._cleanup_task = None
        self._is_running = False
        
        logger.info(f"BrowserManager initialized with max_browsers={self.max_browsers}")
    
    async def start(self):
        """Start the browser manager and background tasks."""
        if self._is_running:
            return
        
        self._is_running = True
        
        # Start cleanup task
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
        logger.info("BrowserManager started")
    
    async def stop(self):
        """Stop the browser manager and cleanup all resources."""
        self._is_running = False
        
        # Cancel cleanup task
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Cleanup all browsers
        await self.cleanup_all()
        logger.info("BrowserManager stopped")
    
    def _generate_browser_id(self) -> str:
        """Generate a unique browser instance ID."""
        import uuid
        return f"browser_{uuid.uuid4().hex[:8]}"
    
    def _get_browser_options(self, **kwargs) -> ChromiumOptions:
        """Create browser options based on configuration and parameters."""
        if not ChromiumOptions:
            raise RuntimeError("PyDoll not available - ChromiumOptions not imported")
        
        options = ChromiumOptions()
        
        # Environment-based defaults
        headless = kwargs.get("headless", os.getenv("PYDOLL_HEADLESS", "false").lower() == "true")
        window_width = int(kwargs.get("window_width", os.getenv("PYDOLL_WINDOW_WIDTH", "1920")))
        window_height = int(kwargs.get("window_height", os.getenv("PYDOLL_WINDOW_HEIGHT", "1080")))
        
        # Configure options
        if headless:
            options.add_argument("--headless")
        
        options.add_argument(f"--window-size={window_width},{window_height}")
        
        # Stealth and performance options
        if os.getenv("PYDOLL_STEALTH_MODE", "true").lower() == "true":
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
        
        # Performance optimizations
        if os.getenv("PYDOLL_DISABLE_IMAGES", "false").lower() == "true":
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
        
        # Proxy configuration
        proxy_server = kwargs.get("proxy", os.getenv("PYDOLL_PROXY_SERVER"))
        if proxy_server:
            options.add_argument(f"--proxy-server={proxy_server}")
        
        # User agent
        user_agent = kwargs.get("user_agent", os.getenv("PYDOLL_USER_AGENT"))
        if user_agent:
            options.add_argument(f"--user-agent={user_agent}")
        
        # Additional arguments from kwargs
        extra_args = kwargs.get("args", [])
        for arg in extra_args:
            options.add_argument(arg)
        
        return options
    
    async def create_browser(self, browser_type: Optional[str] = None, **kwargs) -> str:
        """Create a new browser instance.
        
        Args:
            browser_type: Type of browser ("chrome" or "edge")
            **kwargs: Additional browser configuration options
            
        Returns:
            Browser instance ID
        """
        if not PYDOLL_AVAILABLE:
            raise RuntimeError("PyDoll library not available - cannot create browser")
        
        # Check limits
        if len(self.browsers) >= self.max_browsers:
            # Try to cleanup idle browsers first
            await self._cleanup_idle_browsers()
            
            if len(self.browsers) >= self.max_browsers:
                raise RuntimeError(f"Maximum number of browsers ({self.max_browsers}) reached")
        
        browser_type = browser_type or self.default_browser_type
        browser_id = self._generate_browser_id()
        
        try:
            logger.info(f"Creating {browser_type} browser instance {browser_id}")
            
            # Get browser options
            options = self._get_browser_options(**kwargs)
            
            # Create browser based on type
            if browser_type.lower() == "chrome":
                browser = Chrome(options=options)
            elif browser_type.lower() == "edge":
                browser = Edge(options=options)
            else:
                raise ValueError(f"Unsupported browser type: {browser_type}")
            
            # Start browser
            await browser.start()
            
            # Create browser instance wrapper
            instance = BrowserInstance(browser, browser_type, browser_id)
            self.browsers[browser_id] = instance
            
            # Update statistics
            self.global_stats["total_browsers_created"] += 1
            
            logger.info(f"Browser instance {browser_id} created successfully")
            return browser_id
            
        except Exception as e:
            self.global_stats["total_errors"] += 1
            logger.error(f"Failed to create browser instance {browser_id}: {e}")
            raise
    
    async def get_browser(self, browser_id: str) -> BrowserInstance:
        """Get a browser instance by ID."""
        if browser_id not in self.browsers:
            raise ValueError(f"Browser instance {browser_id} not found")
        
        instance = self.browsers[browser_id]
        if not instance.is_active:
            raise ValueError(f"Browser instance {browser_id} is not active")
        
        instance.update_activity()
        return instance
    
    async def close_browser(self, browser_id: str):
        """Close a specific browser instance."""
        if browser_id not in self.browsers:
            logger.warning(f"Browser instance {browser_id} not found for closing")
            return
        
        instance = self.browsers[browser_id]
        
        try:
            await instance.cleanup()
            del self.browsers[browser_id]
            self.global_stats["total_browsers_destroyed"] += 1
            logger.info(f"Browser instance {browser_id} closed successfully")
            
        except Exception as e:
            logger.error(f"Error closing browser {browser_id}: {e}")
            self.global_stats["total_errors"] += 1
    
    async def create_tab(self, browser_id: str) -> str:
        """Create a new tab in a browser instance."""
        instance = await self.get_browser(browser_id)
        
        if len(instance.tabs) >= self.max_tabs_per_browser:
            raise RuntimeError(f"Maximum tabs per browser ({self.max_tabs_per_browser}) reached")
        
        try:
            # Create new tab
            tab = await instance.browser.new_tab()
            tab_id = f"tab_{len(instance.tabs)}_{int(time.time())}"
            
            instance.tabs[tab_id] = tab
            instance.stats["total_tabs_created"] += 1
            instance.update_activity()
            
            logger.info(f"Created tab {tab_id} in browser {browser_id}")
            return tab_id
            
        except Exception as e:
            logger.error(f"Failed to create tab in browser {browser_id}: {e}")
            self.global_stats["total_errors"] += 1
            raise
    
    async def get_tab(self, browser_id: str, tab_id: Optional[str] = None) -> Tab:
        """Get a tab from a browser instance."""
        instance = await self.get_browser(browser_id)
        
        if tab_id is None:
            # Return the active tab
            if hasattr(instance.browser, 'active_tab') and instance.browser.active_tab:
                return instance.browser.active_tab
            elif instance.tabs:
                # Return the first available tab
                return next(iter(instance.tabs.values()))
            else:
                # Create a new tab if none exist
                new_tab_id = await self.create_tab(browser_id)
                return instance.tabs[new_tab_id]
        
        if tab_id not in instance.tabs:
            raise ValueError(f"Tab {tab_id} not found in browser {browser_id}")
        
        return instance.tabs[tab_id]
    
    async def close_tab(self, browser_id: str, tab_id: str):
        """Close a specific tab."""
        instance = await self.get_browser(browser_id)
        
        if tab_id not in instance.tabs:
            logger.warning(f"Tab {tab_id} not found in browser {browser_id}")
            return
        
        try:
            tab = instance.tabs[tab_id]
            await tab.close()
            del instance.tabs[tab_id]
            instance.update_activity()
            
            logger.info(f"Closed tab {tab_id} in browser {browser_id}")
            
        except Exception as e:
            logger.error(f"Error closing tab {tab_id}: {e}")
            self.global_stats["total_errors"] += 1
    
    def list_browsers(self) -> List[Dict[str, Any]]:
        """List all browser instances with their status."""
        browsers = []
        
        for browser_id, instance in self.browsers.items():
            browsers.append({
                "id": browser_id,
                "type": instance.browser_type,
                "created_at": instance.created_at,
                "uptime": instance.get_uptime(),
                "idle_time": instance.get_idle_time(),
                "tabs_count": len(instance.tabs),
                "is_active": instance.is_active,
                "stats": instance.stats.copy(),
            })
        
        return browsers
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive browser manager statistics."""
        return {
            "global_stats": self.global_stats.copy(),
            "active_browsers": len(self.browsers),
            "max_browsers": self.max_browsers,
            "max_tabs_per_browser": self.max_tabs_per_browser,
            "default_browser_type": self.default_browser_type,
            "total_tabs": sum(len(instance.tabs) for instance in self.browsers.values()),
        }
    
    async def _cleanup_idle_browsers(self):
        """Clean up browsers that have been idle for too long."""
        current_time = time.time()
        browsers_to_close = []
        
        for browser_id, instance in self.browsers.items():
            if current_time - instance.last_activity > self.idle_timeout:
                browsers_to_close.append(browser_id)
        
        for browser_id in browsers_to_close:
            logger.info(f"Closing idle browser {browser_id}")
            await self.close_browser(browser_id)
    
    async def _periodic_cleanup(self):
        """Periodic cleanup task for idle browsers and resources."""
        while self._is_running:
            try:
                await asyncio.sleep(self.cleanup_interval)
                
                if not self._is_running:
                    break
                
                logger.debug("Running periodic cleanup")
                await self._cleanup_idle_browsers()
                
                # Log statistics periodically
                stats = self.get_stats()
                logger.debug(f"Browser manager stats: {stats}")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")
    
    async def cleanup_all(self):
        """Clean up all browser instances."""
        logger.info("Cleaning up all browser instances")
        
        cleanup_tasks = []
        for browser_id, instance in list(self.browsers.items()):
            cleanup_tasks.append(instance.cleanup())
        
        if cleanup_tasks:
            await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        
        self.browsers.clear()
        logger.info("All browser instances cleaned up")


# Global browser manager instance
_browser_manager: Optional[BrowserManager] = None


def get_browser_manager() -> BrowserManager:
    """Get the global browser manager instance."""
    global _browser_manager
    
    if _browser_manager is None:
        _browser_manager = BrowserManager()
    
    return _browser_manager


async def initialize_browser_manager():
    """Initialize and start the global browser manager."""
    manager = get_browser_manager()
    await manager.start()
    return manager


async def shutdown_browser_manager():
    """Shutdown the global browser manager."""
    global _browser_manager
    
    if _browser_manager:
        await _browser_manager.stop()
        _browser_manager = None
