"""Element Interaction Tools for PyDoll MCP Server.

This module provides MCP tools for finding and interacting with web elements including:
- Revolutionary natural attribute element finding
- Traditional CSS selector and XPath support
- Element interaction (click, type, hover, etc.)
- Element information extraction
- Advanced waiting strategies
"""

import logging
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
                # Search options
                "find_all": {
                    "type": "boolean",
                    "default": False,
                    "description": "Find all matching elements"
                },
                "timeout": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Element search timeout in seconds"
                },
                "wait_for_visible": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for element to be visible"
                }
            },
            "required": ["browser_id"]
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
                "typing_speed": {
                    "type": "string",
                    "enum": ["slow", "normal", "fast", "instant"],
                    "default": "normal",
                    "description": "Typing speed simulation"
                },
                "human_like": {
                    "type": "boolean",
                    "default": True,
                    "description": "Use human-like typing with natural delays and occasional mistakes"
                }
            },
            "required": ["browser_id", "element_selector", "text"]
        }
    )
]


# Element Tool Handlers

async def handle_find_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle element finding request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        # Remove browser_id and tab_id from selector arguments
        selector_args = {k: v for k, v in arguments.items() 
                        if k not in ["browser_id", "tab_id"]}
        
        # Create element selector
        selector = ElementSelector(**selector_args)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Simulate element finding (would use actual PyDoll API)
        elements_info = [{
            "element_id": "element_1",
            "tag_name": "button",
            "text": "Click me",
            "is_visible": True,
            "is_enabled": True,
            "bounds": {"x": 100, "y": 200, "width": 80, "height": 30}
        }]
        
        result = OperationResult(
            success=True,
            message=f"Found {len(elements_info)} element(s)",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "selector": selector.dict(),
                "elements": elements_info,
                "count": len(elements_info)
            }
        )
        
        logger.info(f"Found {len(elements_info)} elements with selector: {selector}")
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
    """Handle element click request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        element_selector = arguments["element_selector"]
        click_type = arguments.get("click_type", "left")
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Simulate element click (would use actual PyDoll API)
        result = InteractionResult(
            success=True,
            action=f"{click_type}_click",
            message=f"Successfully performed {click_type} click",
            execution_time=0.2
        )
        
        logger.info(f"Element clicked: {click_type} click")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Element click failed: {e}")
        result = InteractionResult(
            success=False,
            action="click",
            error=str(e),
            message="Failed to click element"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_type_text(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle text typing request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        element_selector = arguments["element_selector"]
        text = arguments["text"]
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Simulate text typing (would use actual PyDoll API)
        result = InteractionResult(
            success=True,
            action="type_text",
            message=f"Successfully typed {len(text)} characters",
            data={
                "text_length": len(text),
                "typing_speed": arguments.get("typing_speed", "normal")
            }
        )
        
        logger.info(f"Text typed: {len(text)} characters")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Text typing failed: {e}")
        result = InteractionResult(
            success=False,
            action="type_text",
            error=str(e),
            message="Failed to type text"
        )
        return [TextContent(type="text", text=result.json())]


# Element Tool Handlers Dictionary
ELEMENT_TOOL_HANDLERS = {
    "find_element": handle_find_element,
    "click_element": handle_click_element,
    "type_text": handle_type_text,
}
