@echo off
echo PyHula Build Script for Windows - Python 3.13
echo ===============================================

REM Check if Python 3.13 is available
py -3.13 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3.13 not found
    echo Please install Python 3.13 or check if it's available with: py --list
    pause
    exit /b 1
)

echo.
echo Using Python 3.13 for building PyHula package...
echo.

REM Clean previous builds and installations
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%d in (*.egg-info) do if exist "%%d" rmdir /s /q "%%d"

REM Uninstall old pyhula versions
echo.
echo Uninstalling old PyHula versions...
py -3.13 -m pip uninstall pyhula -y >nul 2>&1
echo Old versions removed

REM Build C extensions
echo.
echo Building C extensions with Python 3.13...
py -3.13 setup.py build_ext --inplace
if %errorlevel% neq 0 (
    echo ERROR: Failed to build C extensions
    pause
    exit /b 1
)

REM Build wheel
echo.
echo Building wheel with Python 3.13...
py -3.13 setup.py bdist_wheel
if %errorlevel% neq 0 (
    echo WARNING: Failed to build wheel, trying to install wheel package...
    py -3.13 -m pip install wheel
    py -3.13 setup.py bdist_wheel
    if %errorlevel% neq 0 (
        echo ERROR: Failed to build wheel even after installing wheel package
        pause
        exit /b 1
    )
)

echo.
echo ===============================
echo Build completed successfully!
echo.
echo To install the package:
echo   py -3.13 -m pip install dist\pyhula-1.13.1-*.whl
echo.
echo To test installation:
echo   py -3.13 utils\diagnostic.py
echo   py -3.13 simple_test.py
echo.
pause
