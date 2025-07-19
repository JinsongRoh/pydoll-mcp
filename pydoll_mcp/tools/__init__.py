"""MCP Tools for PyDoll browser automation.

This module contains all the Model Context Protocol (MCP) tools that provide
browser automation capabilities to AI assistants like Claude.
"""

from typing import Any, Dict, List, Sequence

from mcp.types import Tool, TextContent

# Import tool definitions and handlers from each category
from .browser_tools import BROWSER_TOOLS, BROWSER_TOOL_HANDLERS
from .navigation_tools import NAVIGATION_TOOLS, NAVIGATION_TOOL_HANDLERS  
from .element_tools import ELEMENT_TOOLS, ELEMENT_TOOL_HANDLERS
from .screenshot_tools import SCREENSHOT_TOOLS, SCREENSHOT_TOOL_HANDLERS
from .script_tools import SCRIPT_TOOLS, SCRIPT_TOOL_HANDLERS
from .advanced_tools import ADVANCED_TOOLS, ADVANCED_TOOL_HANDLERS

# Combine all tools and handlers
ALL_TOOLS = (
    BROWSER_TOOLS +
    NAVIGATION_TOOLS + 
    ELEMENT_TOOLS +
    SCREENSHOT_TOOLS +
    SCRIPT_TOOLS +
    ADVANCED_TOOLS
)

ALL_TOOL_HANDLERS = {
    **BROWSER_TOOL_HANDLERS,
    **NAVIGATION_TOOL_HANDLERS,
    **ELEMENT_TOOL_HANDLERS, 
    **SCREENSHOT_TOOL_HANDLERS,
    **SCRIPT_TOOL_HANDLERS,
    **ADVANCED_TOOL_HANDLERS,
}

# Tool categories for organization
TOOL_CATEGORIES = {
    "browser_management": {
        "description": "Browser lifecycle and configuration management",
        "tools": [tool.name for tool in BROWSER_TOOLS],
        "count": len(BROWSER_TOOLS)
    },
    "navigation_control": {
        "description": "Page navigation and URL management", 
        "tools": [tool.name for tool in NAVIGATION_TOOLS],
        "count": len(NAVIGATION_TOOLS)
    },
    "element_interaction": {
        "description": "Element finding and interaction capabilities",
        "tools": [tool.name for tool in ELEMENT_TOOLS], 
        "count": len(ELEMENT_TOOLS)
    },
    "screenshot_media": {
        "description": "Screenshot and media capture functionality",
        "tools": [tool.name for tool in SCREENSHOT_TOOLS],
        "count": len(SCREENSHOT_TOOLS)
    },
    "script_execution": {
        "description": "JavaScript execution and scripting",
        "tools": [tool.name for tool in SCRIPT_TOOLS],
        "count": len(SCRIPT_TOOLS)
    },
    "advanced_automation": {
        "description": "Advanced automation and protection bypass",
        "tools": [tool.name for tool in ADVANCED_TOOLS],
        "count": len(ADVANCED_TOOLS)
    }
}

# Statistics
TOTAL_TOOLS = len(ALL_TOOLS)
TOTAL_CATEGORIES = len(TOOL_CATEGORIES)

# Export everything
__all__ = [
    # Tool collections
    "ALL_TOOLS",
    "ALL_TOOL_HANDLERS", 
    "TOOL_CATEGORIES",
    
    # Individual category tools
    "BROWSER_TOOLS",
    "NAVIGATION_TOOLS",
    "ELEMENT_TOOLS", 
    "SCREENSHOT_TOOLS",
    "SCRIPT_TOOLS",
    "ADVANCED_TOOLS",
    
    # Individual category handlers
    "BROWSER_TOOL_HANDLERS",
    "NAVIGATION_TOOL_HANDLERS",
    "ELEMENT_TOOL_HANDLERS",
    "SCREENSHOT_TOOL_HANDLERS", 
    "SCRIPT_TOOL_HANDLERS",
    "ADVANCED_TOOL_HANDLERS",
    
    # Statistics
    "TOTAL_TOOLS",
    "TOTAL_CATEGORIES",
    
    # Helper functions
    "get_tool_by_name",
    "get_tools_by_category",
    "get_tool_info",
]


def get_tool_by_name(name: str) -> Tool | None:
    """Get a tool by its name.
    
    Args:
        name: Tool name to search for
        
    Returns:
        Tool object if found, None otherwise
    """
    for tool in ALL_TOOLS:
        if tool.name == name:
            return tool
    return None


def get_tools_by_category(category: str) -> List[Tool]:
    """Get all tools in a specific category.
    
    Args:
        category: Category name (e.g., 'browser_management')
        
    Returns:
        List of tools in the category
    """
    if category not in TOOL_CATEGORIES:
        return []
    
    tool_names = TOOL_CATEGORIES[category]["tools"]
    return [tool for tool in ALL_TOOLS if tool.name in tool_names]


def get_tool_info() -> Dict[str, Any]:
    """Get comprehensive tool information.
    
    Returns:
        Dictionary with tool statistics and information
    """
    return {
        "total_tools": TOTAL_TOOLS,
        "total_categories": TOTAL_CATEGORIES,
        "categories": TOOL_CATEGORIES,
        "tool_names": [tool.name for tool in ALL_TOOLS],
        "capabilities": {
            "browser_automation": True,
            "captcha_bypass": True,
            "network_monitoring": True,
            "element_finding": True,
            "javascript_execution": True,
            "stealth_mode": True,
            "screenshot_capture": True,
            "multi_browser_support": True,
        }
    }


# Utility functions for tool execution

async def execute_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Execute a tool by name with given arguments.
    
    Args:
        name: Tool name to execute
        arguments: Tool arguments
        
    Returns:
        Tool execution result
        
    Raises:
        ValueError: If tool not found
    """
    if name not in ALL_TOOL_HANDLERS:
        raise ValueError(f"Tool '{name}' not found")
    
    handler = ALL_TOOL_HANDLERS[name]
    return await handler(arguments)


def validate_tool_arguments(name: str, arguments: Dict[str, Any]) -> bool:
    """Validate arguments for a specific tool.
    
    Args:
        name: Tool name
        arguments: Arguments to validate
        
    Returns:
        True if arguments are valid
        
    Raises:
        ValueError: If tool not found or arguments invalid
    """
    tool = get_tool_by_name(name)
    if not tool:
        raise ValueError(f"Tool '{name}' not found")
    
    # Basic validation - in a full implementation, this would check against
    # the tool's input schema defined in the Tool object
    required_params = getattr(tool, 'required_parameters', [])
    
    for param in required_params:
        if param not in arguments:
            raise ValueError(f"Missing required parameter: {param}")
    
    return True


# Tool discovery helpers

def search_tools(query: str) -> List[Tool]:
    """Search tools by name or description.
    
    Args:
        query: Search query
        
    Returns:
        List of matching tools
    """
    query_lower = query.lower()
    results = []
    
    for tool in ALL_TOOLS:
        if (query_lower in tool.name.lower() or 
            query_lower in tool.description.lower()):
            results.append(tool)
    
    return results


def get_tools_with_capability(capability: str) -> List[Tool]:
    """Get tools that provide a specific capability.
    
    Args:
        capability: Capability to search for
        
    Returns:
        List of tools with the capability
    """
    capability_mapping = {
        "captcha": ["bypass_cloudflare", "bypass_recaptcha", "enable_stealth_mode"],
        "screenshot": ["take_screenshot", "take_element_screenshot", "generate_pdf"],
        "network": ["enable_network_monitoring", "intercept_requests", "extract_api_responses"],
        "javascript": ["execute_script", "execute_script_on_element", "evaluate_expression"],
        "automation": ["click_element", "type_text", "find_element", "navigate_to"],
    }
    
    tool_names = capability_mapping.get(capability, [])
    return [tool for tool in ALL_TOOLS if tool.name in tool_names]


# Version and compatibility information

TOOLS_VERSION = "1.0.0"
MIN_PYDOLL_VERSION = "2.3.1"
MIN_MCP_VERSION = "1.0.0"

COMPATIBILITY_INFO = {
    "tools_version": TOOLS_VERSION,
    "min_pydoll_version": MIN_PYDOLL_VERSION,
    "min_mcp_version": MIN_MCP_VERSION,
    "supported_browsers": ["chrome", "edge"],
    "supported_platforms": ["windows", "macos", "linux"],
    "python_requirement": ">=3.8",
}


def get_compatibility_info() -> Dict[str, Any]:
    """Get tool compatibility information.
    
    Returns:
        Compatibility information dictionary
    """
    return COMPATIBILITY_INFO.copy()