# GitHub Secrets Setup Guide

이 가이드는 자동 배포를 위한 GitHub Secrets 설정 방법을 설명합니다.

## 🔐 Required Secrets

GitHub 저장소의 Settings > Secrets and variables > Actions에서 다음 secrets을 설정해야 합니다:

### 1. PYPI_API_TOKEN
- **Value**: `[YOUR_PYPI_TOKEN_HERE]`
- **Description**: PyPI API token for uploading packages
- **Permissions**: Package upload scope for all projects
- **Format**: Starts with `pypi-` followed by the token string

### 2. SMITHERY_API_KEY
- **Value**: `[YOUR_SMITHERY_API_KEY_HERE]`
- **Description**: Smithery.ai API key for updating the MCP server registry
- **Format**: UUID format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

### 3. SMITHERY_PROFILE
- **Value**: `[YOUR_SMITHERY_PROFILE_HERE]`
- **Description**: Smithery.ai profile identifier
- **Format**: Alphanumeric string with hyphens

## 📋 Setup Steps

1. **Navigate to Repository Settings**
   - Go to https://github.com/JinsongRoh/pydoll-mcp/settings/secrets/actions

2. **Add New Repository Secret**
   - Click "New repository secret"
   - Enter the secret name and value
   - Click "Add secret"

3. **Repeat for All Required Secrets**
   - Add PYPI_API_TOKEN
   - Add SMITHERY_API_KEY  
   - Add SMITHERY_PROFILE

## 🔒 Security Notes

- These secrets are automatically masked in GitHub Actions logs
- Never commit these values to the repository
- Secrets are only accessible to GitHub Actions workflows
- Review permissions regularly and rotate tokens when needed

## 🧪 Testing the Setup

After adding the secrets, you can test the automated deployment by:

1. **Creating a new tag**:
   ```bash
   git tag v1.5.15-test
   git push origin v1.5.15-test
   ```

2. **Manual workflow trigger**:
   - Go to Actions tab
   - Select "Release and Deploy PyDoll MCP Server v2"
   - Click "Run workflow"
   - Enter version number

## 🔍 Verification

The workflow will:
1. ✅ Create GitHub release with assets
2. ✅ Deploy to PyPI (https://pypi.org/project/pydoll-mcp/)
3. ✅ Update Smithery.ai registry (https://smithery.ai/server/@JinsongRoh/pydoll-mcp)
4. ✅ Generate deployment report

## ⚠️ Troubleshooting

### PyPI Upload Fails
- Check token permissions and expiration
- Verify package version doesn't already exist
- Review PyPI API status

### Smithery.ai Update Fails
- Verify API key and profile are correct
- Check Smithery.ai service status
- Review API endpoint availability

### GitHub Actions Errors
- Check workflow file syntax
- Verify all required secrets are set
- Review GitHub Actions service status

---

**Important**: Remove this file before committing to prevent accidental exposure of sensitive information.