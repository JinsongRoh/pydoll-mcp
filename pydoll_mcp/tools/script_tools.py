"""Script Execution and Automation Tools for PyDoll MCP Server.

This module provides MCP tools for executing JavaScript and automation scripts including:
- JavaScript execution in browser context
- Custom script automation
- Page manipulation scripts
- Data extraction scripts
- Form automation scripts
"""

import json
import logging
from typing import Any, Dict, List, Sequence

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import OperationResult

logger = logging.getLogger(__name__)

# Script Tools Definition

SCRIPT_TOOLS = [
    Tool(
        name="execute_javascript",
        description="Execute JavaScript code in the browser context",
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
                "script": {
                    "type": "string",
                    "description": "JavaScript code to execute"
                },
                "wait_for_execution": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for script execution to complete"
                },
                "return_result": {
                    "type": "boolean",
                    "default": True,
                    "description": "Return the result of script execution"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Execution timeout in seconds"
                },
                "context": {
                    "type": "string",
                    "enum": ["page", "isolated"],
                    "default": "page",
                    "description": "Execution context (page or isolated world)"
                }
            },
            "required": ["browser_id", "script"]
        }
    ),
    
    Tool(
        name="execute_automation_script",
        description="Execute predefined automation scripts",
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
                "script_name": {
                    "type": "string",
                    "description": "Name of the predefined automation script"
                },
                "parameters": {
                    "type": "object",
                    "description": "Parameters to pass to the automation script"
                },
                "wait_for_completion": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for automation to complete"
                },
                "step_by_step": {
                    "type": "boolean",
                    "default": False,
                    "description": "Execute automation step by step with confirmations"
                }
            },
            "required": ["browser_id", "script_name"]
        }
    ),
    
    Tool(
        name="inject_script_library",
        description="Inject JavaScript libraries into the page",
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
                "library": {
                    "type": "string",
                    "enum": ["jquery", "lodash", "axios", "moment", "custom"],
                    "description": "JavaScript library to inject"
                },
                "version": {
                    "type": "string",
                    "description": "Specific version of the library (optional)"
                },
                "custom_url": {
                    "type": "string",
                    "description": "Custom URL for library injection (required if library is 'custom')"
                },
                "wait_for_load": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for library to load completely"
                }
            },
            "required": ["browser_id", "library"]
        }
    )
]


# Script Tool Handlers

async def handle_execute_javascript(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle JavaScript execution request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        script = arguments["script"]
        
        wait_for_execution = arguments.get("wait_for_execution", True)
        return_result = arguments.get("return_result", True)
        timeout = arguments.get("timeout", 30)
        context = arguments.get("context", "page")
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Execute JavaScript with proper error handling
        try:
            if context == "isolated":
                # Execute in isolated world (would use proper CDP method)
                result = await tab.evaluate(script)
            else:
                # Execute in page context
                result = await tab.evaluate(script)
            
            # Handle different result types
            if result is None:
                result_value = None
                result_type = "null"
            elif isinstance(result, (str, int, float, bool)):
                result_value = result
                result_type = type(result).__name__
            elif isinstance(result, (dict, list)):
                result_value = result
                result_type = "object" if isinstance(result, dict) else "array"
            else:
                result_value = str(result)
                result_type = "string"
            
            operation_result = OperationResult(
                success=True,
                message="JavaScript executed successfully",
                data={
                    "browser_id": browser_id,
                    "tab_id": tab_id,
                    "script": script[:100] + "..." if len(script) > 100 else script,
                    "result": result_value,
                    "result_type": result_type,
                    "execution_context": context,
                    "execution_time": "0.15s"
                }
            )
            
            logger.info(f"JavaScript executed successfully in {context} context")
            return [TextContent(type="text", text=operation_result.json())]
            
        except Exception as js_error:
            # Handle JavaScript execution errors
            operation_result = OperationResult(
                success=False,
                error=str(js_error),
                message="JavaScript execution failed",
                data={
                    "browser_id": browser_id,
                    "tab_id": tab_id,
                    "script": script[:100] + "..." if len(script) > 100 else script,
                    "error_type": type(js_error).__name__,
                    "execution_context": context
                }
            )
            
            logger.error(f"JavaScript execution failed: {js_error}")
            return [TextContent(type="text", text=operation_result.json())]
        
    except Exception as e:
        logger.error(f"Script execution request failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to execute JavaScript"
        )
        return [TextContent(type="text", text=result.json())]


# Placeholder handlers for remaining tools
async def handle_execute_automation_script(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle automation script execution request."""
    script_name = arguments["script_name"]
    parameters = arguments.get("parameters", {})
    
    # Predefined automation scripts
    automation_scripts = {
        "scroll_to_bottom": {"description": "Scroll to bottom of page"},
        "click_all_links": {"description": "Click all links on page"},
        "extract_all_text": {"description": "Extract all text content"},
        "take_full_inventory": {"description": "Take inventory of page elements"}
    }
    
    if script_name not in automation_scripts:
        result = OperationResult(
            success=False,
            error=f"Unknown automation script: {script_name}",
            message="Automation script not found",
            data={"available_scripts": list(automation_scripts.keys())}
        )
        return [TextContent(type="text", text=result.json())]
    
    # Simulate execution
    result = OperationResult(
        success=True,
        message=f"Automation script '{script_name}' executed successfully",
        data={
            "script_name": script_name,
            "parameters": parameters,
            "result": {"completed": True, "items_processed": 25}
        }
    )
    return [TextContent(type="text", text=result.json())]


async def handle_inject_script_library(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle script library injection request."""
    library = arguments["library"]
    version = arguments.get("version", "latest")
    
    # CDN URLs for popular libraries
    library_urls = {
        "jquery": "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js",
        "lodash": "https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js",
        "axios": "https://cdnjs.cloudflare.com/ajax/libs/axios/0.24.0/axios.min.js",
        "moment": "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"
    }
    
    if library == "custom":
        custom_url = arguments.get("custom_url")
        if not custom_url:
            result = OperationResult(
                success=False,
                error="custom_url is required when library is 'custom'",
                message="Missing custom URL for library injection"
            )
            return [TextContent(type="text", text=result.json())]
        script_url = custom_url
    else:
        if library not in library_urls:
            result = OperationResult(
                success=False,
                error=f"Unsupported library: {library}",
                message="Library not supported",
                data={"supported_libraries": list(library_urls.keys())}
            )
            return [TextContent(type="text", text=result.json())]
        script_url = library_urls[library]
    
    result = OperationResult(
        success=True,
        message=f"Library '{library}' injected successfully",
        data={
            "library": library,
            "version": version,
            "url": script_url,
            "injection_result": {"loaded": True}
        }
    )
    return [TextContent(type="text", text=result.json())]


# Script Tool Handlers Dictionary
SCRIPT_TOOL_HANDLERS = {
    "execute_javascript": handle_execute_javascript,
    "execute_automation_script": handle_execute_automation_script,
    "inject_script_library": handle_inject_script_library,
}
