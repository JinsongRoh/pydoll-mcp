# PyPI Token Authentication Issue

## ⚠️ Current Issue

The provided PyPI token is returning a 403 Forbidden error:
- Error: "Invalid or non-existent authentication information"
- This typically indicates the token is invalid, expired, or revoked

## 🔧 Resolution Steps

### 1. Generate a New PyPI Token

1. **Login to PyPI**
   - Go to: https://pypi.org/manage/account/token/

2. **Create New Token**
   - Click "Add API token"
   - Token name: `pydoll-mcp-upload`
   - Scope: 
     - For first upload: "Entire account (all projects)"
     - After first upload: Can restrict to "Project: pydoll-mcp"

3. **Copy the Token**
   - The token will start with `pypi-`
   - Copy it immediately (shown only once)

### 2. Test the New Token

```bash
# Set environment variables
export TWINE_USERNAME=__token__
export TWINE_PASSWORD="your-new-pypi-token"

# Upload to PyPI
twine upload dist/*
```

### 3. Alternative: Use .pypirc File

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = your-new-pypi-token
```

Then upload:
```bash
twine upload dist/*
```

## 📦 Package Files Ready

The following files are built and ready for upload:
- `dist/pydoll_mcp-1.5.14-py3-none-any.whl` (89.8 KB)
- `dist/pydoll_mcp-1.5.14.tar.gz` (229.3 KB)

Both files passed `twine check` validation.

## 🚀 After Successful Upload

1. **Verify on PyPI**
   - Check: https://pypi.org/project/pydoll-mcp/1.5.14/

2. **Test Installation**
   ```bash
   pip install --upgrade pydoll-mcp==1.5.14
   ```

3. **Create GitHub Release**
   ```bash
   git tag v1.5.14
   git push origin v1.5.14
   ```

## 🔐 Security Notes

- Never commit tokens to the repository
- Rotate tokens regularly
- Use project-specific tokens when possible
- Store tokens in secure password managers

---

**Status**: Awaiting new PyPI token for upload
**Date**: 2025-07-20