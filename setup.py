#!/usr/bin/env python3
"""Setup script for PyDoll MCP Server.

This setup.py is maintained for compatibility with older build systems.
For modern installation, please use pyproject.toml with pip.
"""

import os
import sys
from pathlib import Path

from setuptools import find_packages, setup

# Ensure Python version compatibility
if sys.version_info < (3, 8):
    print("ERROR: PyDoll MCP Server requires Python 3.8 or higher")
    print(f"You are using Python {sys.version}")
    sys.exit(1)

# Read version from __init__.py
here = Path(__file__).parent
init_file = here / "pydoll_mcp" / "__init__.py"

version = "1.0.0"
if init_file.exists():
    with open(init_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().strip('"').strip("'")
                break

# Read README for long description
readme_file = here / "README.md"
long_description = "PyDoll MCP Server - Revolutionary browser automation with intelligent captcha bypass"
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_file = here / "requirements.txt"
requirements = [
    "pydoll-python>=2.2.0",
    "mcp>=1.0.0",
    "pydantic>=2.0.0",
    "typing-extensions>=4.0.0",
    "asyncio-throttle>=1.0.0",
    "aiofiles>=23.0.0",
    "python-dotenv>=1.0.0",
    "rich>=13.0.0",
    "click>=8.0.0",
]

if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

# Development requirements
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
    "coverage[toml]>=7.0.0",
]

# Documentation requirements
docs_requirements = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings[python]>=0.24.0",
]

# Test requirements
test_requirements = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "aioresponses>=0.7.0",
]

setup(
    name="pydoll-mcp",
    version=version,
    author="Jinsong Roh",
    author_email="jinsongroh@gmail.com",
    description="Revolutionary Model Context Protocol (MCP) server for PyDoll browser automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JinsongRoh/pydoll-mcp",
    project_urls={
        "Homepage": "https://github.com/JinsongRoh/pydoll-mcp",
        "Repository": "https://github.com/JinsongRoh/pydoll-mcp.git",
        "Documentation": "https://github.com/JinsongRoh/pydoll-mcp/wiki",
        "Bug Tracker": "https://github.com/JinsongRoh/pydoll-mcp/issues",
        "Changelog": "https://github.com/JinsongRoh/pydoll-mcp/blob/main/CHANGELOG.md",
        "Discussions": "https://github.com/JinsongRoh/pydoll-mcp/discussions",
        "Sponsor": "https://github.com/sponsors/JinsongRoh",
    },
    packages=find_packages(include=["pydoll_mcp", "pydoll_mcp.*"]),
    package_data={
        "pydoll_mcp": [
            "py.typed",
            "config/*.json",
            "config/*.yaml",
            "templates/*.html",
            "scripts/*.js",
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "docs": docs_requirements,
        "test": test_requirements,
        "all": dev_requirements + docs_requirements + test_requirements,
    },
    entry_points={
        "console_scripts": [
            "pydoll-mcp=pydoll_mcp.server:cli_main",
            "pydoll-mcp-server=pydoll_mcp.server:cli_main",
            "pydoll-mcp-test=pydoll_mcp.cli:test_installation",
        ],
        "mcp.servers": [
            "pydoll=pydoll_mcp.server:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
        "Environment :: Console",
        "Framework :: AsyncIO",
    ],
    keywords=[
        "mcp", "browser-automation", "web-scraping", "captcha-bypass",
        "claude", "ai", "automation", "testing", "selenium-alternative",
        "cloudflare", "recaptcha", "anti-detection", "stealth"
    ],
    zip_safe=False,
)
