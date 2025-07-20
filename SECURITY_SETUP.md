# 🔐 Security Setup Guide for PyDoll MCP Server

This guide explains how to securely configure GitHub Actions for automated releases and deployments without exposing sensitive API keys and tokens in the repository.

## 🚨 Security Issues Identified

The current `release.yml` workflow contains hardcoded API keys that need to be moved to GitHub Secrets immediately:

- ❌ Smithery.ai API key exposed in line 333
- ❌ PyPI token should use environment protection

## 🛡️ Required GitHub Secrets

To enable secure automated releases, configure the following secrets in your GitHub repository:

### Repository Secrets (Settings > Secrets and variables > Actions)

| Secret Name | Description | Where to Get |
|-------------|-------------|--------------|
| `PYPI_API_TOKEN` | PyPI API token for package publishing | [PyPI Account Settings](https://pypi.org/manage/account/#api-tokens) |
| `SMITHERY_API_KEY` | Smithery.ai API key for MCP registry updates | [Smithery.ai Dashboard](https://smithery.ai/dashboard) |
| `SMITHERY_PROFILE` | Smithery.ai profile identifier | Smithery.ai account profile |

### Environment Secrets (for PyPI publishing)

Create a `pypi` environment with the following protection rules:
- ✅ Required reviewers: Repository maintainers
- ✅ Environment secrets: `PYPI_API_TOKEN`

## 🔧 Step-by-Step Setup

### 1. Generate PyPI API Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/#api-tokens)
2. Click "Add API token"
3. Set scope to "Entire account" or specific to "pydoll-mcp" project
4. Copy the token (starts with `pypi-`)

### 2. Get Smithery.ai Credentials

1. Log in to [Smithery.ai Dashboard](https://smithery.ai/dashboard)
2. Navigate to API settings
3. Generate a new API key for GitHub Actions
4. Note your profile identifier

### 3. Configure GitHub Repository Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret** for each:

#### PYPI_API_TOKEN
```
Name: PYPI_API_TOKEN
Secret: <your-pypi-token-here>
```

#### SMITHERY_API_KEY
```
Name: SMITHERY_API_KEY
Secret: your-smithery-api-key-here
```

#### SMITHERY_PROFILE
```
Name: SMITHERY_PROFILE
Secret: your-smithery-profile-id
```

### 4. Configure PyPI Environment

1. Go to **Settings** > **Environments**
2. Click **New environment**
3. Name: `pypi`
4. Configure protection rules:
   - ✅ **Required reviewers**: Add repository maintainers
   - ✅ **Deployment branches**: Only protected branches
5. Add environment secret:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token

## 🔒 Security Best Practices

### API Token Permissions

#### PyPI Token
- ✅ **Scope**: Project-specific (`pydoll-mcp` only)
- ✅ **Permissions**: Upload packages only
- ❌ **Avoid**: Account-wide tokens unless necessary

#### Smithery.ai Token
- ✅ **Scope**: MCP registry updates only
- ✅ **Permissions**: Minimal required access
- ✅ **Expiration**: Set reasonable expiration dates

### GitHub Actions Security

#### Workflow Permissions
```yaml
permissions:
  contents: read      # Read repository contents
  id-token: write     # OIDC token generation
  packages: write     # GitHub Packages (if used)
```

#### Environment Protection
- ✅ Use environments for production deployments
- ✅ Require manual approval for releases
- ✅ Restrict to protected branches only

### Token Rotation

#### Regular Rotation Schedule
- 🔄 **PyPI tokens**: Every 6 months
- 🔄 **Smithery.ai tokens**: Every 6 months
- 🔄 **After security incidents**: Immediately

#### Rotation Process
1. Generate new token
2. Update GitHub secret
3. Test workflow with new token
4. Revoke old token

## 🚫 What NOT to Do

### ❌ Never Commit These
```yaml
# DON'T DO THIS!
env:
  PYPI_TOKEN: <your-pypi-token-here>
  SMITHERY_KEY: sk-1234567890abcdef...
```

### ❌ Never Use in URLs
```bash
# DON'T DO THIS!
curl "https://api.service.com?api_key=secret123"
```

### ❌ Never Log Secrets
```bash
# DON'T DO THIS!
echo "Using token: ${{ secrets.API_TOKEN }}"
```

## ✅ Secure Usage Examples

### Correct Secret Usage
```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}
    
- name: Update Smithery.ai
  env:
    SMITHERY_API_KEY: ${{ secrets.SMITHERY_API_KEY }}
    SMITHERY_PROFILE: ${{ secrets.SMITHERY_PROFILE }}
  run: |
    curl -X POST "https://api.smithery.ai/update" \
      -H "Authorization: Bearer $SMITHERY_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"profile": "'$SMITHERY_PROFILE'", "action": "update"}'
```

## 🔍 Security Verification

### Check for Exposed Secrets
```bash
# Scan for potential secrets in repository
git log --all --full-history -- "*.yml" "*.yaml" | grep -i "token\|key\|secret\|password"

# Use GitHub's secret scanning
# Enabled automatically for public repositories
```

### Test Secret Access
```yaml
- name: Verify secrets are configured
  run: |
    if [ -z "${{ secrets.PYPI_API_TOKEN }}" ]; then
      echo "❌ PYPI_API_TOKEN not configured"
      exit 1
    fi
    
    if [ -z "${{ secrets.SMITHERY_API_KEY }}" ]; then
      echo "❌ SMITHERY_API_KEY not configured"
      exit 1
    fi
    
    echo "✅ All required secrets are configured"
```

## 🆘 Emergency Procedures

### If Secrets Are Exposed

1. **Immediate Actions** (within 1 hour):
   - Revoke exposed tokens immediately
   - Generate new tokens
   - Update GitHub secrets
   - Force-push to remove secrets from git history (if needed)

2. **Investigation** (within 24 hours):
   - Check access logs for unauthorized usage
   - Review recent deployments
   - Audit repository access

3. **Recovery** (within 48 hours):
   - Implement additional security measures
   - Update security documentation
   - Conduct security review

### Emergency Contacts
- **Repository Owner**: [Contact Information]
- **Security Team**: [Contact Information]
- **PyPI Security**: security@pypi.org
- **GitHub Security**: https://github.com/security

## 📚 Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [PyPI API Tokens Guide](https://pypi.org/help/#apitoken)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

---

**⚠️ Important**: After following this guide, immediately update the `release.yml` workflow to use secrets instead of hardcoded values.