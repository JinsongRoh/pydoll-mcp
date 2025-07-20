# 🔧 PyDoll MCP Server v1.5.2 Release Notes

**Release Date**: July 20, 2025

## 🐛 Dependency Fix Release

This patch release resolves the aiofiles version conflict that prevented Smithery.ai deployments.

## 🔧 Bug Fixes

### Fixed aiofiles Version Conflict
- **Issue**: Smithery.ai deployment failed with "The user requested aiofiles>=24.1.0 but pydoll-python 2.3.1 depends on aiofiles<24.0.0"
- **Solution**: Updated aiofiles requirement to `>=23.2.1,<24.0.0` to match PyDoll 2.3.1 dependencies

## 📦 Changes

### requirements.txt
- Changed: `aiofiles>=24.1.0` → `aiofiles>=23.2.1,<24.0.0`

### pyproject.toml
- Changed: `aiofiles>=23.0.0` → `aiofiles>=23.2.1,<24.0.0`
- Updated version to 1.5.2

## ✅ Compatibility

- **PyDoll**: 2.3.1 (required)
- **Python**: 3.8+
- **MCP**: 1.2.0+
- **aiofiles**: 23.2.1 - 23.x (matching PyDoll requirements)

## 📝 Notes

This release ensures smooth deployment on Smithery.ai and other platforms that strictly enforce dependency resolution.

---

For more information, visit:
- GitHub: https://github.com/JinsongRoh/pydoll-mcp
- PyPI: https://pypi.org/project/pydoll-mcp/1.5.2/
- Smithery.ai: https://smithery.ai/server/@JinsongRoh/pydoll-mcp