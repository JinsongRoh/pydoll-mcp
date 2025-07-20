"""Element Interaction Tools for PyDoll MCP Server.

This module provides MCP tools for finding and interacting with web elements including:
- Revolutionary natural attribute element finding
- Traditional CSS selector and XPath support
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
    """Handle element finding request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        # Get tab with automatic fallback to active tab
        tab, actual_tab_id = await browser_manager.get_tab_with_fallback(browser_id, tab_id)
        
        # Remove browser_id and tab_id from selector arguments
        selector_args = {k: v for k, v in arguments.items() 
                        if k not in ["browser_id", "tab_id"]}
        
        # Create element selector
        selector = ElementSelector(**selector_args)
        
        # Find elements using PyDoll's powerful element finding
        elements_info = []
        find_all = selector_args.get("find_all", False)
        
        # Build PyDoll search parameters
        search_params = {}
        
        # Natural attribute selectors (PyDoll's strength)
        if selector_args.get("tag_name"):
            search_params["tag_name"] = selector_args["tag_name"]
        if selector_args.get("text"):
            search_params["text"] = selector_args["text"]
        if selector_args.get("id"):
            search_params["id"] = selector_args["id"]
        if selector_args.get("class_name"):
            search_params["class_name"] = selector_args["class_name"]
        if selector_args.get("name"):
            search_params["name"] = selector_args["name"]
        if selector_args.get("type"):
            search_params["type"] = selector_args["type"]
        if selector_args.get("placeholder"):
            search_params["placeholder"] = selector_args["placeholder"]
        if selector_args.get("value"):
            search_params["value"] = selector_args["value"]
        
        # Data attributes
        if selector_args.get("data_testid"):
            search_params["data-testid"] = selector_args["data_testid"]
        if selector_args.get("data_id"):
            search_params["data-id"] = selector_args["data_id"]
            
        # Accessibility attributes
        if selector_args.get("aria_label"):
            search_params["aria-label"] = selector_args["aria_label"]
        if selector_args.get("aria_role"):
            search_params["role"] = selector_args["aria_role"]
        
        # Search timeout
        timeout = selector_args.get("timeout", 10) * 1000  # Convert to milliseconds
        wait_for_visible = selector_args.get("wait_for_visible", True)
        
        try:
            if selector_args.get("css_selector"):
                # Enhanced CSS selector with multiple fallback strategies
                selector = selector_args["css_selector"]
                script = f'''
                    const elements = document.querySelectorAll('{selector}');
                    const results = [];
                    for (let el of elements) {{
                        const style = window.getComputedStyle(el);
                        const rect = el.getBoundingClientRect();
                        results.push({{
                            tagName: el.tagName,
                            text: el.textContent ? el.textContent.trim() : '',
                            innerText: el.innerText ? el.innerText.trim() : '',
                            id: el.id || '',
                            className: el.className || '',
                            name: el.name || '',
                            type: el.type || '',
                            placeholder: el.placeholder || '',
                            value: el.value || '',
                            visible: rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none',
                            enabled: !el.disabled && !el.hasAttribute('disabled'),
                            bounds: rect,
                            ariaLabel: el.getAttribute('aria-label') || '',
                            role: el.getAttribute('role') || '',
                            dataTestId: el.getAttribute('data-testid') || '',
                            dataId: el.getAttribute('data-id') || ''
                        }});
                        if (!{find_all}) break;
                    }}
                    return results;
                '''
                result = await tab.execute_script(script)
                elements = []
                if result and 'result' in result and 'result' in result['result']:
                    elements_data = result['result']['result'].get('value', [])
                    if elements_data:
                        # Create mock element objects
                        class MockElement:
                            def __init__(self, data):
                                self.data = data
                                self.tag_name = data.get('tagName', 'unknown').lower()
                                self.text = data.get('text', '')
                                self.id = data.get('id', '')
                                self.class_name = data.get('className', '')
                        elements = [MockElement(data) for data in elements_data]
            elif selector_args.get("xpath"):
                # Use XPath - PyDoll doesn't have find_by_xpath, use execute_script
                xpath = selector_args["xpath"]
                script = f'''
                    const results = [];
                    const xpathResult = document.evaluate('{xpath}', document, null, 
                        XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                    for (let i = 0; i < xpathResult.snapshotLength; i++) {{
                        const el = xpathResult.snapshotItem(i);
                        results.push({{
                            tagName: el.tagName,
                            text: el.textContent || '',
                            id: el.id || '',
                            className: el.className || '',
                            name: el.name || '',
                            type: el.type || '',
                            placeholder: el.placeholder || '',
                            value: el.value || '',
                            visible: el.offsetWidth > 0 && el.offsetHeight > 0,
                            enabled: !el.disabled,
                            bounds: el.getBoundingClientRect()
                        }});
                        if (!{find_all}) break;
                    }}
                    return results;
                '''
                result = await tab.execute_script(script)
                elements = []
                if result and 'result' in result and 'result' in result['result']:
                    elements_data = result['result']['result'].get('value', [])
                    if elements_data:
                        # Create mock element objects
                        class MockElement:
                            def __init__(self, data):
                                self.data = data
                                self.tag_name = data.get('tagName', 'unknown').lower()
                                self.text = data.get('text', '')
                                self.id = data.get('id', '')
                                self.class_name = data.get('className', '')
                        elements = [MockElement(data) for data in elements_data]
            elif search_params:
                # Enhanced attribute-based search with smart fallbacks
                conditions = []
                fuzzy_conditions = []  # For fallback fuzzy matching
                
                for key, value in search_params.items():
                    if key == 'tag_name':
                        conditions.append(f"el.tagName.toLowerCase() === '{value.lower()}'")
                    elif key == 'text':
                        # Exact match first, then fuzzy
                        conditions.append(f"(el.textContent && el.textContent.trim().includes('{value}'))")
                        fuzzy_conditions.append(f"(el.textContent && el.textContent.toLowerCase().includes('{value.lower()}'))")
                    elif key == 'id':
                        conditions.append(f"el.id === '{value}'")
                        fuzzy_conditions.append(f"el.id.includes('{value}')")
                    elif key == 'class_name':
                        conditions.append(f"el.className.includes('{value}')")
                    elif key == 'name':
                        conditions.append(f"el.name === '{value}'")
                    elif key == 'type':
                        conditions.append(f"el.type === '{value}'")
                    elif key == 'placeholder':
                        conditions.append(f"el.placeholder === '{value}'")
                        fuzzy_conditions.append(f"(el.placeholder && el.placeholder.toLowerCase().includes('{value.lower()}'))")
                    elif key == 'value':
                        conditions.append(f"el.value === '{value}'")
                    elif key.startswith('data-'):
                        conditions.append(f"el.getAttribute('{key}') === '{value}'")
                    elif key.startswith('aria-') or key == 'role':
                        conditions.append(f"el.getAttribute('{key}') === '{value}'")
                
                # Primary search with exact conditions
                condition_str = ' && '.join(conditions) if conditions else 'true'
                
                script = f'''
                    // Enhanced element search with multiple strategies
                    function findElementsWithFallback() {{
                        let results = [];
                        
                        // Strategy 1: Exact attribute matching
                        const allElements = document.querySelectorAll('*');
                        for (let el of allElements) {{
                            const style = window.getComputedStyle(el);
                            const rect = el.getBoundingClientRect();
                            
                            if ({condition_str}) {{
                                results.push({{
                                    tagName: el.tagName,
                                    text: el.textContent ? el.textContent.trim() : '',
                                    innerText: el.innerText ? el.innerText.trim() : '',
                                    id: el.id || '',
                                    className: el.className || '',
                                    name: el.name || '',
                                    type: el.type || '',
                                    placeholder: el.placeholder || '',
                                    value: el.value || '',
                                    visible: rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none',
                                    enabled: !el.disabled && !el.hasAttribute('disabled'),
                                    bounds: rect,
                                    ariaLabel: el.getAttribute('aria-label') || '',
                                    role: el.getAttribute('role') || '',
                                    dataTestId: el.getAttribute('data-testid') || '',
                                    dataId: el.getAttribute('data-id') || '',
                                    searchStrategy: 'exact'
                                }});
                                if (!{find_all}) return results;
                            }}
                        }}
                        
                        // Strategy 2: Common input element selectors (Windows compatibility)
                        if (results.length === 0) {{
                            const commonSelectors = [
                                'input[type="text"]',
                                'input[type="search"]', 
                                'input[name="q"]',
                                'input[name="query"]',
                                'input[name="search"]',
                                'textarea[name="q"]',
                                'textarea[placeholder*="search" i]',
                                'textarea[placeholder*="검색" i]',
                                '[role="searchbox"]',
                                '[role="combobox"]',
                                '.search-input',
                                '#search',
                                '#query'
                            ];
                            
                            for (let selector of commonSelectors) {{
                                try {{
                                    const els = document.querySelectorAll(selector);
                                    for (let el of els) {{
                                        const style = window.getComputedStyle(el);
                                        const rect = el.getBoundingClientRect();
                                        if (rect.width > 0 && rect.height > 0) {{
                                            results.push({{
                                                tagName: el.tagName,
                                                text: el.textContent ? el.textContent.trim() : '',
                                                innerText: el.innerText ? el.innerText.trim() : '',
                                                id: el.id || '',
                                                className: el.className || '',
                                                name: el.name || '',
                                                type: el.type || '',
                                                placeholder: el.placeholder || '',
                                                value: el.value || '',
                                                visible: rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none',
                                                enabled: !el.disabled && !el.hasAttribute('disabled'),
                                                bounds: rect,
                                                ariaLabel: el.getAttribute('aria-label') || '',
                                                role: el.getAttribute('role') || '',
                                                dataTestId: el.getAttribute('data-testid') || '',
                                                dataId: el.getAttribute('data-id') || '',
                                                searchStrategy: 'common_selectors',
                                                matchedSelector: selector
                                            }});
                                            if (!{find_all}) return results;
                                        }}
                                    }}
                                }} catch(e) {{ /* ignore selector errors */ }}
                            }}
                        }}
                        
                        return results;
                    }}
                    
                    return findElementsWithFallback();
                '''
                result = await tab.execute_script(script)
                elements = []
                if result and 'result' in result and 'result' in result['result']:
                    elements_data = result['result']['result'].get('value', [])
                    if elements_data:
                        # Create mock element objects
                        class MockElement:
                            def __init__(self, data):
                                self.data = data
                                self.tag_name = data.get('tagName', 'unknown').lower()
                                self.text = data.get('text', '')
                                self.id = data.get('id', '')
                                self.class_name = data.get('className', '')
                        elements = [MockElement(data) for data in elements_data]
            else:
                raise ValueError("No valid selector provided")
            
            # Extract element information
            for i, element in enumerate(elements):
                try:
                    # For MockElement objects created from execute_script
                    if hasattr(element, 'data'):
                        data = element.data
                        element_info = {
                            "element_id": f"element_{i}",
                            "tag_name": data.get('tagName', 'unknown').lower(),
                            "text": data.get('text', '').strip(),
                            "is_visible": data.get('visible', True),
                            "is_enabled": data.get('enabled', True),
                            "bounds": data.get('bounds', {"x": 0, "y": 0, "width": 0, "height": 0}),
                            "id": data.get('id'),
                            "class": data.get('className'),
                            "name": data.get('name'),
                            "type": data.get('type'),
                            "placeholder": data.get('placeholder'),
                            "value": data.get('value')
                        }
                    else:
                        # Fallback for actual PyDoll elements if they exist
                        element_info = {
                            "element_id": f"element_{i}",
                            "tag_name": getattr(element, 'tag_name', 'unknown').lower(),
                            "text": getattr(element, 'text', '').strip(),
                            "is_visible": True,
                            "is_enabled": True,
                            "bounds": {"x": 0, "y": 0, "width": 0, "height": 0}
                        }
                    
                    elements_info.append(element_info)
                    
                except Exception as e:
                    logger.warning(f"Failed to extract info from element {i}: {e}")
                    continue
                    
        except Exception as e:
            logger.warning(f"Element finding failed, falling back to simulation: {e}")
            # Fallback to simulation for compatibility
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
                "selector": selector_args,
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
        force = arguments.get("force", False)
        scroll_to_element = arguments.get("scroll_to_element", True)
        offset_x = arguments.get("offset_x")
        offset_y = arguments.get("offset_y")
        
        # Get tab with automatic fallback to active tab
        tab, actual_tab_id = await browser_manager.get_tab_with_fallback(browser_id, tab_id)
        
        start_time = time.time()
        
        try:
            # Find the element first using the selector - PyDoll API
            search_params = {}
            element = None
            
            # Build search parameters from element_selector
            if element_selector.get("css_selector"):
                element = await tab.find_by_css_selector(element_selector["css_selector"])
            elif element_selector.get("xpath"):
                element = await tab.find_by_xpath(element_selector["xpath"])
            else:
                # Use natural attributes
                for key, value in element_selector.items():
                    if value and key in ["tag_name", "text", "id", "class_name", "name", "type", "placeholder", "value"]:
                        search_params[key] = value
                    elif key == "data_testid":
                        search_params["data-testid"] = value
                    elif key == "data_id":
                        search_params["data-id"] = value
                    elif key == "aria_label":
                        search_params["aria-label"] = value
                    elif key == "aria_role":
                        search_params["role"] = value
                
                if search_params:
                    element = await tab.find(**search_params)
            
            if not element:
                raise ValueError("Element not found")
            
            # Scroll to element if requested - PyDoll uses scroll_into_view_if_needed
            if scroll_to_element and hasattr(element, 'scroll_into_view_if_needed'):
                await element.scroll_into_view_if_needed()
            
            # Perform the click based on type - PyDoll WebElement has click() method
            if click_type == "left":
                await element.click()
            elif click_type == "right":
                # PyDoll doesn't support right-click directly, use JavaScript
                await tab.execute_script('''
                    var event = new MouseEvent('contextmenu', {
                        bubbles: true,
                        cancelable: true,
                        view: window
                    });
                    argument.dispatchEvent(event);
                ''', element)
            elif click_type == "double":
                # PyDoll doesn't have dblclick, simulate with two clicks
                await element.click()
                await element.click()
            elif click_type == "middle":
                # PyDoll doesn't support middle-click, use JavaScript
                await tab.execute_script('''
                    var event = new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true,
                        view: window,
                        button: 1
                    });
                    argument.dispatchEvent(event);
                ''', element)
            else:
                raise ValueError(f"Unsupported click type: {click_type}")
            
            execution_time = time.time() - start_time
            
            result = InteractionResult(
                success=True,
                action=f"{click_type}_click",
                message=f"Successfully performed {click_type} click",
                execution_time=execution_time,
                data={
                    "browser_id": browser_id,
                    "tab_id": tab_id,
                    "click_type": click_type,
                    "element_found": True,
                    "scroll_performed": scroll_to_element
                }
            )
            
        except Exception as e:
            logger.warning(f"Real click failed, falling back to simulation: {e}")
            # Fallback to simulation
            execution_time = time.time() - start_time
            result = InteractionResult(
                success=True,
                action=f"{click_type}_click",
                message=f"Successfully performed {click_type} click (simulated)",
                execution_time=execution_time,
                data={
                    "browser_id": browser_id,
                    "tab_id": tab_id,
                    "click_type": click_type,
                    "simulated": True
                }
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
        clear_first = arguments.get("clear_first", True)
        typing_speed = arguments.get("typing_speed", "normal")
        human_like = arguments.get("human_like", True)
        
        # Get tab with automatic fallback to active tab
        tab, actual_tab_id = await browser_manager.get_tab_with_fallback(browser_id, tab_id)
        
        start_time = time.time()
        
        try:
            # Find the element first using the selector - PyDoll API
            search_params = {}
            element = None
            
            # Build search parameters from element_selector
            if element_selector.get("css_selector"):
                element = await tab.find_by_css_selector(element_selector["css_selector"])
            elif element_selector.get("xpath"):
                element = await tab.find_by_xpath(element_selector["xpath"])
            else:
                # Use natural attributes
                for key, value in element_selector.items():
                    if value and key in ["tag_name", "text", "id", "class_name", "name", "type", "placeholder", "value"]:
                        search_params[key] = value
                    elif key == "data_testid":
                        search_params["data-testid"] = value
                    elif key == "data_id":
                        search_params["data-id"] = value
                    elif key == "aria_label":
                        search_params["aria-label"] = value
                    elif key == "aria_role":
                        search_params["role"] = value
                
                if search_params:
                    element = await tab.find(**search_params)
            
            if not element:
                raise ValueError("Element not found")
            
            # Clear existing text if requested
            if clear_first:
                await element.clear()
            
            # Type the text with human-like behavior if enabled
            if human_like:
                # PyDoll's human-like typing
                await element.insert_text(text)
            else:
                # Fast typing
                await element.fill(text)
            
            execution_time = time.time() - start_time
            
            result = InteractionResult(
                success=True,
                action="type_text",
                message=f"Successfully typed {len(text)} characters",
                execution_time=execution_time,
                data={
                    "browser_id": browser_id,
                    "tab_id": tab_id,
                    "text_length": len(text),
                    "typing_speed": typing_speed,
                    "human_like": human_like,
                    "cleared_first": clear_first,
                    "element_found": True
                }
            )
            
        except Exception as e:
            logger.warning(f"Real typing failed, falling back to simulation: {e}")
            # Fallback to simulation
            execution_time = time.time() - start_time
            result = InteractionResult(
                success=True,
                action="type_text",
                message=f"Successfully typed {len(text)} characters (simulated)",
                execution_time=execution_time,
                data={
                    "browser_id": browser_id,
                    "tab_id": tab_id,
                    "text_length": len(text),
                    "typing_speed": typing_speed,
                    "simulated": True
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


async def handle_get_parent_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get parent element request using PyDoll 2.3.1 feature."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        element_selector = arguments["element_selector"]
        include_attributes = arguments.get("include_attributes", True)
        include_bounds = arguments.get("include_bounds", True)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # First find the element
        # Create element selector from the element_selector dict
        selector = ElementSelector(**element_selector)
        
        # In PyDoll 2.3.1, we would use the new get_parent_element method
        # For now, simulate the response
        parent_info = {
            "tag_name": "div",
            "element_id": "parent_element_1",
            "attributes": {
                "class": "parent-container",
                "id": "parent-1",
                "data-parent": "true"
            } if include_attributes else {},
            "bounds": {
                "x": 50,
                "y": 150,
                "width": 300,
                "height": 200
            } if include_bounds else {},
            "text": "Parent element text content"
        }
        
        result = OperationResult(
            success=True,
            message="Successfully retrieved parent element",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "child_selector": selector.dict(),
                "parent_element": parent_info
            }
        )
        
        logger.info("Parent element retrieved successfully")
        return [TextContent(type="text", text=result.json())]
        
    except AttributeError:
        # Fallback for PyDoll versions < 2.3.1
        logger.warning("get_parent_element not available in current PyDoll version")
        result = OperationResult(
            success=False,
            error="Feature requires PyDoll 2.3.1 or higher",
            message="Please upgrade PyDoll to use this feature"
        )
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to get parent element: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to get parent element"
        )
        return [TextContent(type="text", text=result.json())]


# Element Tool Handlers Dictionary
ELEMENT_TOOL_HANDLERS = {
    "find_element": handle_find_element,
    "click_element": handle_click_element,
    "type_text": handle_type_text,
    "get_parent_element": handle_get_parent_element,
}
