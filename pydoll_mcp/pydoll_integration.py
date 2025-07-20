"""Enhanced PyDoll Integration Module.

This module provides enhanced integration with the pydoll-python library,
including error handling, compatibility checks, and Windows-specific optimizations.
"""

import asyncio
import logging
import os
import sys
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)

class PyDollIntegration:
    """Enhanced PyDoll integration with compatibility and error handling."""
    
    def __init__(self):
        self.pydoll_available = False
        self.pydoll_version = None
        self.compatibility_issues = []
        self._check_pydoll_availability()
    
    def _check_pydoll_availability(self):
        """Check PyDoll availability and version compatibility."""
        try:
            import pydoll
            self.pydoll_available = True
            self.pydoll_version = getattr(pydoll, '__version__', 'unknown')
            logger.info(f"PyDoll library available, version: {self.pydoll_version}")
            
            # Check for minimum required features
            self._check_required_features()
            
        except ImportError as e:
            self.pydoll_available = False
            logger.warning(f"PyDoll library not available: {e}")
            self.compatibility_issues.append("PyDoll library not installed")
        except Exception as e:
            self.pydoll_available = False
            logger.error(f"Error checking PyDoll availability: {e}")
            self.compatibility_issues.append(f"PyDoll check failed: {e}")
    
    def _check_required_features(self):
        """Check for required PyDoll features and compatibility."""
        try:
            from pydoll.browser import Chrome, Edge
            from pydoll.browser.options import ChromiumOptions
            from pydoll.browser.tab import Tab
            
            # Check for Windows-specific requirements
            if os.name == 'nt':
                self._check_windows_compatibility()
            
            logger.info("All required PyDoll features available")
            
        except ImportError as e:
            feature = str(e).split("'")[-2] if "'" in str(e) else "unknown"
            self.compatibility_issues.append(f"Missing PyDoll feature: {feature}")
            logger.warning(f"Missing PyDoll feature: {feature}")
    
    def _check_windows_compatibility(self):
        """Check Windows-specific compatibility requirements."""
        issues = []
        
        # Check Python version for Windows
        if sys.version_info < (3, 8):
            issues.append("Python 3.8+ recommended for Windows")
        
        # Check for Windows-specific dependencies
        try:
            import win32api
        except ImportError:
            issues.append("pywin32 recommended for Windows compatibility")
        
        # Check Chrome installation
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]
        
        chrome_found = any(os.path.exists(path) for path in chrome_paths)
        if not chrome_found:
            issues.append("Chrome browser not found in standard locations")
        
        if issues:
            self.compatibility_issues.extend(issues)
            logger.info(f"Windows compatibility notes: {'; '.join(issues)}")
    
    async def create_browser_with_enhanced_options(self, browser_type: str = "chrome", **kwargs):
        """Create browser with enhanced Windows compatibility options."""
        if not self.pydoll_available:
            raise RuntimeError("PyDoll library is not available")
        
        from pydoll.browser import Chrome, Edge
        from pydoll.browser.options import ChromiumOptions
        
        # Enhanced options for Windows compatibility
        options = ChromiumOptions()
        
        # Windows-specific optimizations
        if os.name == 'nt':
            windows_args = [
                "--disable-gpu-sandbox",
                "--disable-software-rasterizer", 
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-features=TranslateUI,VizDisplayCompositor",
                "--disable-ipc-flooding-protection",
                "--force-device-scale-factor=1",
                "--high-dpi-support=1",
                "--disable-extensions-http-throttling"
            ]
            
            for arg in windows_args:
                try:
                    options.add_argument(arg)
                except Exception:
                    pass
        
        # Enhanced stability options
        stability_args = [
            "--no-first-run",
            "--no-default-browser-check", 
            "--disable-default-apps",
            "--disable-popup-blocking",
            "--disable-translate",
            "--disable-component-update",
            "--disable-background-networking",
            "--disable-sync",
            "--disable-features=MediaRouter"
        ]
        
        for arg in stability_args:
            try:
                options.add_argument(arg)
            except Exception:
                pass
        
        # Apply user-provided options
        headless = kwargs.get("headless", False)
        if headless:
            try:
                options.add_argument("--headless=new")
            except Exception:
                options.add_argument("--headless")
        
        window_width = kwargs.get("window_width", 1920)
        window_height = kwargs.get("window_height", 1080)
        try:
            options.add_argument(f"--window-size={window_width},{window_height}")
        except Exception:
            pass
        
        # Custom user data directory for isolation
        user_data_dir = kwargs.get("user_data_dir")
        if user_data_dir:
            try:
                options.add_argument(f"--user-data-dir={user_data_dir}")
            except Exception:
                pass
        
        # Create browser instance
        if browser_type.lower() == "chrome":
            browser = Chrome(options=options)
        elif browser_type.lower() == "edge":
            browser = Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        
        return browser
    
    async def enhanced_tab_operations(self, tab, operation: str, **kwargs):
        """Enhanced tab operations with error handling and retries."""
        max_retries = kwargs.get("max_retries", 3)
        retry_delay = kwargs.get("retry_delay", 1.0)
        
        for attempt in range(max_retries):
            try:
                if operation == "navigate":
                    url = kwargs["url"]
                    await tab.goto(url)
                    
                elif operation == "find_element":
                    selector = kwargs["selector"]
                    element = await tab.find(selector)
                    return element
                    
                elif operation == "execute_script":
                    script = kwargs["script"]
                    result = await tab.execute_script(script)
                    return result
                    
                elif operation == "take_screenshot":
                    filename = kwargs.get("filename", "screenshot.png")
                    await tab.screenshot(filename)
                    
                else:
                    raise ValueError(f"Unknown operation: {operation}")
                
                return True
                
            except Exception as e:
                logger.warning(f"Tab operation '{operation}' failed (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(retry_delay)
        
        return False
    
    def get_compatibility_report(self) -> Dict[str, Any]:
        """Get comprehensive compatibility report."""
        return {
            "pydoll_available": self.pydoll_available,
            "pydoll_version": self.pydoll_version,
            "platform": sys.platform,
            "python_version": sys.version,
            "compatibility_issues": self.compatibility_issues,
            "recommendations": self._get_recommendations(),
            "status": "ready" if self.pydoll_available and not self.compatibility_issues else "issues_detected"
        }
    
    def _get_recommendations(self) -> list:
        """Get platform-specific recommendations."""
        recommendations = []
        
        if not self.pydoll_available:
            recommendations.append("Install pydoll-python: pip install pydoll-python")
        
        if os.name == 'nt':  # Windows
            recommendations.extend([
                "Install Chrome browser if not present",
                "Consider installing pywin32 for better Windows integration: pip install pywin32",
                "Run with elevated privileges if experiencing permission issues",
                "Ensure Windows Defender/antivirus allows browser automation"
            ])
        
        if self.compatibility_issues:
            recommendations.append("Review compatibility issues and update dependencies")
        
        return recommendations

# Global integration instance
_pydoll_integration: Optional[PyDollIntegration] = None

def get_pydoll_integration() -> PyDollIntegration:
    """Get the global PyDoll integration instance."""
    global _pydoll_integration
    if _pydoll_integration is None:
        _pydoll_integration = PyDollIntegration()
    return _pydoll_integration

# Convenience functions
def is_pydoll_available() -> bool:
    """Check if PyDoll is available."""
    return get_pydoll_integration().pydoll_available

def get_compatibility_issues() -> list:
    """Get list of compatibility issues."""
    return get_pydoll_integration().compatibility_issues

def get_pydoll_version() -> Optional[str]:
    """Get PyDoll version string."""
    return get_pydoll_integration().pydoll_version