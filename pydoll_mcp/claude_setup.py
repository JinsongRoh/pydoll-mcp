"""Claude Desktop automatic setup module for PyDoll MCP Server.

This module provides OS-specific automatic configuration for Claude Desktop
to integrate PyDoll MCP Server seamlessly across Windows, macOS, and Linux.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

console = Console()


class ClaudeDesktopSetup:
    """Handles automatic Claude Desktop configuration for PyDoll MCP Server."""
    
    def __init__(self):
        """Initialize the setup handler."""
        self.system = platform.system()
        self.config_path = self._get_config_path()
        self.backup_dir = Path.home() / ".pydoll-mcp" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_config_path(self) -> Optional[Path]:
        """Get the Claude Desktop config path based on the operating system."""
        home = Path.home()
        
        if self.system == "Windows":
            # Windows: %APPDATA%\Claude\claude_desktop_config.json
            appdata = os.environ.get("APPDATA")
            if appdata:
                return Path(appdata) / "Claude" / "claude_desktop_config.json"
        elif self.system == "Darwin":  # macOS
            # macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
            return home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        elif self.system == "Linux":
            # Linux: ~/.config/Claude/claude_desktop_config.json
            return home / ".config" / "Claude" / "claude_desktop_config.json"
        
        return None
    
    def _get_python_executable(self) -> str:
        """Get the Python executable path."""
        # For virtual environments, use the current Python
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            return sys.executable
        
        # Otherwise, try to find the best Python executable
        if self.system == "Windows":
            # Try common Python locations on Windows
            candidates = [
                sys.executable,
                "python",
                "python3",
                "py",
            ]
        else:
            # Unix-like systems
            candidates = [
                sys.executable,
                "python3",
                "python",
            ]
        
        for candidate in candidates:
            try:
                result = subprocess.run(
                    [candidate, "--version"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                if result.returncode == 0:
                    return candidate
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        return sys.executable  # Fallback to current interpreter
    
    def _backup_config(self, config_path: Path) -> Optional[Path]:
        """Create a backup of the existing configuration."""
        if not config_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"claude_desktop_config_{timestamp}.json"
        
        try:
            shutil.copy2(config_path, backup_path)
            console.print(f"✅ Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            console.print(f"⚠️  Failed to create backup: {e}", style="yellow")
            return None
    
    def _load_config(self, config_path: Path) -> Dict:
        """Load existing Claude Desktop configuration."""
        if not config_path.exists():
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            console.print(f"⚠️  Error loading config: {e}", style="yellow")
            return {}
    
    def _save_config(self, config_path: Path, config: Dict) -> bool:
        """Save configuration to Claude Desktop config file."""
        try:
            # Ensure directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write config with pretty formatting
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            console.print(f"❌ Failed to save config: {e}", style="red")
            return False
    
    def _get_mcp_server_config(self) -> Dict:
        """Get the PyDoll MCP Server configuration."""
        python_exe = self._get_python_executable()
        
        config = {
            "command": python_exe,
            "args": ["-m", "pydoll_mcp.server"],
            "env": {
                "PYDOLL_LOG_LEVEL": "INFO",
                "PYTHONIOENCODING": "utf-8",
                "PYTHONUTF8": "1"
            }
        }
        
        # Add Windows-specific environment variables
        if self.system == "Windows":
            config["env"]["PYTHONLEGACYWINDOWSSTDIO"] = "1"
        
        return config
    
    def check_claude_installed(self) -> bool:
        """Check if Claude Desktop is installed."""
        if self.system == "Windows":
            # Check common installation paths
            program_files = [
                Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")),
                Path(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")),
                Path(os.environ.get("LOCALAPPDATA", "")) / "Programs"
            ]
            
            for base_path in program_files:
                if base_path and (base_path / "Claude").exists():
                    return True
                if base_path and (base_path / "Anthropic" / "Claude").exists():
                    return True
            
            # Check if config directory exists
            if self.config_path and self.config_path.parent.exists():
                return True
                
        elif self.system == "Darwin":  # macOS
            # Check Applications folder
            if (Path("/Applications") / "Claude.app").exists():
                return True
            if (Path.home() / "Applications" / "Claude.app").exists():
                return True
                
        elif self.system == "Linux":
            # Check common Linux paths
            paths_to_check = [
                Path("/opt/Claude"),
                Path("/usr/local/bin/claude"),
                Path.home() / ".local" / "share" / "applications" / "claude.desktop"
            ]
            
            for path in paths_to_check:
                if path.exists():
                    return True
        
        # Final check: config directory exists
        if self.config_path and self.config_path.parent.exists():
            return True
        
        return False
    
    def setup(self, force: bool = False) -> bool:
        """Perform automatic Claude Desktop setup."""
        console.print(Panel.fit(
            f"[bold blue]Claude Desktop Auto-Configuration[/bold blue]\n"
            f"OS: {self.system}\n"
            f"Config Path: {self.config_path or 'Not detected'}",
            title="🤖 PyDoll MCP Server Setup"
        ))
        
        # Check if Claude is installed
        if not self.check_claude_installed():
            console.print("\n⚠️  Claude Desktop not detected on this system.", style="yellow")
            console.print("Please install Claude Desktop first: https://claude.ai/desktop")
            
            if not force:
                return False
        
        if not self.config_path:
            console.print("\n❌ Could not determine Claude Desktop config path for this OS.", style="red")
            return False
        
        # Create backup if config exists
        if self.config_path.exists():
            console.print(f"\n📁 Existing configuration found at: {self.config_path}")
            backup_path = self._backup_config(self.config_path)
            
            if not force and not Confirm.ask("Do you want to update the existing configuration?"):
                console.print("Setup cancelled by user.")
                return False
        
        # Load existing config or create new
        config = self._load_config(self.config_path)
        
        # Ensure mcpServers section exists
        if "mcpServers" not in config:
            config["mcpServers"] = {}
        
        # Check if PyDoll MCP is already configured
        if "pydoll" in config["mcpServers"] and not force:
            console.print("\n⚠️  PyDoll MCP Server is already configured.", style="yellow")
            
            if not Confirm.ask("Do you want to update the existing PyDoll configuration?"):
                console.print("Setup cancelled by user.")
                return False
        
        # Add/Update PyDoll MCP configuration
        config["mcpServers"]["pydoll"] = self._get_mcp_server_config()
        
        # Save configuration
        if self._save_config(self.config_path, config):
            console.print(f"\n✅ Configuration saved successfully to: {self.config_path}")
            self._show_success_message()
            return True
        else:
            console.print("\n❌ Failed to save configuration.", style="red")
            return False
    
    def _show_success_message(self):
        """Display success message with next steps."""
        message = f"""
[bold green]✅ PyDoll MCP Server has been configured successfully![/bold green]

[bold]Next Steps:[/bold]
1. {"Restart Claude Desktop application" if self.system == "Windows" else "Restart Claude Desktop"}
2. Look for PyDoll in the MCP servers list
3. Start using PyDoll's 79 automation tools!

[bold]Quick Test:[/bold]
Ask Claude: "Start a browser and navigate to https://example.com"

[bold]Troubleshooting:[/bold]
• Run: [cyan]python -m pydoll_mcp.cli status[/cyan]
• Check logs: [cyan]python -m pydoll_mcp.cli status --logs[/cyan]
"""
        console.print(Panel(message, title="🎉 Setup Complete", expand=False))
    
    def restore_backup(self, backup_path: Optional[Path] = None) -> bool:
        """Restore configuration from backup."""
        if not backup_path:
            # Show available backups
            backups = sorted(self.backup_dir.glob("claude_desktop_config_*.json"), reverse=True)
            
            if not backups:
                console.print("No backups found.", style="yellow")
                return False
            
            # Display backup list
            table = Table(title="Available Backups")
            table.add_column("Index", style="cyan")
            table.add_column("Backup File", style="green")
            table.add_column("Date", style="yellow")
            
            for i, backup in enumerate(backups[:10]):  # Show last 10 backups
                timestamp = backup.stem.split('_', 2)[2]
                date_str = f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:15]}"
                table.add_row(str(i + 1), backup.name, date_str)
            
            console.print(table)
            
            # Ask user to select
            choice = Prompt.ask("Select backup to restore (number)", default="1")
            try:
                index = int(choice) - 1
                if 0 <= index < len(backups):
                    backup_path = backups[index]
                else:
                    console.print("Invalid selection.", style="red")
                    return False
            except ValueError:
                console.print("Invalid input.", style="red")
                return False
        
        # Restore the backup
        try:
            if self.config_path:
                shutil.copy2(backup_path, self.config_path)
                console.print(f"✅ Configuration restored from: {backup_path}")
                return True
            else:
                console.print("❌ Config path not available.", style="red")
                return False
        except Exception as e:
            console.print(f"❌ Failed to restore backup: {e}", style="red")
            return False
    
    def remove_configuration(self) -> bool:
        """Remove PyDoll MCP Server from Claude Desktop configuration."""
        if not self.config_path or not self.config_path.exists():
            console.print("No configuration file found.", style="yellow")
            return False
        
        # Create backup first
        self._backup_config(self.config_path)
        
        # Load config
        config = self._load_config(self.config_path)
        
        if "mcpServers" in config and "pydoll" in config["mcpServers"]:
            del config["mcpServers"]["pydoll"]
            
            # Save updated config
            if self._save_config(self.config_path, config):
                console.print("✅ PyDoll MCP Server configuration removed successfully.")
                return True
            else:
                console.print("❌ Failed to update configuration.", style="red")
                return False
        else:
            console.print("PyDoll MCP Server configuration not found.", style="yellow")
            return False
    
    def show_config_info(self):
        """Display current configuration information."""
        info_lines = [
            f"[bold]Operating System:[/bold] {self.system}",
            f"[bold]Config Path:[/bold] {self.config_path or 'Not detected'}",
            f"[bold]Config Exists:[/bold] {'Yes' if self.config_path and self.config_path.exists() else 'No'}",
            f"[bold]Claude Installed:[/bold] {'Yes' if self.check_claude_installed() else 'Not detected'}",
            f"[bold]Python Executable:[/bold] {self._get_python_executable()}",
            f"[bold]Backup Directory:[/bold] {self.backup_dir}",
        ]
        
        # Check if PyDoll is configured
        if self.config_path and self.config_path.exists():
            config = self._load_config(self.config_path)
            if "mcpServers" in config and "pydoll" in config["mcpServers"]:
                info_lines.append("[bold]PyDoll Status:[/bold] [green]Configured[/green]")
            else:
                info_lines.append("[bold]PyDoll Status:[/bold] [yellow]Not configured[/yellow]")
        
        panel = Panel("\n".join(info_lines), title="Claude Desktop Configuration Info", expand=False)
        console.print(panel)


def main():
    """Main entry point for the claude setup CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PyDoll MCP Server Claude Desktop Setup")
    parser.add_argument("--force", action="store_true", help="Force setup even if Claude Desktop is not detected")
    parser.add_argument("--info", action="store_true", help="Show configuration information only")
    parser.add_argument("--remove", action="store_true", help="Remove PyDoll configuration from Claude Desktop")
    parser.add_argument("--restore", type=str, metavar="BACKUP_PATH", help="Restore configuration from backup")
    
    args = parser.parse_args()
    
    setup = ClaudeDesktopSetup()
    
    if args.info:
        setup.show_config_info()
    elif args.remove:
        setup.remove_configuration()
    elif args.restore:
        backup_path = Path(args.restore) if args.restore else None
        setup.restore_backup(backup_path)
    else:
        setup.setup(force=args.force)


if __name__ == "__main__":
    main()