# PyDoll MCP Server v1.5.6 Release Notes

**Release Date:** 2025-07-20  
**Version:** 1.5.6  
**Previous Version:** 1.5.5

## 🔧 Critical Bug Fixes

### Chrome Security Warning Resolution
- **Fixed:** Removed `--disable-gpu-sandbox` flag causing Chrome security warnings
- **Issue:** Chrome displayed "지원되지 않는 명령줄 플래그(--disable-gpu-sandbox)를 사용 중이므로 안정성과 보안에 문제가 발생합니다" (unsupported command line flag warning)
- **Solution:** Enhanced browser options configuration to maintain stability without compromising security
- **File:** `pydoll_mcp/browser_manager.py:362-367`

### Import Error Resolution
- **Fixed:** `ImportError: cannot import name 'browser_manager' from 'pydoll_mcp.browser_manager'`
- **Issue:** Missing global browser_manager instance export
- **Solution:** Added global browser_manager instance export at module level
- **File:** `pydoll_mcp/browser_manager.py:658-659`

### Serialization Error Resolution
- **Fixed:** `Unable to serialize unknown type: <class 'pydoll_mcp.browser_manager.BrowserInstance'>`
- **Issue:** BrowserInstance objects couldn't be serialized for MCP protocol
- **Solution:** Added `to_dict()` method for proper JSON serialization
- **Enhancements:** 
  - Fixed datetime handling in BrowserInstance
  - Updated browser tool handlers to use `to_dict()` method
- **Files:** 
  - `pydoll_mcp/browser_manager.py:103-116`
  - `pydoll_mcp/tools/browser_tools.py:371`

## 🛡️ Security Improvements

- Removed potentially insecure browser flags while maintaining functionality
- Enhanced browser isolation with proper user data directory management
- Maintained stealth capabilities without compromising Chrome security standards

## 📝 Technical Changes

### Browser Options Optimization
- Streamlined Chrome stability arguments for better compatibility
- Enhanced error handling in browser options configuration
- Improved cache key generation for browser configurations

### Serialization Enhancement
- Added comprehensive `to_dict()` method for BrowserInstance
- Fixed datetime object handling for JSON serialization
- Enhanced compatibility with MCP protocol requirements

### Module Structure
- Added global browser_manager instance for easier access
- Improved import patterns for browser management components
- Enhanced error handling in browser tool handlers

## 🔄 Backward Compatibility

This release maintains full backward compatibility with previous versions while fixing critical runtime issues.

## 🧪 Testing

All fixes have been thoroughly tested to ensure:
- Chrome browsers start without security warnings
- Browser manager imports work correctly
- Browser status queries return proper serialized data
- No regression in existing functionality

## 🚀 Upgrade Instructions

From v1.5.5:
```bash
pip install --upgrade pydoll-mcp==1.5.6
```

From earlier versions:
```bash
pip install --upgrade pydoll-mcp==1.5.6
# Restart your MCP client (Claude Desktop, etc.)
```

## 🔗 Related Issues

- Chrome security flag warnings causing user concern
- Browser startup failures due to import errors
- MCP protocol serialization compliance issues

## 📋 Commit Summary

- fix: Remove --disable-gpu-sandbox flag to eliminate Chrome security warnings
- fix: Add global browser_manager instance export for proper imports  
- fix: Add BrowserInstance.to_dict() method for MCP protocol serialization
- fix: Update datetime handling and tool handlers for JSON compatibility
- chore: Update version to 1.5.6 across all configuration files

---

**Full Changelog:** [v1.5.5...v1.5.6](https://github.com/JinsongRoh/pydoll-mcp/compare/v1.5.5...v1.5.6)