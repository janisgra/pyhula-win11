#!/bin/bash
# Complete PyHula Setup for Linux/macOS
# This installs everything needed for PyHula including dependencies and PyHula itself

echo "Complete PyHula Setup for Linux/macOS"
echo "====================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from your package manager or https://python.org"
    exit 1
fi

echo "Python version:"
python3 --version
echo

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Run the complete setup
echo "Running complete PyHula setup..."
echo "This may take several minutes..."
echo
python3 "$SCRIPT_DIR/setup_complete.py"

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "SUCCESS! PyHula installation complete!"
    echo "========================================"
    echo
    echo "You can now run:"
    echo "  python3 pyhula_import.py"
    echo "  python3 test_installation.py"
    echo
else
    echo
    echo "================================"
    echo "ERROR! Installation failed!"
    echo "================================"
    echo "Check the error messages above."
    echo
    exit 1
fi

echo "Installation complete!"
