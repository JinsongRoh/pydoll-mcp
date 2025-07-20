"""Advanced Search Automation Tools for PyDoll MCP Server.

This module provides intelligent search automation that can automatically:
- Find search boxes on any website
- Input search terms with human-like behavior
- Execute searches by detecting the right submission method
- Handle various search patterns (Google, Bing, DuckDuckGo, etc.)
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Sequence

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import OperationResult

logger = logging.getLogger(__name__)

# Advanced Search Automation Tools Definition

SEARCH_AUTOMATION_TOOLS = [
    Tool(
        name="intelligent_search",
        description="Intelligently perform search on any website with automatic element detection",
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
                "search_query": {
                    "type": "string",
                    "description": "Search query to input"
                },
                "website_type": {
                    "type": "string",
                    "enum": ["auto", "google", "bing", "duckduckgo", "generic"],
                    "default": "auto",
                    "description": "Type of website for optimized search strategy"
                },
                "submit_method": {
                    "type": "string",
                    "enum": ["auto", "enter", "click", "form"],
                    "default": "auto", 
                    "description": "Method to submit the search"
                },
                "wait_for_results": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for search results to load"
                },
                "typing_speed": {
                    "type": "string",
                    "enum": ["slow", "normal", "fast", "instant"],
                    "default": "normal",
                    "description": "Speed of typing the search query"
                }
            },
            "required": ["browser_id", "search_query"]
        }
    )
]

async def handle_intelligent_search(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle intelligent search automation."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        search_query = arguments["search_query"]
        website_type = arguments.get("website_type", "auto")
        submit_method = arguments.get("submit_method", "auto")
        wait_for_results = arguments.get("wait_for_results", True)
        typing_speed = arguments.get("typing_speed", "normal")
        
        # Get tab with automatic fallback to active tab
        tab, actual_tab_id = await browser_manager.get_tab_with_fallback(browser_id, tab_id)
        
        # Enhanced intelligent search script with multiple strategies
        search_script = f'''
        async function performIntelligentSearch() {{
            const searchQuery = '{search_query}';
            const websiteType = '{website_type}';
            const submitMethod = '{submit_method}';
            const typingSpeed = '{typing_speed}';
            
            let searchResult = {{
                success: false,
                method: '',
                elementFound: false,
                searchExecuted: false,
                details: {{}}
            }};
            
            // Strategy 1: Auto-detect website type if needed
            let detectedSiteType = websiteType;
            if (websiteType === 'auto') {{
                const url = window.location.href.toLowerCase();
                if (url.includes('google.')) detectedSiteType = 'google';
                else if (url.includes('bing.')) detectedSiteType = 'bing';
                else if (url.includes('duckduckgo.')) detectedSiteType = 'duckduckgo';
                else detectedSiteType = 'generic';
            }}
            
            // Strategy 2: Website-specific search element selectors
            let searchSelectors = [];
            switch (detectedSiteType) {{
                case 'google':
                    searchSelectors = [
                        'textarea[name="q"]',
                        'input[name="q"]',
                        '[role="combobox"][name="q"]',
                        'textarea[title*="검색" i]',
                        'textarea[title*="Search" i]'
                    ];
                    break;
                case 'bing':
                    searchSelectors = [
                        'input[name="q"]',
                        '#sb_form_q',
                        '.b_searchbox'
                    ];
                    break;
                case 'duckduckgo':
                    searchSelectors = [
                        'input[name="q"]',
                        '#search_form_input',
                        '.search__input'
                    ];
                    break;
                default:
                    searchSelectors = [
                        'input[type="search"]',
                        'input[name="q"]',
                        'input[name="query"]',
                        'input[name="search"]',
                        'textarea[name="q"]',
                        '[role="searchbox"]',
                        '[role="combobox"]',
                        'input[placeholder*="search" i]',
                        'input[placeholder*="검색" i]',
                        'textarea[placeholder*="search" i]',
                        'textarea[placeholder*="검색" i]',
                        '.search-input',
                        '#search',
                        '#query',
                        '.searchbox'
                    ];
            }}
            
            // Strategy 3: Find search element
            let searchElement = null;
            let foundSelector = '';
            
            for (let selector of searchSelectors) {{
                try {{
                    const elements = document.querySelectorAll(selector);
                    for (let el of elements) {{
                        const rect = el.getBoundingClientRect();
                        const style = window.getComputedStyle(el);
                        
                        // Check if element is visible and interactable
                        if (rect.width > 0 && rect.height > 0 && 
                            style.visibility !== 'hidden' && 
                            style.display !== 'none' &&
                            !el.disabled) {{
                            searchElement = el;
                            foundSelector = selector;
                            break;
                        }}
                    }}
                    if (searchElement) break;
                }} catch(e) {{
                    console.log('Selector failed:', selector, e);
                }}
            }}
            
            if (!searchElement) {{
                searchResult.details.error = 'No search element found';
                return searchResult;
            }}
            
            searchResult.elementFound = true;
            searchResult.details.selector = foundSelector;
            searchResult.details.element = {{
                tagName: searchElement.tagName,
                name: searchElement.name,
                id: searchElement.id,
                placeholder: searchElement.placeholder
            }};
            
            // Strategy 4: Focus and clear the search element
            try {{
                searchElement.focus();
                await new Promise(resolve => setTimeout(resolve, 100));
                
                // Clear existing content
                searchElement.value = '';
                searchElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                await new Promise(resolve => setTimeout(resolve, 100));
            }} catch(e) {{
                console.log('Focus/clear failed:', e);
            }}
            
            // Strategy 5: Type search query with realistic timing
            try {{
                const typeDelay = typingSpeed === 'instant' ? 0 :
                                typingSpeed === 'fast' ? 50 :
                                typingSpeed === 'normal' ? 100 : 200;
                
                for (let i = 0; i < searchQuery.length; i++) {{
                    searchElement.value += searchQuery[i];
                    searchElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    searchElement.dispatchEvent(new Event('keyup', {{ bubbles: true }}));
                    
                    if (typeDelay > 0) {{
                        await new Promise(resolve => setTimeout(resolve, typeDelay + Math.random() * 50));
                    }}
                }}
                
                // Final input event
                searchElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                searchResult.details.textEntered = true;
                
            }} catch(e) {{
                searchResult.details.typeError = e.message;
                return searchResult;
            }}
            
            // Strategy 6: Submit the search
            let submitted = false;
            
            if (submitMethod === 'auto' || submitMethod === 'enter') {{
                try {{
                    // Try Enter key first
                    const enterEvent = new KeyboardEvent('keydown', {{
                        key: 'Enter',
                        code: 'Enter',
                        keyCode: 13,
                        which: 13,
                        bubbles: true,
                        cancelable: true
                    }});
                    searchElement.dispatchEvent(enterEvent);
                    
                    const enterUpEvent = new KeyboardEvent('keyup', {{
                        key: 'Enter',
                        code: 'Enter',
                        keyCode: 13,
                        which: 13,
                        bubbles: true,
                        cancelable: true
                    }});
                    searchElement.dispatchEvent(enterUpEvent);
                    
                    submitted = true;
                    searchResult.method = 'enter';
                }} catch(e) {{
                    console.log('Enter key failed:', e);
                }}
            }}
            
            if (!submitted && (submitMethod === 'auto' || submitMethod === 'click')) {{
                try {{
                    // Find submit button
                    const buttonSelectors = [
                        'button[type="submit"]',
                        'input[type="submit"]',
                        'button[aria-label*="search" i]',
                        'button[aria-label*="검색" i]',
                        '.search-button',
                        '#search-button',
                        '[data-testid*="search"]'
                    ];
                    
                    let submitButton = null;
                    for (let selector of buttonSelectors) {{
                        const buttons = document.querySelectorAll(selector);
                        for (let btn of buttons) {{
                            const rect = btn.getBoundingClientRect();
                            if (rect.width > 0 && rect.height > 0) {{
                                submitButton = btn;
                                break;
                            }}
                        }}
                        if (submitButton) break;
                    }}
                    
                    if (submitButton) {{
                        submitButton.click();
                        submitted = true;
                        searchResult.method = 'click';
                        searchResult.details.submitButton = {{
                            tagName: submitButton.tagName,
                            text: submitButton.textContent,
                            id: submitButton.id
                        }};
                    }}
                }} catch(e) {{
                    console.log('Click submit failed:', e);
                }}
            }}
            
            if (!submitted && (submitMethod === 'auto' || submitMethod === 'form')) {{
                try {{
                    // Try form submission
                    const form = searchElement.closest('form');
                    if (form) {{
                        form.submit();
                        submitted = true;
                        searchResult.method = 'form';
                    }}
                }} catch(e) {{
                    console.log('Form submit failed:', e);
                }}
            }}
            
            searchResult.searchExecuted = submitted;
            searchResult.success = submitted;
            
            return searchResult;
        }}
        
        return await performIntelligentSearch();
        '''
        
        # Execute the intelligent search
        result = await tab.execute_script(search_script)
        search_data = {}
        
        if result and 'result' in result and 'result' in result['result']:
            search_data = result['result']['result'].get('value', {})
        
        # Wait for results if requested
        if wait_for_results and search_data.get('success'):
            await asyncio.sleep(2)  # Give time for results to load
            
            # Check if we're on a results page
            results_check_script = '''
                return {{
                    url: window.location.href,
                    title: document.title,
                    hasResults: document.querySelectorAll('a[href*="http"]').length > 5
                }};
            '''
            results_result = await tab.execute_script(results_check_script)
            if results_result and 'result' in results_result and 'result' in results_result['result']:
                results_data = results_result['result']['result'].get('value', {})
                search_data['resultsPage'] = results_data
        
        if search_data.get('success'):
            result = OperationResult(
                success=True,
                message=f"Successfully performed search for '{search_query}' using {search_data.get('method', 'unknown')} method",
                data={
                    "browser_id": browser_id,
                    "tab_id": actual_tab_id,
                    "search_query": search_query,
                    "website_type": website_type,
                    "search_details": search_data
                }
            )
        else:
            result = OperationResult(
                success=False,
                message=f"Failed to perform search for '{search_query}'",
                error=search_data.get('details', {}).get('error', 'Unknown error'),
                data={
                    "browser_id": browser_id,
                    "tab_id": actual_tab_id,
                    "search_query": search_query,
                    "search_details": search_data
                }
            )
        
        logger.info(f"Intelligent search completed: {search_data.get('success', False)}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Intelligent search failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to perform intelligent search"
        )
        return [TextContent(type="text", text=result.json())]


# Search Automation Tool Handlers Dictionary
SEARCH_AUTOMATION_TOOL_HANDLERS = {
    "intelligent_search": handle_intelligent_search,
}