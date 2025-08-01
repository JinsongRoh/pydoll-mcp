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
from collections import deque
from contextlib import asynccontextmanager

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


class BrowserMetrics:
    """Track browser performance metrics."""
    
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.navigation_times = deque(maxlen=max_history)
        self.memory_usage = deque(maxlen=max_history)
        self.cpu_usage = deque(maxlen=max_history)
        self.error_count = 0
        self.total_operations = 0
    
    def record_navigation(self, duration: float):
        """Record navigation timing."""
        self.navigation_times.append(duration)
        self.total_operations += 1
    
    def get_avg_navigation_time(self) -> float:
        """Get average navigation time."""
        if not self.navigation_times:
            return 0.0
        return sum(self.navigation_times) / len(self.navigation_times)
    
    def record_error(self):
        """Record an error occurrence."""
        self.error_count += 1
    
    def get_error_rate(self) -> float:
        """Get error rate as percentage."""
        if self.total_operations == 0:
            return 0.0
        return (self.error_count / self.total_operations) * 100


class BrowserInstance:
    """Represents a managed browser instance with metadata."""
    
    def __init__(self, browser, browser_type: str, instance_id: str):
        from datetime import datetime
        self.browser = browser
        self.browser_type = browser_type
        self.instance_id = instance_id
        self.created_at = datetime.now()
        self.tabs: Dict[str, Tab] = {}
        self.active_tab_id: Optional[str] = None
        self.is_active = True
        self.last_activity = time.time()
        self.metrics = BrowserMetrics()
        
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
        from datetime import datetime
        return (datetime.now() - self.created_at).total_seconds()
    
    def get_idle_time(self) -> float:
        """Get time since last activity in seconds."""
        return time.time() - self.last_activity
    
    def to_dict(self) -> dict:
        """Convert browser instance to serializable dictionary."""
        return {
            "instance_id": self.instance_id,
            "browser_type": self.browser_type,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "uptime": self.get_uptime(),
            "idle_time": self.get_idle_time(),
            "tabs_count": len(self.tabs),
            "stats": self.stats,
            "error_rate": self.metrics.get_error_rate(),
            "avg_navigation_time": self.metrics.get_avg_navigation_time()
        }
    
    @asynccontextmanager
    async def tab_context(self, tab_id: str):
        """Context manager for safe tab operations."""
        tab = self.tabs.get(tab_id)
        if not tab:
            raise ValueError(f"Tab {tab_id} not found")
        
        try:
            yield tab
            self.update_activity()
        except Exception as e:
            self.metrics.record_error()
            logger.error(f"Error in tab operation: {e}")
            raise
    
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


class BrowserPool:
    """Pool of browser instances for improved resource management."""
    
    def __init__(self, max_size: int = 3):
        self.max_size = max_size
        self.available = deque()
        self.in_use = set()
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> Optional[BrowserInstance]:
        """Acquire a browser instance from the pool."""
        async with self._lock:
            if self.available:
                instance = self.available.popleft()
                self.in_use.add(instance)
                return instance
            return None
    
    async def release(self, instance: BrowserInstance):
        """Release a browser instance back to the pool."""
        async with self._lock:
            if instance in self.in_use:
                self.in_use.remove(instance)
                if len(self.available) < self.max_size and instance.is_active:
                    self.available.append(instance)
                else:
                    await instance.cleanup()
    
    async def clear(self):
        """Clear all instances from the pool."""
        async with self._lock:
            # Cleanup available instances
            while self.available:
                instance = self.available.popleft()
                await instance.cleanup()
            
            # Cleanup in-use instances
            for instance in list(self.in_use):
                await instance.cleanup()
            self.in_use.clear()


class BrowserManager:
    """Centralized browser management for PyDoll MCP Server."""
    
    def __init__(self):
        self.browsers: Dict[str, BrowserInstance] = {}
        self.default_browser_type = os.getenv("PYDOLL_BROWSER_TYPE", "chrome").lower()
        self.max_browsers = int(os.getenv("PYDOLL_MAX_BROWSERS", "3"))
        self.max_tabs_per_browser = int(os.getenv("PYDOLL_MAX_TABS_PER_BROWSER", "10"))
        self.cleanup_interval = int(os.getenv("PYDOLL_CLEANUP_INTERVAL", "300"))  # 5 minutes
        self.idle_timeout = int(os.getenv("PYDOLL_IDLE_TIMEOUT", "1800"))  # 30 minutes
        
        # Browser pool for better resource management
        self.browser_pool = BrowserPool(max_size=self.max_browsers)
        
        # Global statistics
        self.global_stats = {
            "total_browsers_created": 0,
            "total_browsers_destroyed": 0,
            "total_errors": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }
        
        # Cleanup task
        self._cleanup_task = None
        self._is_running = False
        
        # Performance optimization: Browser option cache
        self._options_cache = {}
        
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
        await self.browser_pool.clear()
        logger.info("BrowserManager stopped")
    
    def _generate_browser_id(self) -> str:
        """Generate a unique browser instance ID."""
        import uuid
        return f"browser_{uuid.uuid4().hex[:8]}"
    
    def _generate_tab_id(self) -> str:
        """Generate a unique tab ID."""
        import uuid
        return f"tab_{uuid.uuid4().hex[:8]}"
    
    async def _check_existing_chrome_processes(self):
        """Check for existing Chrome processes and warn user."""
        import psutil
        chrome_processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                        chrome_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if chrome_processes:
                logger.warning(f"Found {len(chrome_processes)} existing Chrome processes. "
                             "This may cause conflicts. Consider closing Chrome or using a custom user data directory.")
                # Add a unique user data directory to avoid conflicts
                import tempfile
                temp_dir = tempfile.mkdtemp(prefix="pydoll_chrome_")
                logger.info(f"Using temporary user data directory: {temp_dir}")
                return temp_dir
        except ImportError:
            logger.debug("psutil not available, skipping Chrome process check")
        except Exception as e:
            logger.debug(f"Error checking Chrome processes: {e}")
        
        return None
    
    def _get_browser_options(self, **kwargs) -> ChromiumOptions:
        """Create browser options based on configuration and parameters."""
        if not ChromiumOptions:
            raise RuntimeError("PyDoll not available - ChromiumOptions not imported")
        
        # Create cache key from kwargs (convert lists to tuples for hashability)
        def make_hashable(obj):
            if isinstance(obj, list):
                return tuple(obj)
            elif isinstance(obj, dict):
                return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
            return obj
        
        hashable_kwargs = {k: make_hashable(v) for k, v in kwargs.items()}
        cache_key = hash(frozenset(hashable_kwargs.items()))
        
        # Check cache first
        if cache_key in self._options_cache:
            self.global_stats["cache_hits"] += 1
            return self._options_cache[cache_key]
        
        self.global_stats["cache_misses"] += 1
        
        options = ChromiumOptions()
        
        # Environment-based defaults
        headless = kwargs.get("headless", os.getenv("PYDOLL_HEADLESS", "false").lower() == "true")
        window_width = int(kwargs.get("window_width", os.getenv("PYDOLL_WINDOW_WIDTH", "1920")))
        window_height = int(kwargs.get("window_height", os.getenv("PYDOLL_WINDOW_HEIGHT", "1080")))
        
        # Configure options
        if headless:
            try:
                options.add_argument("--headless=new")  # Use new headless mode
            except Exception:
                pass
        
        try:
            options.add_argument(f"--window-size={window_width},{window_height}")
        except Exception:
            pass
        
        # Stealth and performance options (Chrome compatible)
        if os.getenv("PYDOLL_STEALTH_MODE", "true").lower() == "true":
            # Enhanced stealth options for modern Chrome
            # Note: --no-first-run and --no-default-browser-check are already added by PyDoll
            stealth_args = [
                # "--no-default-browser-check",  # Already added by PyDoll
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--disable-extensions",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-ipc-flooding-protection",
                "--disable-component-extensions-with-background-pages",
                "--disable-default-apps",
                "--disable-sync",
                "--disable-background-networking",
                "--disable-client-side-phishing-detection",
            ]
            
            for arg in stealth_args:
                try:
                    options.add_argument(arg)
                except Exception:
                    # Skip if argument already exists
                    pass
        
        # Additional stability options (removed --disable-gpu-sandbox for security)
        stability_args = [
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox",
        ]
        
        for arg in stability_args:
            try:
                options.add_argument(arg)
            except Exception:
                # Skip if argument already exists
                pass
        
        # Enhanced performance optimizations
        if os.getenv("PYDOLL_DISABLE_IMAGES", "false").lower() == "true":
            try:
                options.add_argument("--disable-images")
            except Exception:
                pass
        
        # Windows-specific optimizations for better compatibility
        if os.name == 'nt':  # Windows
            try:
                # Windows-specific Chrome arguments for better stability
                options.add_argument("--disable-features=VizDisplayCompositor,VizHitTestSurfaceLayer")
                options.add_argument("--disable-backgrounding-occluded-windows")
                options.add_argument("--disable-renderer-backgrounding")
                options.add_argument("--force-device-scale-factor=1")
            except Exception:
                pass
        
        # Memory and CPU optimizations
        performance_args = [
            "--memory-pressure-off",
            "--max_old_space_size=4096",
            "--aggressive-cache-discard",
            "--disable-background-mode",
            "--disable-hang-monitor",
            "--disable-prompt-on-repost",
            "--disable-domain-reliability",
        ]
        
        for arg in performance_args:
            try:
                options.add_argument(arg)
            except Exception:
                # Skip if argument already exists
                pass
        
        # User data directory configuration
        user_data_dir = kwargs.get("user_data_dir")
        if user_data_dir:
            try:
                options.add_argument(f"--user-data-dir={user_data_dir}")
                logger.debug(f"Using custom user data directory: {user_data_dir}")
            except Exception:
                pass
        
        # Proxy configuration
        proxy = kwargs.get("proxy", os.getenv("PYDOLL_PROXY"))
        if proxy:
            try:
                options.add_argument(f"--proxy-server={proxy}")
            except Exception:
                pass
        
        # Custom binary path
        binary_path = kwargs.get("binary_path", os.getenv("PYDOLL_BINARY_PATH"))
        if binary_path:
            options.binary_location = binary_path
        
        # Custom user data directory
        user_data_dir = kwargs.get("user_data_dir", os.getenv("PYDOLL_USER_DATA_DIR"))
        if user_data_dir:
            try:
                options.add_argument(f"--user-data-dir={user_data_dir}")
            except Exception:
                pass
        
        # Additional custom arguments
        custom_args = kwargs.get("custom_args", [])
        for arg in custom_args:
            try:
                options.add_argument(arg)
            except Exception:
                # Skip if argument already exists
                pass
        
        # Cache the options
        self._options_cache[cache_key] = options
        
        return options
    
    async def create_browser(self, browser_type: Optional[str] = None, **kwargs) -> BrowserInstance:
        """Create a new browser instance with optimized settings."""
        if not PYDOLL_AVAILABLE:
            raise RuntimeError("PyDoll library is not available. Please install with: pip install pydoll-python")
        
        # Check pool first
        pooled_instance = await self.browser_pool.acquire()
        if pooled_instance:
            logger.info(f"Reusing pooled browser instance {pooled_instance.instance_id}")
            return pooled_instance
        
        # Check browser limit
        if len(self.browsers) >= self.max_browsers:
            # Try to cleanup idle browsers
            await self._cleanup_idle_browsers()
            
            if len(self.browsers) >= self.max_browsers:
                raise RuntimeError(f"Maximum browser limit ({self.max_browsers}) reached")
        
        browser_type = browser_type or self.default_browser_type
        browser_id = self._generate_browser_id()
        
        try:
            logger.info(f"Creating new {browser_type} browser instance {browser_id}")
            
            # Check for existing Chrome processes if user data dir is default
            temp_user_data_dir = None
            if browser_type == "chrome" and not kwargs.get("user_data_dir"):
                temp_user_data_dir = await self._check_existing_chrome_processes()
                if temp_user_data_dir:
                    kwargs["user_data_dir"] = temp_user_data_dir
            
            # Get browser options
            options = self._get_browser_options(**kwargs)
            
            # Create browser based on type
            if browser_type == "chrome":
                browser = Chrome(options=options)
            elif browser_type == "edge":
                browser = Edge(options=options)
            else:
                raise ValueError(f"Unsupported browser type: {browser_type}")
            
            # Start browser - browser.start() returns the initial Tab
            start_time = time.time()
            initial_tab = await browser.start()
            startup_time = time.time() - start_time
            
            # Create browser instance
            instance = BrowserInstance(browser, browser_type, browser_id)
            instance.metrics.record_navigation(startup_time)
            
            # IMPORTANT: PyDoll's browser.start() ALWAYS returns the initial Tab object
            # We must register this tab immediately
            if initial_tab:
                default_tab_id = self._generate_tab_id()
                instance.tabs[default_tab_id] = initial_tab
                instance.active_tab_id = default_tab_id
                # Store the tab reference in browser object for compatibility
                instance.browser.tab = initial_tab
                logger.info(f"Registered initial tab from browser.start(): {default_tab_id}")
                
                # Enhanced Windows compatibility: Wait for tab to be fully ready
                try:
                    await asyncio.sleep(1)  # Give tab time to initialize
                    # Try to get tab title to ensure it's ready
                    await self._ensure_tab_ready(initial_tab, default_tab_id)
                except Exception as e:
                    logger.warning(f"Tab initialization check failed: {e}")
            else:
                # This should never happen with PyDoll
                logger.error("CRITICAL: No initial tab returned from browser.start() - this is unexpected!")
                raise RuntimeError("PyDoll browser.start() did not return a tab")
            
            # Store instance
            self.browsers[browser_id] = instance
            self.global_stats["total_browsers_created"] += 1
            
            logger.info(f"Browser {browser_id} created successfully in {startup_time:.2f}s with {len(instance.tabs)} initial tab(s)")
            return instance
            
        except Exception as e:
            self.global_stats["total_errors"] += 1
            logger.error(f"Failed to create browser: {e}")
            raise
    
    async def get_browser(self, browser_id: str) -> Optional[BrowserInstance]:
        """Get a browser instance by ID."""
        return self.browsers.get(browser_id)
    
    async def get_tab(self, browser_id: str, tab_id: str):
        """Get a tab from a browser instance."""
        instance = self.browsers.get(browser_id)
        if not instance:
            raise ValueError(f"Browser {browser_id} not found")
        
        tab = instance.tabs.get(tab_id)
        if not tab:
            raise ValueError(f"Tab {tab_id} not found in browser {browser_id}")
        
        return await self.ensure_tab_methods(tab)
    
    async def get_active_tab_id(self, browser_id: str) -> Optional[str]:
        """Get the active tab ID for a browser instance."""
        instance = self.browsers.get(browser_id)
        if not instance:
            return None
        
        # Return cached active tab if available
        if instance.active_tab_id and instance.active_tab_id in instance.tabs:
            return instance.active_tab_id
        
        # If no active tab cached, try to find one
        if instance.tabs:
            # Return the first available tab
            first_tab_id = next(iter(instance.tabs.keys()))
            instance.active_tab_id = first_tab_id
            return first_tab_id
        
        return None
    
    async def get_tab_with_fallback(self, browser_id: str, tab_id: Optional[str] = None):
        """Get a tab with automatic fallback to active tab if tab_id is None."""
        instance = self.browsers.get(browser_id)
        if not instance:
            raise ValueError(f"Browser {browser_id} not found")
        
        # If no tab_id provided, get the active tab
        if tab_id is None:
            tab_id = await self.get_active_tab_id(browser_id)
            if tab_id is None:
                raise ValueError(f"No active tab found in browser {browser_id}")
        
        # Get the specific tab
        tab = instance.tabs.get(tab_id)
        if not tab:
            # Try to get active tab as fallback
            active_tab_id = await self.get_active_tab_id(browser_id)
            if active_tab_id and active_tab_id != tab_id:
                tab = instance.tabs.get(active_tab_id)
                if tab:
                    logger.warning(f"Tab {tab_id} not found, using active tab {active_tab_id}")
                    tab_id = active_tab_id
            
            if not tab:
                raise ValueError(f"Tab {tab_id} not found in browser {browser_id}")
        
        return await self.ensure_tab_methods(tab), tab_id
    
    async def destroy_browser(self, browser_id: str):
        """Destroy a browser instance and cleanup resources."""
        instance = self.browsers.get(browser_id)
        if not instance:
            logger.warning(f"Browser {browser_id} not found")
            return
        
        try:
            logger.info(f"Destroying browser {browser_id}")
            
            # Release to pool first
            await self.browser_pool.release(instance)
            
            # Remove from active browsers
            del self.browsers[browser_id]
            self.global_stats["total_browsers_destroyed"] += 1
            
            logger.info(f"Browser {browser_id} destroyed successfully")
            
        except Exception as e:
            self.global_stats["total_errors"] += 1
            logger.error(f"Failed to destroy browser {browser_id}: {e}")
            raise
    
    async def cleanup_all(self):
        """Cleanup all browser instances."""
        logger.info("Cleaning up all browser instances")
        
        browser_ids = list(self.browsers.keys())
        for browser_id in browser_ids:
            try:
                await self.destroy_browser(browser_id)
            except Exception as e:
                logger.error(f"Failed to destroy browser {browser_id}: {e}")
        
        self.browsers.clear()
        logger.info("All browser instances cleaned up")
    
    async def _cleanup_idle_browsers(self):
        """Cleanup browsers that have been idle for too long."""
        current_time = time.time()
        idle_browsers = []
        
        for browser_id, instance in self.browsers.items():
            if instance.get_idle_time() > self.idle_timeout:
                idle_browsers.append(browser_id)
        
        for browser_id in idle_browsers:
            logger.info(f"Cleaning up idle browser {browser_id}")
            try:
                await self.destroy_browser(browser_id)
            except Exception as e:
                logger.error(f"Failed to cleanup idle browser {browser_id}: {e}")
    
    async def _periodic_cleanup(self):
        """Periodically cleanup idle resources."""
        while self._is_running:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_idle_browsers()
                
                # Log statistics
                logger.info(f"Browser stats: Active={len(self.browsers)}, "
                          f"Created={self.global_stats['total_browsers_created']}, "
                          f"Destroyed={self.global_stats['total_browsers_destroyed']}, "
                          f"Errors={self.global_stats['total_errors']}")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in periodic cleanup: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get browser manager statistics."""
        stats = {
            "active_browsers": len(self.browsers),
            "max_browsers": self.max_browsers,
            "global_stats": self.global_stats.copy(),
            "browser_details": [],
        }
        
        for browser_id, instance in self.browsers.items():
            stats["browser_details"].append({
                "id": browser_id,
                "type": instance.browser_type,
                "uptime": instance.get_uptime(),
                "idle_time": instance.get_idle_time(),
                "tabs": len(instance.tabs),
                "stats": instance.stats.copy(),
                "avg_navigation_time": instance.metrics.get_avg_navigation_time(),
                "error_rate": instance.metrics.get_error_rate(),
            })
        
        return stats
    
    async def _ensure_tab_ready(self, tab, tab_id: str):
        """Enhanced tab readiness check for Windows compatibility."""
        try:
            # Try multiple methods to ensure tab is ready
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    # Check if tab has basic properties
                    if hasattr(tab, 'page_title'):
                        title = await tab.page_title()
                        logger.debug(f"Tab {tab_id} title: {title}")
                        break
                    elif hasattr(tab, 'execute_script'):
                        # Try to execute a simple script to verify tab is ready
                        result = await tab.execute_script('return document.readyState;')
                        if result:
                            logger.debug(f"Tab {tab_id} ready state check passed")
                            break
                    else:
                        # Basic existence check
                        logger.debug(f"Tab {tab_id} basic existence check passed")
                        break
                except Exception as e:
                    if attempt == max_attempts - 1:
                        logger.warning(f"Tab readiness check failed after {max_attempts} attempts: {e}")
                    else:
                        await asyncio.sleep(0.5)  # Wait before retry
        except Exception as e:
            logger.warning(f"Tab readiness check error: {e}")

    # Backward compatibility methods
    async def ensure_tab_methods(self, tab):
        """Ensure tab has all required methods for compatibility."""
        if not hasattr(tab, 'fetch_domain_commands'):
            # Add stub method for older PyDoll versions
            async def fetch_domain_commands_stub(domain: Optional[str] = None):
                return {"error": "fetch_domain_commands not available in this PyDoll version"}
            tab.fetch_domain_commands = fetch_domain_commands_stub
        
        if not hasattr(tab, 'get_parent_element'):
            # Add stub method for older PyDoll versions
            async def get_parent_element_stub(selector: str):
                return {"error": "get_parent_element not available in this PyDoll version"}
            tab.get_parent_element = get_parent_element_stub
        
        return tab


# Global browser manager instance
_browser_manager: Optional[BrowserManager] = None


def get_browser_manager() -> BrowserManager:
    """Get the global browser manager instance."""
    global _browser_manager
    if _browser_manager is None:
        _browser_manager = BrowserManager()
    return _browser_manager


async def cleanup_browser_manager():
    """Cleanup the global browser manager."""
    global _browser_manager
    if _browser_manager:
        await _browser_manager.stop()
        _browser_manager = None


# Create global browser manager instance for easy access
browser_manager = get_browser_manager()