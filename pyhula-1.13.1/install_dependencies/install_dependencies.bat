@echo off
REM PyHula Dependency Installer for Windows
REM This batch file installs all required dependencies for PyHula

echo PyHula Dependency Installer
echo ==========================
echo.

REM Check if Python launcher is available
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using Python launcher...
    set PYTHON_CMD=py
) else (
    REM Fall back to default python command
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python is not installed or not in PATH
        echo Please install Python 3.8+ from https://python.org
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
)

echo Python version:
%PYTHON_CMD% --version
echo.

REM Run the Python dependency installer
echo Running dependency installer...
%PYTHON_CMD% "%~dp0install_dependencies.py"

if %errorlevel% equ 0 (
    echo.
    echo [OK] Dependencies installation completed successfully!
    echo You can now run PyHula scripts.
) else (
    echo.
    echo [ERROR] Dependencies installation failed!
    echo Check the error messages above for troubleshooting.
)

echo.
echo Press any key to exit...
pause >nul
