# 🔐 GitHub Secrets Setup for PyDoll MCP Server

This guide explains how to configure GitHub Actions secrets for automated releases and deployments.

## 🔑 PyPI Deployment (No Secrets Needed!)

**PyPI deployment now uses Trusted Publisher (OIDC) authentication.** No API tokens or passwords are required!

The repository is already configured with:
- **Publisher**: GitHub
- **Repository**: JinsongRoh/pydoll-mcp
- **Workflow**: release.yml
- **Environment**: pypi

## 📋 Optional GitHub Secrets

Configure the following secrets in your GitHub repository settings only if needed:

### Repository Secrets (Settings > Secrets and variables > Actions)

| Secret Name | Description | Required For |
|-------------|-------------|--------------|
| `SMITHERY_AI_KEY` | Smithery.ai API key | Smithery.ai updates (optional) |

## 🔧 GitHub Environment Setup (Required)

### Create "pypi" Environment
1. Go to your repository: https://github.com/JinsongRoh/pydoll-mcp
2. Click on **Settings** tab
3. In the left sidebar, find **Environments**
4. Click **New environment**
5. Name it exactly: `pypi` (lowercase)
6. Click **Configure environment**
7. No additional settings needed - just save

### Optional: Add Smithery.ai Secret
If you want automatic Smithery.ai updates:
1. Go to **Settings** > **Secrets and variables** > **Actions**
2. Click **New repository secret**
3. Name: `SMITHERY_AI_KEY`
4. Secret: Your Smithery.ai API key

## 🚀 Automated Deployment Process

When you create a new release tag (e.g., `v1.5.15`), the workflow will automatically:

1. **Create GitHub Release** with assets
2. **Deploy to PyPI** using Trusted Publisher (OIDC) - no secrets needed!
3. **Update Smithery.ai** registry
4. **Verify deployment** and generate reports

### Triggering a Release

#### Option 1: Create a Git Tag
```bash
git tag v1.5.15
git push origin v1.5.15
```

#### Option 2: Manual Workflow Dispatch
1. Go to **Actions** tab
2. Select **🚀 Release and Deploy PyDoll MCP Server**
3. Click **Run workflow**
4. Enter version number (e.g., `1.5.15`)
5. Click **Run workflow**

## 🔍 Verification

### Required Setup:
1. Go to **Settings** > **Environments**
2. Verify you have a `pypi` environment created

### Optional Secrets:
1. Go to **Settings** > **Secrets and variables** > **Actions**
2. If configured, you should see:
   - SMITHERY_AI_KEY (optional)

## 📊 Monitoring Deployments

Track deployment status:
- **GitHub Actions**: https://github.com/JinsongRoh/pydoll-mcp/actions
- **PyPI Package**: https://pypi.org/project/pydoll-mcp/
- **Smithery.ai**: https://smithery.ai/server/@JinsongRoh/pydoll-mcp

## 🆘 Troubleshooting

### PyPI Upload Fails
- Verify the `pypi` environment exists in GitHub repository settings
- Check that the environment name is exactly `pypi` (lowercase)
- Ensure the version doesn't already exist on PyPI
- The workflow file must be named `release.yml`

### Smithery.ai Update Fails
- Verify `SMITHERY_AI_KEY` is correct
- Check Smithery.ai service status
- The workflow continues even if Smithery update fails

### GitHub Release Fails
- Ensure the tag doesn't already exist
- Check repository permissions
- Verify GitHub Actions is enabled

## 🔒 Security Notes

- PyPI deployment now uses OIDC - no tokens to manage or rotate!
- Never commit secrets to the repository
- For Smithery.ai keys, rotate regularly if used
- Monitor for unauthorized access in PyPI and GitHub logs

---

**Last Updated**: 2025-07-20
**Workflow File**: `.github/workflows/release.yml`