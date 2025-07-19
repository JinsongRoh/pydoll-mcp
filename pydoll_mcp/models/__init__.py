"""Data models for PyDoll MCP Server.

This module contains Pydantic models for request/response validation,
configuration management, and data structure definitions.
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic.types import StrictBool, StrictInt, StrictStr

# Version information
__version__ = "1.0.0"

# Export all model classes
__all__ = [
    # Base models
    "BaseRequest",
    "BaseResponse", 
    "ErrorResponse",
    
    # Browser models
    "BrowserConfig",
    "BrowserInstance",
    "BrowserStatus",
    "TabInfo",
    
    # Element models
    "ElementSelector",
    "ElementInfo",
    "InteractionResult",
    
    # Network models
    "NetworkRequest",
    "NetworkResponse",
    "NetworkFilter",
    
    # Screenshot models
    "ScreenshotConfig",
    "ScreenshotResult",
    
    # Configuration models
    "ServerConfig",
    "ToolConfig",
    
    # Result models
    "OperationResult",
    "BatchResult",
]


# Base Models

class BaseRequest(BaseModel):
    """Base class for all request models."""
    
    operation_id: Optional[str] = Field(None, description="Unique operation identifier")
    timeout: Optional[int] = Field(30, description="Operation timeout in seconds")
    
    class Config:
        extra = "forbid"
        validate_assignment = True


class BaseResponse(BaseModel):
    """Base class for all response models."""
    
    success: StrictBool = Field(description="Whether the operation succeeded")
    message: Optional[str] = Field(None, description="Human-readable message")
    operation_id: Optional[str] = Field(None, description="Operation identifier")
    timestamp: Optional[str] = Field(None, description="Response timestamp")
    
    class Config:
        extra = "forbid"


class ErrorResponse(BaseResponse):
    """Error response model."""
    
    success: StrictBool = Field(False, description="Always False for errors")
    error_code: Optional[str] = Field(None, description="Error code")
    error_type: Optional[str] = Field(None, description="Error type")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    @validator('success')
    def success_must_be_false(cls, v):
        if v is not False:
            raise ValueError('success must be False for error responses')
        return v


# Browser Models

class BrowserConfig(BaseModel):
    """Browser configuration model."""
    
    browser_type: str = Field("chrome", description="Browser type (chrome, edge)")
    headless: bool = Field(False, description="Run browser in headless mode")
    window_width: int = Field(1920, description="Browser window width")
    window_height: int = Field(1080, description="Browser window height")
    stealth_mode: bool = Field(True, description="Enable stealth/anti-detection mode")
    proxy_server: Optional[str] = Field(None, description="Proxy server (host:port)")
    user_agent: Optional[str] = Field(None, description="Custom user agent string")
    disable_images: bool = Field(False, description="Disable image loading")
    disable_css: bool = Field(False, description="Disable CSS loading")
    block_ads: bool = Field(True, description="Block advertisement requests")
    enable_captcha_bypass: bool = Field(True, description="Enable automatic captcha bypass")
    custom_args: List[str] = Field(default_factory=list, description="Additional browser arguments")
    start_timeout: int = Field(30, description="Browser startup timeout in seconds (PyDoll 2.3.1+)")
    
    @validator('browser_type')
    def validate_browser_type(cls, v):
        if v.lower() not in ['chrome', 'edge']:
            raise ValueError('browser_type must be "chrome" or "edge"')
        return v.lower()
    
    @validator('window_width', 'window_height')
    def validate_dimensions(cls, v):
        if v < 100 or v > 7680:  # Up to 8K width
            raise ValueError('Window dimensions must be between 100 and 7680')
        return v


class BrowserInstance(BaseModel):
    """Browser instance information model."""
    
    instance_id: str = Field(description="Unique browser instance identifier")
    browser_type: str = Field(description="Browser type")
    pid: Optional[int] = Field(None, description="Browser process ID")
    created_at: str = Field(description="Instance creation timestamp")
    status: str = Field(description="Current status (active, stopped, crashed)")
    tabs_count: int = Field(0, description="Number of open tabs")
    memory_usage: Optional[float] = Field(None, description="Memory usage in MB")
    cpu_usage: Optional[float] = Field(None, description="CPU usage percentage")
    
    class Config:
        schema_extra = {
            "example": {
                "instance_id": "browser_abc123",
                "browser_type": "chrome", 
                "pid": 12345,
                "created_at": "2024-01-15T10:30:00Z",
                "status": "active",
                "tabs_count": 3,
                "memory_usage": 245.6,
                "cpu_usage": 12.5
            }
        }


class BrowserStatus(BaseModel):
    """Browser status model."""
    
    is_running: bool = Field(description="Whether browser is running")
    is_responsive: bool = Field(description="Whether browser is responsive")
    version: Optional[str] = Field(None, description="Browser version")
    user_data_dir: Optional[str] = Field(None, description="User data directory path")
    active_tab_count: int = Field(0, description="Number of active tabs")
    total_memory_usage: Optional[float] = Field(None, description="Total memory usage in MB")


class TabInfo(BaseModel):
    """Tab information model."""
    
    tab_id: str = Field(description="Unique tab identifier")
    title: Optional[str] = Field(None, description="Page title")
    url: Optional[str] = Field(None, description="Current URL")
    status: str = Field("loading", description="Tab status (loading, complete, error)")
    is_active: bool = Field(False, description="Whether tab is currently active")
    favicon_url: Optional[str] = Field(None, description="Favicon URL")


# Element Models

class ElementSelector(BaseModel):
    """Element selector model."""
    
    # Natural attribute selectors
    id: Optional[str] = Field(None, description="Element ID")
    class_name: Optional[str] = Field(None, description="CSS class name") 
    tag_name: Optional[str] = Field(None, description="HTML tag name")
    text: Optional[str] = Field(None, description="Element text content")
    name: Optional[str] = Field(None, description="Element name attribute")
    type: Optional[str] = Field(None, description="Element type attribute")
    
    # Data attributes
    data_testid: Optional[str] = Field(None, description="data-testid attribute")
    data_id: Optional[str] = Field(None, description="data-id attribute")
    
    # Accessibility attributes
    aria_label: Optional[str] = Field(None, description="aria-label attribute")
    aria_role: Optional[str] = Field(None, description="aria-role attribute")
    
    # Traditional selectors
    css_selector: Optional[str] = Field(None, description="CSS selector")
    xpath: Optional[str] = Field(None, description="XPath expression")
    
    # Search options
    find_all: bool = Field(False, description="Find all matching elements")
    timeout: int = Field(10, description="Timeout for element finding")
    wait_for_visible: bool = Field(True, description="Wait for element to be visible")
    
    @validator('timeout')
    def validate_timeout(cls, v):
        if v < 1 or v > 300:  # Max 5 minutes
            raise ValueError('Timeout must be between 1 and 300 seconds')
        return v


class ElementInfo(BaseModel):
    """Element information model."""
    
    element_id: str = Field(description="Internal element identifier")
    tag_name: str = Field(description="HTML tag name")
    text: Optional[str] = Field(None, description="Element text content")
    attributes: Dict[str, str] = Field(default_factory=dict, description="Element attributes")
    bounds: Optional[Dict[str, float]] = Field(None, description="Element bounding box")
    is_visible: bool = Field(False, description="Whether element is visible")
    is_clickable: bool = Field(False, description="Whether element is clickable")


class InteractionResult(BaseModel):
    """Element interaction result model."""
    
    success: bool = Field(description="Whether interaction succeeded")
    action: str = Field(description="Action performed (click, type, etc.)")
    element_id: Optional[str] = Field(None, description="Target element ID")
    message: Optional[str] = Field(None, description="Result message")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")


# Network Models

class NetworkRequest(BaseModel):
    """Network request model."""
    
    request_id: str = Field(description="Unique request identifier")
    url: str = Field(description="Request URL")
    method: str = Field(description="HTTP method")
    headers: Dict[str, str] = Field(default_factory=dict, description="Request headers")
    body: Optional[str] = Field(None, description="Request body")
    timestamp: str = Field(description="Request timestamp")
    resource_type: Optional[str] = Field(None, description="Resource type (xhr, fetch, etc.)")


class NetworkResponse(BaseModel):
    """Network response model."""
    
    request_id: str = Field(description="Corresponding request identifier")
    status_code: int = Field(description="HTTP status code")
    status_text: str = Field(description="HTTP status text")
    headers: Dict[str, str] = Field(default_factory=dict, description="Response headers")
    body: Optional[str] = Field(None, description="Response body")
    size: Optional[int] = Field(None, description="Response size in bytes")
    timing: Optional[Dict[str, float]] = Field(None, description="Request timing information")


class NetworkFilter(BaseModel):
    """Network filtering configuration."""
    
    include_patterns: List[str] = Field(default_factory=list, description="URL patterns to include")
    exclude_patterns: List[str] = Field(default_factory=list, description="URL patterns to exclude")
    resource_types: List[str] = Field(default_factory=list, description="Resource types to monitor")
    capture_bodies: bool = Field(False, description="Whether to capture response bodies")
    max_body_size: int = Field(1048576, description="Maximum body size to capture (bytes)")


# Screenshot Models

class ScreenshotConfig(BaseModel):
    """Screenshot configuration model."""
    
    format: str = Field("png", description="Image format (png, jpeg)")
    quality: Optional[int] = Field(None, description="JPEG quality (1-100)")
    full_page: bool = Field(False, description="Capture full page")
    element_selector: Optional[ElementSelector] = Field(None, description="Element to capture")
    viewport_only: bool = Field(True, description="Capture viewport only")
    hide_scrollbars: bool = Field(True, description="Hide scrollbars in screenshot")
    
    @validator('format')
    def validate_format(cls, v):
        if v.lower() not in ['png', 'jpeg', 'jpg']:
            raise ValueError('format must be "png", "jpeg", or "jpg"')
        return v.lower()
    
    @validator('quality')
    def validate_quality(cls, v):
        if v is not None and (v < 1 or v > 100):
            raise ValueError('quality must be between 1 and 100')
        return v


class ScreenshotResult(BaseModel):
    """Screenshot result model."""
    
    success: bool = Field(description="Whether screenshot was successful")
    file_path: Optional[str] = Field(None, description="Path to saved screenshot file")
    base64_data: Optional[str] = Field(None, description="Base64 encoded image data")
    width: Optional[int] = Field(None, description="Image width in pixels")
    height: Optional[int] = Field(None, description="Image height in pixels")
    file_size: Optional[int] = Field(None, description="File size in bytes")


# Configuration Models

class ServerConfig(BaseModel):
    """Server configuration model."""
    
    log_level: str = Field("INFO", description="Logging level")
    max_browsers: int = Field(3, description="Maximum concurrent browsers")
    max_tabs_per_browser: int = Field(10, description="Maximum tabs per browser")
    cleanup_interval: int = Field(300, description="Cleanup interval in seconds")
    idle_timeout: int = Field(1800, description="Browser idle timeout in seconds")
    enable_telemetry: bool = Field(False, description="Enable usage telemetry")
    
    @validator('log_level')
    def validate_log_level(cls, v):
        if v.upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError('Invalid log level')
        return v.upper()


class ToolConfig(BaseModel):
    """Tool configuration model."""
    
    tool_name: str = Field(description="Tool name")
    enabled: bool = Field(True, description="Whether tool is enabled")
    timeout: int = Field(30, description="Default timeout for tool operations")
    rate_limit: Optional[int] = Field(None, description="Rate limit (requests per minute)")
    custom_settings: Dict[str, Any] = Field(default_factory=dict, description="Custom tool settings")


# Result Models

class OperationResult(BaseModel):
    """Generic operation result model."""
    
    success: bool = Field(description="Whether operation succeeded")
    data: Optional[Dict[str, Any]] = Field(None, description="Operation result data")
    message: Optional[str] = Field(None, description="Result message")
    error: Optional[str] = Field(None, description="Error message if failed")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class BatchResult(BaseModel):
    """Batch operation result model."""
    
    total_operations: int = Field(description="Total number of operations")
    successful_operations: int = Field(description="Number of successful operations")
    failed_operations: int = Field(description="Number of failed operations")
    results: List[OperationResult] = Field(description="Individual operation results")
    execution_time: Optional[float] = Field(None, description="Total execution time")
    
    @validator('successful_operations', 'failed_operations')
    def validate_operation_counts(cls, v, values):
        if 'total_operations' in values:
            total = values['total_operations']
            if v > total:
                raise ValueError('Operation count cannot exceed total')
        return v
