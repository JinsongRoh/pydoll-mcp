@echo off
REM PyDoll MCP Server - Windows Installation Script
REM This script automatically installs and configures PyDoll MCP Server for Claude Desktop

echo.
echo ========================================
echo  PyDoll MCP Server v1.0.0 Installer
echo  Revolutionary Browser Automation for AI
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set python_version=%%v
echo Found Python %python_version%

REM Extract major and minor version
for /f "tokens=1,2 delims=." %%a in ("%python_version%") do (
    set major=%%a
    set minor=%%b
)

if %major% lss 3 (
    echo ERROR: Python 3.8+ required, found %python_version%
    pause
    exit /b 1
)

if %major% equ 3 if %minor% lss 8 (
    echo ERROR: Python 3.8+ required, found %python_version%
    pause
    exit /b 1
)

echo ✅ Python version check passed

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not installed or not in PATH
    echo Please install pip or reinstall Python with pip
    pause
    exit /b 1
)

echo ✅ pip is available

REM Upgrade pip
echo.
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install PyDoll MCP Server
echo.
echo 🚀 Installing PyDoll MCP Server...
pip install pydoll-mcp

if %errorlevel% neq 0 (
    echo.
    echo ❌ Installation failed. Trying alternative method...
    pip install --user pydoll-mcp
    
    if %errorlevel% neq 0 (
        echo ❌ Installation failed completely
        echo.
        echo Troubleshooting steps:
        echo 1. Run as Administrator
        echo 2. Try: pip install --user pydoll-mcp
        echo 3. Check internet connection
        echo 4. Try: pip install -i https://pypi.org/simple/ pydoll-mcp
        pause
        exit /b 1
    )
)

echo ✅ PyDoll MCP Server installed successfully

REM Test installation
echo.
echo 🧪 Testing installation...
python -c "import pydoll_mcp; print('Import successful')" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Installation test failed
    echo Try running: pip install --force-reinstall pydoll-mcp
    pause
    exit /b 1
)

echo ✅ Installation test passed

REM Check for Chrome/Edge
echo.
echo 🌐 Checking for supported browsers...

set browser_found=0

REM Check for Chrome
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Google Chrome found
    set browser_found=1
)

REM Check for Edge
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Microsoft Edge found
    set browser_found=1
)

if %browser_found% equ 0 (
    echo ⚠️  No supported browsers found
    echo Please install Google Chrome or Microsoft Edge
    echo Chrome: https://www.google.com/chrome/
    echo Edge: https://www.microsoft.com/edge/
)

REM Configure Claude Desktop
echo.
echo ⚙️  Configuring Claude Desktop...

set config_dir=%APPDATA%\Claude
set config_file=%config_dir%\claude_desktop_config.json

REM Create Claude config directory
if not exist "%config_dir%" (
    mkdir "%config_dir%"
    echo Created Claude config directory: %config_dir%
)

REM Check if config file exists
if exist "%config_file%" (
    echo.
    echo ⚠️  Claude Desktop config file already exists
    echo Current file: %config_file%
    echo.
    choice /C YN /M "Do you want to backup and update the existing config"
    if errorlevel 2 goto :skip_config
    
    REM Backup existing config
    copy "%config_file%" "%config_file%.backup.%date:/=-%_%time::=-%"
    echo 📄 Backed up existing config
)

REM Create new config
echo.
echo 📝 Creating Claude Desktop configuration...

(
echo {
echo   "mcpServers": {
echo     "pydoll": {
echo       "command": "python",
echo       "args": ["-m", "pydoll_mcp.server"],
echo       "env": {
echo         "PYDOLL_LOG_LEVEL": "INFO",
echo         "PYDOLL_BROWSER_TYPE": "chrome",
echo         "PYDOLL_HEADLESS": "false",
echo         "PYDOLL_STEALTH_MODE": "true",
echo         "PYDOLL_AUTO_CAPTCHA_BYPASS": "true"
echo       }
echo     }
echo   }
echo }
) > "%config_file%"

echo ✅ Claude Desktop configuration created
echo Config file: %config_file%

:skip_config

REM Run comprehensive test
echo.
echo 🔍 Running comprehensive test...
python -m pydoll_mcp.cli test

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Some tests failed, but installation completed
    echo Check the test results above for any issues
) else (
    echo ✅ All tests passed!
)

REM Create desktop shortcut (optional)
echo.
choice /C YN /M "Create desktop shortcut for PyDoll MCP test"
if errorlevel 1 (
    set shortcut_path=%USERPROFILE%\Desktop\PyDoll MCP Test.bat
    (
    echo @echo off
    echo python -m pydoll_mcp.cli test --browser
    echo pause
    ) > "%shortcut_path%"
    echo ✅ Desktop shortcut created
)

REM Installation complete
echo.
echo ========================================
echo  🎉 Installation Complete!
echo ========================================
echo.
echo ✨ PyDoll MCP Server is now installed and configured
echo.
echo 📋 Next Steps:
echo   1. Restart Claude Desktop to load the server
echo   2. Open Claude and try: "Start a browser and go to example.com"
echo   3. Enjoy revolutionary browser automation!
echo.
echo 🔧 Configuration:
echo   Config file: %config_file%
echo   Log location: %USERPROFILE%\.local\share\pydoll-mcp\logs\
echo.
echo 📚 Resources:
echo   GitHub: https://github.com/JinsongRoh/pydoll-mcp
echo   Documentation: See INSTALLATION_GUIDE.md
echo   Issues: https://github.com/JinsongRoh/pydoll-mcp/issues
echo.
echo 🚀 Ready to revolutionize your browser automation!
echo.

pause
