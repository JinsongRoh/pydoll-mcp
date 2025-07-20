# 🚨 PyPI Token Security Incident Response

## Incident Summary

**Date**: 2025-07-20
**Severity**: CRITICAL
**Status**: Token Revoked by PyPI

### What Happened

1. PyPI API token was discovered in a public URL
2. Token was found in the uploaded package: `pydoll_mcp-1.5.13.tar.gz`
3. Token was automatically revoked by PyPI security team
4. Source: `.claude/settings.local.json` file contained hardcoded tokens

## Immediate Actions Taken

### 1. Security Fixes Applied

- ✅ Added `.claude/` to `.gitignore`
- ✅ Added `prune .claude` to `MANIFEST.in`
- ✅ Token has been automatically revoked by PyPI

### 2. Package Security Check

```bash
# Check current package for sensitive files
tar -tzf dist/pydoll_mcp-1.5.14.tar.gz | grep -E "(\.claude|secret|token|key|password)"
```

## Prevention Measures

### 1. Never Hardcode Tokens

- Use environment variables
- Use GitHub Secrets for CI/CD
- Use `.pypirc` file with proper permissions (chmod 600)

### 2. Pre-Upload Checklist

Before uploading to PyPI:
1. Check package contents: `tar -tzf dist/*.tar.gz | less`
2. Search for secrets: `grep -r "pypi-" . --exclude-dir=.git`
3. Verify `.gitignore` includes all sensitive paths
4. Verify `MANIFEST.in` excludes sensitive files

### 3. Secure Token Storage

#### Option A: Environment Variables
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD="your-token-here"
twine upload dist/*
```

#### Option B: .pypirc File
```ini
[pypi]
username = __token__
password = your-token-here
```

Then: `chmod 600 ~/.pypirc`

#### Option C: GitHub Secrets (CI/CD)
Add token to repository secrets as `PYPI_API_TOKEN`

## Recovery Steps

### 1. Generate New PyPI Token

1. Login to https://pypi.org
2. Go to Account Settings → API tokens
3. Create new token with appropriate scope
4. Store securely (password manager recommended)

### 2. Clean Build

```bash
# Remove old builds
rm -rf dist/ build/ *.egg-info

# Rebuild with security fixes
python -m build

# Verify no secrets in package
tar -tzf dist/*.tar.gz | grep -v "\.pyc" | grep -E "(\.claude|\.env|\.pypirc|secret|token|password)"
```

### 3. Upload with New Token

```bash
# Using environment variable (recommended)
TWINE_USERNAME=__token__ TWINE_PASSWORD="new-token" twine upload dist/*
```

## Lessons Learned

1. **Never commit tokens** - Even in local settings files
2. **Always check package contents** - Before uploading
3. **Use proper .gitignore** - Include all sensitive directories
4. **Use MANIFEST.in properly** - Explicitly exclude sensitive files
5. **Regular security audits** - Check for exposed secrets regularly

## Security Tools

### 1. Pre-commit Hooks
Add to `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
    - id: detect-secrets
```

### 2. GitHub Secret Scanning
Enable secret scanning in repository settings

### 3. Regular Audits
```bash
# Search for potential secrets
grep -r "pypi-\|password\|secret\|token\|key" . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude="*.md"
```

## Contact

If you discover any security issues:
- Email: enjoydays@gmail.com
- GitHub Security Advisory: https://github.com/JinsongRoh/pydoll-mcp/security

---

**Remember**: Security is everyone's responsibility. When in doubt, ask for help!