@echo off
REM PyDoll MCP Server - Claude Desktop Setup Script for Windows
REM This script automatically configures Claude Desktop to use PyDoll MCP Server

echo ========================================
echo PyDoll MCP Server - Claude Desktop Setup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if pydoll-mcp is installed
python -c "import pydoll_mcp" >nul 2>&1
if errorlevel 1 (
    echo WARNING: PyDoll MCP Server is not installed
    echo Installing PyDoll MCP Server...
    pip install pydoll-mcp
    if errorlevel 1 (
        echo ERROR: Failed to install PyDoll MCP Server
        pause
        exit /b 1
    )
    echo PyDoll MCP Server installed successfully!
    echo.
)

REM Create Claude configuration directory
if not exist "%APPDATA%\Claude" (
    echo Creating Claude configuration directory...
    mkdir "%APPDATA%\Claude"
)

REM Backup existing configuration if it exists
if exist "%APPDATA%\Claude\claude_desktop_config.json" (
    echo Backing up existing Claude Desktop configuration...
    copy "%APPDATA%\Claude\claude_desktop_config.json" "%APPDATA%\Claude\claude_desktop_config.json.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%" >nul
    echo Backup created: claude_desktop_config.json.backup.*
)

REM Create new Claude Desktop configuration
echo Creating Claude Desktop configuration...
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
echo         "PYDOLL_AUTO_CAPTCHA_BYPASS": "true",
echo         "PYDOLL_WINDOW_WIDTH": "1920",
echo         "PYDOLL_WINDOW_HEIGHT": "1080"
echo       }
echo     }
echo   }
echo }
) > "%APPDATA%\Claude\claude_desktop_config.json"

REM Verify configuration was created
if exist "%APPDATA%\Claude\claude_desktop_config.json" (
    echo ✅ Claude Desktop configuration created successfully!
    echo Configuration file: %APPDATA%\Claude\claude_desktop_config.json
) else (
    echo ❌ Failed to create Claude Desktop configuration
    pause
    exit /b 1
)

echo.
echo Testing PyDoll MCP Server installation...
python -m pydoll_mcp.server --test
if errorlevel 1 (
    echo ⚠️  PyDoll MCP Server test failed
    echo Check the installation and try again
) else (
    echo ✅ PyDoll MCP Server test passed!
)

echo.
echo ========================================
echo Setup completed successfully! 🎉
echo ========================================
echo.
echo Next steps:
echo 1. Restart Claude Desktop application
echo 2. Open a new conversation
echo 3. Try: "Start a browser and navigate to https://example.com"
echo.
echo Configuration location: %APPDATA%\Claude\claude_desktop_config.json
echo.
echo For troubleshooting, see:
echo https://github.com/JinsongRoh/pydoll-mcp/blob/main/INSTALLATION_GUIDE.md
echo.

pause
