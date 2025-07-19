#!/usr/bin/env python3
"""Post-installation setup for PyDoll MCP Server.

This module handles automatic Claude Desktop configuration after pip installation.
"""

import json
import os
import platform
import sys
from pathlib import Path
from typing import Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()


def get_claude_config_path() -> Optional[Path]:
    """Get the Claude Desktop configuration file path for the current OS."""
    system = platform.system().lower()
    
    if system == "windows":
        config_dir = Path(os.environ.get("APPDATA", "")) / "Claude"
    elif system == "darwin":  # macOS
        config_dir = Path.home() / "Library" / "Application Support" / "Claude"
    else:  # Linux and other Unix-like systems
        config_dir = Path.home() / ".config" / "Claude"
    
    return config_dir / "claude_desktop_config.json"


def get_default_config() -> Dict:
    """Get the default PyDoll MCP configuration."""
    return {
        "mcpServers": {
            "pydoll": {
                "command": "python",
                "args": ["-m", "pydoll_mcp.server"],
                "env": {
                    "PYDOLL_LOG_LEVEL": "INFO"
                }
            }
        }
    }


def merge_configs(existing_config: Dict, new_config: Dict) -> Dict:
    """Merge new MCP server config with existing configuration."""
    if "mcpServers" not in existing_config:
        existing_config["mcpServers"] = {}
    
    # Add or update pydoll server config
    existing_config["mcpServers"]["pydoll"] = new_config["mcpServers"]["pydoll"]
    
    return existing_config


def backup_existing_config(config_path: Path) -> Optional[Path]:
    """Create a backup of existing configuration."""
    if not config_path.exists():
        return None
    
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = config_path.with_suffix(f".backup.{timestamp}.json")
    
    try:
        backup_path.write_text(config_path.read_text(encoding="utf-8"), encoding="utf-8")
        return backup_path
    except Exception:
        return None


def setup_claude_desktop() -> bool:
    """Set up Claude Desktop configuration automatically."""
    console.print("\n🤖 PyDoll MCP Server - Claude Desktop Setup", style="bold blue")
    console.print("=" * 60)
    
    # Get config path
    config_path = get_claude_config_path()
    if not config_path:
        console.print("❌ Could not determine Claude Desktop config path", style="red")
        return False
    
    console.print(f"📁 Config location: {config_path}")
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if config file exists
    existing_config = {}
    if config_path.exists():
        try:
            existing_config = json.loads(config_path.read_text(encoding="utf-8"))
            console.print("✅ Found existing Claude Desktop configuration", style="green")
        except Exception as e:
            console.print(f"⚠️  Error reading existing config: {e}", style="yellow")
            existing_config = {}
    else:
        console.print("📝 Creating new Claude Desktop configuration", style="blue")
    
    # Check if pydoll is already configured
    if (existing_config.get("mcpServers", {}).get("pydoll") is not None):
        console.print("✅ PyDoll MCP Server already configured!", style="green")
        
        if not Confirm.ask("🔄 Update existing configuration?", default=False):
            console.print("⏭️  Skipping configuration update", style="yellow")
            return True
    
    # Get new configuration
    new_config = get_default_config()
    
    # Merge configurations
    merged_config = merge_configs(existing_config.copy(), new_config)
    
    # Create backup if config exists
    backup_path = backup_existing_config(config_path)
    if backup_path:
        console.print(f"💾 Created backup: {backup_path.name}", style="cyan")
    
    # Write new configuration
    try:
        config_path.write_text(
            json.dumps(merged_config, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        console.print("✅ Claude Desktop configuration updated!", style="bold green")
        
        # Show configuration
        config_preview = json.dumps(new_config["mcpServers"]["pydoll"], indent=2)
        console.print(Panel(
            config_preview,
            title="PyDoll MCP Configuration",
            border_style="green"
        ))
        
        return True
        
    except Exception as e:
        console.print(f"❌ Failed to write configuration: {e}", style="red")
        return False


def show_post_install_message():
    """Show post-installation message and setup options."""
    console.print("\n🎉 PyDoll MCP Server installed successfully!", style="bold green")
    console.print("=" * 60)
    
    # Show quick start options
    console.print("\n🚀 Quick Start Options:", style="bold blue")
    console.print("1. 🔧 Auto-configure Claude Desktop")
    console.print("2. 📋 Generate config manually")
    console.print("3. 🧪 Test installation")
    console.print("4. ⏭️  Skip setup (configure later)")
    
    try:
        choice = console.input("\n🎯 Choose an option (1-4): ").strip()
        
        if choice == "1":
            return setup_claude_desktop()
        elif choice == "2":
            show_manual_config()
            return True
        elif choice == "3":
            test_installation()
            return True
        else:
            show_manual_instructions()
            return True
            
    except (KeyboardInterrupt, EOFError):
        console.print("\n⏭️  Setup skipped", style="yellow")
        show_manual_instructions()
        return False


def show_manual_config():
    """Show manual configuration instructions."""
    config_path = get_claude_config_path()
    config = get_default_config()
    
    console.print("\n📋 Manual Configuration", style="bold blue")
    console.print("=" * 40)
    console.print(f"📁 Config file: {config_path}")
    console.print("\n📝 Add this to your Claude Desktop config:")
    
    config_text = json.dumps(config, indent=2)
    console.print(Panel(config_text, border_style="blue", title="Configuration"))


def test_installation():
    """Test the installation."""
    console.print("\n🧪 Testing installation...", style="bold blue")
    
    try:
        from .cli import test_installation as run_test
        run_test(verbose=True)
    except Exception as e:
        console.print(f"❌ Test failed: {e}", style="red")
        console.print("💡 Try: python -m pydoll_mcp.cli test-installation")


def show_manual_instructions():
    """Show manual setup instructions."""
    console.print("\n📚 Manual Setup Instructions", style="bold blue")
    console.print("=" * 50)
    
    console.print("🔧 To configure Claude Desktop manually:")
    console.print("  python -m pydoll_mcp.cli generate-config")
    console.print("\n🧪 To test your installation:")
    console.print("  python -m pydoll_mcp.cli test-installation")
    console.print("\n🌐 To test browser automation:")
    console.print("  python -m pydoll_mcp.cli test-browser")
    console.print("\n📖 Documentation:")
    console.print("  https://github.com/JinsongRoh/pydoll-mcp")


def main():
    """Main post-installation setup function."""
    # Only run in interactive mode
    if not sys.stdin.isatty():
        return
    
    # Skip if already configured (check for marker file)
    marker_file = Path.home() / ".pydoll-mcp-configured"
    if marker_file.exists():
        return
    
    try:
        success = show_post_install_message()
        
        if success:
            # Create marker file to avoid repeated setup
            marker_file.touch()
            
        console.print("\n🎊 Setup completed! Restart Claude Desktop to use PyDoll MCP Server.", style="bold green")
        
    except Exception as e:
        console.print(f"\n❌ Setup error: {e}", style="red")
        console.print("💡 You can run setup manually with: python -m pydoll_mcp.cli generate-config")


if __name__ == "__main__":
    main()
