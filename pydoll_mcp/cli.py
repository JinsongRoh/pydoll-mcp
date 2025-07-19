"""CLI module for PyDoll MCP Server.

This module provides command-line interface utilities for testing,
diagnosing, and managing the PyDoll MCP Server installation.
"""

import asyncio
import sys
import traceback
from typing import Dict, List, Optional, Tuple

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from . import __version__, get_package_info, health_check, get_pydoll_version
from .claude_setup import ClaudeDesktopSetup

console = Console()


def generate_config_json() -> str:
    """Generate Claude Desktop configuration JSON."""
    import json
    import os
    
    config = {
        "mcpServers": {
            "pydoll": {
                "command": "python",
                "args": ["-m", "pydoll_mcp.server"],
                "env": {
                    "PYTHONIOENCODING": "utf-8",
                    "PYDOLL_LOG_LEVEL": "INFO"
                }
            }
        }
    }
    
    return json.dumps(config, indent=2)


def format_status_icon(status: bool) -> str:
    """Format status as icon with color."""
    return "✅" if status else "❌"


def get_tool_count() -> int:
    """Get accurate count of available tools."""
    try:
        from .server import PyDollMCPServer
        
        # Create a temporary server instance to count tools
        server = PyDollMCPServer()
        tools = server.list_tools()
        return len(tools)
    except Exception:
        # Fallback to static count from __init__.py
        from . import TOTAL_TOOLS
        return TOTAL_TOOLS


def check_system_requirements() -> Dict[str, any]:
    """Check system requirements and dependencies."""
    requirements = {
        "python_version_ok": False,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "dependencies": {},
        "errors": []
    }
    
    # Check Python version
    if sys.version_info >= (3, 8):
        requirements["python_version_ok"] = True
    
    # Check dependencies
    deps_to_check = [
        ("pydoll", "pydoll-python"),
        ("mcp", "mcp"),
        ("pydantic", "pydantic"),
        ("click", "click"),
        ("rich", "rich"),
    ]
    
    for module_name, package_name in deps_to_check:
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            requirements["dependencies"][package_name] = {
                "installed": True,
                "version": version
            }
        except ImportError:
            requirements["dependencies"][package_name] = {
                "installed": False,
                "version": None
            }
            requirements["errors"].append(f"Missing dependency: {package_name}")
    
    return requirements


async def test_server_startup() -> Tuple[bool, Optional[str]]:
    """Test if the MCP server can start properly."""
    try:
        from .server import PyDollMCPServer
        
        server = PyDollMCPServer()
        # Test basic server functionality
        tools = server.list_tools()
        
        if len(tools) > 0:
            return True, None
        else:
            return False, "No tools available"
            
    except Exception as e:
        return False, str(e)


def display_status_table(verbose: bool = False) -> None:
    """Display comprehensive status information in a table."""
    table = Table(title="PyDoll MCP Server Status", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Value", style="green")
    
    # Basic package info
    table.add_row("Package Version", "✅", __version__)
    
    # PyDoll version with enhanced detection
    pydoll_version = get_pydoll_version()
    pydoll_status = "✅" if pydoll_version and pydoll_version not in ["unknown", None] else "❌"
    pydoll_display = pydoll_version or "Not detected"
    table.add_row("PyDoll Version", pydoll_status, pydoll_display)
    
    # System requirements
    sys_reqs = check_system_requirements()
    python_status = format_status_icon(sys_reqs["python_version_ok"])
    table.add_row("Python Version", python_status, sys_reqs["python_version"])
    
    # Tool count
    try:
        tool_count = get_tool_count()
        table.add_row("Tools Available", "✅", str(tool_count))
    except Exception as e:
        table.add_row("Tools Available", "❌", f"Error: {str(e)}")
    
    # Dependencies
    if verbose:
        for dep_name, dep_info in sys_reqs["dependencies"].items():
            status = format_status_icon(dep_info["installed"])
            version = dep_info["version"] or "Not installed"
            table.add_row(f"Dependency: {dep_name}", status, version)
    
    # Health check
    health_info = health_check()
    overall_status = format_status_icon(health_info["overall_status"])
    table.add_row("Overall Health", overall_status, "OK" if health_info["overall_status"] else "Issues detected")
    
    console.print(table)
    
    # Show errors if any
    if sys_reqs["errors"] or health_info["errors"]:
        console.print("\n[bold red]Issues Found:[/bold red]")
        for error in sys_reqs["errors"] + health_info["errors"]:
            console.print(f"• {error}", style="red")


@click.group()
@click.version_option(version=__version__, prog_name="pydoll-mcp")
def cli():
    """PyDoll MCP Server CLI utilities."""
    pass


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Show detailed dependency information")
@click.option("--logs", is_flag=True, help="Show recent log information")
@click.option("--stats", is_flag=True, help="Show performance statistics")
def status(verbose: bool, logs: bool, stats: bool):
    """Show PyDoll MCP Server status and health information."""
    console.print(f"\n[bold blue]PyDoll MCP Server v{__version__}[/bold blue]")
    console.print("Checking system status...\n")
    
    display_status_table(verbose)
    
    if logs:
        console.print("\n[bold yellow]📋 System Information:[/bold yellow]")
        try:
            health_info = health_check()
            if health_info.get("system_info"):
                sys_info = health_info["system_info"]
                console.print(f"  • System: {sys_info.get('system', 'Unknown')}")
                console.print(f"  • Platform: {sys_info.get('platform', 'Unknown')}")
                console.print(f"  • Architecture: {sys_info.get('architecture', 'Unknown')}")
        except Exception as e:
            console.print(f"  ❌ Could not fetch system info: {e}")
    
    if stats:
        console.print("\n[bold yellow]📊 Performance Stats:[/bold yellow]")
        try:
            tool_count = get_tool_count()
            package_info = get_package_info()
            console.print(f"  • Total Tools: {tool_count}")
            console.print(f"  • Tool Categories: {len(package_info.get('tool_categories', {}))}")
            console.print(f"  • PyDoll Version: {get_pydoll_version()}")
        except Exception as e:
            console.print(f"  ❌ Could not fetch stats: {e}")


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Show detailed test output")
def test_installation(verbose: bool):
    """Test PyDoll MCP Server installation and functionality."""
    
    def run_test():
        """Synchronous wrapper for the async test."""
        return asyncio.run(_async_test_installation(verbose))
    
    run_test()


async def _async_test_installation(verbose: bool):
    """Async implementation of installation test."""
    console.print(f"\n[bold blue]Testing PyDoll MCP Server v{__version__} Installation[/bold blue]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Test 1: Package installation
        task1 = progress.add_task("Checking package installation...", total=1)
        try:
            package_info = get_package_info()
            progress.update(task1, completed=1)
            console.print("✅ Package installation: OK")
        except Exception as e:
            progress.update(task1, completed=1)
            console.print(f"❌ Package installation: FAILED - {e}")
            return
        
        # Test 2: Dependencies
        task2 = progress.add_task("Checking dependencies...", total=1)
        sys_reqs = check_system_requirements()
        progress.update(task2, completed=1)
        
        missing_deps = [name for name, info in sys_reqs["dependencies"].items() if not info["installed"]]
        if missing_deps:
            console.print(f"❌ Dependencies: MISSING - {', '.join(missing_deps)}")
            return
        else:
            console.print("✅ Dependencies: OK")
        
        # Test 3: PyDoll version detection
        task3 = progress.add_task("Checking PyDoll version...", total=1)
        pydoll_version = get_pydoll_version()
        progress.update(task3, completed=1)
        
        if pydoll_version and pydoll_version not in ["unknown", None]:
            console.print(f"✅ PyDoll version: {pydoll_version}")
        else:
            console.print("⚠️  PyDoll version: Could not detect (but may still work)")
        
        # Test 4: Server startup
        task4 = progress.add_task("Testing server startup...", total=1)
        server_ok, server_error = await test_server_startup()
        progress.update(task4, completed=1)
        
        if server_ok:
            console.print("✅ Server startup: OK")
        else:
            console.print(f"❌ Server startup: FAILED - {server_error}")
            return
        
        # Test 5: Tool enumeration
        task5 = progress.add_task("Counting available tools...", total=1)
        try:
            tool_count = get_tool_count()
            progress.update(task5, completed=1)
            console.print(f"✅ Tools available: {tool_count}")
        except Exception as e:
            progress.update(task5, completed=1)
            console.print(f"❌ Tool enumeration: FAILED - {e}")
            return
    
    # Success summary
    console.print("\n[bold green]✨ Installation Test Complete![/bold green]")
    console.print(f"[green]✨ Total Tools Available: {tool_count}[/green]")
    console.print("[green]🚀 PyDoll MCP Server is ready to use![/green]")


@cli.command()
def info():
    """Show detailed package information."""
    package_info = get_package_info()
    
    # Create info panel
    info_text = f"""
[bold]Package:[/bold] {package_info['description']}
[bold]Version:[/bold] {package_info['version']}
[bold]Author:[/bold] {package_info['author']}
[bold]License:[/bold] {package_info['license']}
[bold]URL:[/bold] {package_info['url']}

[bold]Python Requirements:[/bold] {package_info['python_requires']}
[bold]PyDoll Version:[/bold] {package_info['pydoll_version']}
[bold]Total Tools:[/bold] {package_info['total_tools']}
"""
    
    console.print(Panel(info_text, title="PyDoll MCP Server Information", expand=False))
    
    # Show tool categories
    console.print("\n[bold]Tool Categories:[/bold]")
    for category, info in package_info['tool_categories'].items():
        count = info.get('count', 0) if isinstance(info, dict) else info
        console.print(f"  • {category.replace('_', ' ').title()}: {count} tools")


@cli.command()
def doctor():
    """Run comprehensive diagnostic checks."""
    console.print(f"\n[bold blue]PyDoll MCP Server Doctor v{__version__}[/bold blue]")
    console.print("Running comprehensive diagnostic checks...\n")
    
    issues_found = []
    
    # Check 1: Package integrity
    console.print("[bold]1. Package Integrity Check[/bold]")
    try:
        package_info = get_package_info()
        console.print("   ✅ Package information accessible")
    except Exception as e:
        issue = f"Package integrity issue: {e}"
        issues_found.append(issue)
        console.print(f"   ❌ {issue}")
    
    # Check 2: PyDoll version detection
    console.print("\n[bold]2. PyDoll Version Detection[/bold]")
    pydoll_version = get_pydoll_version()
    if pydoll_version and pydoll_version not in ["unknown", None]:
        console.print(f"   ✅ PyDoll version detected: {pydoll_version}")
    else:
        issue = "PyDoll version not detected properly"
        issues_found.append(issue)
        console.print(f"   ❌ {issue}")
        console.print("   💡 Try: pip install --upgrade pydoll-python")
    
    # Check 3: System compatibility
    console.print("\n[bold]3. System Compatibility[/bold]")
    sys_reqs = check_system_requirements()
    if sys_reqs["python_version_ok"]:
        console.print(f"   ✅ Python version OK: {sys_reqs['python_version']}")
    else:
        issue = f"Python version too old: {sys_reqs['python_version']} (requires >=3.8)"
        issues_found.append(issue)
        console.print(f"   ❌ {issue}")
    
    # Check 4: Dependencies
    console.print("\n[bold]4. Dependency Check[/bold]")
    for dep_name, dep_info in sys_reqs["dependencies"].items():
        if dep_info["installed"]:
            console.print(f"   ✅ {dep_name}: {dep_info['version']}")
        else:
            issue = f"Missing dependency: {dep_name}"
            issues_found.append(issue)
            console.print(f"   ❌ {issue}")
    
    # Check 5: Tool count consistency
    console.print("\n[bold]5. Tool Count Verification[/bold]")
    try:
        tool_count = get_tool_count()
        from . import TOTAL_TOOLS
        if tool_count == TOTAL_TOOLS:
            console.print(f"   ✅ Tool count consistent: {tool_count}")
        else:
            console.print(f"   ⚠️  Tool count mismatch: {tool_count} vs {TOTAL_TOOLS} (expected)")
    except Exception as e:
        issue = f"Tool counting error: {e}"
        issues_found.append(issue)
        console.print(f"   ❌ {issue}")
    
    # Summary
    console.print(f"\n[bold]Diagnostic Summary[/bold]")
    if not issues_found:
        console.print("[bold green]🎉 No issues found! PyDoll MCP Server is healthy.[/bold green]")
    else:
        console.print(f"[bold red]⚠️  {len(issues_found)} issues found:[/bold red]")
        for i, issue in enumerate(issues_found, 1):
            console.print(f"   {i}. {issue}")
        
        console.print("\n[bold yellow]💡 Recommended Actions:[/bold yellow]")
        console.print("   • Run: pip install --upgrade pydoll-mcp")
        console.print("   • Run: pip install --upgrade pydoll-python")
        console.print("   • Check Python version (requires >=3.8)")


@cli.command()
def version():
    """Show version information."""
    package_info = get_package_info()
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Component", style="cyan")
    table.add_column("Version", style="green")
    
    table.add_row("PyDoll MCP Server", package_info['version'])
    table.add_row("PyDoll Library", package_info['pydoll_version'])
    table.add_row("Python", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Add dependency versions
    sys_reqs = check_system_requirements()
    for dep_name, dep_info in sys_reqs["dependencies"].items():
        if dep_info["installed"]:
            table.add_row(dep_name, dep_info["version"])
    
    console.print(table)


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Force setup without confirmation prompts")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed setup information")
def auto_setup(force: bool, verbose: bool):
    """Automatically configure Claude Desktop to use PyDoll MCP Server."""
    setup = ClaudeDesktopSetup()
    
    if verbose:
        setup.show_config_info()
        console.print()
    
    success = setup.setup(force=force)
    
    if success:
        console.print("\n[bold green]🎉 Claude Desktop setup completed successfully![/bold green]")
        console.print("\n[bold]Next Steps:[/bold]")
        console.print("1. Restart Claude Desktop application")
        console.print("2. Look for 'pydoll' in the available MCP servers")
        console.print("3. Start automating with PyDoll!")
    else:
        console.print("\n[bold red]❌ Setup failed. Please check the output above for details.[/bold red]")
        console.print("\n[bold]Troubleshooting:[/bold]")
        console.print("• Run: [cyan]python -m pydoll_mcp.cli setup-info[/cyan] for more details")
        console.print("• Check: https://github.com/JinsongRoh/pydoll-mcp for documentation")


@cli.command()
def setup_info():
    """Show Claude Desktop configuration information."""
    setup = ClaudeDesktopSetup()
    setup.show_config_info()


@cli.command()
@click.option("--backup-path", "-b", type=click.Path(exists=True), help="Specific backup file to restore")
def restore_config(backup_path: Optional[str]):
    """Restore Claude Desktop configuration from backup."""
    setup = ClaudeDesktopSetup()
    
    if backup_path:
        from pathlib import Path
        backup_file = Path(backup_path)
        success = setup.restore_backup(backup_file)
    else:
        success = setup.restore_backup()
    
    if success:
        console.print("[bold green]✅ Configuration restored successfully![/bold green]")
        console.print("Please restart Claude Desktop to apply changes.")
    else:
        console.print("[bold red]❌ Failed to restore configuration.[/bold red]")


@cli.command()
@click.confirmation_option(prompt="Are you sure you want to remove PyDoll from Claude Desktop?")
def remove_config():
    """Remove PyDoll MCP Server from Claude Desktop configuration."""
    setup = ClaudeDesktopSetup()
    
    success = setup.remove_configuration()
    
    if success:
        console.print("[bold green]✅ PyDoll configuration removed successfully![/bold green]")
        console.print("Please restart Claude Desktop to apply changes.")
    else:
        console.print("[bold red]❌ Failed to remove configuration.[/bold red]")


def main():
    """Main CLI entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        if "--debug" in sys.argv:
            console.print("\n[red]Debug traceback:[/red]")
            console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
