#!/usr/bin/env python3
"""
PyPI Publishing Script for PyDoll MCP Server

This script handles the build and publish process for PyPI.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_artifacts():
    """Clean previous build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_remove = ['build', 'dist', '*.egg-info', '.eggs']
    for pattern in dirs_to_remove:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"   Removed: {path}")
            else:
                path.unlink()
                print(f"   Removed: {path}")

def check_requirements():
    """Check if required tools are installed."""
    print("🔍 Checking requirements...")
    
    # Skip checking if we're in a virtual environment
    # The user should have already installed requirements
    print("   ✅ Assuming build tools are installed in the environment")

def build_package():
    """Build the package."""
    print("\n📦 Building package...")
    
    try:
        subprocess.run([sys.executable, '-m', 'build'], check=True)
        print("   ✅ Package built successfully")
        
        # List built files
        dist_files = list(Path('dist').glob('*'))
        print("\n   Built files:")
        for file in dist_files:
            size_mb = file.stat().st_size / 1024 / 1024
            print(f"   - {file.name} ({size_mb:.2f} MB)")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Build failed: {e}")
        return False

def check_package():
    """Check package with twine."""
    print("\n🔍 Checking package...")
    
    try:
        subprocess.run([sys.executable, '-m', 'twine', 'check', 'dist/*'], check=True)
        print("   ✅ Package check passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Package check failed: {e}")
        return False

def upload_to_testpypi():
    """Upload to TestPyPI."""
    print("\n🧪 Uploading to TestPyPI...")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'twine', 'upload',
            '--repository', 'testpypi',
            'dist/*'
        ], check=True)
        print("   ✅ Upload to TestPyPI successful")
        print("\n   Test installation with:")
        print("   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pydoll-mcp")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Upload to TestPyPI failed: {e}")
        return False

def upload_to_pypi():
    """Upload to PyPI."""
    print("\n🚀 Uploading to PyPI...")
    
    # Confirm before uploading to production
    response = input("\n⚠️  Are you sure you want to upload to PyPI? (yes/no): ")
    if response.lower() != 'yes':
        print("   Upload cancelled")
        return False
    
    try:
        subprocess.run([
            sys.executable, '-m', 'twine', 'upload',
            'dist/*'
        ], check=True)
        print("   ✅ Upload to PyPI successful")
        print("\n   Install with:")
        print("   pip install pydoll-mcp")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Upload to PyPI failed: {e}")
        return False

def main():
    """Main publishing workflow."""
    print("🚀 PyDoll MCP Server Publishing Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('pyproject.toml').exists():
        print("❌ Error: pyproject.toml not found. Run this script from the project root.")
        sys.exit(1)
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    if '--help' in args or '-h' in args:
        print("\nUsage: python publish.py [options]")
        print("\nOptions:")
        print("  --test     Upload to TestPyPI only")
        print("  --prod     Upload to PyPI (production)")
        print("  --build    Build only, don't upload")
        print("  --clean    Clean build artifacts only")
        print("  --help     Show this help message")
        sys.exit(0)
    
    # Clean build artifacts
    if '--clean' in args:
        clean_build_artifacts()
        if len(args) == 1:
            sys.exit(0)
    else:
        clean_build_artifacts()
    
    # Check requirements
    check_requirements()
    
    # Build package
    if not build_package():
        sys.exit(1)
    
    if '--build' in args:
        print("\n✅ Build complete. Skipping upload.")
        sys.exit(0)
    
    # Check package
    if not check_package():
        sys.exit(1)
    
    # Upload based on arguments
    if '--prod' in args:
        if not upload_to_pypi():
            sys.exit(1)
    elif '--test' in args or not args:
        if not upload_to_testpypi():
            sys.exit(1)
    
    print("\n✅ Publishing complete!")

if __name__ == "__main__":
    main()