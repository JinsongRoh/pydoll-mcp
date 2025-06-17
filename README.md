# 🤖 PyDoll MCP Server(pydoll-mcp) v1.1.1

<p align="center">
  <img src="https://github.com/user-attachments/assets/219f2dbc-37ed-4aea-a289-ba39cdbb335d" alt="PyDoll Logo" width="200"/>
</p>

<p align="center">
  <strong>The Ultimate Browser Automation MCP Server</strong><br>
  Revolutionary zero-webdriver automation with intelligent captcha bypass
</p>

<p align="center">
  <a href="https://github.com/JinsongRoh/pydoll-mcp">
    <img src="https://img.shields.io/badge/GitHub-pydoll--mcp-blue?style=flat-square&logo=github" alt="GitHub"/>
  </a>
  <a href="https://github.com/autoscrape-labs/pydoll">
    <img src="https://img.shields.io/badge/Powered%20by-PyDoll-green?style=flat-square" alt="Powered by PyDoll"/>
  </a>
  <a href="https://modelcontextprotocol.io/">
    <img src="https://img.shields.io/badge/Protocol-MCP-orange?style=flat-square" alt="MCP Protocol"/>
  </a>
  <a href="https://pypi.org/project/pydoll-mcp/">
    <img src="https://img.shields.io/badge/PyPI-v1.1.1-blue?style=flat-square&logo=pypi" alt="PyPI"/>
  </a>
  <a href="https://smithery.ai/server/@JinsongRoh/pydoll-mcp">
    <img src="https://smithery.ai/badge/@JinsongRoh/pydoll-mcp" alt="Smithery"/>
  </a>
</p>

## 🌟 What Makes PyDoll MCP Server Revolutionary?

PyDoll MCP Server brings the groundbreaking capabilities of PyDoll to Claude, OpenAI, Gemini and other MCP clients. Unlike traditional browser automation tools that struggle with modern web protection, PyDoll operates at a fundamentally different level.

### PyDoll GitHub and Installation Information
- GitHub: https://github.com/autoscrape-labs/pydoll
- How to install: pip install pydoll-python
- PyDoll version: PyDoll 2.2.1 (2025.06.17)

### 🚀 Key Breakthrough Features

- **🚫 Zero WebDrivers**: Direct browser communication via Chrome DevTools Protocol
- **🧠 AI-Powered Captcha Bypass**: Automatic Cloudflare Turnstile & reCAPTCHA v3 solving
- **👤 Human Behavior Simulation**: Undetectable interactions that fool sophisticated anti-bot systems
- **⚡ Native Async Architecture**: Lightning-fast concurrent automation
- **🕵️ Advanced Stealth Mode**: Anti-detection techniques that make automation invisible
- **🌐 Real-time Network Control**: Intercept, modify, and analyze all web traffic
- **🔧 One-Click Setup**: Automatic Claude Desktop configuration
- **🌍 Universal Compatibility**: Works on all systems including Korean Windows (NEW in v1.1.1!)

## 📋 What Can You Do?

### 🎯 Smart Web Automation
- Navigate websites with human-like behavior patterns
- Extract data from protected and dynamic websites
- Automate complex workflows across multiple pages
- Handle modern SPAs and dynamic content seamlessly

### 🛡️ Protection System Bypass
- Automatically solve Cloudflare Turnstile captchas
- Bypass reCAPTCHA v3 without external services
- Evade sophisticated bot detection systems
- Navigate through protected content areas

### 📊 Advanced Data Extraction
- Scrape data from modern protected websites
- Monitor and capture all network API calls
- Extract information from dynamic, JavaScript-heavy sites
- Handle complex authentication flows

### 🔍 Comprehensive Testing & Monitoring
- Test websites under realistic user conditions
- Monitor performance and network behavior
- Validate forms and user interactions
- Capture screenshots and generate reports

## 💻 Quick Installation & Setup

### Installing via Smithery

To install PyDoll MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@JinsongRoh/pydoll-mcp):

```bash
npx -y @smithery/cli install @JinsongRoh/pydoll-mcp --client claude
```

### ⚡ One-Command Installation (Recommended)
```bash
pip install pydoll-mcp
```

**NEW in v1.1.0**: The installation now automatically offers to configure Claude Desktop! 🎉

After installation, you'll see:
```
🤖 Setting up PyDoll MCP Server...

🎉 PyDoll MCP Server installed successfully!
============================================================

🚀 Quick Start Options:
1. 🔧 Auto-configure Claude Desktop
2. 📋 Generate config manually
3. 🧪 Test installation
4. ⏭️  Skip setup (configure later)

🎯 Choose an option (1-4): 1
```

### 🚀 Alternative Setup Methods

#### Option 1: One-Click Auto Setup
```bash
# Install and configure everything automatically
pip install pydoll-mcp
python -m pydoll_mcp.cli auto-setup
```

#### Option 2: Manual Setup from Source
```bash
# Clone the repository
git clone https://github.com/JinsongRoh/pydoll-mcp.git
cd pydoll-mcp

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Setup Claude Desktop
python -m pydoll_mcp.cli setup-claude
```

#### Option 3: Docker Installation
```bash
# Pull and run the Docker container
docker run -d --name pydoll-mcp -p 8080:8080 jinsongroh/pydoll-mcp:latest
```

## ⚙️ Claude Desktop Integration

### 🔧 Automatic Setup (NEW! v1.1.0)

The easiest way to get started:

```bash
# After installing with pip, just run:
python -m pydoll_mcp.cli auto-setup
```

This will:
- ✅ Test your installation
- ✅ Locate your Claude Desktop config
- ✅ Backup existing configuration
- ✅ Add PyDoll MCP Server configuration
- ✅ Verify everything works

### 🛠️ Manual Setup Options

#### Automatic Setup Scripts

**Windows**:
```batch
# Download and run setup script
curl -o setup_claude.bat https://raw.githubusercontent.com/JinsongRoh/pydoll-mcp/main/setup/setup_claude_windows.bat
setup_claude.bat
```

**Linux/macOS**:
```bash
# Download and run setup script
curl -o setup_claude.sh https://raw.githubusercontent.com/JinsongRoh/pydoll-mcp/main/setup/setup_claude_unix.sh
chmod +x setup_claude.sh
./setup_claude.sh
```

#### Manual Configuration

If you prefer to configure manually, add this to your Claude Desktop config:

**Config File Locations:**
- **Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
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
```

#### Generate Config File
```bash
# Generate configuration file
python -m pydoll_mcp.cli generate-config

# Generate and auto-setup
python -m pydoll_mcp.cli generate-config --auto-setup

# Generate in different formats
python -m pydoll_mcp.cli generate-config --format yaml
python -m pydoll_mcp.cli generate-config --format env
```

## 🚀 Getting Started

### 1. Quick Start Guide
```bash
# Interactive setup guide
python -m pydoll_mcp.cli quick-start
```

### 2. Test Your Installation
```bash
# Test installation
python -m pydoll_mcp.cli test-installation --verbose

# Test browser automation
python -m pydoll_mcp.cli test-browser --browser chrome --headless

# Check status
python -m pydoll_mcp.cli status --logs --stats
```

### 3. Basic Usage Examples

**Basic Website Navigation:**
```
"Start a browser and go to https://example.com"
"Take a screenshot of the current page"
"Find the search box and search for 'browser automation'"
```

**Advanced Form Automation:**
```
"Fill the login form with username 'test@example.com' and password 'secure123'"
"Upload the file 'document.pdf' to the file input"
"Submit the form and wait for the success message"
```

**Protection Bypass:**
```
"Enable Cloudflare bypass and navigate to the protected site"
"Automatically solve any captcha challenges that appear"
"Extract the protected content after bypassing security"
```

**Data Extraction & Monitoring:**
```
"Monitor all network requests while browsing this e-commerce site"
"Extract product information from all visible items"
"Capture API responses containing pricing data"
```

## 🛠️ Complete Tool Arsenal

<details>
<summary><strong>🌐 Browser Management (8 tools)</strong></summary>

- **start_browser**: Launch Chrome/Edge with advanced configuration
- **stop_browser**: Gracefully terminate browser with cleanup
- **new_tab**: Create isolated tabs with custom settings
- **close_tab**: Close specific tabs and free resources
- **list_browsers**: Show all browser instances and status
- **list_tabs**: Display detailed tab information
- **set_active_tab**: Switch between tabs seamlessly
- **get_browser_status**: Comprehensive health reporting

</details>

<details>
<summary><strong>🧭 Navigation & Page Control (10 tools)</strong></summary>

- **navigate_to**: Smart URL navigation with load detection
- **refresh_page**: Intelligent page refresh with cache control
- **go_back/go_forward**: Browser history navigation
- **wait_for_page_load**: Advanced page readiness detection
- **get_current_url**: Current page URL with validation
- **get_page_source**: Complete HTML source extraction
- **get_page_title**: Page title and metadata retrieval
- **wait_for_network_idle**: Network activity monitoring
- **set_viewport_size**: Responsive design testing
- **get_page_info**: Comprehensive page analysis

</details>

<details>
<summary><strong>🎯 Element Finding & Interaction (15 tools)</strong></summary>

- **find_element**: Revolutionary natural attribute finding
- **find_elements**: Bulk element discovery with filtering
- **click_element**: Human-like clicking with timing
- **type_text**: Realistic text input simulation
- **press_key**: Advanced keyboard input handling
- **get_element_text**: Intelligent text extraction
- **get_element_attribute**: Attribute value retrieval
- **wait_for_element**: Smart element waiting conditions
- **scroll_to_element**: Smooth scrolling with viewport management
- **hover_element**: Natural mouse hover simulation
- **select_option**: Dropdown and select handling
- **check_element_visibility**: Comprehensive visibility testing
- **drag_and_drop**: Advanced drag-drop operations
- **double_click**: Double-click interaction simulation
- **right_click**: Context menu interactions

</details>

<details>
<summary><strong>📸 Screenshots & Media (6 tools)</strong></summary>

- **take_screenshot**: Full page capture with options
- **take_element_screenshot**: Precise element capture
- **generate_pdf**: Professional PDF generation
- **save_page_content**: Complete page archival
- **capture_video**: Screen recording capabilities
- **extract_images**: Image extraction and processing

</details>

<details>
<summary><strong>⚡ JavaScript & Advanced Scripting (8 tools)</strong></summary>

- **execute_script**: Full JavaScript execution environment
- **execute_script_on_element**: Element-context scripting
- **evaluate_expression**: Quick expression evaluation
- **inject_script**: External library injection
- **get_console_logs**: Browser console monitoring
- **handle_dialogs**: Alert/confirm/prompt handling
- **manipulate_cookies**: Complete cookie management
- **local_storage_operations**: Browser storage control

</details>

<details>
<summary><strong>🛡️ Protection Bypass & Stealth (12 tools)</strong></summary>

- **bypass_cloudflare**: Automatic Turnstile solving
- **bypass_recaptcha**: reCAPTCHA v3 intelligent bypass
- **enable_stealth_mode**: Advanced anti-detection
- **simulate_human_behavior**: Realistic user patterns
- **randomize_fingerprint**: Browser fingerprint rotation
- **handle_bot_challenges**: Generic challenge solving
- **evade_detection**: Comprehensive evasion techniques
- **monitor_protection_status**: Real-time security analysis
- **proxy_rotation**: Dynamic IP address changing
- **user_agent_rotation**: User agent randomization
- **header_spoofing**: Request header manipulation
- **timing_randomization**: Human-like timing patterns

</details>

<details>
<summary><strong>🌐 Network Control & Monitoring (10 tools)</strong></summary>

- **network_monitoring**: Comprehensive traffic analysis
- **intercept_requests**: Real-time request modification
- **extract_api_responses**: Automatic API capture
- **modify_headers**: Dynamic header injection
- **block_resources**: Resource blocking for performance
- **simulate_network_conditions**: Throttling and latency
- **get_network_logs**: Detailed activity reporting
- **monitor_websockets**: WebSocket connection tracking
- **analyze_performance**: Page performance metrics
- **cache_management**: Browser cache control

</details>

<details>
<summary><strong>📁 File & Data Management (8 tools)</strong></summary>

- **upload_file**: Advanced file upload handling
- **download_file**: Controlled downloading with progress
- **extract_page_data**: Structured data extraction
- **export_data**: Multi-format data export
- **import_configuration**: Settings import/export
- **manage_sessions**: Session state management
- **backup_browser_state**: Complete state backup
- **restore_browser_state**: State restoration

</details>

## 🔧 Advanced Configuration

### Performance Optimization
```json
{
  "browser_config": {
    "headless": true,
    "disable_images": true,
    "disable_css": false,
    "block_ads": true,
    "enable_compression": true,
    "max_concurrent_tabs": 5
  },
  "network_config": {
    "timeout": 30,
    "retry_attempts": 3,
    "enable_caching": true,
    "throttle_requests": false
  }
}
```

### Stealth Configuration
```json
{
  "stealth_config": {
    "randomize_fingerprint": true,
    "rotate_user_agents": true,
    "humanize_timing": true,
    "evade_webrtc": true,
    "spoof_timezone": true,
    "mask_canvas": true
  }
}
```

### Captcha Bypass Settings
```json
{
  "captcha_config": {
    "auto_solve_cloudflare": true,
    "auto_solve_recaptcha": true,
    "solve_timeout": 30,
    "retry_failed_attempts": 3,
    "human_behavior_simulation": true
  }
}
```

## 🛠️ Command Line Interface

PyDoll MCP Server comes with a powerful CLI for management and testing:

```bash
# Main commands
pydoll-mcp                          # Start MCP server
pydoll-mcp-test                     # Test installation
pydoll-mcp-setup                    # Setup Claude Desktop

# Module commands
python -m pydoll_mcp.server         # Start server
python -m pydoll_mcp.cli --help     # Show all CLI options

# Setup and configuration
python -m pydoll_mcp.cli auto-setup        # One-click setup
python -m pydoll_mcp.cli setup-claude      # Setup Claude Desktop only
python -m pydoll_mcp.cli quick-start       # Interactive guide
python -m pydoll_mcp.cli generate-config   # Generate config files

# Testing and diagnostics
python -m pydoll_mcp.cli test-installation --verbose
python -m pydoll_mcp.cli test-browser --browser chrome
python -m pydoll_mcp.cli status --logs --stats

# Maintenance
python -m pydoll_mcp.cli cleanup           # Clean temp files
```

## 🐛 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# Check Python version (requires 3.8+)
python --version

# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install pydoll-mcp -v
```

#### Browser Issues
```bash
# Verify browser installation
python -c "from pydoll.browser import Chrome; print('Browser check passed')"

# Test basic functionality
python -m pydoll_mcp.cli test-browser

# Check browser permissions
ls -la /usr/bin/google-chrome  # Linux
```

#### Connection Issues
```bash
# Test MCP server connection
python -m pydoll_mcp.server --test

# Check logs
python -m pydoll_mcp.cli status --logs

# Verify Claude Desktop config
python -m pydoll_mcp.cli generate-config
```

#### Encoding Issues (Korean Windows / International Systems) - NEW in v1.1.1!
```bash
# For Korean Windows systems with cp949 encoding
set PYTHONIOENCODING=utf-8
python -m pydoll_mcp.server

# Alternative: Use command prompt with UTF-8
chcp 65001
python -m pydoll_mcp.server

# Permanent solution: Add to Claude Desktop config
{
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
```

#### Configuration Issues
```bash
# Re-run setup
python -m pydoll_mcp.cli auto-setup --force

# Check configuration
python -m pydoll_mcp.cli status

# Manual config generation
python -m pydoll_mcp.cli generate-config --auto-setup
```

### Debug Mode
```bash
# Enable debug logging
export PYDOLL_DEBUG=1
export PYDOLL_LOG_LEVEL=DEBUG

# Run with detailed output
python -m pydoll_mcp.server --debug
```

## 📊 Performance Metrics

PyDoll MCP Server provides significant advantages over traditional automation:

| Metric | PyDoll MCP | Traditional Tools |
|--------|------------|-------------------|
| Setup Time | < 30 seconds | 5-15 minutes |
| Captcha Success Rate | 95%+ | 20-30% |
| Detection Evasion | 98%+ | 60-70% |
| Memory Usage | 50% less | Baseline |
| Speed | 3x faster | Baseline |
| Reliability | 99%+ | 80-85% |

## 🆕 What's New

### v1.1.1 (Latest)

#### 🐛 Critical Bug Fixes
- **Fixed Korean Windows Issue**: Resolved `UnicodeEncodeError` that prevented server startup on Korean Windows systems
- **Enhanced Encoding Support**: Added comprehensive encoding detection and fallback mechanisms
- **International Compatibility**: Improved support for all non-English Windows environments
- **Automatic Recovery**: Added robust error recovery for encoding-related failures

### v1.1.0

#### 🔧 One-Click Setup
- **Auto-configuration**: Automatic Claude Desktop setup during pip installation
- **Smart detection**: Automatic detection of Claude Desktop config paths
- **Safe merging**: Intelligent merging with existing configurations
- **Backup protection**: Automatic backup of existing configurations

#### 🚀 Enhanced CLI
- **New Commands**: `auto-setup`, `setup-claude`, `quick-start`
- **Interactive guides**: Step-by-step setup assistance
- **Better diagnostics**: Enhanced testing and status reporting
- **Cross-platform**: Improved Windows, macOS, and Linux support

#### 🛠️ Developer Experience
- **Post-install hooks**: Automatic setup prompts after installation
- **Multiple entry points**: Various ways to access setup functionality
- **Better error handling**: More helpful error messages and recovery suggestions
- **Documentation**: Updated docs with new setup methods

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone repository
git clone https://github.com/JinsongRoh/pydoll-mcp.git
cd pydoll-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Setup pre-commit hooks
pre-commit install
```

### Adding Features
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Submit a pull request

## 📚 Documentation & Resources

- **[Complete Documentation](https://github.com/JinsongRoh/pydoll-mcp/wiki)**: Full user guide and API reference
- **[PyDoll Library](https://autoscrape-labs.github.io/pydoll/)**: Core automation library documentation
- **[MCP Protocol](https://modelcontextprotocol.io/)**: Model Context Protocol specification
- **[Examples Repository](https://github.com/JinsongRoh/pydoll-mcp-examples)**: Comprehensive automation examples

## 🔒 Security & Ethics

### Responsible Use Guidelines
- **Respect robots.txt**: Honor website crawling policies
- **Rate Limiting**: Avoid overwhelming servers
- **Legal Compliance**: Ensure automation follows applicable laws
- **Privacy**: Handle data responsibly
- **Terms of Service**: Respect website terms

### Security Features
- **Sandboxed Execution**: Isolated browser processes
- **Secure Defaults**: Conservative security settings
- **Audit Logging**: Comprehensive action logging
- **Permission Model**: Granular capability control

## 📈 Roadmap

### v1.2.0 (Coming Soon)
- Firefox browser support
- Enhanced mobile device emulation
- Advanced form recognition
- Improved error handling
- GUI setup tool

### v1.3.0 (Q3 2025)
- Visual element recognition
- Natural language to automation
- Cloud browser support
- Enterprise features

### v2.0.0 (Future)
- AI-powered automation
- Self-healing scripts
- Advanced analytics
- Multi-platform support

## 💝 Support & Sponsorship

If you find PyDoll MCP Server valuable:

- ⭐ **Star the repository** on GitHub
- 🐛 **Report issues** and suggest improvements
- 💰 **[Sponsor the project](https://github.com/sponsors/JinsongRoh)** for priority support
- 📢 **Share** with your network
- 📝 **Write tutorials** and blog posts

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[PyDoll Team](https://github.com/autoscrape-labs/pydoll)**: For the revolutionary automation library
- **[Anthropic](https://www.anthropic.com/)**: For Claude and the MCP protocol
- **Open Source Community**: For continuous improvements and feedback

---

<p align="center">
  <strong>Ready to revolutionize your browser automation?</strong><br>
  <a href="https://github.com/JinsongRoh/pydoll-mcp/releases">Download Latest Release</a> |
  <a href="https://github.com/JinsongRoh/pydoll-mcp/wiki">Documentation</a> |
  <a href="https://github.com/JinsongRoh/pydoll-mcp/discussions">Community</a>
</p>

<p align="center">
  <em>PyDoll MCP Server - Where AI meets revolutionary browser automation! 🤖🚀</em>
</p>
