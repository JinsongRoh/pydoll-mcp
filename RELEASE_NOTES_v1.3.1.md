# 🔧 PyDoll MCP Server v1.3.1 Release Notes

**Release Date**: July 20, 2025  
**Version**: 1.3.1  
**Status**: Bug Fix Release

---

## 🐛 Bug Fixes

This release addresses critical issues discovered during comprehensive testing of v1.3.0.

### 1. **Tool Loading Issue Fixed** 🔧

**Problem**: Only 28 out of 79 documented tools were actually loading in v1.3.0.

**Solution**: 
- Created `protection_tools.py` module with 12 stealth and bypass tools
- Created `network_tools.py` module with 10 network monitoring tools
- Created `file_tools.py` module with 8 file management tools
- Updated `tools/__init__.py` to properly import all tool modules

**Result**: All 79 tools now load correctly ✅

### 2. **Pydantic V2 Compatibility** ⚙️

**Problem**: Deprecation warnings for `schema_extra` configuration in Pydantic V2.

**Solution**:
- Changed `schema_extra` to `json_schema_extra` in `models/__init__.py`
- Achieved full Pydantic V2 compliance

**Result**: No more deprecation warnings ✅

### 3. **CLI Function Missing** 🛠️

**Problem**: `generate_config_json()` function was missing from cli.py, causing import errors.

**Solution**:
- Added `generate_config_json()` function to generate Claude Desktop configuration
- Function returns properly formatted JSON configuration

**Result**: Configuration generation works correctly ✅

## 📊 Verification

### Tool Count by Category

| Category | v1.3.0 | v1.3.1 | Status |
|----------|--------|--------|--------|
| Browser Management | 8 | 8 | ✅ |
| Navigation Control | 11 | 11 | ✅ |
| Element Interaction | 16 | 16 | ✅ |
| Screenshot & Media | 6 | 6 | ✅ |
| JavaScript Scripting | 8 | 8 | ✅ |
| **Protection Bypass** | 0 | 12 | ✅ Fixed |
| **Network Monitoring** | 0 | 10 | ✅ Fixed |
| **File Management** | 0 | 8 | ✅ Fixed |
| **Total** | **28** | **79** | ✅ |

## 🚀 Quick Upgrade

```bash
pip install --upgrade pydoll-mcp
```

## ✅ What's Fixed

- ✅ All 79 tools now properly load and function
- ✅ No more Pydantic deprecation warnings
- ✅ CLI configuration generation works correctly
- ✅ Full compatibility with documentation

## 📝 Technical Details

### New Files Added
- `/pydoll_mcp/tools/protection_tools.py` - Protection and stealth tools
- `/pydoll_mcp/tools/network_tools.py` - Network monitoring tools
- `/pydoll_mcp/tools/file_tools.py` - File management tools

### Files Modified
- `/pydoll_mcp/tools/__init__.py` - Added new module imports
- `/pydoll_mcp/models/__init__.py` - Pydantic V2 compatibility
- `/pydoll_mcp/cli.py` - Added missing function
- `/pydoll_mcp/__init__.py` - Version bump to 1.3.1
- `/pyproject.toml` - Version bump to 1.3.1

## 🙏 Thank You

Thanks to our users for reporting these issues promptly. Your feedback helps us maintain the quality and reliability of PyDoll MCP Server.

---

**Ready for reliable automation?**

📖 [Documentation](https://github.com/JinsongRoh/pydoll-mcp) | 🐛 [Report Issues](https://github.com/JinsongRoh/pydoll-mcp/issues) | 💬 [Discussions](https://github.com/JinsongRoh/pydoll-mcp/discussions)