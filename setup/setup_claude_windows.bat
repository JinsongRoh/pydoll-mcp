@echo off
REM PyDoll MCP Server - Claude Desktop Setup Script for Windows
REM This script automatically configures Claude Desktop to use PyDoll MCP Server

echo.
echo ========================================================
echo PyDoll MCP Server - Claude Desktop Setup for Windows
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [1/6] Checking Python installation...
python --version
echo     OK: Python is available

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo [2/6] Checking pip availability...
pip --version
echo     OK: pip is available

REM Install PyDoll MCP Server
echo [3/6] Installing PyDoll MCP Server...
pip install pydoll-mcp
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyDoll MCP Server
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo     OK: PyDoll MCP Server installed

REM Test installation
echo [4/6] Testing installation...
python -m pydoll_mcp.server --test >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Installation test failed, but continuing setup
) else (
    echo     OK: Installation test passed
)

REM Find Claude Desktop config directory
set "CLAUDE_CONFIG_DIR=%APPDATA%\Claude"
if not exist "%CLAUDE_CONFIG_DIR%" (
    echo [5/6] Creating Claude Desktop config directory...
    mkdir "%CLAUDE_CONFIG_DIR%"
    echo     OK: Created %CLAUDE_CONFIG_DIR%
) else (
    echo [5/6] Found Claude Desktop config directory...
    echo     OK: %CLAUDE_CONFIG_DIR%
)

REM Create configuration file
set "CONFIG_FILE=%CLAUDE_CONFIG_DIR%\claude_desktop_config.json"

echo [6/6] Creating Claude Desktop configuration...

REM Check if config file already exists
if exist "%CONFIG_FILE%" (
    echo     WARNING: Configuration file already exists
    echo     File: %CONFIG_FILE%
    echo.
    set /p "OVERWRITE=Do you want to overwrite the existing configuration? (y/N): "
    if /i not "%OVERWRITE%"=="y" (
        echo     Skipping configuration file creation
        goto :backup_existing
    )
    
    REM Backup existing config
    copy "%CONFIG_FILE%" "%CONFIG_FILE%.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%" >nul 2>&1
    echo     OK: Backed up existing configuration
)

REM Generate configuration content
(
echo {
echo   "mcpServers": {
echo     "pydoll": {
echo       "command": "python",
echo       "args": ["-m", "pydoll_mcp.server"],
echo       "env": {
echo         "PYDOLL_LOG_LEVEL": "INFO"
echo       }
echo     }
echo   }
echo }
) > "%CONFIG_FILE%"

if %errorlevel% neq 0 (
    echo ERROR: Failed to create configuration file
    pause
    exit /b 1
)

echo     OK: Configuration file created

:backup_existing
echo.
echo ========================================================
echo Setup completed successfully!
echo ========================================================
echo.
echo Configuration saved to:
echo %CONFIG_FILE%
echo.
echo Next steps:
echo 1. Restart Claude Desktop if it's currently running
echo 2. Test the setup by asking Claude:
echo    "Start a browser and go to https://example.com"
echo.
echo Troubleshooting:
echo - If Claude Desktop doesn't recognize the server, restart the application
echo - Check logs in: %USERPROFILE%\.local\share\pydoll-mcp\logs\
echo - Run test: python -m pydoll_mcp.server --test
echo.
echo Resources:
echo - Documentation: https://github.com/JinsongRoh/pydoll-mcp
echo - Issues: https://github.com/JinsongRoh/pydoll-mcp/issues
echo.
echo Happy automating with PyDoll MCP Server!
echo ========================================================

REM Test configuration (optional)
set /p "TEST_CONFIG=Would you like to test the configuration now? (y/N): "
if /i "%TEST_CONFIG%"=="y" (
    echo.
    echo Testing PyDoll MCP Server...
    python -m pydoll_mcp.server --test
    echo.
    echo Test completed. Check the output above for any issues.
)

echo.
echo Press any key to exit...
pause >nul