@echo off
REM PyHula Quick Setup for Windows
REM This installs only what's needed without disrupting existing packages

echo PyHula Quick Setup for Windows
echo ===============================
echo This script installs only what's needed without disrupting existing packages.
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

REM Run the quick setup (from the setup_quick subfolder)
echo Running quick setup...
echo This will only install missing components...
echo.
%PYTHON_CMD% "%~dp0setup_quick.py"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! PyHula is ready to use!
    echo ========================================
    echo.
    echo You can now run:
    echo   %PYTHON_CMD% ..\test_installation.py
    echo   %PYTHON_CMD% ..\pyhula_import.py
    echo.
) else (
    echo.
    echo ================================
    echo ERROR! Setup failed!
    echo ================================
    echo Check the error messages above.
    echo.
)

echo Press any key to exit...
pause >nul
