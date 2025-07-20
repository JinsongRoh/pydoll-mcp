# 🐛 PyDoll MCP Server v1.5.4 Release Notes

**Release Date**: July 20, 2025

## 🎯 Chrome Browser Conflict Resolution

This release addresses critical issues with Chrome browser conflicts and improves tab management functionality.

## 🐛 Bug Fixes

### Chrome Process Conflict Resolution
- **Fixed**: Browser startup failures when Chrome is already running
- **Added**: Automatic detection of existing Chrome processes using psutil
- **Implemented**: Automatic temporary user data directory creation to avoid conflicts
- **Resolved**: "unhashable type: 'list'" error during browser creation

### Tab Management Improvements
- **Fixed**: Missing `get_tab` method in BrowserManager causing navigation failures
- **Added**: Proper tab retrieval and management methods
- **Fixed**: "'BrowserManager' object has no attribute 'get_tab'" error

## ✨ New Features

### Chrome Process Detection
- Automatically detects running Chrome processes before starting a new instance
- Creates isolated user data directories to prevent conflicts
- Provides clear warning messages about existing Chrome processes

### Enhanced Browser Options
- Added support for custom user data directories
- Improved browser option caching and handling
- Better error messages for debugging browser issues

## 🔧 Technical Details

### New Dependencies
```toml
psutil>=5.9.0  # Process and system utilities for Chrome detection
```

### Code Improvements
- Added `_check_existing_chrome_processes()` method for Chrome detection
- Enhanced browser creation logic with conflict prevention
- Improved error handling and logging

## ✅ Compatibility

- **PyDoll**: 2.3.1 (required)
- **Python**: 3.8+
- **MCP**: 1.2.0+
- **OS**: Windows, macOS, Linux

## 💡 Usage Tips

If you encounter browser startup issues:
1. Close any existing Chrome browsers
2. Or let PyDoll MCP automatically create an isolated instance
3. Check logs for detailed error messages

## 📝 Notes

This release significantly improves reliability when Chrome is already running on the system, making PyDoll MCP more robust for daily use.

---

For more information, visit:
- GitHub: https://github.com/JinsongRoh/pydoll-mcp
- PyPI: https://pypi.org/project/pydoll-mcp/1.5.4/
- Smithery.ai: https://smithery.ai/server/@JinsongRoh/pydoll-mcp