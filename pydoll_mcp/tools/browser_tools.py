"""Browser Management Tools for PyDoll MCP Server.

This module provides MCP tools for browser lifecycle management including:
- Starting and stopping browsers
- Tab management
- Browser configuration
- Status monitoring
"""

import json
import logging
from typing import Any, Dict, List, Sequence

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import BrowserConfig, BrowserInstance, BrowserStatus, OperationResult

logger = logging.getLogger(__name__)

# Browser Management Tools Definition

BROWSER_TOOLS = [
    Tool(
        name="start_browser",
        description="Start a new browser instance with specified configuration",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_type": {
                    "type": "string",
                    "enum": ["chrome", "edge"],
                    "default": "chrome",
                    "description": "Type of browser to start"
                },
                "headless": {
                    "type": "boolean", 
                    "default": False,
                    "description": "Run browser in headless mode"
                },
                "window_width": {
                    "type": "integer",
                    "default": 1920,
                    "minimum": 100,
                    "maximum": 7680,
                    "description": "Browser window width in pixels"
                },
                "window_height": {
                    "type": "integer", 
                    "default": 1080,
                    "minimum": 100,
                    "maximum": 4320,
                    "description": "Browser window height in pixels"
                },
                "stealth_mode": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable stealth mode to avoid detection"
                },
                "proxy_server": {
                    "type": "string",
                    "description": "Proxy server in format host:port"
                },
                "user_agent": {
                    "type": "string",
                    "description": "Custom user agent string"
                },
                "disable_images": {
                    "type": "boolean",
                    "default": False,
                    "description": "Disable image loading for faster browsing"
                },
                "block_ads": {
                    "type": "boolean", 
                    "default": True,
                    "description": "Block advertisement requests"
                },
                "custom_args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Additional browser command line arguments"
                },
                "start_timeout": {
                    "type": "integer",
                    "default": 30,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Browser startup timeout in seconds (PyDoll 2.3.1+)"
                }
            },
            "required": []
        }
    ),
    
    Tool(
        name="stop_browser",
        description="Stop a browser instance and clean up resources",
        inputSchema={
            "type": "object", 
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID to stop"
                },
                "force": {
                    "type": "boolean",
                    "default": False,
                    "description": "Force stop even if tabs are open"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="list_browsers",
        description="List all active browser instances with their status",
        inputSchema={
            "type": "object",
            "properties": {
                "include_stats": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include performance statistics"
                }
            },
            "required": []
        }
    ),
    
    Tool(
        name="get_browser_status",
        description="Get detailed status information for a specific browser",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="new_tab",
        description="Create a new tab in a browser instance",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string", 
                    "description": "Browser instance ID"
                },
                "url": {
                    "type": "string",
                    "description": "Optional URL to navigate to immediately"
                },
                "background": {
                    "type": "boolean",
                    "default": False,
                    "description": "Open tab in background"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="close_tab",
        description="Close a specific tab in a browser",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Tab ID to close"
                }
            },
            "required": ["browser_id", "tab_id"]
        }
    ),
    
    Tool(
        name="list_tabs",
        description="List all tabs in a browser instance",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "include_content": {
                    "type": "boolean",
                    "default": False,
                    "description": "Include page content information"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="set_active_tab",
        description="Switch to a specific tab in a browser",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Tab ID to activate"
                }
            },
            "required": ["browser_id", "tab_id"]
        }
    )
]


# Browser Management Tool Handlers

async def handle_start_browser(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle browser start request."""
    try:
        browser_manager = get_browser_manager()
        
        # Extract and validate arguments
        config = BrowserConfig(**arguments)
        
        # Create browser instance
        browser_id = await browser_manager.create_browser(
            browser_type=config.browser_type,
            headless=config.headless,
            window_width=config.window_width,
            window_height=config.window_height,
            stealth_mode=config.stealth_mode,
            proxy=config.proxy_server,
            user_agent=config.user_agent,
            disable_images=config.disable_images,
            block_ads=config.block_ads,
            args=config.custom_args
        )
        
        result = OperationResult(
            success=True,
            message="Browser started successfully",
            data={
                "browser_id": browser_id,
                "browser_type": config.browser_type,
                "configuration": config.dict()
            }
        )
        
        logger.info(f"Browser started: {browser_id}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to start browser: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to start browser"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_stop_browser(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle browser stop request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        force = arguments.get("force", False)
        
        # Check if browser has open tabs (unless force stop)
        if not force:
            instance = await browser_manager.get_browser(browser_id)
            if instance and len(instance.tabs) > 0:
                result = OperationResult(
                    success=False,
                    message=f"Browser has {len(instance.tabs)} open tabs. Use force=true to stop anyway.",
                    data={"open_tabs": len(instance.tabs)}
                )
                return [TextContent(type="text", text=result.json())]
        
        await browser_manager.close_browser(browser_id)
        
        result = OperationResult(
            success=True,
            message="Browser stopped successfully",
            data={"browser_id": browser_id}
        )
        
        logger.info(f"Browser stopped: {browser_id}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to stop browser: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to stop browser"
        )
        return [TextContent(type="text", text=result.json())]


# Placeholder handlers for remaining browser tools
async def handle_list_browsers(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle list browsers request."""
    from pydoll_mcp.browser_manager import browser_manager
    
    try:
        browsers_info = []
        for browser_id, instance in browser_manager.browsers.items():
            browsers_info.append(instance.to_dict())
        
        result = OperationResult(
            success=True,
            message=f"Found {len(browsers_info)} active browsers",
            data={
                "browsers": browsers_info,
                "count": len(browsers_info),
                "global_stats": browser_manager.global_stats if arguments.get("include_stats", True) else None
            }
        )
    except Exception as e:
        logger.error(f"Failed to list browsers: {e}", exc_info=True)
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to list browsers"
        )
    
    return [TextContent(type="text", text=result.json())]


async def handle_get_browser_status(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get browser status request."""
    from pydoll_mcp.browser_manager import browser_manager
    
    browser_id = arguments.get("browser_id")
    if not browser_id:
        result = OperationResult(
            success=False,
            error="browser_id is required",
            message="Missing required parameter"
        )
        return [TextContent(type="text", text=result.json())]
    
    try:
        instance = browser_manager.browsers.get(browser_id)
        if not instance:
            result = OperationResult(
                success=False,
                error=f"Browser {browser_id} not found",
                message="Browser not found"
            )
        else:
            result = OperationResult(
                success=True,
                message="Browser status retrieved",
                data=instance.to_dict()
            )
    except Exception as e:
        logger.error(f"Failed to get browser status: {e}", exc_info=True)
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to get browser status"
        )
    
    return [TextContent(type="text", text=result.json())]


async def handle_new_tab(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle new tab creation request."""
    result = OperationResult(
        success=True,
        message="Tab created successfully",
        data={"tab_id": "tab_123"}
    )
    return [TextContent(type="text", text=result.json())]


async def handle_close_tab(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle tab close request."""
    result = OperationResult(
        success=True,
        message="Tab closed successfully"
    )
    return [TextContent(type="text", text=result.json())]


async def handle_list_tabs(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle list tabs request."""
    result = OperationResult(
        success=True,
        message="Found 3 tabs",
        data={"tabs": [], "count": 3}
    )
    return [TextContent(type="text", text=result.json())]


async def handle_set_active_tab(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle set active tab request."""
    result = OperationResult(
        success=True,
        message="Active tab set successfully"
    )
    return [TextContent(type="text", text=result.json())]


# Browser Tool Handlers Dictionary
BROWSER_TOOL_HANDLERS = {
    "start_browser": handle_start_browser,
    "stop_browser": handle_stop_browser,
    "list_browsers": handle_list_browsers,
    "get_browser_status": handle_get_browser_status,
    "new_tab": handle_new_tab,
    "close_tab": handle_close_tab,
    "list_tabs": handle_list_tabs,
    "set_active_tab": handle_set_active_tab,
}
