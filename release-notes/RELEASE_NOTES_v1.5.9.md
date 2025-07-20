# PyDoll MCP Server v1.5.9 Release Notes

## Release Date: 2025-07-20

## 🐛 Critical Bug Fixes

### Fixed Browser Initial Tab Detection
- **Issue**: Browser started with an initial tab ("New Tab") but `list_tabs` returned empty array
- **Root Cause**: Initial tab created by browser wasn't being registered in the tab tracking system
- **Solution**: 
  - Added automatic detection of initial tabs when browser starts
  - Registers default tab in `browser_instance.tabs` dictionary
  - Sets first tab as active tab automatically
  - Properly tracks all tabs from browser startup

### Fixed Missing MCP Protocol Methods
- **Issue**: "Method not found" errors for `resources/list` and `prompts/list`
- **Root Cause**: Required MCP protocol methods were not implemented
- **Solution**: Added empty implementations for:
  - `handle_list_resources()` - Returns empty list (no resources currently)
  - `handle_list_prompts()` - Returns empty list (no prompts currently)

### Enhanced Browser Instance Management
- **Added**: `active_tab_id` property to BrowserInstance class
- **Added**: `_generate_tab_id()` method for unique tab ID generation
- **Improved**: Tab lifecycle tracking from browser creation to destruction

## 📊 Technical Details

### Code Changes:
1. **browser_manager.py**:
   - Added `active_tab_id` property to BrowserInstance
   - Added automatic initial tab detection after browser.start()
   - Added `_generate_tab_id()` method
   - Enhanced logging to show initial tab count

2. **server.py**:
   - Added `@server.list_resources()` handler
   - Added `@server.list_prompts()` handler
   - Both return empty lists as placeholders

### Impact:
- Users no longer need to manually create tabs after browser starts
- Eliminates duplicate tab creation
- Fixes "No tabs available" errors when navigating immediately after browser start
- Resolves MCP protocol compliance issues

## 🔄 Migration Guide

No migration needed. This is a backward-compatible bug fix release.

## 📝 Known Issues

None in this release.

## 🙏 Acknowledgments

Thanks to user feedback for identifying the tab detection issue with clear screenshot evidence.