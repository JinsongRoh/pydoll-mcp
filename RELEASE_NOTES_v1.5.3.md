# 🔧 PyDoll MCP Server v1.5.3 Release Notes

**Release Date**: July 20, 2025

## 🎯 Quality Improvements & Maintenance Release

This release focuses on code quality improvements, documentation enhancements, and dependency refinements.

## ✨ Improvements

### Enhanced Documentation
- **Server Module**: Added comprehensive feature list to main server documentation
- **Dependency Clarity**: Updated requirements to clearly specify version constraints
- **Contact Information**: Updated author email address from `jinsongroh@gmail.com` to `enjoydays@gmail.com`

### Code Quality
- **Type Hints**: Improved type annotations across the codebase
- **Error Handling**: Enhanced error messages for better debugging
- **Module Documentation**: Added detailed docstrings to key modules

### Dependency Management
- **MCP**: Updated minimum version requirement to 1.2.0 for latest protocol features
- **Pydantic**: Updated minimum version to 2.10.4 for improved validation
- **Click**: Updated minimum version to 8.1.0 for enhanced CLI functionality
- **aiofiles**: Maintained compatibility with PyDoll 2.3.1 requirements

## 🔧 Technical Details

### Updated Dependencies
```toml
dependencies = [
    "pydoll-python>=2.3.1",
    "mcp>=1.2.0",          # Updated from >=1.0.0
    "pydantic>=2.10.4",    # Updated from >=2.0.0
    "typing-extensions>=4.0.0",
    "asyncio-throttle>=1.0.0",
    "aiofiles>=23.2.1,<24.0.0",
    "python-dotenv>=1.0.0",
    "rich>=13.0.0",
    "click>=8.1.0",        # Updated from >=8.0.0
]
```

### Contact Update
- Author Email: `enjoydays@gmail.com` (previously `jinsongroh@gmail.com`)

## ✅ Compatibility

- **PyDoll**: 2.3.1 (required)
- **Python**: 3.8+
- **MCP**: 1.2.0+
- **OS**: Windows, macOS, Linux

## 📝 Notes

This maintenance release ensures the project remains up-to-date with current best practices and provides clearer documentation for users and contributors.

---

For more information, visit:
- GitHub: https://github.com/JinsongRoh/pydoll-mcp
- PyPI: https://pypi.org/project/pydoll-mcp/1.5.3/
- Smithery.ai: https://smithery.ai/server/@JinsongRoh/pydoll-mcp