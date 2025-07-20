# PyDoll MCP Server v1.5.15 Release Notes

## 🐛 Critical Bug Fixes

### Fixed Pydantic Model Method Call Error
- **Issue**: `AttributeError: 'OperationResult' object has no attribute 'to_dict'`
- **Cause**: Incorrect method call on Pydantic models
- **Solution**: Replaced all `result.to_dict()` calls with the correct `result.dict()` method
- **Files Fixed**:
  - `pydoll_mcp/tools/file_tools.py` (8 occurrences)
  - `pydoll_mcp/tools/network_tools.py` (10 occurrences)
  - `pydoll_mcp/tools/protection_tools.py` (12 occurrences)

### Fixed Tab ID Handling
- **Issue**: `Tab None not found in browser` errors
- **Cause**: Some handlers were passing `tab_id=None` to `get_tab()` instead of using proper fallback
- **Solution**: Updated screenshot handler to use `get_tab_with_fallback()` which properly handles None tab_id
- **Files Fixed**:
  - `pydoll_mcp/tools/screenshot_tools.py`

### Fixed PyDoll API Compatibility
- **Issue**: `Tab.take_screenshot() got an unexpected keyword argument 'full_page'`
- **Cause**: MCP Server was passing unsupported parameters to PyDoll's `take_screenshot` method
- **Solution**: Updated to only use supported parameters: `path`, `quality`, and `as_base64`
- **Files Fixed**:
  - `pydoll_mcp/tools/screenshot_tools.py`

## 🔧 Technical Details

### PyDoll API Alignment
- Removed unsupported screenshot parameters (`full_page`, `type`, `clip`)
- Now uses `as_base64=True` to get screenshot data for processing
- Maintains backward compatibility with MCP tool interface

### Error Handling Improvements
- Better fallback mechanisms for browser operations
- Improved error messages for debugging
- Consistent tab ID handling across all tools

## 📊 Impact

This release addresses critical runtime errors that were preventing proper operation of:
- Data extraction tools
- Screenshot capture functionality
- Network monitoring tools
- Protection/stealth mode tools

## 🚀 Upgrade Instructions

```bash
pip install --upgrade pydoll-mcp==1.5.15
```

## ✅ Testing Recommendations

After upgrading, test the following functionality:
1. Screenshot capture with various options
2. Data extraction from web pages
3. Network request monitoring
4. Browser tab management
5. Stealth mode operations

## 🙏 Acknowledgments

Thanks to the users who reported these issues through log analysis, helping us identify and fix these critical bugs quickly.