@echo off
REM PyHula Quick Setup Launcher
REM This script launches the quick setup from its subfolder

echo Starting PyHula Quick Setup...
echo.

cd /d "%~dp0setup_quick"
if exist setup_quick.bat (
    call setup_quick.bat
) else (
    echo [ERROR] Quick setup files not found in setup_quick folder
    pause
)
