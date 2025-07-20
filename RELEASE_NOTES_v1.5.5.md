# 🐛 PyDoll MCP Server v1.5.5 Release Notes

**Release Date**: July 20, 2025

## 🎯 Critical Browser Options Fix

This release addresses the critical "unhashable type: 'list'" error that prevented browser startup and improves browser status reporting accuracy.

## 🐛 Critical Bug Fixes

### Browser Options Caching Fix
- **Fixed**: "unhashable type: 'list'" error in browser options cache handling
- **Added**: Safe cache key generation that converts lists to tuples for hashability
- **Resolved**: Browser startup failures caused by unhashable objects in kwargs
- **Improved**: Browser options caching stability and performance

### Browser Status Reporting
- **Fixed**: Inaccurate browser count reporting in `list_browsers`
- **Enhanced**: Real browser instance detection and status reporting
- **Added**: Proper browser status details including uptime, tab count, and statistics
- **Improved**: Browser manager integration with tool handlers

### Browser Manager Enhancements
- **Fixed**: Browser instance state consistency
- **Added**: Robust browser status checking with real instance data
- **Improved**: Error handling and logging for browser operations
- **Enhanced**: Browser lifecycle management

## ✨ Improvements

### Better Error Handling
- Enhanced error messages for debugging browser initialization issues
- Improved exception handling in browser options processing
- Better fallback mechanisms for browser status detection

### Tool Integration
- Updated browser tool handlers to use actual browser manager instances
- Improved data consistency between tools and browser manager
- Enhanced browser status API with detailed information

## 🔧 Technical Details

### Cache Key Generation Fix
```python
def make_hashable(obj):
    if isinstance(obj, list):
        return tuple(obj)
    elif isinstance(obj, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
    return obj
```

### Browser Status Integration
- Real-time browser instance tracking
- Accurate browser count and status reporting
- Proper uptime calculation and tab management

## ✅ Compatibility

- **PyDoll**: 2.3.1 (required)
- **Python**: 3.8+
- **MCP**: 1.2.0+
- **OS**: Windows, macOS, Linux

## 💡 Usage Notes

This release fixes critical browser startup issues:
1. Browser creation should now work reliably without "unhashable type" errors
2. Browser status commands will show accurate information
3. Improved error messages help with debugging any remaining issues

## 📝 Migration Notes

No migration required - this is a bug fix release that maintains full backward compatibility.

## 🚀 Performance

- Faster browser options caching due to improved hash key generation
- More efficient browser status queries
- Reduced memory usage in browser manager operations

---

For more information, visit:
- GitHub: https://github.com/JinsongRoh/pydoll-mcp
- PyPI: https://pypi.org/project/pydoll-mcp/1.5.5/
- Smithery.ai: https://smithery.ai/server/@JinsongRoh/pydoll-mcp