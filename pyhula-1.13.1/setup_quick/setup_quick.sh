#!/bin/bash
# PyHula Quick Setup for Linux/macOS
# This installs only what's needed without disrupting existing packages

echo "PyHula Quick Setup for Linux/macOS"
echo "==================================="
echo "This script installs only what's needed without disrupting existing packages."
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from your package manager or https://python.org"
    echo
    echo "On Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "On macOS with Homebrew: brew install python"
    echo "On Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

echo "Python version:"
python3 --version
echo

# Check Python version compatibility
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -ne 3 ] || [ "$MINOR" -lt 8 ]; then
    echo "[ERROR] Python $PYTHON_VERSION is not compatible"
    echo "PyHula requires Python 3.8 or higher"
    exit 1
fi

echo "[OK] Python $PYTHON_VERSION is compatible"
echo

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the quick setup
echo "Running quick setup..."
echo "This will only install missing components..."
echo
python3 "$SCRIPT_DIR/setup_quick.py"

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "SUCCESS! PyHula is ready to use!"
    echo "========================================"
    echo
    echo "You can now run:"
    echo "  python3 ../pyhula_import.py"
    echo "  python3 ../test_installation.py"
    echo
else
    echo
    echo "================================"
    echo "ERROR! Setup failed!"
    echo "================================"
    echo "Check the error messages above."
    echo
fi

echo "Press Enter to exit..."
read
