# 🐛 PyDoll MCP Server v1.5.1 Release Notes

**Release Date**: July 20, 2025

## 🔧 Critical Bug Fix Release

This patch release addresses critical compatibility issues with PyDoll 2.3.1 that prevented browser instances from starting correctly.

## 🐛 Bug Fixes

### Fixed PyDoll ChromiumOptions Compatibility
- **Issue**: Browser creation failed with `'ChromiumOptions' object has no attribute 'add_experimental_option'` error
- **Root Cause**: PyDoll's ChromiumOptions class doesn't implement `add_experimental_option` method from Selenium
- **Solution**: Removed unsupported `start_timeout` parameter from browser initialization

### Fixed Duplicate Browser Arguments
- **Issue**: Browser startup failed with `ArgumentAlreadyExistsInOptions` errors
- **Root Cause**: PyDoll automatically adds `--no-first-run` and `--no-default-browser-check` arguments
- **Solution**: Removed duplicate arguments from our configuration and added proper exception handling

## 💻 Technical Details

### Changes Made
1. **browser_manager.py**:
   - Removed `start_timeout` parameter from Chrome/Edge browser instantiation
   - Added exception handling for duplicate browser arguments
   - Enhanced error handling in `_get_browser_options` method

2. **browser_tools.py**:
   - Removed `start_timeout` parameter from `handle_start_browser` function
   - Maintained backward compatibility with BrowserConfig model

3. **models/__init__.py**:
   - Kept `start_timeout` field for API compatibility but no longer used

## ✅ Testing

All browser functionality has been tested and verified:
- ✅ Chrome browser creation
- ✅ Edge browser creation  
- ✅ Headless mode operation
- ✅ Browser pool functionality
- ✅ Tab management

## 📦 Installation

### Upgrade from v1.5.0
```bash
pip install --upgrade pydoll-mcp==1.5.1
```

### Fresh Installation
```bash
pip install pydoll-mcp==1.5.1
```

## 🔄 Compatibility

- **PyDoll**: 2.3.1 (required)
- **Python**: 3.8+ 
- **MCP**: 1.2.0+
- **OS**: Windows, macOS, Linux

## 🙏 Acknowledgments

Thanks to users who reported the browser initialization issues, helping us identify and fix this critical bug quickly.

## 📝 Notes

This is a critical patch release. All users on v1.5.0 should upgrade immediately to restore browser automation functionality.

---

For more information, visit:
- GitHub: https://github.com/JinsongRoh/pydoll-mcp
- PyPI: https://pypi.org/project/pydoll-mcp/1.5.1/
- Issues: https://github.com/JinsongRoh/pydoll-mcp/issues