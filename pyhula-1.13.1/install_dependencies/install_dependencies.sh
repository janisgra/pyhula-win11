#!/bin/bash
# PyHula Dependency Installer for Linux/macOS
# This script installs all required dependencies for PyHula

echo "PyHula Dependency Installer"
echo "=========================="
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

# Run the Python dependency installer
echo "Running dependency installer..."
python3 "$SCRIPT_DIR/install_dependencies.py"

if [ $? -eq 0 ]; then
    echo
    echo "[OK] Dependencies installation completed successfully!"
    echo "You can now run PyHula scripts."
else
    echo
    echo "[ERROR] Dependencies installation failed!"
    echo "Check the error messages above for troubleshooting."
    exit 1
fi

echo
echo "Installation complete!"
