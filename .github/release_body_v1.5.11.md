# PyDoll MCP Server v1.5.11

## 🔧 Critical Tab ID and PyDoll API Fixes

### Fixed Tab ID Parameter Handling
- **Issue**: `find_element` failed with "Tab None not found" errors even when tab_id was provided
- **Root Cause**: Tab ID parameter wasn't being properly passed to element finding methods
- **Solution**: 
  - Added proper tab validation with clear error messages
  - Ensured tab_id is correctly handled throughout the element tools

### Enhanced PyDoll API Compatibility
- **Issue**: PyDoll doesn't have `find_by_css_selector`, `find_by_xpath`, or `evaluate` methods
- **Solution**: 
  - Rewrote all element finding to use `execute_script` with JavaScript
  - CSS selector queries now use `document.querySelectorAll()`
  - XPath queries use `document.evaluate()`
  - Natural attribute searches implemented with custom JavaScript logic

### Specific Changes:

1. **Element Tools (`element_tools.py`)**:
   - Added tab validation to ensure tab exists before operations
   - Replaced non-existent PyDoll methods with execute_script implementations
   - Fixed selector.dict() error by using selector_args directly
   - Created MockElement class to standardize element data structure

2. **Script Tools (`script_tools.py`)**:
   - Replaced `tab.evaluate()` with `tab.execute_script()`
   - Fixed result parsing for PyDoll's nested response structure
   - Properly extract value and type from execution results

### Impact:
- Element finding now works correctly with all selector types
- Tab ID is properly validated and used in all operations
- JavaScript execution returns proper results
- No more "Tab None not found" errors when tab_id is provided

## Installation

```bash
pip install --upgrade pydoll-mcp==1.5.11
```

## Testing

After updating, test with:
```bash
# Start browser
browser_id = start_browser()

# Navigate and find elements
navigate_to(browser_id, "https://www.google.com")
tab_id = list_tabs(browser_id)[0]["id"]

# This should now work correctly
find_element(browser_id, tab_id, css_selector="input[name='q']")
```

## Links
- [PyPI Package](https://pypi.org/project/pydoll-mcp/1.5.11/)
- [Documentation](https://github.com/JinsongRoh/pydoll-mcp/wiki)
- [Issues](https://github.com/JinsongRoh/pydoll-mcp/issues)