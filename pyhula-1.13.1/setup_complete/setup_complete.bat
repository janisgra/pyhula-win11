@echo off
REM Complete PyHula Setup for Windows
REM This installs everything needed for PyHula including dependencies and PyHula itself

echo Complete PyHula Setup for Windows
echo ===================================
echo.

REM Check if Python launcher is available
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using Python launcher to find best version...
    echo Available Python versions:
    py -0
    echo.
    echo Using Python 3.13 for compatibility...
    set PYTHON_CMD=py -3.13
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

echo Python version being used:
%PYTHON_CMD% --version
echo.

REM Run the complete setup
echo Running complete PyHula setup...
echo This may take several minutes...
echo.
%PYTHON_CMD% "%~dp0setup_complete.py"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! PyHula installation complete!
    echo ========================================
    echo.
    echo You can now run:
    echo   %PYTHON_CMD% pyhula_import.py
    echo   %PYTHON_CMD% test_installation.py
    echo.
) else (
    echo.
    echo ================================
    echo ERROR! Installation failed!
    echo ================================
    echo Check the error messages above.
    echo.
)

echo Press any key to exit...
pause >nul
