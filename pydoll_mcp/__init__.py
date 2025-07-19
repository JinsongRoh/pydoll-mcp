"""PyDoll MCP Server - Revolutionary Browser Automation for AI.

This package provides a Model Context Protocol (MCP) server that brings the full power
of PyDoll browser automation to Claude and other MCP-compatible AI systems.

PyDoll MCP Server features:
- Zero webdriver browser automation via Chrome DevTools Protocol
- Intelligent Cloudflare Turnstile and reCAPTCHA v3 bypass
- Human-like interaction simulation with advanced anti-detection
- Real-time network monitoring and request interception
- Comprehensive element finding and interaction capabilities
- Professional screenshot and PDF generation
- Advanced JavaScript execution environment
- Complete browser lifecycle management

For installation and usage instructions, see:
https://github.com/JinsongRoh/pydoll-mcp
"""

__version__ = "1.1.4"
__author__ = "Jinsong Roh"
__email__ = "jinsongroh@gmail.com"
__license__ = "MIT"
__description__ = "Revolutionary Model Context Protocol server for PyDoll browser automation"
__url__ = "https://github.com/JinsongRoh/pydoll-mcp"

# Package metadata
__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__license__",
    "__description__",
    "__url__",
    "PyDollMCPServer",
    "get_browser_manager",
    "main",
]

# Version information tuple
VERSION_INFO = tuple(int(part) for part in __version__.split("."))

# Minimum Python version required
PYTHON_REQUIRES = ">=3.8"

# Core dependencies
CORE_DEPENDENCIES = [
    "pydoll-python>=2.2.0",
    "mcp>=1.0.0", 
    "pydantic>=2.0.0",
    "typing-extensions>=4.0.0",
]

# Feature information
FEATURES = {
    "browser_automation": "Zero-webdriver browser control via Chrome DevTools Protocol",
    "captcha_bypass": "Intelligent Cloudflare Turnstile and reCAPTCHA v3 solving",
    "stealth_mode": "Advanced anti-detection and human behavior simulation", 
    "network_control": "Real-time network monitoring and request interception",
    "element_finding": "Revolutionary natural attribute element finding",
    "media_capture": "Professional screenshot and PDF generation",
    "javascript_execution": "Advanced JavaScript execution environment",
    "multi_browser": "Chrome and Edge browser support",
    "async_performance": "Native asyncio-based high-performance automation",
    "mcp_integration": "Full Model Context Protocol server implementation",
}

# Dynamic tool counting - this will be updated by server.py when tools are loaded
TOOL_CATEGORIES = {
    "browser_management": {"count": 8, "description": "Browser lifecycle and session management"},
    "navigation_control": {"count": 6, "description": "Page navigation and control"},
    "element_interaction": {"count": 15, "description": "Element finding and interaction"},
    "screenshot_media": {"count": 8, "description": "Screenshot and media capture"},
    "javascript_scripting": {"count": 10, "description": "JavaScript execution and scripting"},
    "protection_bypass": {"count": 5, "description": "Captcha and protection bypass"},
    "network_monitoring": {"count": 4, "description": "Network monitoring and interception"},
}

# Total tools available - calculated from categories
TOTAL_TOOLS = sum(cat["count"] for cat in TOOL_CATEGORIES.values())

def update_tool_counts(tool_counts: dict):
    """Update tool category counts dynamically."""
    global TOTAL_TOOLS, TOOL_CATEGORIES
    
    for category, count in tool_counts.items():
        if category in TOOL_CATEGORIES:
            TOOL_CATEGORIES[category]["count"] = count
    
    TOTAL_TOOLS = sum(cat.get("count", 0) for cat in TOOL_CATEGORIES.values())

# Import main components for easy access
try:
    from .server import PyDollMCPServer, main
    from .browser_manager import get_browser_manager
except ImportError:
    # During installation, these may not be available yet
    PyDollMCPServer = None
    main = None
    get_browser_manager = None

# Enhanced PyDoll version detection
def get_pydoll_version():
    """Get PyDoll version with multiple detection methods."""
    try:
        import pydoll
        
        # Method 1: Check __version__ attribute
        if hasattr(pydoll, '__version__') and pydoll.__version__ != "unknown":
            return pydoll.__version__
        
        # Method 2: Try importlib.metadata (Python 3.8+)
        try:
            import importlib.metadata
            return importlib.metadata.version('pydoll-python')
        except Exception:
            pass
        
        # Method 3: Try older pkg_resources
        try:
            import pkg_resources
            return pkg_resources.get_distribution('pydoll-python').version
        except Exception:
            pass
        
        # Method 4: Check version attribute
        if hasattr(pydoll, 'version'):
            return pydoll.version
        
        # Method 5: Check VERSION attribute
        if hasattr(pydoll, 'VERSION'):
            return pydoll.VERSION
        
        # Method 6: Feature-based version detection
        try:
            from pydoll.browser import Chrome
            if hasattr(Chrome, 'create_session'):  # v2.2.1+ feature
                return "2.2.1"
            else:
                return "2.2.0+"
        except (ImportError, AttributeError):
            return "2.0.0+"
        
    except ImportError:
        return None
    except Exception:
        return "unknown"

# Package information for debugging
def get_package_info():
    """Get comprehensive package information for debugging."""
    return {
        "version": __version__,
        "version_info": VERSION_INFO,
        "author": __author__,
        "email": __email__, 
        "license": __license__,
        "description": __description__,
        "url": __url__,
        "python_requires": PYTHON_REQUIRES,
        "core_dependencies": CORE_DEPENDENCIES,
        "features": FEATURES,
        "tool_categories": TOOL_CATEGORIES,
        "total_tools": TOTAL_TOOLS,
        "pydoll_version": get_pydoll_version(),
    }

# Version check function
def check_version():
    """Check if the current version meets requirements."""
    import sys
    
    if sys.version_info < (3, 8):
        raise RuntimeError(
            f"PyDoll MCP Server requires Python 3.8 or higher. "
            f"You are using Python {sys.version_info.major}.{sys.version_info.minor}"
        )
    
    return True

# Enhanced dependency check function  
def check_dependencies():
    """Check if all required dependencies are available."""
    missing_deps = []
    
    pydoll_version = get_pydoll_version()
    if pydoll_version is None:
        missing_deps.append("pydoll-python>=2.2.0")
    
    try:
        import mcp
    except ImportError:
        missing_deps.append("mcp>=1.0.0")
    
    try:
        import pydantic
        # Check if it's Pydantic v2
        if hasattr(pydantic, 'VERSION'):
            pydantic_version = pydantic.VERSION
        else:
            # For older versions or version detection
            try:
                import pkg_resources
                pydantic_version = pkg_resources.get_distribution("pydantic").version
            except:
                pydantic_version = "unknown"
    except ImportError:
        missing_deps.append("pydantic>=2.0.0")
    
    if missing_deps:
        raise ImportError(
            f"Missing required dependencies: {', '.join(missing_deps)}. "
            f"Please install with: pip install {' '.join(missing_deps)}"
        )
    
    return {
        "pydoll_version": pydoll_version,
        "dependencies_ok": True,
    }

# Health check function with improved reliability
def health_check():
    """Perform a comprehensive health check of the package."""
    health_info = {
        "version_ok": False,
        "dependencies_ok": False,
        "browser_available": False,
        "pydoll_version": "unknown",
        "python_version": None,
        "system_info": {},
        "errors": [],
    }
    
    # Add Python version info
    import sys
    health_info["python_version"] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # Add system info
    try:
        import platform
        health_info["system_info"] = {
            "system": platform.system(),
            "platform": platform.platform(),
            "architecture": platform.architecture()[0],
        }
    except Exception:
        pass
    
    try:
        check_version()
        health_info["version_ok"] = True
    except Exception as e:
        health_info["errors"].append(f"Version check failed: {e}")
    
    try:
        dep_info = check_dependencies()
        health_info["dependencies_ok"] = dep_info["dependencies_ok"]
        health_info["pydoll_version"] = dep_info.get("pydoll_version", "unknown")
    except Exception as e:
        health_info["errors"].append(f"Dependency check failed: {e}")
    
    try:
        # Test basic browser availability
        import pydoll.browser
        health_info["browser_available"] = True
    except Exception as e:
        health_info["errors"].append(f"Browser check failed: {e}")
    
    health_info["overall_status"] = (
        health_info["version_ok"] and 
        health_info["dependencies_ok"] and 
        health_info["browser_available"]
    )
    
    return health_info

# CLI entry point information
def get_cli_info():
    """Get information about available CLI commands."""
    return {
        "main_server": "pydoll-mcp",
        "server_alias": "pydoll-mcp-server", 
        "test_command": "pydoll-mcp-test",
        "module_run": "python -m pydoll_mcp.server",
        "test_module": "python -m pydoll_mcp.server --test",
        "status_check": "python -m pydoll_mcp.cli status",
    }

# Banner for CLI display
BANNER = f"""
PyDoll MCP Server v{__version__}
Revolutionary Browser Automation for AI

* Features:
  * Zero-webdriver automation via Chrome DevTools Protocol
  * Intelligent Cloudflare Turnstile & reCAPTCHA v3 bypass  
  * Human-like interactions with advanced anti-detection
  * Real-time network monitoring & request interception
  * {TOTAL_TOOLS} powerful automation tools across {len(TOOL_CATEGORIES)} categories

> Ready to revolutionize your browser automation!
"""

# Alternative banner with emojis for UTF-8 capable terminals
BANNER_WITH_EMOJIS = f"""
🤖 PyDoll MCP Server v{__version__}
Revolutionary Browser Automation for AI

✨ Features:
  • Zero-webdriver automation via Chrome DevTools Protocol
  • Intelligent Cloudflare Turnstile & reCAPTCHA v3 bypass  
  • Human-like interactions with advanced anti-detection
  • Real-time network monitoring & request interception
  • {TOTAL_TOOLS} powerful automation tools across {len(TOOL_CATEGORIES)} categories

🚀 Ready to revolutionize your browser automation!
"""

def print_banner(use_stderr=True):
    """Print the package banner with comprehensive encoding safety for all platforms.
    
    Args:
        use_stderr: If True, print to stderr instead of stdout (for MCP compatibility)
    """
    import sys
    import os
    
    # Choose output stream - use stderr for MCP compatibility
    output_stream = sys.stderr if use_stderr else sys.stdout
    
    # Determine which banner to use based on encoding capabilities
    banner_to_use = BANNER  # Safe default
    
    try:
        # Test emoji support
        test_emoji = "🤖"
        
        # Check current encoding
        current_encoding = 'utf-8'
        if hasattr(output_stream, 'encoding') and output_stream.encoding:
            current_encoding = output_stream.encoding.lower()
        
        # Try encoding test
        test_emoji.encode(current_encoding if current_encoding != 'cp949' else 'utf-8')
        
        # If we reach here and not using problematic encoding, use emoji banner
        if current_encoding not in ['cp949', 'euc-kr']:
            banner_to_use = BANNER_WITH_EMOJIS
            
    except (UnicodeEncodeError, UnicodeDecodeError, LookupError, AttributeError):
        # Stick with safe banner
        banner_to_use = BANNER
    
    # Print banner with multiple fallback levels
    try:
        print(banner_to_use, file=output_stream, flush=True)
        return
    except UnicodeEncodeError:
        pass
    
    # Fallback 1: Try simple banner without emojis
    try:
        print(BANNER, file=output_stream, flush=True)
        return
    except UnicodeEncodeError:
        pass
    
    # Fallback 2: Ultra-safe ASCII-only banner
    try:
        safe_banner = f"""
PyDoll MCP Server v{__version__}
Revolutionary Browser Automation for AI

Features:
  - Zero-webdriver automation via Chrome DevTools Protocol
  - Intelligent Cloudflare Turnstile & reCAPTCHA v3 bypass  
  - Human-like interactions with advanced anti-detection
  - Real-time network monitoring & request interception
  - {TOTAL_TOOLS} powerful automation tools across {len(TOOL_CATEGORIES)} categories

Ready to revolutionize your browser automation!
"""
        print(safe_banner, file=output_stream, flush=True)
        return
    except (UnicodeEncodeError, Exception):
        pass
    
    # Ultimate fallback: Minimal output
    try:
        print(f"PyDoll MCP Server v{__version__} - Starting...", file=output_stream, flush=True)
    except Exception:
        # If even this fails, just continue silently
        pass

# Export version for external access
def get_version():
    """Get the current package version."""
    return __version__

# For compatibility with other version detection methods
version = __version__
VERSION = __version__
