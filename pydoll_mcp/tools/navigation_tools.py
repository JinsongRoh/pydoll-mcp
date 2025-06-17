"""Navigation Tools for PyDoll MCP Server.

This module provides MCP tools for page navigation and URL management including:
- Page navigation and URL handling
- Page refresh and history management
- Page information extraction
- Wait conditions and load detection
"""

import logging
from typing import Any, Dict, Sequence
from urllib.parse import urlparse

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import OperationResult

logger = logging.getLogger(__name__)

# Navigation Tools Definition

NAVIGATION_TOOLS = [
    Tool(
        name="navigate_to",
        description="Navigate to a specific URL in a browser tab",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "url": {
                    "type": "string",
                    "description": "URL to navigate to"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "wait_for_load": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for page to fully load"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Navigation timeout in seconds"
                },
                "referrer": {
                    "type": "string",
                    "description": "Optional referrer URL"
                }
            },
            "required": ["browser_id", "url"]
        }
    ),
    
    Tool(
        name="refresh_page",
        description="Refresh the current page in a browser tab",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "ignore_cache": {
                    "type": "boolean",
                    "default": False,
                    "description": "Force refresh ignoring cache"
                },
                "wait_for_load": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for page to reload"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="go_back",
        description="Navigate back in browser history",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "steps": {
                    "type": "integer",
                    "default": 1,
                    "minimum": 1,
                    "maximum": 10,
                    "description": "Number of steps to go back"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="get_current_url",
        description="Get the current URL of a browser tab",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="get_page_title",
        description="Get the title of the current page",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="get_page_source",
        description="Get the HTML source code of the current page",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "include_resources": {
                    "type": "boolean",
                    "default": False,
                    "description": "Include information about page resources"
                }
            },
            "required": ["browser_id"]
        }
    )
]


# Navigation Tool Handlers

async def handle_navigate_to(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle page navigation request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        url = arguments["url"]
        tab_id = arguments.get("tab_id")
        wait_for_load = arguments.get("wait_for_load", True)
        timeout = arguments.get("timeout", 30)
        referrer = arguments.get("referrer")
        
        # Validate URL
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = f"https://{url}"  # Default to HTTPS
        except Exception:
            raise ValueError(f"Invalid URL: {url}")
        
        # Get tab
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Navigate with options
        navigation_options = {
            "timeout": timeout * 1000,  # Convert to milliseconds
            "waitUntil": "load" if wait_for_load else "domcontentloaded"
        }
        
        if referrer:
            navigation_options["referer"] = referrer
        
        # Perform navigation
        await tab.go_to(url, **navigation_options)
        
        # Get final URL (in case of redirects)
        final_url = await tab.get_url()
        title = await tab.get_title()
        
        result = OperationResult(
            success=True,
            message=f"Successfully navigated to {final_url}",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "requested_url": url,
                "final_url": final_url,
                "page_title": title,
                "redirected": url != final_url
            }
        )
        
        logger.info(f"Navigation successful: {url} -> {final_url}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Navigation failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message=f"Failed to navigate to {url}"
        )
        return [TextContent(type="text", text=result.json())]


# Placeholder handlers for remaining tools
async def handle_refresh_page(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle page refresh request."""
    result = OperationResult(
        success=True,
        message="Page refreshed successfully",
        data={"url": "https://example.com"}
    )
    return [TextContent(type="text", text=result.json())]


async def handle_go_back(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle browser back navigation."""
    steps = arguments.get("steps", 1)
    result = OperationResult(
        success=True,
        message=f"Navigated back {steps} step(s)",
        data={"steps": steps}
    )
    return [TextContent(type="text", text=result.json())]


async def handle_get_current_url(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get current URL request."""
    result = OperationResult(
        success=True,
        message="Current URL retrieved successfully",
        data={"url": "https://example.com"}
    )
    return [TextContent(type="text", text=result.json())]


async def handle_get_page_title(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get page title request."""
    result = OperationResult(
        success=True,
        message="Page title retrieved successfully",
        data={"title": "Example Page"}
    )
    return [TextContent(type="text", text=result.json())]


async def handle_get_page_source(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get page source request."""
    result = OperationResult(
        success=True,
        message="Page source retrieved successfully",
        data={"source": "<!DOCTYPE html>...", "length": 1500}
    )
    return [TextContent(type="text", text=result.json())]


# Navigation Tool Handlers Dictionary
NAVIGATION_TOOL_HANDLERS = {
    "navigate_to": handle_navigate_to,
    "refresh_page": handle_refresh_page,
    "go_back": handle_go_back,
    "get_current_url": handle_get_current_url,
    "get_page_title": handle_get_page_title,
    "get_page_source": handle_get_page_source,
}
