# PyDoll MCP Server v1.5.10

## 🔧 PyDoll API Compatibility Fixes

### Fixed PyDoll API Integration
- **Issue**: Previous implementation used incorrect/non-existent PyDoll methods
- **Root Cause**: Assumed PyDoll had methods like `get_url()`, `get_title()`, `get_content()` which don't exist
- **Solution**: 
  - All data retrieval now uses PyDoll's `execute_script()` method with JavaScript
  - Properly parse the nested result structure from execute_script responses
  - Store initial tab reference in browser object for compatibility

### Specific Changes:

1. **Navigation Tools**:
   - `get_current_url`: Now uses `execute_script("return window.location.href")`
   - `get_page_title`: Now uses `execute_script("return document.title")`
   - `get_page_source`: Now uses `execute_script("return document.documentElement.outerHTML")`
   - Fixed result parsing to extract values from PyDoll's nested response structure

2. **Browser Tools**:
   - `list_tabs`: Updated to retrieve URL and title via JavaScript execution
   - Improved error handling when tab information cannot be retrieved

3. **Browser Manager**:
   - Added `browser.tab` assignment to store initial tab reference
   - Better error messages when PyDoll operations fail
   - Ensured initial tab is always registered and accessible

### Impact:
- Users can now successfully navigate and retrieve page information
- Tab listing shows actual URLs and titles instead of defaults
- All PyDoll operations now use the correct API methods
- Improved stability and reliability of browser automation

## Installation

```bash
pip install --upgrade pydoll-mcp==1.5.10
```

## Links
- [PyPI Package](https://pypi.org/project/pydoll-mcp/1.5.10/)
- [Documentation](https://github.com/JinsongRoh/pydoll-mcp/wiki)
- [Issues](https://github.com/JinsongRoh/pydoll-mcp/issues)