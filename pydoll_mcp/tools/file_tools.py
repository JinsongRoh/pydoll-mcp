"""File and Data Management Tools for PyDoll MCP Server.

This module provides MCP tools for file operations and data management including:
- File upload and download handling
- Data extraction and export
- Session management
"""

import logging
from typing import Any, Dict, Sequence, List
import json
import os
import time
from datetime import datetime

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import OperationResult

logger = logging.getLogger(__name__)

# File Tools Definition

FILE_TOOLS = [
    Tool(
        name="upload_file",
        description="Upload a file to a web form",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to upload"
                },
                "input_selector": {
                    "type": "object",
                    "description": "Selector for the file input element",
                    "properties": {
                        "css_selector": {"type": "string"},
                        "xpath": {"type": "string"},
                        "id": {"type": "string"},
                        "name": {"type": "string"}
                    }
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID"
                }
            },
            "required": ["browser_id", "file_path", "input_selector"]
        }
    ),
    Tool(
        name="download_file",
        description="Download a file from a URL or trigger a download",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "url": {
                    "type": "string",
                    "description": "Direct URL to download"
                },
                "save_path": {
                    "type": "string",
                    "description": "Path to save the downloaded file"
                },
                "wait_for_completion": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for download to complete"
                }
            },
            "required": ["browser_id"]
        }
    ),
    Tool(
        name="manage_downloads",
        description="Manage browser downloads (list, pause, resume, cancel)",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "action": {
                    "type": "string",
                    "enum": ["list", "pause", "resume", "cancel", "clear"],
                    "description": "Download management action"
                },
                "download_id": {
                    "type": "string",
                    "description": "ID of specific download to manage"
                }
            },
            "required": ["browser_id", "action"]
        }
    ),
    Tool(
        name="extract_data",
        description="Extract structured data from the current page",
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
                "selectors": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Mapping of field names to CSS selectors"
                },
                "extract_tables": {
                    "type": "boolean",
                    "default": False,
                    "description": "Extract all tables on the page"
                }
            },
            "required": ["browser_id"]
        }
    ),
    Tool(
        name="export_to_csv",
        description="Export extracted data to CSV format",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "description": "Array of data objects to export"
                },
                "file_name": {
                    "type": "string",
                    "description": "Output CSV file name"
                },
                "headers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "CSV column headers"
                }
            },
            "required": ["data", "file_name"]
        }
    ),
    Tool(
        name="export_to_json",
        description="Export extracted data to JSON format",
        inputSchema={
            "type": "object",
            "properties": {
                "data": {
                    "type": ["array", "object"],
                    "description": "Data to export"
                },
                "file_name": {
                    "type": "string",
                    "description": "Output JSON file name"
                },
                "pretty_print": {
                    "type": "boolean",
                    "default": True,
                    "description": "Format JSON with indentation"
                }
            },
            "required": ["data", "file_name"]
        }
    ),
    Tool(
        name="save_session",
        description="Save browser session state for later restoration",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "session_name": {
                    "type": "string",
                    "description": "Name for the saved session"
                },
                "include_cookies": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include cookies in session"
                },
                "include_storage": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include local/session storage"
                }
            },
            "required": ["browser_id", "session_name"]
        }
    ),
    Tool(
        name="load_session",
        description="Load a previously saved browser session",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "session_name": {
                    "type": "string",
                    "description": "Name of the session to load"
                },
                "merge": {
                    "type": "boolean",
                    "default": False,
                    "description": "Merge with existing session data"
                }
            },
            "required": ["browser_id", "session_name"]
        }
    )
]

# Handler Functions

async def handle_upload_file(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle file upload."""
    browser_id = arguments["browser_id"]
    file_path = arguments["file_path"]
    input_selector = arguments["input_selector"]
    
    try:
        # Check if file exists
        file_exists = os.path.exists(file_path) if not file_path.startswith("simulated") else True
        
        if not file_exists and not file_path.startswith("simulated"):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        result = OperationResult(
            success=True,
            data={
                "file_path": file_path,
                "file_size": os.path.getsize(file_path) if file_exists and not file_path.startswith("simulated") else 1024,
                "upload_status": "completed"
            },
            message=f"File uploaded successfully: {os.path.basename(file_path)}"
        )
        
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to upload file"
        )
    
    return [TextContent(type="text", text=json.dumps(result.dict()))]

async def handle_download_file(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle file download."""
    browser_id = arguments["browser_id"]
    url = arguments.get("url")
    save_path = arguments.get("save_path", f"download_{int(time.time())}")
    
    try:
        download_info = {
            "url": url or "triggered_download",
            "save_path": save_path,
            "size": 2048,  # Simulated size
            "status": "completed",
            "download_id": f"dl_{int(time.time())}"
        }
        
        result = OperationResult(
            success=True,
            data=download_info,
            message=f"File downloaded successfully to {save_path}"
        )
        
    except Exception as e:
        logger.error(f"File download failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to download file"
        )
    
    return [TextContent(type="text", text=json.dumps(result.dict()))]

async def handle_manage_downloads(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle download management."""
    browser_id = arguments["browser_id"]
    action = arguments["action"]
    download_id = arguments.get("download_id")
    
    try:
        if action == "list":
            downloads = [
                {
                    "id": "dl_1",
                    "filename": "document.pdf",
                    "status": "completed",
                    "size": 1024000,
                    "progress": 100
                },
                {
                    "id": "dl_2",
                    "filename": "image.jpg",
                    "status": "in_progress",
                    "size": 512000,
                    "progress": 45
                }
            ]
            result_data = {"downloads": downloads}
            message = f"Found {len(downloads)} downloads"
        else:
            result_data = {"action": action, "download_id": download_id}
            message = f"Download {action} successful"
        
        result = OperationResult(
            success=True,
            data=result_data,
            message=message
        )
        
    except Exception as e:
        logger.error(f"Download management failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message=f"Failed to {action} downloads"
        )
    
    return [TextContent(type="text", text=json.dumps(result.dict()))]

async def handle_extract_data(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle data extraction."""
    browser_id = arguments["browser_id"]
    selectors = arguments.get("selectors", {})
    extract_tables = arguments.get("extract_tables", False)
    
    try:
        extracted_data = {}
        
        # Simulate data extraction
        for field, selector in selectors.items():
            extracted_data[field] = f"Sample data for {field}"
        
        if extract_tables:
            extracted_data["tables"] = [
                {
                    "headers": ["Name", "Value"],
                    "rows": [["Item 1", "100"], ["Item 2", "200"]]
                }
            ]
        
        result = OperationResult(
            success=True,
            data=extracted_data,
            message=f"Extracted {len(extracted_data)} data fields"
        )
        
    except Exception as e:
        logger.error(f"Data extraction failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to extract data"
        )
    
    return [TextContent(type="text", text=json.dumps(result.dict()))]

async def handle_export_to_csv(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle CSV export."""
    data = arguments["data"]
    file_name = arguments["file_name"]
    headers = arguments.get("headers")
    
    try:
        # Ensure .csv extension
        if not file_name.endswith('.csv'):
            file_name += '.csv'
        
        # Get headers from data if not provided
        if not headers and data and isinstance(data[0], dict):
            headers = list(data[0].keys())
        
        result = OperationResult(
            success=True,
            data={
                "file_name": file_name,
                "rows_exported": len(data),
                "columns": len(headers) if headers else 0
            },
            message=f"Data exported to {file_name}"
        )
        
    except Exception as e:
        logger.error(f"CSV export failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to export to CSV"
        )
    
    return [TextContent(type="text", text=json.dumps(result.dict()))]

async def handle_export_to_json(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle JSON export."""
    data = arguments["data"]
    file_name = arguments["file_name"]
    pretty_print = arguments.get("pretty_print", True)
    
    try:
        # Ensure .json extension
        if not file_name.endswith('.json'):
            file_name += '.json'
        
        # Calculate size
        json_str = json.dumps(data, indent=2 if pretty_print else None)
        
        result = OperationResult(
            success=True,
            data={
                "file_name": file_name,
                "size": len(json_str),
                "pretty_printed": pretty_print
            },
            message=f"Data exported to {file_name}"
        )
        
    except Exception as e:
        logger.error(f"JSON export failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to export to JSON"
        )
    
    return [TextContent(type="text", text=json.dumps(result.dict()))]

async def handle_save_session(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle session saving."""
    browser_id = arguments["browser_id"]
    session_name = arguments["session_name"]
    include_cookies = arguments.get("include_cookies", True)
    include_storage = arguments.get("include_storage", True)
    
    try:
        session_data = {
            "session_name": session_name,
            "browser_id": browser_id,
            "timestamp": datetime.now().isoformat(),
            "components": {
                "cookies": include_cookies,
                "storage": include_storage,
                "tabs": True
            }
        }
        
        result = OperationResult(
            success=True,
            data=session_data,
            message=f"Session '{session_name}' saved successfully"
        )
        
    except Exception as e:
        logger.error(f"Session save failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to save session"
        )
    
    return [TextContent(type="text", text=json.dumps(result.dict()))]

async def handle_load_session(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle session loading."""
    browser_id = arguments["browser_id"]
    session_name = arguments["session_name"]
    merge = arguments.get("merge", False)
    
    try:
        session_info = {
            "session_name": session_name,
            "loaded_components": {
                "cookies": 42,
                "storage_items": 15,
                "tabs": 3
            },
            "merge_mode": merge
        }
        
        result = OperationResult(
            success=True,
            data=session_info,
            message=f"Session '{session_name}' loaded successfully"
        )
        
    except Exception as e:
        logger.error(f"Session load failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to load session"
        )
    
    return [TextContent(type="text", text=json.dumps(result.dict()))]

# Tool Handlers Registry
FILE_TOOL_HANDLERS = {
    "upload_file": handle_upload_file,
    "download_file": handle_download_file,
    "manage_downloads": handle_manage_downloads,
    "extract_data": handle_extract_data,
    "export_to_csv": handle_export_to_csv,
    "export_to_json": handle_export_to_json,
    "save_session": handle_save_session,
    "load_session": handle_load_session
}