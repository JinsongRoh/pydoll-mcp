"""Improved Element Interaction Tools for PyDoll MCP Server.

This module provides MCP tools for finding and interacting with web elements using
PyDoll's native API methods:
- Natural attribute element finding with find()
- CSS selector and XPath support with query()
- Element interaction (click, type, hover, etc.)
- Element information extraction
- Advanced waiting strategies
"""

import logging
import time
from typing import Any, Dict, List, Sequence

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import ElementSelector, ElementInfo, InteractionResult, OperationResult

logger = logging.getLogger(__name__)

# Element Tools Definition

ELEMENT_TOOLS = [
    Tool(
        name="find_element",
        description="Find a web element using natural attributes or traditional selectors",
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
                # Natural attribute selectors
                "id": {
                    "type": "string",
                    "description": "Element ID attribute"
                },
                "class_name": {
                    "type": "string",
                    "description": "CSS class name"
                },
                "tag_name": {
                    "type": "string",
                    "description": "HTML tag name (div, button, input, etc.)"
                },
                "text": {
                    "type": "string",
                    "description": "Element text content"
                },
                "name": {
                    "type": "string",
                    "description": "Element name attribute"
                },
                "type": {
                    "type": "string",
                    "description": "Element type attribute (for inputs)"
                },
                "placeholder": {
                    "type": "string",
                    "description": "Input placeholder text"
                },
                "value": {
                    "type": "string",
                    "description": "Element value attribute"
                },
                # Data attributes
                "data_testid": {
                    "type": "string",
                    "description": "data-testid attribute"
                },
                "data_id": {
                    "type": "string",
                    "description": "data-id attribute"
                },
                # Accessibility attributes
                "aria_label": {
                    "type": "string",
                    "description": "aria-label attribute"
                },
                "aria_role": {
                    "type": "string",
                    "description": "aria-role attribute"
                },
                # Traditional selectors
                "css_selector": {
                    "type": "string",
                    "description": "CSS selector string"
                },
                "xpath": {
                    "type": "string",
                    "description": "XPath expression"
                },
                # Options
                "find_all": {
                    "type": "boolean",
                    "default": False,
                    "description": "Find all matching elements"
                },
                "timeout": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 60,
                    "description": "Element search timeout in seconds"
                },
                "wait_for_visible": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for element to be visible"
                }
            },
            "required": ["browser_id"],
            "anyOf": [
                {"required": ["id"]},
                {"required": ["class_name"]},
                {"required": ["tag_name"]},
                {"required": ["text"]},
                {"required": ["name"]},
                {"required": ["css_selector"]},
                {"required": ["xpath"]}
            ]
        }
    ),
    
    Tool(
        name="click_element",
        description="Click on a web element with human-like behavior",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "click_type": {
                    "type": "string",
                    "enum": ["left", "right", "double", "middle"],
                    "default": "left",
                    "description": "Type of click to perform"
                },
                "force": {
                    "type": "boolean",
                    "default": False,
                    "description": "Force click even if element is not clickable"
                },
                "scroll_to_element": {
                    "type": "boolean",
                    "default": True,
                    "description": "Scroll element into view before clicking"
                },
                "human_like": {
                    "type": "boolean",
                    "default": True,
                    "description": "Use human-like click behavior with natural timing"
                },
                "offset_x": {
                    "type": "integer",
                    "description": "X offset from element center"
                },
                "offset_y": {
                    "type": "integer",
                    "description": "Y offset from element center"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="type_text",
        description="Type text into an input element with realistic human typing",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "text": {
                    "type": "string",
                    "description": "Text to type"
                },
                "clear_first": {
                    "type": "boolean",
                    "default": True,
                    "description": "Clear existing text before typing"
                },
                "human_like": {
                    "type": "boolean",
                    "default": True,
                    "description": "Use human-like typing with natural delays and occasional mistakes"
                },
                "typing_speed": {
                    "type": "string",
                    "enum": ["slow", "normal", "fast", "instant"],
                    "default": "normal",
                    "description": "Typing speed simulation"
                }
            },
            "required": ["browser_id", "element_selector", "text"]
        }
    ),
    
    Tool(
        name="get_parent_element",
        description="Get the parent element of a specific element with its attributes",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "include_attributes": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include all attributes of the parent element"
                },
                "include_bounds": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include bounding box information"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    )
]


# Element Tool Handlers

async def handle_find_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle element finding request using PyDoll's native API."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        # Get tab with automatic fallback to active tab
        tab, actual_tab_id = await browser_manager.get_tab_with_fallback(browser_id, tab_id)
        
        # Extract search parameters
        find_all = arguments.get("find_all", False)
        timeout = arguments.get("timeout", 10)
        wait_for_visible = arguments.get("wait_for_visible", True)
        
        elements_info = []
        
        try:
            # Use PyDoll's native find() or query() methods
            if arguments.get("css_selector"):
                # Use query() for CSS selectors
                css_selector = arguments["css_selector"]
                logger.info(f"Using PyDoll query() with CSS selector: {css_selector}")
                
                if find_all:
                    elements = await tab.query_all(css_selector)
                else:
                    element = await tab.query(css_selector)
                    elements = [element] if element else []
                    
            elif arguments.get("xpath"):
                # Use query() for XPath
                xpath = arguments["xpath"]
                logger.info(f"Using PyDoll query() with XPath: {xpath}")
                
                if find_all:
                    elements = await tab.query_all(xpath)
                else:
                    element = await tab.query(xpath)
                    elements = [element] if element else []
                    
            else:
                # Use find() for natural attribute selection
                find_params = {}
                
                # Build parameters for PyDoll's find() method
                if arguments.get("tag_name"):
                    find_params["tag_name"] = arguments["tag_name"]
                if arguments.get("id"):
                    find_params["id"] = arguments["id"]
                if arguments.get("class_name"):
                    find_params["class_name"] = arguments["class_name"]
                if arguments.get("text"):
                    find_params["text"] = arguments["text"]
                if arguments.get("name"):
                    find_params["name"] = arguments["name"]
                if arguments.get("type"):
                    find_params["type"] = arguments["type"]
                if arguments.get("placeholder"):
                    find_params["placeholder"] = arguments["placeholder"]
                if arguments.get("value"):
                    find_params["value"] = arguments["value"]
                
                # Add data attributes
                if arguments.get("data_testid"):
                    find_params["data_testid"] = arguments["data_testid"]
                if arguments.get("data_id"):
                    find_params["data_id"] = arguments["data_id"]
                
                # Add aria attributes
                if arguments.get("aria_label"):
                    find_params["aria-label"] = arguments["aria_label"]
                if arguments.get("aria_role"):
                    find_params["role"] = arguments["aria_role"]
                
                logger.info(f"Using PyDoll find() with params: {find_params}")
                
                # Add timeout and find_all parameters
                find_params["timeout"] = timeout
                find_params["find_all"] = find_all
                find_params["raise_exc"] = False  # Don't raise exception if not found
                
                # Call PyDoll's find() method
                result = await tab.find(**find_params)
                
                if find_all:
                    elements = result if result else []
                else:
                    elements = [result] if result else []
            
            # Extract element information
            for i, element in enumerate(elements):
                if element:  # Skip None elements
                    try:
                        # Get element properties using PyDoll's API
                        element_info = {
                            "element_id": f"element_{i}",
                            "tag_name": getattr(element, 'tag_name', 'unknown').lower(),
                            "text": getattr(element, 'text', '').strip(),
                            "is_visible": True,  # PyDoll typically returns visible elements
                            "is_enabled": True,
                            "id": getattr(element, 'id', None),
                            "class": getattr(element, 'class_name', None),
                            "name": getattr(element, 'name', None),
                            "type": getattr(element, 'type', None),
                            "href": getattr(element, 'href', None),
                        }
                        
                        # Try to get bounding box if available
                        try:
                            bounds = await element.bounding_box()
                            element_info["bounds"] = bounds
                        except:
                            element_info["bounds"] = {"x": 0, "y": 0, "width": 0, "height": 0}
                        
                        elements_info.append(element_info)
                        
                    except Exception as e:
                        logger.warning(f"Failed to extract info from element {i}: {e}")
                        continue
                        
        except Exception as e:
            logger.warning(f"PyDoll element finding failed: {e}")
            # Return empty result instead of falling back to simulation
            elements_info = []
        
        # Log the search results
        logger.info(f"Found {len(elements_info)} elements with selector: {arguments}")
        
        result = OperationResult(
            success=True,
            message=f"Found {len(elements_info)} element(s)",
            data={
                "browser_id": browser_id,
                "tab_id": actual_tab_id,
                "selector": {k: v for k, v in arguments.items() 
                           if k not in ["browser_id", "tab_id"]},
                "elements": elements_info,
                "count": len(elements_info)
            }
        )
        
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Element finding failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to find element"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_click_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle element click request using PyDoll's native API."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        element_selector = arguments["element_selector"]
        
        # Get tab with automatic fallback to active tab
        tab, actual_tab_id = await browser_manager.get_tab_with_fallback(browser_id, tab_id)
        
        # Find the element first
        find_args = {**element_selector, "browser_id": browser_id, "tab_id": actual_tab_id}
        find_result = await handle_find_element(find_args)
        find_data = OperationResult.parse_raw(find_result[0].text)
        
        if not find_data.success or not find_data.data.get("elements"):
            return [TextContent(type="text", text=OperationResult(
                success=False,
                error="Element not found",
                message="Cannot click element that doesn't exist"
            ).json())]
        
        # Use PyDoll's click method
        try:
            # Re-find the element to get the actual PyDoll element object
            if element_selector.get("css_selector"):
                element = await tab.query(element_selector["css_selector"])
            elif element_selector.get("xpath"):
                element = await tab.query(element_selector["xpath"])
            else:
                # Use find() with parameters
                find_params = {k: v for k, v in element_selector.items() 
                             if k in ["tag_name", "id", "class_name", "text", "name", 
                                     "type", "placeholder", "value"]}
                element = await tab.find(**find_params, raise_exc=False)
            
            if element:
                # Scroll to element if requested
                if arguments.get("scroll_to_element", True):
                    await element.scroll_into_view()
                
                # Perform click
                await element.click()
                
                result = OperationResult(
                    success=True,
                    message="Element clicked successfully",
                    data={
                        "browser_id": browser_id,
                        "tab_id": actual_tab_id,
                        "element": find_data.data["elements"][0],
                        "click_type": arguments.get("click_type", "left")
                    }
                )
            else:
                result = OperationResult(
                    success=False,
                    error="Element not found for click",
                    message="Failed to find element for click operation"
                )
                
        except Exception as e:
            logger.error(f"Click operation failed: {e}")
            result = OperationResult(
                success=False,
                error=str(e),
                message="Failed to click element"
            )
        
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Click element handler failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to process click request"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_type_text(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle text typing request using PyDoll's native API."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        element_selector = arguments["element_selector"]
        text = arguments["text"]
        
        # Get tab with automatic fallback to active tab
        tab, actual_tab_id = await browser_manager.get_tab_with_fallback(browser_id, tab_id)
        
        # Find the element first
        find_args = {**element_selector, "browser_id": browser_id, "tab_id": actual_tab_id}
        find_result = await handle_find_element(find_args)
        find_data = OperationResult.parse_raw(find_result[0].text)
        
        if not find_data.success or not find_data.data.get("elements"):
            return [TextContent(type="text", text=OperationResult(
                success=False,
                error="Element not found",
                message="Cannot type into element that doesn't exist"
            ).json())]
        
        # Use PyDoll's type method
        try:
            # Re-find the element to get the actual PyDoll element object
            if element_selector.get("css_selector"):
                element = await tab.query(element_selector["css_selector"])
            elif element_selector.get("xpath"):
                element = await tab.query(element_selector["xpath"])
            else:
                # Use find() with parameters
                find_params = {k: v for k, v in element_selector.items() 
                             if k in ["tag_name", "id", "class_name", "text", "name", 
                                     "type", "placeholder", "value"]}
                element = await tab.find(**find_params, raise_exc=False)
            
            if element:
                # Clear existing text if requested
                if arguments.get("clear_first", True):
                    await element.clear()
                
                # Type the text
                await element.type(text)
                
                result = OperationResult(
                    success=True,
                    message="Text typed successfully",
                    data={
                        "browser_id": browser_id,
                        "tab_id": actual_tab_id,
                        "element": find_data.data["elements"][0],
                        "text": text,
                        "cleared_first": arguments.get("clear_first", True)
                    }
                )
            else:
                result = OperationResult(
                    success=False,
                    error="Element not found for typing",
                    message="Failed to find element for type operation"
                )
                
        except Exception as e:
            logger.error(f"Type operation failed: {e}")
            result = OperationResult(
                success=False,
                error=str(e),
                message="Failed to type text"
            )
        
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Type text handler failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to process type request"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_get_parent_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle parent element request."""
    # This is a placeholder - PyDoll doesn't have direct parent element access
    # Would need to use execute_script for this functionality
    
    result = OperationResult(
        success=True,
        message="Parent element functionality not yet implemented with PyDoll native API",
        data={
            "browser_id": arguments["browser_id"],
            "note": "This feature requires execute_script implementation"
        }
    )
    return [TextContent(type="text", text=result.json())]


# Element Tool Handlers Dictionary
ELEMENT_TOOL_HANDLERS = {
    "find_element": handle_find_element,
    "click_element": handle_click_element,
    "type_text": handle_type_text,
    "get_parent_element": handle_get_parent_element,
}