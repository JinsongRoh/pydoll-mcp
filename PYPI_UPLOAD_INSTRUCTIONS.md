# PyPI Upload Instructions for pydoll-mcp v1.5.0

## Prerequisites

1. PyPI account (https://pypi.org/account/register/)
2. API token from PyPI (https://pypi.org/manage/account/token/)
3. Python with `twine` installed

## Installation of Upload Tools

```bash
# Using pipx (recommended)
pipx install twine

# Or in a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install twine
```

## Configure PyPI Credentials

### Option 1: Using .pypirc file (Recommended)

Create `~/.pypirc` file:

```ini
[pypi]
username = __token__
password = pypi-YOUR_API_TOKEN_HERE  # Replace with your actual PyPI API token
```

### Option 2: Environment Variables

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_API_TOKEN_HERE  # Replace with your actual PyPI API token
```

## Upload to PyPI

### 1. Verify Package Contents

```bash
# Check the built packages
ls -la dist/
# Expected output:
# pydoll_mcp-1.5.0-py3-none-any.whl
# pydoll_mcp-1.5.0.tar.gz

# Check package contents
tar -tzf dist/pydoll_mcp-1.5.0.tar.gz | head -20
```

### 2. Test Upload to TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps pydoll-mcp
```

### 3. Upload to Production PyPI

```bash
# Upload to PyPI
twine upload dist/*

# You'll see output like:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading pydoll_mcp-1.5.0-py3-none-any.whl
# Uploading pydoll_mcp-1.5.0.tar.gz
# View at: https://pypi.org/project/pydoll-mcp/1.5.0/
```

## Post-Upload Verification

1. Check PyPI page: https://pypi.org/project/pydoll-mcp/
2. Test installation:
   ```bash
   pip install pydoll-mcp==1.5.0
   ```
3. Verify package info:
   ```bash
   pip show pydoll-mcp
   ```

## Common Issues

### Authentication Failed
- Ensure you're using `__token__` as username
- Check your API token is correct and has upload permissions
- Make sure token starts with `pypi-`

### Package Already Exists
- Version 1.5.0 may already be uploaded
- Increment version in pyproject.toml and rebuild

### Invalid Distribution
- Ensure packages were built with latest tools
- Check for errors during build process

## Alternative: Using publish.py Script

The project includes a `publish.py` script that can automate the upload:

```bash
python publish.py
```

This script will:
1. Clean previous builds
2. Build new distributions
3. Upload to PyPI

## GitHub Release

After PyPI upload, create a GitHub release:

```bash
git tag v1.5.0
git push origin v1.5.0
```

Then create release on GitHub with the dist files attached.