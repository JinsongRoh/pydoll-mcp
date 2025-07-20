# PyPI Trusted Publisher Setup Guide

## Overview

PyPI's Trusted Publishers feature uses OpenID Connect (OIDC) to provide a secure, password-free mechanism for publishing packages. This eliminates the need for API tokens or passwords in GitHub Actions.

## Current Configuration

### PyPI Settings
- **Project**: pydoll-mcp
- **Publisher Type**: GitHub
- **Repository**: JinsongRoh/pydoll-mcp
- **Workflow**: release.yml
- **Environment**: pypi

### GitHub Workflow Requirements

1. **Environment Name**: The workflow must specify `environment: pypi` in the deploy job
2. **Permissions**: The workflow must have `id-token: write` permission
3. **Action**: Use `pypa/gh-action-pypi-publish@release/v1` for publishing

## Setup Verification

### ✅ PyPI Side (Already Configured)
The trusted publisher is already configured on PyPI with:
- Repository: `JinsongRoh/pydoll-mcp`
- Workflow: `release.yml`
- Environment: `pypi`

### ✅ GitHub Workflow (Updated)
The workflow has been updated to:
1. Include `environment: pypi` in the deploy-pypi job
2. Add `permissions: id-token: write`
3. Use the official PyPA GitHub Action for publishing
4. Remove the deprecated username/password authentication

## Benefits

1. **Enhanced Security**: No API tokens stored in GitHub Secrets
2. **Automatic Authentication**: GitHub and PyPI handle authentication via OIDC
3. **Simplified Workflow**: No need to manage or rotate API tokens
4. **Audit Trail**: All deployments are tracked through GitHub environments

## Troubleshooting

If deployment fails:

1. **Verify Environment Name**: Ensure the workflow uses `environment: pypi` (exact match)
2. **Check Permissions**: Confirm `id-token: write` is set in the workflow
3. **Repository Match**: The GitHub repository must match exactly: `JinsongRoh/pydoll-mcp`
4. **Workflow File**: Must be named `release.yml` in `.github/workflows/`

## Testing

To test the deployment:
1. Create a new tag: `git tag v1.5.16`
2. Push the tag: `git push origin v1.5.16`
3. Monitor the GitHub Actions workflow
4. Check PyPI for the new release

## References

- [PyPI Trusted Publishers Documentation](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [PyPA Publishing Action](https://github.com/pypa/gh-action-pypi-publish)