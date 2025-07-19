#!/bin/bash

# PyDoll MCP Server - Claude Desktop Setup Script for Unix/Linux/macOS
# This script automatically configures Claude Desktop to use PyDoll MCP Server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Header
echo
echo "========================================================"
echo "PyDoll MCP Server - Claude Desktop Setup for Unix/Linux/macOS"
echo "========================================================"
echo

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
    OS="windows"
else
    log_warning "Unknown OS type: $OSTYPE, assuming Linux"
    OS="linux"
fi

log_info "Detected OS: $OS"

# Step 1: Check Python installation
echo
log_info "[1/6] Checking Python installation..."

if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        log_error "Python is not installed or not in PATH"
        echo "Please install Python 3.8+ using your package manager:"
        case $OS in
            "linux")
                echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
                echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
                echo "  Arch:          sudo pacman -S python python-pip"
                ;;
            "macos")
                echo "  Homebrew:      brew install python"
                echo "  MacPorts:      sudo port install python38"
                echo "  Or download from: https://python.org"
                ;;
        esac
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

PYTHON_VERSION=$(${PYTHON_CMD} --version 2>&1)
log_success "Found Python: $PYTHON_VERSION"

# Check Python version
PYTHON_MAJOR=$(${PYTHON_CMD} -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(${PYTHON_CMD} -c "import sys; print(sys.version_info.minor)")

if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
    log_error "Python 3.8+ is required. Found: $PYTHON_VERSION"
    exit 1
fi

# Step 2: Check pip availability
echo
log_info "[2/6] Checking pip availability..."

if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        log_error "pip is not available"
        echo "Please install pip using your package manager or get-pip.py"
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

PIP_VERSION=$(${PIP_CMD} --version 2>&1)
log_success "Found pip: $PIP_VERSION"

# Step 3: Install PyDoll MCP Server
echo
log_info "[3/6] Installing PyDoll MCP Server..."

if $PIP_CMD install pydoll-mcp; then
    log_success "PyDoll MCP Server installed successfully"
else
    log_error "Failed to install PyDoll MCP Server"
    echo "Please check your internet connection and try again"
    echo "You can also try: $PIP_CMD install --user pydoll-mcp"
    exit 1
fi

# Step 4: Test installation
echo
log_info "[4/6] Testing installation..."

if $PYTHON_CMD -m pydoll_mcp.server --test >/dev/null 2>&1; then
    log_success "Installation test passed"
else
    log_warning "Installation test failed, but continuing setup"
    log_info "You can run the test manually later: $PYTHON_CMD -m pydoll_mcp.server --test"
fi

# Step 5: Determine Claude Desktop config directory
echo
log_info "[5/6] Locating Claude Desktop config directory..."

case $OS in
    "macos")
        CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
        ;;
    "linux")
        CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
        ;;
    *)
        CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
        ;;
esac

if [[ ! -d "$CLAUDE_CONFIG_DIR" ]]; then
    log_info "Creating Claude Desktop config directory..."
    mkdir -p "$CLAUDE_CONFIG_DIR"
    log_success "Created: $CLAUDE_CONFIG_DIR"
else
    log_success "Found: $CLAUDE_CONFIG_DIR"
fi

# Step 6: Create configuration file
echo
log_info "[6/6] Creating Claude Desktop configuration..."

CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

# Check if config file already exists
if [[ -f "$CONFIG_FILE" ]]; then
    log_warning "Configuration file already exists: $CONFIG_FILE"
    echo
    read -p "Do you want to overwrite the existing configuration? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Skipping configuration file creation"
    else
        # Backup existing config
        BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$CONFIG_FILE" "$BACKUP_FILE"
        log_success "Backed up existing configuration to: $BACKUP_FILE"
        CREATE_CONFIG=true
    fi
else
    CREATE_CONFIG=true
fi

if [[ "$CREATE_CONFIG" == true ]]; then
    # Generate configuration content
    cat > "$CONFIG_FILE" << 'EOF'
{
  "mcpServers": {
    "pydoll": {
      "command": "python3",
      "args": ["-m", "pydoll_mcp.server"],
      "env": {
        "PYDOLL_LOG_LEVEL": "INFO"
      }
    }
  }
}
EOF

    # Adjust python command based on what we found
    if [[ "$PYTHON_CMD" == "python" ]]; then
        sed -i.tmp 's/"python3"/"python"/g' "$CONFIG_FILE" && rm "$CONFIG_FILE.tmp"
    fi

    log_success "Configuration file created: $CONFIG_FILE"
fi

# Success message
echo
echo "========================================================"
echo "Setup completed successfully!"
echo "========================================================"
echo
echo "Configuration saved to:"
echo "  $CONFIG_FILE"
echo
echo "Next steps:"
echo "  1. Restart Claude Desktop if it's currently running"
echo "  2. Test the setup by asking Claude:"
echo "     \"Start a browser and go to https://example.com\""
echo
echo "Troubleshooting:"
echo "  - If Claude Desktop doesn't recognize the server, restart the application"
echo "  - Check logs in: $HOME/.local/share/pydoll-mcp/logs/"
echo "  - Run test: $PYTHON_CMD -m pydoll_mcp.server --test"
echo "  - Check permissions: ls -la \"$CONFIG_FILE\""
echo
echo "Resources:"
echo "  - Documentation: https://github.com/JinsongRoh/pydoll-mcp"
echo "  - Issues: https://github.com/JinsongRoh/pydoll-mcp/issues"
echo
echo "Happy automating with PyDoll MCP Server!"
echo "========================================================"

# Optional configuration test
echo
read -p "Would you like to test the configuration now? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo
    log_info "Testing PyDoll MCP Server..."
    echo
    if $PYTHON_CMD -m pydoll_mcp.server --test; then
        echo
        log_success "Configuration test completed successfully!"
    else
        echo
        log_warning "Test completed with issues. Check the output above."
    fi
fi

# Additional OS-specific instructions
echo
case $OS in
    "macos")
        echo "macOS-specific notes:"
        echo "  - You may need to grant Chrome browser permissions in System Preferences"
        echo "  - If you encounter permission issues, try: chmod 755 \"$CONFIG_FILE\""
        ;;
    "linux")
        echo "Linux-specific notes:"
        echo "  - Ensure you have a compatible browser (Chrome/Chromium) installed"
        echo "  - For headless operation, you may need: sudo apt install xvfb"
        echo "  - If you encounter permission issues, check file ownership"
        ;;
esac

echo
echo "Setup script completed. Enjoy using PyDoll MCP Server!"
