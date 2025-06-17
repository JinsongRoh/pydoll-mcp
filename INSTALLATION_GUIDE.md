# 🚀 PyDoll MCP Server Installation Guide

This comprehensive guide will help you install PyDoll MCP Server on Windows, macOS, and Linux systems.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+, CentOS 7+)
- **Browser**: Chrome or Edge (automatically detected)
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 500MB free space

### Pre-Installation Checklist
- [ ] Python 3.8+ installed
- [ ] pip package manager available
- [ ] Chrome or Edge browser installed
- [ ] Internet connection for package downloads
- [ ] Administrator/sudo access (for system-wide installation)

## 🔧 Installation Methods

### Method 1: Quick Install via pip (Recommended)

#### Windows
```cmd
# Open Command Prompt or PowerShell as Administrator
# Install PyDoll MCP Server
pip install pydoll-mcp

# Verify installation
pydoll-mcp --version
python -m pydoll_mcp.server --test
```

#### macOS
```bash
# Open Terminal
# Install PyDoll MCP Server
pip install pydoll-mcp

# If you encounter permission issues, use:
pip install --user pydoll-mcp

# Verify installation
pydoll-mcp --version
python -m pydoll_mcp.server --test
```

#### Linux (Ubuntu/Debian)
```bash
# Update package manager
sudo apt update

# Install Python pip if not already installed
sudo apt install python3-pip python3-venv

# Install PyDoll MCP Server
pip3 install pydoll-mcp

# Alternative: Install in user directory
pip3 install --user pydoll-mcp

# Verify installation
pydoll-mcp --version
python3 -m pydoll_mcp.server --test
```

#### Linux (CentOS/RHEL/Fedora)
```bash
# Update package manager
sudo yum update  # CentOS/RHEL
sudo dnf update  # Fedora

# Install Python pip
sudo yum install python3-pip  # CentOS/RHEL
sudo dnf install python3-pip  # Fedora

# Install PyDoll MCP Server
pip3 install pydoll-mcp

# Verify installation
pydoll-mcp --version
python3 -m pydoll_mcp.server --test
```

### Method 2: Install from Source

#### For All Platforms
```bash
# Clone the repository
git clone https://github.com/JinsongRoh/pydoll-mcp.git
cd pydoll-mcp

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Verify installation
python -m pydoll_mcp.server --test
```

### Method 3: Docker Installation

#### Prerequisites for Docker
- Docker Desktop (Windows/macOS) or Docker Engine (Linux)
- 4GB+ RAM allocated to Docker

#### Docker Installation Steps
```bash
# Pull the official Docker image
docker pull jinsongroh/pydoll-mcp:latest

# Run the container
docker run -d \\
  --name pydoll-mcp \\
  -p 8080:8080 \\
  -v $(pwd)/config:/app/config \\
  jinsongroh/pydoll-mcp:latest

# Verify container is running
docker ps

# Check logs
docker logs pydoll-mcp

# Test the server
docker exec pydoll-mcp python -m pydoll_mcp.server --test
```

## ⚙️ Claude Desktop Integration

### Automatic Setup Scripts

#### Windows Automatic Setup
```batch
@echo off
echo Setting up PyDoll MCP Server for Claude Desktop...

# Create the configuration directory
if not exist "%APPDATA%\\Claude" mkdir "%APPDATA%\\Claude"

# Create claude_desktop_config.json
echo {
echo   "mcpServers": {
echo     "pydoll": {
echo       "command": "python",
echo       "args": ["-m", "pydoll_mcp.server"],
echo       "env": {
echo         "PYDOLL_LOG_LEVEL": "INFO",
echo         "PYDOLL_BROWSER_TYPE": "chrome"
echo       }
echo     }
echo   }
echo } > "%APPDATA%\\Claude\\claude_desktop_config.json"

echo Claude Desktop configuration updated!
echo Please restart Claude Desktop to activate PyDoll MCP Server.
pause
```

Save as `setup_claude_windows.bat` and run as Administrator.

#### macOS/Linux Automatic Setup
```bash
#!/bin/bash
echo "Setting up PyDoll MCP Server for Claude Desktop..."

# Determine the configuration directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
else
    CONFIG_DIR="$HOME/.config/Claude"
fi

# Create configuration directory
mkdir -p "$CONFIG_DIR"

# Create claude_desktop_config.json
cat > "$CONFIG_DIR/claude_desktop_config.json" << 'EOF'
{
  "mcpServers": {
    "pydoll": {
      "command": "python",
      "args": ["-m", "pydoll_mcp.server"],
      "env": {
        "PYDOLL_LOG_LEVEL": "INFO",
        "PYDOLL_BROWSER_TYPE": "chrome"
      }
    }
  }
}
EOF

echo "Claude Desktop configuration updated!"
echo "Please restart Claude Desktop to activate PyDoll MCP Server."
echo "Configuration file location: $CONFIG_DIR/claude_desktop_config.json"
```

Save as `setup_claude_unix.sh`, make executable with `chmod +x setup_claude_unix.sh`, and run.

### Manual Claude Desktop Configuration

#### Step 1: Locate Configuration File
- **Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Step 2: Create/Edit Configuration
```json
{
  "mcpServers": {
    "pydoll": {
      "command": "python",
      "args": ["-m", "pydoll_mcp.server"],
      "env": {
        "PYDOLL_LOG_LEVEL": "INFO",
        "PYDOLL_BROWSER_TYPE": "chrome",
        "PYDOLL_HEADLESS": "false",
        "PYDOLL_WINDOW_WIDTH": "1920",
        "PYDOLL_WINDOW_HEIGHT": "1080"
      }
    }
  }
}
```

#### Step 3: Advanced Configuration Options
```json
{
  "mcpServers": {
    "pydoll": {
      "command": "python",
      "args": ["-m", "pydoll_mcp.server"],
      "env": {
        "PYDOLL_LOG_LEVEL": "INFO",
        "PYDOLL_BROWSER_TYPE": "chrome",
        "PYDOLL_HEADLESS": "false",
        "PYDOLL_STEALTH_MODE": "true",
        "PYDOLL_AUTO_CAPTCHA_BYPASS": "true",
        "PYDOLL_PROXY_SERVER": "",
        "PYDOLL_USER_AGENT": "",
        "PYDOLL_WINDOW_WIDTH": "1920",
        "PYDOLL_WINDOW_HEIGHT": "1080",
        "PYDOLL_DISABLE_IMAGES": "false",
        "PYDOLL_BLOCK_ADS": "true",
        "PYDOLL_TIMEOUT": "30"
      }
    }
  }
}
```

## 🧪 Verification & Testing

### Basic Functionality Test
```bash
# Test PyDoll core
python -c "import pydoll; print('✅ PyDoll imported successfully')"

# Test MCP server
python -m pydoll_mcp.server --test

# Test browser automation
python -c "
import asyncio
from pydoll.browser import Chrome

async def test():
    try:
        async with Chrome() as browser:
            tab = await browser.start()
            await tab.go_to('https://example.com')
            title = await tab.get_title()
            print(f'✅ Browser test successful: {title}')
    except Exception as e:
        print(f'❌ Browser test failed: {e}')

asyncio.run(test())
"
```

### Comprehensive Test Suite
```bash
# Run all tests
python -m pytest tests/ -v

# Run integration tests
python tests/test_integration.py

# Run browser compatibility tests
python tests/test_browser_compatibility.py

# Run MCP server tests
python tests/test_mcp_server.py
```

### Claude Desktop Integration Test
1. Restart Claude Desktop after configuration
2. Open a new conversation in Claude
3. Type: `"Start a browser and navigate to https://example.com"`
4. Claude should respond with browser automation results

## 🛠️ Troubleshooting

### Common Installation Issues

#### Issue 1: Python Version Compatibility
```bash
# Check Python version
python --version

# If version is < 3.8, install newer Python:
# Windows: Download from python.org
# macOS: brew install python@3.11
# Linux: sudo apt install python3.11
```

#### Issue 2: Permission Denied Errors
```bash
# Windows: Run Command Prompt as Administrator
# macOS/Linux: Use sudo or install in user directory
pip install --user pydoll-mcp
```

#### Issue 3: Browser Not Found
```bash
# Install Chrome
# Windows: Download from google.com/chrome
# macOS: brew install --cask google-chrome
# Linux: sudo apt install google-chrome-stable

# Or install Edge
# Windows: Usually pre-installed
# macOS: Download from microsoft.com/edge
# Linux: See Microsoft Edge Linux installation guide
```

#### Issue 4: Network/Firewall Issues
```bash
# Check internet connection
ping google.com

# Install with different index
pip install -i https://pypi.org/simple/ pydoll-mcp

# Use proxy if needed
pip install --proxy http://proxy:port pydoll-mcp
```

#### Issue 5: Dependencies Conflict
```bash
# Create clean virtual environment
python -m venv clean_env
source clean_env/bin/activate  # macOS/Linux
clean_env\\Scripts\\activate   # Windows

# Install fresh
pip install pydoll-mcp
```

### Advanced Troubleshooting

#### Enable Debug Logging
```bash
# Set environment variables
export PYDOLL_DEBUG=1
export PYDOLL_LOG_LEVEL=DEBUG

# Run with debug output
python -m pydoll_mcp.server --debug
```

#### Check Browser Process
```bash
# Windows
tasklist | findstr chrome
tasklist | findstr msedge

# macOS/Linux
ps aux | grep -i chrome
ps aux | grep -i edge
```

#### Network Debugging
```bash
# Test network connectivity
python -c "
import aiohttp
import asyncio

async def test_network():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get') as resp:
            print(f'Status: {resp.status}')
            print('✅ Network connectivity OK')

asyncio.run(test_network())
"
```

### Performance Optimization

#### System Optimization
```bash
# Increase file descriptor limits (Linux/macOS)
ulimit -n 4096

# Set browser process limits
export PYDOLL_MAX_BROWSER_INSTANCES=3
export PYDOLL_MAX_TABS_PER_BROWSER=10

# Enable performance mode
export PYDOLL_PERFORMANCE_MODE=1
```

#### Memory Management
```bash
# Monitor memory usage
python -c "
import psutil
print(f'Available memory: {psutil.virtual_memory().available / 1024**3:.2f} GB')
"

# Set memory limits for browsers
export PYDOLL_BROWSER_MEMORY_LIMIT=1024  # MB
```

## 📊 Configuration Reference

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `PYDOLL_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `PYDOLL_BROWSER_TYPE` | `chrome` | Browser to use (chrome, edge) |
| `PYDOLL_HEADLESS` | `false` | Run browser in headless mode |
| `PYDOLL_STEALTH_MODE` | `true` | Enable anti-detection features |
| `PYDOLL_AUTO_CAPTCHA_BYPASS` | `true` | Automatically solve captchas |
| `PYDOLL_TIMEOUT` | `30` | Default timeout in seconds |
| `PYDOLL_USER_AGENT` | (auto) | Custom user agent string |
| `PYDOLL_PROXY_SERVER` | (none) | Proxy server (host:port) |
| `PYDOLL_WINDOW_WIDTH` | `1920` | Browser window width |
| `PYDOLL_WINDOW_HEIGHT` | `1080` | Browser window height |

### Configuration File
Create `~/.pydoll/config.json` for persistent settings:
```json
{
  "browser": {
    "type": "chrome",
    "headless": false,
    "window_size": [1920, 1080],
    "stealth_mode": true
  },
  "automation": {
    "timeout": 30,
    "retry_attempts": 3,
    "human_behavior": true
  },
  "captcha": {
    "auto_solve": true,
    "cloudflare_bypass": true,
    "recaptcha_bypass": true
  },
  "network": {
    "monitor_requests": true,
    "block_ads": true,
    "enable_cache": true
  }
}
```

## 🔄 Updates & Maintenance

### Updating PyDoll MCP Server
```bash
# Update to latest version
pip install --upgrade pydoll-mcp

# Update with dependencies
pip install --upgrade --force-reinstall pydoll-mcp

# Check for updates
pip list --outdated | grep pydoll
```

### Version Management
```bash
# Check current version
pydoll-mcp --version

# Install specific version
pip install pydoll-mcp==1.0.0

# List available versions
pip index versions pydoll-mcp
```

## 📞 Support & Resources

### Getting Help
- **Documentation**: [GitHub Wiki](https://github.com/JinsongRoh/pydoll-mcp/wiki)
- **Issues**: [GitHub Issues](https://github.com/JinsongRoh/pydoll-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JinsongRoh/pydoll-mcp/discussions)
- **Email**: jinsongroh@gmail.com

### Useful Resources
- **PyDoll Documentation**: [autoscrape-labs.github.io/pydoll](https://autoscrape-labs.github.io/pydoll/)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **Example Scripts**: [GitHub Examples](https://github.com/JinsongRoh/pydoll-mcp/tree/main/examples)

---

**Congratulations! 🎉 You've successfully installed PyDoll MCP Server!**

Ready to revolutionize your browser automation experience? Start by asking Claude to help you automate any web task!