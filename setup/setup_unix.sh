#!/bin/bash

# PyDoll MCP Server - Unix/Linux/macOS Installation Script
# This script automatically installs and configures PyDoll MCP Server for Claude Desktop

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emojis for better UX
CHECK="✅"
CROSS="❌"
WARNING="⚠️ "
ROCKET="🚀"
GEAR="⚙️ "
BOOK="📚"
SPARKLES="✨"

# Helper functions
print_header() {
    echo -e "${BLUE}"
    echo "========================================"
    echo "  PyDoll MCP Server v1.0.0 Installer"
    echo "  Revolutionary Browser Automation for AI"
    echo "========================================"
    echo -e "${NC}"
}

print_step() {
    echo -e "\n${CYAN}$1${NC}"
}

print_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

print_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${WARNING}$1${NC}"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        if command -v apt-get &> /dev/null; then
            DISTRO="debian"
        elif command -v yum &> /dev/null; then
            DISTRO="rhel"
        elif command -v dnf &> /dev/null; then
            DISTRO="fedora"
        else
            DISTRO="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        DISTRO="macos"
    else
        OS="unknown"
        DISTRO="unknown"
    fi
}

# Check Python installation
check_python() {
    print_step "${GEAR}Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        if ! command -v python &> /dev/null; then
            print_error "Python is not installed"
            echo "Please install Python 3.8+ using your system package manager:"
            echo ""
            case $DISTRO in
                "debian")
                    echo "  sudo apt update && sudo apt install python3 python3-pip"
                    ;;
                "rhel")
                    echo "  sudo yum install python3 python3-pip"
                    ;;
                "fedora")
                    echo "  sudo dnf install python3 python3-pip"
                    ;;
                "macos")
                    echo "  brew install python3"
                    echo "  or download from https://python.org"
                    ;;
                *)
                    echo "  See https://python.org for installation instructions"
                    ;;
            esac
            exit 1
        else
            PYTHON_CMD="python"
        fi
    else
        PYTHON_CMD="python3"
    fi
    
    # Check Python version
    PYTHON_VERSION=$(${PYTHON_CMD} --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -lt "3" ] || ([ "$PYTHON_MAJOR" -eq "3" ] && [ "$PYTHON_MINOR" -lt "8" ]); then
        print_error "Python 3.8+ required, found $PYTHON_VERSION"
        exit 1
    fi
    
    print_success "Python $PYTHON_VERSION found"
}

# Check pip installation
check_pip() {
    print_step "${GEAR}Checking pip installation..."
    
    if ! command -v pip3 &> /dev/null; then
        if ! command -v pip &> /dev/null; then
            print_error "pip is not installed"
            echo "Installing pip..."
            
            case $DISTRO in
                "debian")
                    sudo apt update && sudo apt install python3-pip
                    ;;
                "rhel")
                    sudo yum install python3-pip
                    ;;
                "fedora")
                    sudo dnf install python3-pip
                    ;;
                "macos")
                    ${PYTHON_CMD} -m ensurepip --upgrade
                    ;;
                *)
                    print_error "Please install pip manually"
                    exit 1
                    ;;
            esac
            PIP_CMD="pip3"
        else
            PIP_CMD="pip"
        fi
    else
        PIP_CMD="pip3"
    fi
    
    print_success "pip is available"
}

# Install PyDoll MCP Server
install_pydoll_mcp() {
    print_step "${ROCKET}Installing PyDoll MCP Server..."
    
    # Upgrade pip first
    echo "Upgrading pip..."
    ${PYTHON_CMD} -m pip install --upgrade pip
    
    # Install PyDoll MCP Server
    echo "Installing PyDoll MCP Server..."
    
    if ! $PIP_CMD install pydoll-mcp; then
        print_warning "Global installation failed, trying user installation..."
        if ! $PIP_CMD install --user pydoll-mcp; then
            print_error "Installation failed completely"
            echo ""
            echo "Troubleshooting steps:"
            echo "1. Try: sudo $PIP_CMD install pydoll-mcp"
            echo "2. Try: $PIP_CMD install --user pydoll-mcp"
            echo "3. Check internet connection"
            echo "4. Try: $PIP_CMD install -i https://pypi.org/simple/ pydoll-mcp"
            exit 1
        fi
    fi
    
    print_success "PyDoll MCP Server installed successfully"
}

# Test installation
test_installation() {
    print_step "🧪 Testing installation..."
    
    if ! ${PYTHON_CMD} -c "import pydoll_mcp; print('Import successful')" &> /dev/null; then
        print_error "Installation test failed"
        echo "Try running: $PIP_CMD install --force-reinstall pydoll-mcp"
        exit 1
    fi
    
    print_success "Installation test passed"
}

# Check browsers
check_browsers() {
    print_step "🌐 Checking for supported browsers..."
    
    BROWSER_FOUND=false
    
    # Check for Chrome variants
    for chrome_cmd in google-chrome google-chrome-stable chromium chromium-browser; do
        if command -v $chrome_cmd &> /dev/null; then
            print_success "Chrome/Chromium found: $chrome_cmd"
            BROWSER_FOUND=true
            break
        fi
    done
    
    # Check for Edge (if available on Linux)
    if command -v microsoft-edge &> /dev/null; then
        print_success "Microsoft Edge found"
        BROWSER_FOUND=true
    fi
    
    # macOS specific checks
    if [[ "$OS" == "macos" ]]; then
        if [ -d "/Applications/Google Chrome.app" ]; then
            print_success "Google Chrome found (macOS)"
            BROWSER_FOUND=true
        fi
        
        if [ -d "/Applications/Microsoft Edge.app" ]; then
            print_success "Microsoft Edge found (macOS)"
            BROWSER_FOUND=true
        fi
    fi
    
    if [ "$BROWSER_FOUND" = false ]; then
        print_warning "No supported browsers found"
        echo "Please install Google Chrome or Microsoft Edge:"
        case $DISTRO in
            "debian")
                echo "  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -"
                echo "  sudo sh -c 'echo \"deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main\" > /etc/apt/sources.list.d/google-chrome.list'"
                echo "  sudo apt update && sudo apt install google-chrome-stable"
                ;;
            "rhel"|"fedora")
                echo "  sudo dnf install google-chrome-stable"
                ;;
            "macos")
                echo "  brew install --cask google-chrome"
                echo "  or download from https://www.google.com/chrome/"
                ;;
        esac
    fi
}

# Configure Claude Desktop
configure_claude() {
    print_step "${GEAR}Configuring Claude Desktop..."
    
    # Determine config directory
    if [[ "$OS" == "macos" ]]; then
        CONFIG_DIR="$HOME/Library/Application Support/Claude"
    else
        CONFIG_DIR="$HOME/.config/Claude"
    fi
    
    CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
    
    # Create config directory
    mkdir -p "$CONFIG_DIR"
    echo "Created Claude config directory: $CONFIG_DIR"
    
    # Check if config file exists
    if [ -f "$CONFIG_FILE" ]; then
        echo ""
        print_warning "Claude Desktop config file already exists"
        echo "Current file: $CONFIG_FILE"
        echo ""
        read -p "Do you want to backup and update the existing config? (y/N): " -n 1 -r
        echo ""
        
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Skipping Claude Desktop configuration"
            return
        fi
        
        # Backup existing config
        BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$CONFIG_FILE" "$BACKUP_FILE"
        print_success "Backed up existing config to: $BACKUP_FILE"
    fi
    
    # Create new config
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
        "PYDOLL_AUTO_CAPTCHA_BYPASS": "true"
      }
    }
  }
}
EOF
    
    print_success "Claude Desktop configuration created"
    echo "Config file: $CONFIG_FILE"
}

# Run comprehensive test
run_tests() {
    print_step "🔍 Running comprehensive test..."
    
    if ! ${PYTHON_CMD} -m pydoll_mcp.cli test; then
        echo ""
        print_warning "Some tests failed, but installation completed"
        echo "Check the test results above for any issues"
    else
        print_success "All tests passed!"
    fi
}

# Create launcher script
create_launcher() {
    print_step "📝 Creating launcher script..."
    
    LAUNCHER_DIR="$HOME/.local/bin"
    mkdir -p "$LAUNCHER_DIR"
    
    LAUNCHER_FILE="$LAUNCHER_DIR/pydoll-mcp-test"
    
    cat > "$LAUNCHER_FILE" << EOF
#!/bin/bash
# PyDoll MCP Server Test Launcher
${PYTHON_CMD} -m pydoll_mcp.cli test --browser
EOF
    
    chmod +x "$LAUNCHER_FILE"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$LAUNCHER_DIR:"* ]]; then
        echo ""
        print_warning "Add $LAUNCHER_DIR to your PATH to use pydoll-mcp-test command"
        echo "Add this line to your ~/.bashrc or ~/.zshrc:"
        echo "export PATH=\"\$PATH:$LAUNCHER_DIR\""
    fi
    
    print_success "Launcher script created: $LAUNCHER_FILE"
}

# Main installation function
main() {
    print_header
    
    # Detect operating system
    detect_os
    echo "Detected OS: $OS ($DISTRO)"
    
    # Pre-installation checks
    check_python
    check_pip
    
    # Install PyDoll MCP Server
    install_pydoll_mcp
    
    # Test installation
    test_installation
    
    # Check browsers
    check_browsers
    
    # Configure Claude Desktop
    configure_claude
    
    # Run tests
    run_tests
    
    # Create launcher script
    create_launcher
    
    # Installation complete
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}  🎉 Installation Complete!${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${SPARKLES} PyDoll MCP Server is now installed and configured"
    echo ""
    echo -e "${BOOK} Next Steps:"
    echo "  1. Restart Claude Desktop to load the server"
    echo "  2. Open Claude and try: \"Start a browser and go to example.com\""
    echo "  3. Enjoy revolutionary browser automation!"
    echo ""
    echo -e "${GEAR} Configuration:"
    echo "  Config file: $CONFIG_FILE"
    echo "  Log location: ~/.local/share/pydoll-mcp/logs/"
    echo ""
    echo -e "${BOOK} Resources:"
    echo "  GitHub: https://github.com/JinsongRoh/pydoll-mcp"
    echo "  Documentation: See INSTALLATION_GUIDE.md"
    echo "  Issues: https://github.com/JinsongRoh/pydoll-mcp/issues"
    echo ""
    echo -e "${ROCKET} Ready to revolutionize your browser automation!"
    echo ""
}

# Run main function
main "$@"
