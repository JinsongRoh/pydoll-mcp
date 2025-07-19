"""PyDoll MCP Server - Main Server Implementation.

This module provides the core MCP server implementation for PyDoll browser automation.
It handles tool registration, request routing, error handling, and lifecycle management.

Features:
- Complete browser automation via Chrome DevTools Protocol
- AI-powered captcha solving (Cloudflare Turnstile, reCAPTCHA v3)
- Advanced anti-detection and stealth mode
- Real-time network monitoring and interception
- Comprehensive element interaction capabilities
- Professional screenshot and PDF generation
"""

import asyncio
import logging
import os
import signal
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from . import __version__, BANNER, health_check, print_banner
from .browser_manager import get_browser_manager

# Import all tools and handlers from the tools module
try:
    from .tools import (
        ALL_TOOLS,
        ALL_TOOL_HANDLERS,
        BROWSER_TOOLS,
        NAVIGATION_TOOLS,
        ELEMENT_TOOLS,
        SCREENSHOT_TOOLS,
        SCRIPT_TOOLS,
        ADVANCED_TOOLS,
        PROTECTION_TOOLS,
        NETWORK_TOOLS,
        FILE_TOOLS,
        BROWSER_TOOL_HANDLERS,
        NAVIGATION_TOOL_HANDLERS,
        ELEMENT_TOOL_HANDLERS,
        SCREENSHOT_TOOL_HANDLERS,
        SCRIPT_TOOL_HANDLERS,
        ADVANCED_TOOL_HANDLERS,
        PROTECTION_TOOL_HANDLERS,
        NETWORK_TOOL_HANDLERS,
        FILE_TOOL_HANDLERS,
        TOTAL_TOOLS,
        TOOL_CATEGORIES
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Successfully imported {TOTAL_TOOLS} tools across {len(TOOL_CATEGORIES)} categories")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to import tools: {e}")
    # Fallback to empty tools if import fails
    ALL_TOOLS = []
    ALL_TOOL_HANDLERS = {}
    BROWSER_TOOLS = []
    NAVIGATION_TOOLS = []
    ELEMENT_TOOLS = []
    SCREENSHOT_TOOLS = []
    SCRIPT_TOOLS = []
    ADVANCED_TOOLS = []
    PROTECTION_TOOLS = []
    NETWORK_TOOLS = []
    FILE_TOOLS = []
    BROWSER_TOOL_HANDLERS = {}
    NAVIGATION_TOOL_HANDLERS = {}
    ELEMENT_TOOL_HANDLERS = {}
    SCREENSHOT_TOOL_HANDLERS = {}
    SCRIPT_TOOL_HANDLERS = {}
    ADVANCED_TOOL_HANDLERS = {}
    PROTECTION_TOOL_HANDLERS = {}
    NETWORK_TOOL_HANDLERS = {}
    FILE_TOOL_HANDLERS = {}
    TOTAL_TOOLS = 0
    TOOL_CATEGORIES = {}

# Configure logging
def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Setup comprehensive logging for the PyDoll MCP Server."""
    # Create logs directory if it doesn't exist
    log_dir = Path.home() / ".local" / "share" / "pydoll-mcp" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Default log file
    if log_file is None:
        log_file = str(log_dir / "server.log")
    
    # Configure logging format
    log_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # File handler with rotation
    try:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(log_format, date_format))
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not setup file logging: {e}", file=sys.stderr)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    root_logger.addHandler(console_handler)
    
    return logging.getLogger(__name__)

# Environment-based configuration
LOG_LEVEL = os.getenv("PYDOLL_LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("PYDOLL_LOG_FILE")
DEBUG_MODE = os.getenv("PYDOLL_DEBUG", "0").lower() in ("1", "true", "yes")

# Setup logger
logger = setup_logging(LOG_LEVEL, LOG_FILE)


def setup_server_encoding():
    """Setup server encoding for cross-platform compatibility."""
    import locale
    
    # Force UTF-8 for all output
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    # Special handling for Windows
    if sys.platform.startswith('win'):
        try:
            # Set console to UTF-8
            import subprocess
            subprocess.run(['chcp', '65001'], capture_output=True, shell=True, timeout=1)
        except Exception:
            pass
        
        # Handle Korean Windows (CP949)
        try:
            current_locale = locale.getdefaultlocale()
            if current_locale and current_locale[1] and any(enc in current_locale[1].lower() for enc in ['cp949', 'euc-kr']):
                os.environ['LC_ALL'] = 'C.UTF-8'
                os.environ['LANG'] = 'C.UTF-8'
        except Exception:
            pass
    
    # Ensure streams use UTF-8
    try:
        import io
        import codecs
        
        # Only stdout needs special handling for MCP protocol
        if hasattr(sys.stdout, 'buffer'):
            if sys.stdout.encoding != 'utf-8':
                try:
                    sys.stdout = io.TextIOWrapper(
                        sys.stdout.buffer,
                        encoding='utf-8',
                        errors='replace',
                        newline=None,
                        line_buffering=True
                    )
                except Exception:
                    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
        
        # Stderr for logging and messages
        if hasattr(sys.stderr, 'buffer'):
            if sys.stderr.encoding != 'utf-8':
                try:
                    sys.stderr = io.TextIOWrapper(
                        sys.stderr.buffer,
                        encoding='utf-8',
                        errors='replace',
                        newline=None,
                        line_buffering=True
                    )
                except Exception:
                    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
    except Exception:
        pass


class PyDollMCPServer:
    """Advanced PyDoll MCP Server for browser automation.
    
    This server provides comprehensive browser automation capabilities through
    the Model Context Protocol, featuring:
    - Zero-webdriver browser control
    - Intelligent captcha bypass
    - Human-like interaction simulation
    - Real-time network monitoring
    - Advanced stealth capabilities
    """
    
    def __init__(self, server_name: str = "pydoll-mcp"):
        """Initialize the PyDoll MCP Server.
        
        Args:
            server_name: Name identifier for the MCP server
        """
        self.server_name = server_name
        self.server = Server(server_name)
        self.browser_manager = None
        self.is_running = False
        self.startup_time = None
        
        # Performance metrics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "uptime_start": None,
        }
        
        logger.info(f"Initializing PyDoll MCP Server v{__version__}")
        
        # Perform health check
        if DEBUG_MODE:
            health_info = health_check()
            logger.debug(f"Health check results: {health_info}")
            
            if not health_info["overall_status"]:
                logger.warning("Health check detected issues:")
                for error in health_info["errors"]:
                    logger.warning(f"  - {error}")
    
    async def initialize(self):
        """Initialize server components."""
        try:
            # Initialize browser manager
            self.browser_manager = get_browser_manager()
            logger.info("Browser manager initialized")
            
            # Setup tools and handlers
            self._setup_tools()
            logger.info("Tools and handlers registered")
            
            # Setup signal handlers for graceful shutdown
            self._setup_signal_handlers()
            logger.info("Signal handlers configured")
            
            # Update stats
            import time
            self.stats["uptime_start"] = time.time()
            
        except Exception as e:
            logger.error(f"Failed to initialize server: {e}", exc_info=True)
            raise
    
    def _setup_tools(self):
        """Register all tools with the MCP server."""
        # Use ALL_TOOLS and ALL_TOOL_HANDLERS from tools module
        all_tools = ALL_TOOLS
        all_handlers = ALL_TOOL_HANDLERS
        
        logger.info(f"Registering {len(all_tools)} tools across {len(all_handlers)} handlers")
        
        # Store references for access in handlers
        self.all_tools = all_tools
        self.all_handlers = all_handlers
        
        # Register list_tools handler
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List all available automation tools."""
            logger.debug(f"Listing {len(self.all_tools)} available tools")
            return self.all_tools
        
        # Register call_tool handler
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
            """Handle tool execution with comprehensive error handling."""
            self.stats["total_requests"] += 1
            start_time = asyncio.get_event_loop().time()
            
            logger.info(f"Executing tool: {name}")
            logger.debug(f"Tool arguments: {arguments}")
            
            if name not in self.all_handlers:
                self.stats["failed_requests"] += 1
                error_result = {
                    "success": False,
                    "error": "ToolNotFound",
                    "message": f"Tool '{name}' is not available",
                    "available_tools": list(self.all_handlers.keys())
                }
                logger.error(f"Unknown tool requested: {name}")
                return [TextContent(type="text", text=str(error_result))]
            
            try:
                # Execute the tool handler
                handler = self.all_handlers[name]
                result = await handler(arguments)
                
                # Calculate execution time
                execution_time = asyncio.get_event_loop().time() - start_time
                
                self.stats["successful_requests"] += 1
                logger.info(f"Tool {name} completed successfully in {execution_time:.2f}s")
                
                # Add execution metadata to result if it's a dict
                if isinstance(result, list) and len(result) > 0:
                    if hasattr(result[0], 'text'):
                        try:
                            import json
                            result_data = json.loads(result[0].text)
                            if isinstance(result_data, dict):
                                result_data["_metadata"] = {
                                    "execution_time": execution_time,
                                    "tool_name": name,
                                    "server_version": __version__
                                }
                                result[0].text = json.dumps(result_data)
                        except (json.JSONDecodeError, AttributeError):
                            pass
                
                return result
                
            except Exception as e:
                execution_time = asyncio.get_event_loop().time() - start_time
                self.stats["failed_requests"] += 1
                
                logger.error(f"Tool {name} failed after {execution_time:.2f}s: {e}", exc_info=True)
                
                error_result = {
                    "success": False,
                    "error": type(e).__name__,
                    "message": str(e),
                    "tool_name": name,
                    "execution_time": execution_time,
                    "debug_info": {
                        "arguments": arguments,
                        "server_version": __version__
                    } if DEBUG_MODE else None
                }
                
                return [TextContent(type="text", text=str(error_result))]
    
    def _collect_all_tools(self) -> list[Tool]:
        """Collect all available tools from different categories."""
        return ALL_TOOLS
    
    def _collect_all_handlers(self) -> dict[str, Any]:
        """Collect all tool handlers from different categories."""
        return ALL_TOOL_HANDLERS
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            
            # Create cleanup task
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.cleanup())
            else:
                loop.run_until_complete(self.cleanup())
            
            sys.exit(0)
        
        # Handle common termination signals
        for sig in [signal.SIGINT, signal.SIGTERM]:
            try:
                signal.signal(sig, signal_handler)
            except (OSError, ValueError) as e:
                logger.warning(f"Could not register signal handler for {sig}: {e}")
    
    async def cleanup(self):
        """Perform comprehensive cleanup of server resources."""
        logger.info("Starting PyDoll MCP Server cleanup...")
        
        try:
            self.is_running = False
            
            # Print final statistics
            self._log_final_stats()
            
            # Cleanup browser manager
            if self.browser_manager:
                await self.browser_manager.cleanup_all()
                logger.info("Browser manager cleanup completed")
            
            # Additional cleanup tasks
            await self._cleanup_temp_files()
            
            logger.info("PyDoll MCP Server cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}", exc_info=True)
    
    async def _cleanup_temp_files(self):
        """Clean up temporary files and directories."""
        try:
            # Clean up browser profiles and temp directories
            temp_dirs = [
                Path.home() / ".local" / "share" / "pydoll-mcp" / "temp",
                Path("/tmp") / "pydoll-mcp" if os.name != "nt" else Path(os.environ.get("TEMP", "")) / "pydoll-mcp"
            ]
            
            for temp_dir in temp_dirs:
                if temp_dir.exists() and temp_dir.is_dir():
                    import shutil
                    try:
                        shutil.rmtree(temp_dir)
                        logger.debug(f"Cleaned up temp directory: {temp_dir}")
                    except Exception as e:
                        logger.warning(f"Could not clean temp directory {temp_dir}: {e}")
                        
        except Exception as e:
            logger.warning(f"Error during temp file cleanup: {e}")
    
    def _log_final_stats(self):
        """Log final server statistics."""
        try:
            import time
            if self.stats["uptime_start"]:
                uptime = time.time() - self.stats["uptime_start"]
                
                logger.info("=== PyDoll MCP Server Statistics ===")
                logger.info(f"Total Requests: {self.stats['total_requests']}")
                logger.info(f"Successful: {self.stats['successful_requests']}")
                logger.info(f"Failed: {self.stats['failed_requests']}")
                logger.info(f"Success Rate: {(self.stats['successful_requests'] / max(1, self.stats['total_requests']) * 100):.1f}%")
                logger.info(f"Uptime: {uptime:.1f} seconds")
                
                if self.stats["total_requests"] > 0:
                    logger.info(f"Avg Request Rate: {self.stats['total_requests'] / uptime:.2f} req/sec")
                
        except Exception as e:
            logger.warning(f"Error calculating final stats: {e}")
    
    async def run(self):
        """Run the PyDoll MCP Server with comprehensive error handling."""
        try:
            # Initialize server components
            await self.initialize()
            
            # Print startup banner
            if not DEBUG_MODE:
                print_banner()
            
            logger.info(f"PyDoll MCP Server v{__version__} is ready")
            logger.info(f"Available tools: {len(self._collect_all_tools())}")
            logger.info("Waiting for MCP client connections...")
            
            self.is_running = True
            
            # Run the MCP server with stdio transport
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
                
        except KeyboardInterrupt:
            logger.info("Server interrupted by user")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            raise
        finally:
            await self.cleanup()


async def main():
    """Main entry point for the PyDoll MCP Server."""
    # Ensure proper encoding setup
    setup_server_encoding()
    
    server = PyDollMCPServer()
    await server.run()


def cli_main():
    """CLI entry point with argument handling."""
    # Setup encoding early
    setup_server_encoding()
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PyDoll MCP Server - Revolutionary Browser Automation for AI",
        epilog="For more information, visit: https://github.com/JinsongRoh/pydoll-mcp"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"PyDoll MCP Server v{__version__}"
    )
    
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Run health check and exit"
    )
    
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug mode with verbose logging"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=LOG_LEVEL,
        help="Set logging level"
    )
    
    parser.add_argument(
        "--log-file",
        help="Custom log file path"
    )
    
    args = parser.parse_args()
    
    # Handle test mode
    if args.test:
        print(f"PyDoll MCP Server v{__version__} - Health Check", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        
        health_info = health_check()
        
        for check, status in health_info.items():
            if check == "errors":
                continue
            elif check == "overall_status":
                print(f"Overall Status: {'✅ PASS' if status else '❌ FAIL'}", file=sys.stderr)
            else:
                print(f"{check.replace('_', ' ').title()}: {'✅' if status else '❌'}", file=sys.stderr)
        
        if health_info["errors"]:
            print("\\nErrors:", file=sys.stderr)
            for error in health_info["errors"]:
                print(f"  - {error}", file=sys.stderr)
        
        sys.exit(0 if health_info["overall_status"] else 1)
    
    # Update logging configuration based on arguments
    if args.debug:
        os.environ["PYDOLL_DEBUG"] = "1"
        args.log_level = "DEBUG"
    
    global logger
    logger = setup_logging(args.log_level, args.log_file)
    
    try:
        logger.info(f"Starting PyDoll MCP Server v{__version__}")
        logger.debug(f"Arguments: {vars(args)}")
        
        asyncio.run(main())
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    cli_main()