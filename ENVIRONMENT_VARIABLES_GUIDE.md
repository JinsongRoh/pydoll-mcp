# 🔐 Environment Variables Security Guide

This guide explains how to securely use environment variables for sensitive information in PyDoll MCP Server.

## 🚨 Security Principles

1. **Never commit secrets** - Use environment variables or secure vaults
2. **Use placeholders in code** - Replace actual values with descriptive placeholders
3. **Document required variables** - Clearly list what needs to be configured
4. **Validate at runtime** - Check for required variables before using them

## 📋 Required Environment Variables

### For PyPI Deployment

| Variable | Description | Example |
|----------|-------------|---------|
| `TWINE_USERNAME` | PyPI username (always `__token__` for tokens) | `__token__` |
| `TWINE_PASSWORD` | PyPI API token | `pypi-...` (starts with `pypi-`) |

### For GitHub Actions

| Secret Name | Description | Where to Set |
|-------------|-------------|--------------|
| `PYPI_API_TOKEN` | PyPI API token | Repository Secrets |
| `SMITHERY_API_KEY` | Smithery.ai API key | Repository Secrets |
| `SMITHERY_PROFILE` | Smithery.ai profile | Repository Secrets |

## 🔧 Configuration Methods

### 1. Local Development (.env file)

Create a `.env` file in project root (already in .gitignore):

```bash
# .env
TWINE_USERNAME=__token__
TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
SMITHERY_API_KEY=your-smithery-key
SMITHERY_PROFILE=your-profile
```

Load in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()

twine_password = os.getenv('TWINE_PASSWORD')
if not twine_password:
    raise ValueError("TWINE_PASSWORD not set")
```

### 2. Shell Environment

```bash
# Linux/Mac
export TWINE_USERNAME=__token__
export TWINE_PASSWORD="pypi-YOUR_TOKEN_HERE"

# Windows (Command Prompt)
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE

# Windows (PowerShell)
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-YOUR_TOKEN_HERE"
```

### 3. GitHub Actions Secrets

Set in: Repository Settings → Secrets and variables → Actions

```yaml
# In workflow file
- name: Upload to PyPI
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: twine upload dist/*
```

### 4. CI/CD Platforms

#### GitHub Actions
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

#### GitLab CI
```yaml
variables:
  API_KEY: $CI_API_KEY  # Set in GitLab project settings
```

#### Jenkins
```groovy
withCredentials([string(credentialsId: 'api-key', variable: 'API_KEY')]) {
    sh 'echo $API_KEY'
}
```

## 🛡️ Security Best Practices

### 1. Validation

Always validate environment variables at startup:

```python
# pydoll_mcp/config.py
import os
from typing import Dict, Optional

def get_required_env(key: str) -> str:
    """Get required environment variable or raise error."""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Required environment variable {key} not set")
    return value

def get_optional_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get optional environment variable with default."""
    return os.getenv(key, default)

# Usage
PYPI_TOKEN = get_required_env('PYPI_TOKEN')
DEBUG_MODE = get_optional_env('DEBUG', 'false').lower() == 'true'
```

### 2. Logging

Never log sensitive values:

```python
# ❌ BAD - Don't do this
logger.info(f"Using token: {api_token}")

# ✅ GOOD - Log only non-sensitive parts
logger.info(f"Using token: {api_token[:8]}...")
logger.info("API token configured")
```

### 3. Error Messages

Provide helpful error messages without exposing secrets:

```python
# ❌ BAD
raise Exception(f"Failed to authenticate with token {token}")

# ✅ GOOD
raise Exception("Failed to authenticate. Check PYPI_TOKEN environment variable")
```

## 📝 Documentation Standards

### In Code Comments

```python
# Configuration requires PYPI_TOKEN environment variable
# Set via: export PYPI_TOKEN=your-token-here
pypi_token = os.getenv('PYPI_TOKEN')
```

### In README/Docs

```markdown
## Configuration

Set the following environment variables:

- `PYPI_TOKEN` - Your PyPI API token (get from https://pypi.org/manage/account/token/)
- `SMITHERY_KEY` - Smithery.ai API key (optional)

Example:
\`\`\`bash
export PYPI_TOKEN=pypi-YOUR_TOKEN_HERE
\`\`\`
```

## 🔍 Security Scanning

### Pre-commit Hooks

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### Manual Scanning

```bash
# Search for potential secrets
grep -r "password\|secret\|token\|key\|api" . \
  --include="*.py" \
  --include="*.yml" \
  --include="*.yaml" \
  --exclude-dir=".venv" \
  --exclude-dir=".git"

# Use git-secrets
git secrets --scan
```

## 🚀 Deployment Checklist

Before deploying:

- [ ] All secrets removed from code
- [ ] Environment variables documented
- [ ] `.env` file in `.gitignore`
- [ ] CI/CD secrets configured
- [ ] Security scan passed
- [ ] Error handling doesn't expose secrets
- [ ] Logs don't contain sensitive data

## 🆘 If Secrets Are Exposed

1. **Immediately revoke** the exposed token/key
2. **Generate new** credentials
3. **Update** all systems using the credentials
4. **Audit** logs for unauthorized access
5. **Document** the incident

## 📚 Resources

- [12 Factor App - Config](https://12factor.net/config)
- [OWASP - Secrets Management](https://owasp.org/www-project-secrets-management/)
- [GitHub - Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

---

**Remember**: When in doubt, use environment variables. Never commit secrets!