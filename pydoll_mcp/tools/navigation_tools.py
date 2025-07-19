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
    ),
    
    Tool(
        name="fetch_domain_commands",
        description="Fetch all possible commands available for the current domain from Chrome DevTools Protocol",
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
                "domain": {
                    "type": "string",
                    "description": "Chrome DevTools Protocol domain (e.g., 'Page', 'Network', 'DOM')"
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
        
        # Get tab and ensure it has all necessary methods
        tab = await browser_manager.get_tab(browser_id, tab_id)
        tab = await browser_manager.ensure_tab_methods(tab)
        
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
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        ignore_cache = arguments.get("ignore_cache", False)
        wait_for_load = arguments.get("wait_for_load", True)
        
        # Get tab and ensure it has all necessary methods
        tab = await browser_manager.get_tab(browser_id, tab_id)
        tab = await browser_manager.ensure_tab_methods(tab)
        
        # Refresh page
        if ignore_cache:
            await tab.reload(ignore_cache=True)
        else:
            await tab.reload()
            
        if wait_for_load:
            await tab.wait_for_load_state("load")
        
        # Get current URL and title after refresh
        url = await tab.get_url()
        title = await tab.get_title()
        
        result = OperationResult(
            success=True,
            message="Page refreshed successfully",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "url": url,
                "title": title,
                "ignore_cache": ignore_cache
            }
        )
        
        logger.info(f"Page refresh successful: {url}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Page refresh failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to refresh page"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_go_back(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle browser back navigation."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        steps = arguments.get("steps", 1)
        
        # Get tab and ensure it has all necessary methods
        tab = await browser_manager.get_tab(browser_id, tab_id)
        tab = await browser_manager.ensure_tab_methods(tab)
        
        # Navigate back the specified number of steps
        for _ in range(steps):
            await tab.go_back()
            
        # Get current URL after navigation
        url = await tab.get_url()
        title = await tab.get_title()
        
        result = OperationResult(
            success=True,
            message=f"Navigated back {steps} step(s)",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "steps": steps,
                "current_url": url,
                "current_title": title
            }
        )
        
        logger.info(f"Back navigation successful: {steps} steps")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Back navigation failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message=f"Failed to navigate back {steps} step(s)"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_get_current_url(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get current URL request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        # Get tab and ensure it has all necessary methods
        tab = await browser_manager.get_tab(browser_id, tab_id)
        tab = await browser_manager.ensure_tab_methods(tab)
        
        # Get current URL
        url = await tab.get_url()
        
        result = OperationResult(
            success=True,
            message="Current URL retrieved successfully",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "url": url
            }
        )
        
        logger.info(f"Current URL retrieved: {url}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to get current URL: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to retrieve current URL"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_get_page_title(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get page title request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        # Get tab and ensure it has all necessary methods
        tab = await browser_manager.get_tab(browser_id, tab_id)
        tab = await browser_manager.ensure_tab_methods(tab)
        
        # Get page title
        title = await tab.get_title()
        url = await tab.get_url()
        
        result = OperationResult(
            success=True,
            message="Page title retrieved successfully",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "title": title,
                "url": url
            }
        )
        
        logger.info(f"Page title retrieved: {title}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to get page title: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to retrieve page title"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_get_page_source(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get page source request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        include_resources = arguments.get("include_resources", False)
        
        # Get tab and ensure it has all necessary methods
        tab = await browser_manager.get_tab(browser_id, tab_id)
        tab = await browser_manager.ensure_tab_methods(tab)
        
        # Get page source
        source = await tab.get_content()
        url = await tab.get_url()
        title = await tab.get_title()
        
        data = {
            "browser_id": browser_id,
            "tab_id": tab_id,
            "url": url,
            "title": title,
            "source": source,
            "length": len(source)
        }
        
        # Include resources information if requested
        if include_resources:
            try:
                # Get basic page metrics
                data["resources"] = {
                    "source_size": len(source),
                    "encoding": "utf-8",
                    "content_type": "text/html"
                }
            except Exception as e:
                logger.warning(f"Failed to get resource information: {e}")
        
        result = OperationResult(
            success=True,
            message="Page source retrieved successfully",
            data=data
        )
        
        logger.info(f"Page source retrieved: {len(source)} characters")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to get page source: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to retrieve page source"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_fetch_domain_commands(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle fetch domain commands request using PyDoll 2.3.1 feature."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        domain = arguments.get("domain")
        
        # Get tab and ensure it has all necessary methods
        tab = await browser_manager.get_tab(browser_id, tab_id)
        tab = await browser_manager.ensure_tab_methods(tab)
        
        # Call PyDoll 2.3.1's new fetch_domain_commands method
        if domain:
            commands = await tab.fetch_domain_commands(domain)
            message = f"Successfully fetched commands for domain: {domain}"
        else:
            # Fetch all available domains
            commands = await tab.fetch_domain_commands()
            message = "Successfully fetched all available domain commands"
        
        result = OperationResult(
            success=True,
            message=message,
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "domain": domain,
                "commands": commands,
                "command_count": len(commands) if isinstance(commands, list) else sum(len(cmds) for cmds in commands.values())
            }
        )
        
        logger.info(f"Domain commands fetched successfully: {domain or 'all'}")
        return [TextContent(type="text", text=result.json())]
        
    except AttributeError:
        # Fallback for PyDoll versions < 2.3.1
        logger.warning("fetch_domain_commands not available in current PyDoll version")
        result = OperationResult(
            success=False,
            error="Feature requires PyDoll 2.3.1 or higher",
            message="Please upgrade PyDoll to use this feature"
        )
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to fetch domain commands: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to fetch domain commands"
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
    "fetch_domain_commands": handle_fetch_domain_commands,
}
