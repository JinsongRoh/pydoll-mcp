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

__version__ = "1.1.3"
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

# Tool categories and counts
TOOL_CATEGORIES = {
    "browser_management": 8,
    "navigation_control": 10, 
    "element_interaction": 15,
    "screenshot_media": 6,
    "javascript_scripting": 8,
    "protection_bypass": 12,
    "network_monitoring": 10,
    "file_data_management": 8,
}

# Total tools available
TOTAL_TOOLS = sum(TOOL_CATEGORIES.values())

# Import main components for easy access
try:
    from .server import PyDollMCPServer, main
    from .browser_manager import get_browser_manager
except ImportError:
    # During installation, these may not be available yet
    PyDollMCPServer = None
    main = None
    get_browser_manager = None

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

# Dependency check function  
def check_dependencies():
    """Check if all required dependencies are available."""
    missing_deps = []
    
    try:
        import pydoll
        if hasattr(pydoll, '__version__'):
            pydoll_version = pydoll.__version__
        else:
            pydoll_version = "unknown"
    except ImportError:
        missing_deps.append("pydoll-python>=2.2.0")
        pydoll_version = None
    
    try:
        import mcp
    except ImportError:
        missing_deps.append("mcp>=1.0.0")
    
    try:
        import pydantic
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

# Health check function
def health_check():
    """Perform a comprehensive health check of the package."""
    health_info = {
        "version_ok": False,
        "dependencies_ok": False,
        "browser_available": False,
        "errors": [],
    }
    
    try:
        check_version()
        health_info["version_ok"] = True
    except Exception as e:
        health_info["errors"].append(f"Version check failed: {e}")
    
    try:
        dep_info = check_dependencies()
        health_info["dependencies_ok"] = dep_info["dependencies_ok"]
        health_info["pydoll_version"] = dep_info.get("pydoll_version")
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
