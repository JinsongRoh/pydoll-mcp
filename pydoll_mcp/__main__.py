#!/usr/bin/env python3
"""PyDoll MCP Server - Main Module Entry Point.

This module serves as the main entry point when running the package as a module:
    python -m pydoll_mcp

It provides the same functionality as running the server directly but ensures
proper module loading and initialization with comprehensive encoding support.
"""

import sys
import os
from typing import Optional

# Add parent directory to path to ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_encoding():
    """Setup proper UTF-8 encoding for cross-platform compatibility with special focus on Korean Windows."""
    # Force UTF-8 encoding on Windows systems to prevent cp949 errors
    if sys.platform.startswith('win'):
        # Set environment variables for UTF-8
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ['PYTHONUTF8'] = '1'
        
        # Try to set console code page to UTF-8
        try:
            import subprocess
            subprocess.run(['chcp', '65001'], capture_output=True, shell=True, timeout=5)
        except (subprocess.TimeoutExpired, Exception):
            pass
        
        # Try to reconfigure stdout/stderr to use UTF-8
        try:
            import io
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(
                    sys.stdout.buffer, 
                    encoding='utf-8', 
                    errors='replace',
                    newline='\n'
                )
            if hasattr(sys.stderr, 'buffer'):
                sys.stderr = io.TextIOWrapper(
                    sys.stderr.buffer, 
                    encoding='utf-8', 
                    errors='replace',
                    newline='\n'
                )
        except (AttributeError, OSError):
            # Fallback for systems where buffer manipulation isn't supported
            pass

def main():
    """Main entry point for module execution with encoding safety."""
    # Setup encoding before any output
    setup_encoding()
    
    try:
        # Import and run the server
        from .server import cli_main
        cli_main()
    except ImportError as e:
        print(f"Error importing server module: {e}", file=sys.stderr)
        print("Please ensure pydoll-mcp is properly installed:", file=sys.stderr)
        print("pip install pydoll-mcp", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error starting PyDoll MCP Server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
