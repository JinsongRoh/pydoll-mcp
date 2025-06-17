# Contributing to PyDoll MCP Server

Thank you for your interest in contributing to PyDoll MCP Server! This document provides guidelines and information for contributors.

## 🌟 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **🐛 Bug Reports**: Help us identify and fix issues
- **✨ Feature Requests**: Suggest new capabilities
- **💻 Code Contributions**: Implement features or fix bugs
- **📚 Documentation**: Improve guides, examples, and API docs
- **🧪 Testing**: Add tests or improve test coverage
- **🎨 UI/UX**: Improve user experience and interfaces
- **🌍 Translations**: Help make the project accessible globally

### Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/JinsongRoh/pydoll-mcp.git
   cd pydoll-mcp
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\\Scripts\\activate   # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

3. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

4. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

## 🐛 Reporting Bugs

### Before Submitting a Bug Report

1. **Check existing issues** to avoid duplicates
2. **Update to the latest version** to see if the issue persists
3. **Test with minimal configuration** to isolate the problem

### How to Submit a Bug Report

Use our bug report template and include:

- **Environment Information**:
  - PyDoll MCP Server version
  - Python version
  - Operating system
  - Browser type and version
  - Claude Desktop version (if applicable)

- **Reproduction Steps**:
  ```
  1. Start PyDoll MCP Server
  2. Execute command '...'
  3. Observe error
  ```

- **Expected vs Actual Behavior**
- **Error Messages/Logs**
- **Screenshots** (if applicable)

### Bug Report Template

```markdown
**Environment:**
- PyDoll MCP Server: v1.0.0
- Python: 3.11.0
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- Browser: Chrome 120.0.6099.109

**Bug Description:**
A clear description of what the bug is.

**Reproduction Steps:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What you expected to happen.

**Actual Behavior:**
What actually happened.

**Error Logs:**
```
Paste error logs here
```

**Additional Context:**
Any other relevant information.
```

## ✨ Feature Requests

### Before Submitting a Feature Request

1. **Check existing feature requests** to avoid duplicates
2. **Consider if the feature fits the project scope**
3. **Think about implementation complexity**

### Feature Request Template

```markdown
**Feature Summary:**
A brief description of the proposed feature.

**Problem Statement:**
What problem does this feature solve?

**Proposed Solution:**
How would you like this feature to work?

**Alternative Solutions:**
Any alternative approaches you've considered.

**Use Cases:**
- Use case 1: ...
- Use case 2: ...

**Implementation Ideas:**
Technical suggestions (optional).

**Priority:**
Low / Medium / High
```

## 💻 Code Contributions

### Development Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   git checkout -b bugfix/issue-number
   ```

2. **Make Your Changes**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation
   - Ensure all tests pass

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new browser automation feature"
   ```

4. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Coding Standards

#### Python Code Style

We use the following tools for code quality:

- **Black**: Code formatting
- **Ruff**: Linting and code analysis
- **MyPy**: Type checking
- **isort**: Import sorting

```bash
# Format code
black .

# Check linting
ruff check .

# Type checking
mypy pydoll_mcp/

# Sort imports
isort .
```

#### Code Structure

```python
"""Module docstring describing the purpose."""

import asyncio
import logging
from typing import Dict, List, Optional

from pydoll_mcp.models import SomeModel

logger = logging.getLogger(__name__)


class ExampleClass:
    """Class docstring following Google style."""
    
    def __init__(self, param: str) -> None:
        """Initialize the class.
        
        Args:
            param: Description of parameter.
        """
        self.param = param
    
    async def async_method(self, data: Dict[str, str]) -> List[str]:
        """Async method with type hints.
        
        Args:
            data: Input data dictionary.
            
        Returns:
            List of processed strings.
            
        Raises:
            ValueError: If data is invalid.
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        result = []
        for key, value in data.items():
            result.append(f"{key}: {value}")
        
        return result
```

#### Documentation Style

Use Google-style docstrings:

```python
def function_example(param1: str, param2: int = 0) -> bool:
    """Summary line in one sentence.
    
    Longer description if needed. This can span multiple lines
    and should provide additional context about the function.
    
    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter. Defaults to 0.
        
    Returns:
        Description of return value.
        
    Raises:
        ValueError: Description of when this exception is raised.
        RuntimeError: Description of when this exception is raised.
        
    Example:
        Basic usage example:
        
        ```python
        result = function_example("test", 5)
        print(result)  # True
        ```
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    
    return len(param1) > param2
```

### Testing Guidelines

#### Test Structure

```python
"""Test module for ExampleClass."""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock

from pydoll_mcp.example import ExampleClass


class TestExampleClass:
    """Test suite for ExampleClass."""
    
    @pytest.fixture
    def example_instance(self):
        """Create an ExampleClass instance for testing."""
        return ExampleClass("test")
    
    def test_init(self, example_instance):
        """Test class initialization."""
        assert example_instance.param == "test"
    
    @pytest_asyncio.fixture
    async def async_method_test(self, example_instance):
        """Test async method."""
        data = {"key1": "value1", "key2": "value2"}
        result = await example_instance.async_method(data)
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert "key1: value1" in result
    
    def test_async_method_empty_data(self, example_instance):
        """Test async method with empty data."""
        with pytest.raises(ValueError, match="Data cannot be empty"):
            await example_instance.async_method({})
```

#### Test Categories

- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test component interactions
- **Browser Tests**: Test browser automation features
- **Performance Tests**: Test performance characteristics

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test category
pytest -m unit
pytest -m integration
pytest -m browser

# Run with coverage
pytest --cov=pydoll_mcp --cov-report=html

# Run performance tests
pytest -m performance --benchmark-only
```

### Pull Request Guidelines

#### Before Submitting

- [ ] All tests pass
- [ ] Code is properly formatted
- [ ] Documentation is updated
- [ ] Changelog is updated (if applicable)
- [ ] No merge conflicts

#### Pull Request Template

```markdown
## Description

Brief description of changes made.

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues

Fixes #123
Closes #456

## Changes Made

- Added feature X
- Fixed bug Y
- Updated documentation Z

## Testing

- [ ] Added unit tests
- [ ] Added integration tests
- [ ] Manual testing performed
- [ ] All existing tests pass

## Screenshots (if applicable)

Add screenshots here.

## Checklist

- [ ] My code follows the project's coding standards
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## 📚 Documentation Contributions

### Types of Documentation

- **API Documentation**: Function/class docstrings
- **User Guides**: Installation, configuration, usage
- **Examples**: Code examples and tutorials
- **Developer Docs**: Architecture, contributing guidelines

### Documentation Standards

- Use clear, concise language
- Provide practical examples
- Include error handling
- Keep documentation up-to-date with code changes

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation locally
mkdocs serve

# View at http://localhost:8000
```

## 🧪 Testing Contributions

### Adding Tests

1. **Identify untested code**:
   ```bash
   pytest --cov=pydoll_mcp --cov-report=html
   open htmlcov/index.html
   ```

2. **Write comprehensive tests**:
   - Test normal operation
   - Test error conditions
   - Test edge cases

3. **Add performance tests** for critical paths

### Test Environment

```bash
# Set up test environment
export PYDOLL_TEST_MODE=true
export PYDOLL_HEADLESS=true

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/browser/
```

## 🚀 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `pydoll_mcp/__init__.py`
- [ ] Update `CHANGELOG.md`
- [ ] Create release notes
- [ ] Tag release: `git tag v1.0.0`
- [ ] Push tags: `git push --tags`

## 🤝 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- **Be respectful** of different viewpoints and experiences
- **Be collaborative** and help others learn
- **Be patient** with newcomers
- **Be constructive** in feedback and criticism

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community chat
- **Pull Requests**: Code review and technical discussion

### Recognition

Contributors will be:

- Listed in the project README
- Mentioned in release notes
- Invited to the contributors team (for significant contributions)

## 🛠️ Development Tools

### Recommended Tools

- **IDE**: VS Code, PyCharm, or similar
- **Git GUI**: GitKraken, SourceTree, or command line
- **Terminal**: Windows Terminal, iTerm2, or similar
- **Browser**: Chrome DevTools for debugging

### VS Code Setup

Recommended extensions:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "charliermarsh.ruff",
    "ms-python.mypy-type-checker",
    "ms-python.pylint",
    "ms-toolsai.jupyter"
  ]
}
```

### Environment Variables

```bash
# Development environment
export PYDOLL_DEBUG=1
export PYDOLL_LOG_LEVEL=DEBUG
export PYDOLL_BROWSER_TYPE=chrome
export PYDOLL_HEADLESS=false
```

## 📋 Troubleshooting

### Common Development Issues

#### Import Errors
```bash
# Solution: Install in editable mode
pip install -e .
```

#### Test Failures
```bash
# Solution: Check environment
pytest tests/test_specific.py -v -s
```

#### Browser Issues
```bash
# Solution: Check browser installation
python -c "from pydoll.browser import Chrome; print('OK')"
```

### Getting Help

1. **Check existing documentation**
2. **Search GitHub issues**
3. **Ask in GitHub Discussions**
4. **Create a detailed issue**

## 🎉 Thank You!

Thank you for contributing to PyDoll MCP Server! Your contributions help make browser automation more accessible and powerful for everyone.

### Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for a list of all contributors.

### License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing! 🚀**

For more information, visit our [GitHub repository](https://github.com/JinsongRoh/pydoll-mcp).
