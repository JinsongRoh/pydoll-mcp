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
- One-click automatic Claude Desktop setup (NEW in v1.1.0!)
- Cross-platform encoding compatibility (NEW in v1.1.1!)

For installation and usage instructions, see:
https://github.com/JinsongRoh/pydoll-mcp
"""

__version__ = "1.5.14"
__author__ = "Jinsong Roh"
__email__ = "enjoydays@gmail.com"
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
    "get_pydoll_version",
    "get_package_info", 
    "health_check",
    "main",
]

# Version information tuple
VERSION_INFO = tuple(int(part) for part in __version__.split("."))

# Minimum Python version required
PYTHON_REQUIRES = ">=3.8"

# Core dependencies
CORE_DEPENDENCIES = [
    "pydoll-python>=2.3.1",
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
    "one_click_setup": "Automatic Claude Desktop configuration (NEW in v1.1.0!)",
    "encoding_compatibility": "Cross-platform encoding safety (NEW in v1.1.1!)",
}

# Tool categories and counts
TOOL_CATEGORIES = {
    "browser_management": 8,
    "navigation_control": 11,  # Added fetch_domain_commands
    "element_interaction": 16,  # Added get_parent_element
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

# Enhanced PyDoll version detection with robust fallback mechanisms
def get_pydoll_version():
    """Get PyDoll version with multiple detection methods and robust error handling."""
    try:
        # Method 1: Direct pydoll import
        import pydoll
        if hasattr(pydoll, '__version__'):
            version = pydoll.__version__
            if version and version != "unknown":
                return version
    except ImportError:
        pass
    except Exception:
        pass
    
    try:
        # Method 2: Through pydoll.browser module
        import pydoll.browser
        if hasattr(pydoll.browser, '__version__'):
            version = pydoll.browser.__version__
            if version and version != "unknown":
                return version
    except (ImportError, AttributeError):
        pass
    except Exception:
        pass
    
    try:
        # Method 3: Package metadata via importlib
        import importlib.metadata
        try:
            version = importlib.metadata.version('pydoll-python')
            if version:
                return version
        except importlib.metadata.PackageNotFoundError:
            pass
    except ImportError:
        pass
    except Exception:
        pass
    
    try:
        # Method 4: Pkg_resources fallback
        import pkg_resources
        try:
            version = pkg_resources.get_distribution('pydoll-python').version
            if version:
                return version
        except pkg_resources.DistributionNotFound:
            pass
    except ImportError:
        pass
    except Exception:
        pass
    
    try:
        # Method 5: Check if we can import pydoll at all
        import pydoll
        # If we can import but no version, assume it's working
        return "2.3.1+ (version detection failed)"
    except ImportError:
        pass
    except Exception:
        pass
    
    # If all methods fail
    return None

# Package information for debugging
def get_package_info():
    """Get comprehensive package information for debugging."""
    pydoll_version = get_pydoll_version()
    
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
        "pydoll_version": pydoll_version,
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
        pydoll_version = get_pydoll_version()
        if not pydoll_version:
            pydoll_version = "unknown"
    except ImportError:
        missing_deps.append("pydoll-python>=2.3.1")
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

# Enhanced health check function with system info
def health_check():
    """Perform a comprehensive health check of the package."""
    import platform
    
    health_info = {
        "version_ok": False,
        "dependencies_ok": False,
        "browser_available": False,
        "errors": [],
        "system_info": {},
    }
    
    # Add system information
    try:
        health_info["system_info"] = {
            "system": platform.system(),
            "platform": platform.platform(),
            "architecture": platform.architecture()[0],
            "python_version": platform.python_version(),
            "processor": platform.processor() or "Unknown",
        }
    except Exception as e:
        health_info["errors"].append(f"System info gathering failed: {e}")
    
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
        "setup_command": "pydoll-mcp-setup",
        "module_run": "python -m pydoll_mcp.server",
        "test_module": "python -m pydoll_mcp.server --test",
        "setup_module": "python -m pydoll_mcp.cli auto-setup",
    }

# Banner for CLI display
BANNER = f"""
[PyDoll] PyDoll MCP Server v{__version__}
Revolutionary Browser Automation for AI

* Features:
  * Zero-webdriver automation via Chrome DevTools Protocol
  * Intelligent Cloudflare Turnstile & reCAPTCHA v3 bypass  
  * Human-like interactions with advanced anti-detection
  * Real-time network monitoring & request interception
  * {TOTAL_TOOLS} powerful automation tools across {len(TOOL_CATEGORIES)} categories
  * One-click automatic Claude Desktop setup

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
  • One-click automatic Claude Desktop setup

🚀 Ready to revolutionize your browser automation!
"""

def print_banner():
    """Print the package banner with encoding safety."""
    import sys
    import locale
    
    # Try to determine the best banner to use
    banner_to_use = BANNER
    
    try:
        # Check if we can safely print emojis
        if hasattr(sys.stderr, 'encoding'):
            encoding = sys.stderr.encoding or 'utf-8'
            
            # Test if we can encode emojis with current encoding
            test_emoji = "🤖"
            test_emoji.encode(encoding)
            
            # If we get here, emojis are supported
            banner_to_use = BANNER_WITH_EMOJIS
            
    except (UnicodeEncodeError, AttributeError, LookupError):
        # Fall back to safe banner without emojis
        banner_to_use = BANNER
    
    try:
        # Try to print the banner to stderr (not stdout for MCP compliance)
        print(banner_to_use, file=sys.stderr)
    except UnicodeEncodeError:
        # Final fallback - simple text banner
        fallback_banner = f"""
PyDoll MCP Server v{__version__}
Revolutionary Browser Automation for AI

Features:
  - Zero-webdriver automation via Chrome DevTools Protocol
  - Intelligent Cloudflare Turnstile & reCAPTCHA v3 bypass  
  - Human-like interactions with advanced anti-detection
  - Real-time network monitoring & request interception
  - {TOTAL_TOOLS} powerful automation tools across {len(TOOL_CATEGORIES)} categories
  - One-click automatic Claude Desktop setup

Ready to revolutionize your browser automation!
"""
        print(fallback_banner, file=sys.stderr)
    except Exception as e:
        # Ultimate fallback
        print(f"PyDoll MCP Server v{__version__} - Starting...", file=sys.stderr)

# Export version for external access
def get_version():
    """Get the current package version."""
    return __version__

# For compatibility with other version detection methods
version = __version__
VERSION = __version__
