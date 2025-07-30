# Complete Setup Scripts

This folder contains scripts for a **complete PyHula installation** - they install all dependencies AND build and install PyHula itself from source.

## What These Scripts Do

Unlike the conservative setup_quick scripts that only install missing components, these scripts perform a **full installation**:

1. **Check Python compatibility** (requires Python 3.8+)
2. **Install build tools** (setuptools, wheel, Cython)
3. **Install all dependencies** (numpy, opencv-python, pyserial, etc.)
4. **Build PyHula from source** (creates wheel package)
5. **Install PyHula** (from the built wheel)
6. **Test the installation** (verify everything works)

## When to Use Complete Setup

Use these scripts when you want a **fresh, complete installation**:
- First-time PyHula installation
- Clean installation after removing previous versions
- Setting up PyHula in a new environment
- You want to ensure all dependencies are properly installed

## Scripts Available

### `setup_complete.py`
Main Python script that does all the heavy lifting. Can be run directly:
```bash
python setup_complete.py
```

### `setup_complete.bat` (Windows)
Windows batch file wrapper. Double-click to run or use from Command Prompt:
```cmd
setup_complete.bat
```

### `setup_complete.sh` (Linux/macOS)
Shell script wrapper for Unix-like systems:
```bash
chmod +x setup_complete.sh
./setup_complete.sh
```

## Installation Time

Complete installation typically takes **5-15 minutes** depending on:
- Your internet connection (for downloading packages)
- Your system performance (for building from source)
- Whether dependencies need to be compiled

## Requirements

- **Python 3.8 or higher**
- **Internet connection** (for downloading packages)
- **Build tools** (Visual Studio Build Tools on Windows, development tools on Linux/macOS)

## What Gets Installed

The complete setup installs:
- **Core PyHula library** (built from source)
- **Essential dependencies**: numpy, opencv-python, scipy, matplotlib
- **Drone communication**: pyserial, pymavlink
- **Image processing**: pillow
- **Build tools**: setuptools, wheel, Cython

## Troubleshooting

If installation fails:
1. **Check Python version**: Must be 3.8 or higher
2. **Install build tools**: Visual Studio Build Tools (Windows) or development packages (Linux)
3. **Check internet connection**: Required for downloading packages
4. **Run as administrator/sudo**: May be needed for system-wide installation

## Alternative Options

- **Quick setup**: Use `../setup_quick/` scripts for conservative installation
- **Dependencies only**: Use `../install_dependencies/install_dependencies.py` for just dependencies
- **Manual installation**: Follow instructions in `../INSTALL.md`

## Support

If you encounter issues:
- Check the error messages in the console output
- Ensure you have the required build tools installed
- Try the quick setup scripts as an alternative
- Refer to the main project documentation
