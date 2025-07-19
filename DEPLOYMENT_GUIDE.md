# 🚀 PyDoll MCP Server Deployment Guide

## GitHub Actions Automated Release Pipeline

The PyDoll MCP Server is configured with a comprehensive automated release pipeline that handles:

### 🔄 Release Workflow Triggers

The release workflow is triggered by:
- **Git Tags**: Creating a tag starting with `v*` (e.g., `v1.4.0`)
- **Manual Dispatch**: Using GitHub Actions UI with version input

### 📋 Release Pipeline Steps

#### 1. **Package Building & Testing**
- Multi-platform testing (Ubuntu, Windows, macOS)
- Python version compatibility (3.8 - 3.12)
- Package verification and integrity checks
- Installation testing

#### 2. **GitHub Release Creation**
- Automatic release notes generation
- Binary distribution uploads (.whl, .tar.gz)
- Comprehensive metadata and documentation links

#### 3. **PyPI Publication**
- Secure token-based authentication
- Automatic package upload to PyPI
- Multi-platform installation verification

#### 4. **Smithery.ai Registry Update**
- Automatic MCP registry update
- Comprehensive metadata submission
- Tool capabilities and features documentation

#### 5. **Post-Release Validation**
- Cross-platform installation testing
- Functionality verification
- Success notifications

## 🔧 Manual Release Process

### Creating a New Release

1. **Update Version Numbers**
   ```bash
   # Update version in pyproject.toml and pydoll_mcp/__init__.py
   vim pyproject.toml
   vim pydoll_mcp/__init__.py
   ```

2. **Update Documentation**
   ```bash
   # Update CHANGELOG.md and README.md
   vim CHANGELOG.md
   vim README.md
   ```

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "Release vX.X.X - Description"
   git push origin main
   ```

4. **Create Release Tag**
   ```bash
   git tag vX.X.X
   git push origin vX.X.X
   ```

5. **Monitor Release Pipeline**
   - Visit: https://github.com/JinsongRoh/pydoll-mcp/actions
   - Watch the automated pipeline execution

### 🔑 Required Secrets

Ensure these GitHub Secrets are configured:

- `PYPI_API_TOKEN`: PyPI API token for package publishing
- `GITHUB_TOKEN`: Automatically provided by GitHub

### 🌐 Smithery.ai Integration

The release pipeline automatically updates the Smithery.ai MCP registry with:

```json
{
  "name": "pydoll-mcp",
  "description": "Revolutionary browser automation MCP server...",
  "version": "X.X.X",
  "installation": {
    "type": "pip",
    "package": "pydoll-mcp"
  },
  "configuration": {
    "command": "python",
    "args": ["-m", "pydoll_mcp.server"],
    "env": {
      "PYDOLL_LOG_LEVEL": "INFO"
    }
  },
  "capabilities": {
    "browser_automation": true,
    "captcha_bypass": true,
    "stealth_mode": true,
    // ... more capabilities
  }
}
```

## 📦 Distribution Channels

After a successful release, the package is available through:

1. **PyPI**: `pip install pydoll-mcp`
2. **GitHub Releases**: Binary downloads
3. **Smithery.ai**: MCP registry listing
4. **Docker Hub**: Container images (if configured)

## 🔍 Release Verification

### Verify PyPI Release
```bash
pip install pydoll-mcp==X.X.X
python -c "import pydoll_mcp; print(pydoll_mcp.__version__)"
```

### Verify GitHub Release
- Check: https://github.com/JinsongRoh/pydoll-mcp/releases
- Download and test binary distributions

### Verify Smithery.ai Update
- Visit: https://smithery.ai/package/pydoll-mcp
- Confirm latest version and metadata

## 🐛 Troubleshooting

### Common Issues

1. **PyPI Upload Failures**
   - Check PYPI_API_TOKEN validity
   - Verify package version uniqueness
   - Review package metadata compliance

2. **Smithery.ai Update Failures**
   - Verify API endpoint accessibility
   - Check JSON payload formatting
   - Review rate limiting restrictions

3. **GitHub Release Failures**
   - Ensure GITHUB_TOKEN permissions
   - Verify tag naming conventions
   - Check repository access rights

### Debug Commands

```bash
# Test package building locally
python -m build
python -m twine check dist/*

# Test server functionality
python -m pydoll_mcp.cli test-installation

# Verify tool registration
python -c "from pydoll_mcp.tools import ALL_TOOLS; print(f'Tools: {len(ALL_TOOLS)}')"
```

## 📈 Release Metrics

Track release success through:
- GitHub Actions workflow status
- PyPI download statistics
- Smithery.ai registry views
- Community feedback and issues

---

**Note**: This automated pipeline ensures consistent, reliable releases while maintaining high quality standards and broad distribution coverage.