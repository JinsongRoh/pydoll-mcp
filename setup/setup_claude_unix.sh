#!/bin/bash
# PyDoll MCP Server - Claude Desktop Setup Script for Linux/macOS
# This script automatically configures Claude Desktop to use PyDoll MCP Server

set -e

echo "========================================"
echo "PyDoll MCP Server - Claude Desktop Setup"
echo "========================================"
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    print_error "Python is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    echo
    echo "Installation instructions:"
    echo "- Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "- CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "- Fedora: sudo dnf install python3 python3-pip"
    echo "- macOS: brew install python@3.11"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo "Using Python: $($PYTHON_CMD --version)"

# Check if pydoll-mcp is installed
if ! $PYTHON_CMD -c "import pydoll_mcp" &> /dev/null; then
    print_warning "PyDoll MCP Server is not installed"
    echo "Installing PyDoll MCP Server..."
    
    if ! $PIP_CMD install pydoll-mcp; then
        print_error "Failed to install PyDoll MCP Server"
        echo "Try installing with --user flag:"
        echo "$PIP_CMD install --user pydoll-mcp"
        exit 1
    fi
    
    print_success "PyDoll MCP Server installed successfully!"
    echo
fi

# Determine the configuration directory based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    print_info "Detected macOS"
else
    # Linux
    CONFIG_DIR="$HOME/.config/Claude"
    print_info "Detected Linux"
fi

CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

# Create configuration directory if it doesn't exist
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Creating Claude configuration directory..."
    mkdir -p "$CONFIG_DIR"
    print_success "Configuration directory created: $CONFIG_DIR"
fi

# Backup existing configuration if it exists
if [ -f "$CONFIG_FILE" ]; then
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="${CONFIG_FILE}.backup.${TIMESTAMP}"
    
    echo "Backing up existing Claude Desktop configuration..."
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    print_success "Backup created: $(basename $BACKUP_FILE)"
fi

# Create new Claude Desktop configuration
echo "Creating Claude Desktop configuration..."
cat > "$CONFIG_FILE" << 'EOF'
{
  "mcpServers": {
    "pydoll": {
      "command": "python3",
      "args": ["-m", "pydoll_mcp.server"],
      "env": {
        "PYDOLL_LOG_LEVEL": "INFO",
        "PYDOLL_BROWSER_TYPE": "chrome",
        "PYDOLL_HEADLESS": "false",
        "PYDOLL_STEALTH_MODE": "true",
        "PYDOLL_AUTO_CAPTCHA_BYPASS": "true",
        "PYDOLL_WINDOW_WIDTH": "1920",
        "PYDOLL_WINDOW_HEIGHT": "1080"
      }
    }
  }
}
EOF

# Verify configuration was created
if [ -f "$CONFIG_FILE" ]; then
    print_success "Claude Desktop configuration created successfully!"
    echo "Configuration file: $CONFIG_FILE"
else
    print_error "Failed to create Claude Desktop configuration"
    exit 1
fi

echo
echo "Testing PyDoll MCP Server installation..."
if $PYTHON_CMD -m pydoll_mcp.server --test; then
    print_success "PyDoll MCP Server test passed!"
else
    print_warning "PyDoll MCP Server test failed"
    echo "Check the installation and try again"
fi

echo
echo "========================================"
echo "Setup completed successfully! 🎉"
echo "========================================"
echo
echo "Next steps:"
echo "1. Restart Claude Desktop application"
echo "2. Open a new conversation"
echo "3. Try: \"Start a browser and navigate to https://example.com\""
echo
echo "Configuration location: $CONFIG_FILE"
echo
echo "For troubleshooting, see:"
echo "https://github.com/JinsongRoh/pydoll-mcp/blob/main/INSTALLATION_GUIDE.md"
echo

# Check if browser is available
if command -v google-chrome &> /dev/null || command -v google-chrome-stable &> /dev/null; then
    print_success "Google Chrome detected"
elif command -v microsoft-edge &> /dev/null || command -v microsoft-edge-stable &> /dev/null; then
    print_success "Microsoft Edge detected"
else
    print_warning "No supported browser detected"
    echo "Please install Google Chrome or Microsoft Edge:"
    echo "- Chrome: https://www.google.com/chrome/"
    echo "- Edge: https://www.microsoft.com/edge"
fi

echo
print_info "Setup script completed. You can now use PyDoll MCP Server with Claude!"
