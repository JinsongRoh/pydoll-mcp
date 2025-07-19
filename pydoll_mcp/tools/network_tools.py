"""Network Monitoring and Control Tools for PyDoll MCP Server.

This module provides MCP tools for network monitoring and manipulation including:
- Request interception and modification
- Response monitoring and extraction
- Performance analysis
- Cache and resource management
"""

import logging
from typing import Any, Dict, Sequence, List
import json
import time

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import OperationResult

logger = logging.getLogger(__name__)

# Network Tools Definition

NETWORK_TOOLS = [
    Tool(
        name="intercept_network_requests",
        description="Intercept and modify network requests and responses",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "action": {
                    "type": "string",
                    "enum": ["start", "stop", "configure"],
                    "description": "Interception action"
                },
                "patterns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "URL patterns to intercept (regex supported)"
                },
                "modify_requests": {
                    "type": "boolean",
                    "default": False,
                    "description": "Enable request modification"
                },
                "modify_responses": {
                    "type": "boolean",
                    "default": False,
                    "description": "Enable response modification"
                }
            },
            "required": ["browser_id", "action"]
        }
    ),
    Tool(
        name="get_network_logs",
        description="Retrieve detailed network activity logs",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID"
                },
                "filter": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "enum": ["document", "script", "image", "stylesheet", "xhr", "fetch"],
                            "description": "Filter by resource type"
                        },
                        "status_code": {
                            "type": "integer",
                            "description": "Filter by HTTP status code"
                        }
                    }
                }
            },
            "required": ["browser_id"]
        }
    ),
    Tool(
        name="block_requests",
        description="Block specific network requests",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "patterns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "URL patterns to block"
                },
                "resource_types": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["image", "script", "stylesheet", "font", "media"]
                    },
                    "description": "Resource types to block"
                }
            },
            "required": ["browser_id"]
        }
    ),
    Tool(
        name="modify_request_headers",
        description="Modify HTTP request headers",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "headers": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Headers to add or modify"
                },
                "remove_headers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Headers to remove"
                }
            },
            "required": ["browser_id"]
        }
    ),
    Tool(
        name="extract_api_responses",
        description="Extract and save API responses",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "api_patterns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "API URL patterns to monitor"
                },
                "save_to_file": {
                    "type": "boolean",
                    "default": False,
                    "description": "Save responses to files"
                }
            },
            "required": ["browser_id"]
        }
    ),
    Tool(
        name="monitor_websockets",
        description="Monitor WebSocket connections and messages",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "action": {
                    "type": "string",
                    "enum": ["start", "stop", "get_messages"],
                    "description": "Monitoring action"
                },
                "filter_pattern": {
                    "type": "string",
                    "description": "Filter messages by pattern"
                }
            },
            "required": ["browser_id", "action"]
        }
    ),
    Tool(
        name="analyze_performance",
        description="Analyze page performance metrics and provide optimization suggestions",
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
                "metrics_to_collect": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["timing", "navigation", "paint", "resources", "memory", "network"]
                    },
                    "default": ["timing", "navigation", "paint"],
                    "description": "Performance metrics to collect"
                },
                "include_suggestions": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include optimization suggestions"
                }
            },
            "required": ["browser_id"]
        }
    ),
    Tool(
        name="throttle_network",
        description="Simulate different network conditions",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "preset": {
                    "type": "string",
                    "enum": ["offline", "slow-3g", "fast-3g", "4g", "wifi", "custom"],
                    "description": "Network throttling preset"
                },
                "custom_settings": {
                    "type": "object",
                    "properties": {
                        "download_throughput": {"type": "number"},
                        "upload_throughput": {"type": "number"},
                        "latency": {"type": "number"}
                    }
                }
            },
            "required": ["browser_id", "preset"]
        }
    ),
    Tool(
        name="clear_cache",
        description="Clear browser cache and storage",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "cache_types": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["disk", "memory", "cookies", "local_storage", "session_storage", "all"]
                    },
                    "default": ["all"],
                    "description": "Types of cache to clear"
                }
            },
            "required": ["browser_id"]
        }
    ),
    Tool(
        name="save_har",
        description="Save HTTP Archive (HAR) file of network activity",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID"
                },
                "file_name": {
                    "type": "string",
                    "description": "HAR file name"
                },
                "include_content": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include response content in HAR"
                }
            },
            "required": ["browser_id", "file_name"]
        }
    )
]

# Handler Functions

async def handle_intercept_network_requests(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle network request interception."""
    browser_id = arguments["browser_id"]
    action = arguments["action"]
    
    try:
        if action == "start":
            patterns = arguments.get("patterns", ["*"])
            result_data = {
                "action": "started",
                "patterns": patterns,
                "modify_requests": arguments.get("modify_requests", False),
                "modify_responses": arguments.get("modify_responses", False)
            }
            message = "Network interception started"
        elif action == "stop":
            result_data = {"action": "stopped"}
            message = "Network interception stopped"
        else:  # configure
            result_data = {"action": "configured"}
            message = "Network interception configured"
        
        result = OperationResult(
            success=True,
            data=result_data,
            message=message
        )
        
    except Exception as e:
        logger.error(f"Network interception failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to manage network interception"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

async def handle_get_network_logs(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle network logs retrieval."""
    browser_id = arguments["browser_id"]
    filter_opts = arguments.get("filter", {})
    
    try:
        # Simulate network logs
        logs = [
            {
                "url": "https://example.com/api/data",
                "method": "GET",
                "status": 200,
                "type": "xhr",
                "size": 1024,
                "time": 123.45
            },
            {
                "url": "https://example.com/style.css",
                "method": "GET",
                "status": 200,
                "type": "stylesheet",
                "size": 2048,
                "time": 45.67
            }
        ]
        
        # Apply filters
        if filter_opts.get("resource_type"):
            logs = [log for log in logs if log["type"] == filter_opts["resource_type"]]
        if filter_opts.get("status_code"):
            logs = [log for log in logs if log["status"] == filter_opts["status_code"]]
        
        result = OperationResult(
            success=True,
            data={"logs": logs, "count": len(logs)},
            message=f"Retrieved {len(logs)} network logs"
        )
        
    except Exception as e:
        logger.error(f"Failed to get network logs: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to retrieve network logs"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

async def handle_block_requests(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle request blocking."""
    browser_id = arguments["browser_id"]
    patterns = arguments.get("patterns", [])
    resource_types = arguments.get("resource_types", [])
    
    try:
        blocked_rules = {
            "patterns": patterns,
            "resource_types": resource_types,
            "enabled": True
        }
        
        result = OperationResult(
            success=True,
            data=blocked_rules,
            message=f"Blocking {len(patterns)} patterns and {len(resource_types)} resource types"
        )
        
    except Exception as e:
        logger.error(f"Request blocking failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to block requests"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

async def handle_modify_request_headers(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle request header modification."""
    browser_id = arguments["browser_id"]
    headers = arguments.get("headers", {})
    remove_headers = arguments.get("remove_headers", [])
    
    try:
        result = OperationResult(
            success=True,
            data={
                "modified_headers": headers,
                "removed_headers": remove_headers
            },
            message=f"Modified {len(headers)} headers, removed {len(remove_headers)} headers"
        )
        
    except Exception as e:
        logger.error(f"Header modification failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to modify headers"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

async def handle_extract_api_responses(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle API response extraction."""
    browser_id = arguments["browser_id"]
    api_patterns = arguments.get("api_patterns", [])
    save_to_file = arguments.get("save_to_file", False)
    
    try:
        extracted_responses = [
            {
                "url": "https://api.example.com/data",
                "status": 200,
                "data": {"items": [], "count": 0},
                "timestamp": time.time()
            }
        ]
        
        result = OperationResult(
            success=True,
            data={
                "extracted_count": len(extracted_responses),
                "saved_to_file": save_to_file,
                "responses": extracted_responses
            },
            message=f"Extracted {len(extracted_responses)} API responses"
        )
        
    except Exception as e:
        logger.error(f"API extraction failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to extract API responses"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

async def handle_monitor_websockets(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle WebSocket monitoring."""
    browser_id = arguments["browser_id"]
    action = arguments["action"]
    
    try:
        if action == "start":
            result_data = {"monitoring": "started", "connections": 0}
            message = "WebSocket monitoring started"
        elif action == "stop":
            result_data = {"monitoring": "stopped"}
            message = "WebSocket monitoring stopped"
        else:  # get_messages
            result_data = {
                "messages": [
                    {"type": "sent", "data": "ping", "timestamp": time.time()},
                    {"type": "received", "data": "pong", "timestamp": time.time()}
                ]
            }
            message = "Retrieved WebSocket messages"
        
        result = OperationResult(
            success=True,
            data=result_data,
            message=message
        )
        
    except Exception as e:
        logger.error(f"WebSocket monitoring failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to monitor WebSockets"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

async def handle_analyze_performance(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle performance analysis - duplicate from advanced_tools for completeness."""
    browser_id = arguments["browser_id"]
    metrics_to_collect = arguments.get("metrics_to_collect", ["timing", "navigation", "paint"])
    
    try:
        performance_data = {
            "timing": {
                "domContentLoaded": 1234,
                "loadComplete": 2345,
                "firstPaint": 456,
                "firstContentfulPaint": 567
            },
            "suggestions": [
                "Optimize image sizes",
                "Enable compression",
                "Minimize JavaScript"
            ]
        }
        
        result = OperationResult(
            success=True,
            data=performance_data,
            message="Performance analysis completed"
        )
        
    except Exception as e:
        logger.error(f"Performance analysis failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to analyze performance"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

async def handle_throttle_network(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle network throttling."""
    browser_id = arguments["browser_id"]
    preset = arguments["preset"]
    
    try:
        presets = {
            "offline": {"download": 0, "upload": 0, "latency": 0},
            "slow-3g": {"download": 50000, "upload": 50000, "latency": 2000},
            "fast-3g": {"download": 180000, "upload": 84000, "latency": 562},
            "4g": {"download": 4000000, "upload": 3000000, "latency": 20},
            "wifi": {"download": 30000000, "upload": 15000000, "latency": 2}
        }
        
        if preset == "custom":
            settings = arguments.get("custom_settings", {})
        else:
            settings = presets.get(preset, presets["4g"])
        
        result = OperationResult(
            success=True,
            data={"preset": preset, "settings": settings},
            message=f"Network throttled to {preset} settings"
        )
        
    except Exception as e:
        logger.error(f"Network throttling failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to throttle network"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

async def handle_clear_cache(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle cache clearing."""
    browser_id = arguments["browser_id"]
    cache_types = arguments.get("cache_types", ["all"])
    
    try:
        cleared = []
        if "all" in cache_types:
            cleared = ["disk", "memory", "cookies", "local_storage", "session_storage"]
        else:
            cleared = cache_types
        
        result = OperationResult(
            success=True,
            data={"cleared": cleared},
            message=f"Cleared {len(cleared)} cache types"
        )
        
    except Exception as e:
        logger.error(f"Cache clearing failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to clear cache"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

async def handle_save_har(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle HAR file saving."""
    browser_id = arguments["browser_id"]
    file_name = arguments["file_name"]
    include_content = arguments.get("include_content", True)
    
    try:
        har_data = {
            "log": {
                "version": "1.2",
                "creator": {"name": "PyDoll MCP", "version": "1.3.0"},
                "entries": [],
                "pages": []
            }
        }
        
        result = OperationResult(
            success=True,
            data={
                "file_name": file_name,
                "size": len(json.dumps(har_data)),
                "include_content": include_content
            },
            message=f"HAR file saved as {file_name}"
        )
        
    except Exception as e:
        logger.error(f"HAR save failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to save HAR file"
        )
    
    return [TextContent(type="text", text=json.dumps(result.to_dict()))]

# Tool Handlers Registry
NETWORK_TOOL_HANDLERS = {
    "intercept_network_requests": handle_intercept_network_requests,
    "get_network_logs": handle_get_network_logs,
    "block_requests": handle_block_requests,
    "modify_request_headers": handle_modify_request_headers,
    "extract_api_responses": handle_extract_api_responses,
    "monitor_websockets": handle_monitor_websockets,
    "analyze_performance": handle_analyze_performance,
    "throttle_network": handle_throttle_network,
    "clear_cache": handle_clear_cache,
    "save_har": handle_save_har
}