# PyHula Build and Installation Instructions

## For Windows

### Prerequisites
1. Python 3.8+ installed
2. Visual Studio Build Tools 2022 (or Visual Studio Community)
3. Windows SDK

### Build Steps
```powershell
# Navigate to wherever you put the PyHula files
cd C:\path\to\your\pyhula-1.13.1

# Install build dependencies
pip install setuptools wheel numpy Cython

# Run the automated build script (recommended)
python build.py

# OR build manually:
python setup.py build_ext --inplace
python setup.py bdist_wheel

# Install the built wheel
pip install dist\pyhula-1.13.1-*.whl

# Test the installation
python test_installation.py
```

## For Linux

```bash
# On Ubuntu/Debian systems:
sudo apt-get update
sudo apt-get install python3-dev build-essential

# On CentOS/RHEL/Fedora systems:
sudo dnf install python3-devel gcc gcc-c++
# (older systems might need 'yum' instead of 'dnf')
```

### Build Steps
```bash
# Navigate to the directory
cd /path/to/pyhula-1.13.1

# Install build dependencies
pip install setuptools wheel numpy Cython

# Build everything
python build.py

# Install
pip install dist/pyhula-1.13.1-*.whl

# Test
python test_installation.py
```

## For macOS

### Prerequisites
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python if needed
brew install python
```

Then the build process is the same as Linux:

```bash
cd /path/to/pyhula-1.13.1
pip install setuptools wheel numpy Cython
python build.py
pip install dist/pyhula-1.13.1-*.whl
python test_installation.py
```

## Quick Installation (Pre-built Wheel)

If you have a pre-built wheel file:

```bash
# Install dependencies first
pip install numpy opencv-python pyserial pymavlink scipy

# Install PyHula
pip install pyhula-1.13.1-cp313-cp313-win_amd64.whl

# Test
python -c "import pyhula; print('PyHula installed successfully!')"
```

## Troubleshooting

### Common Issues

1. **"Microsoft Visual C++ 14.0 is required"** (Windows)
   - Install Visual Studio Build Tools 2022
   - Or install Visual Studio Community 2022

2. **"Python.h: No such file or directory"** (Linux)
   - Install python3-dev: `sudo apt-get install python3-dev`

3. **"command 'gcc' failed"** (macOS)
   - Install Xcode Command Line Tools: `xcode-select --install`

4. **ImportError: No module named 'cv2'**
   - Install OpenCV: `pip install opencv-python`

5. **ImportError: No module named 'pymavlink'**
   - Install PyMAVLink: `pip install pymavlink`

### Build Environment Variables

For advanced users, you can set these environment variables:

```bash
rm -rf build/ dist/ *.egg-info/
python build.py
```

## Advanced Build Configuration

**Windows:**
```cmd
set DISTUTILS_USE_SDK=1
set MSSdk=1
```

**Linux/macOS:**
```bash
export CC=gcc
export CXX=g++
```

## Python Version Compatibility

I've tested PyHula thoroughly with these Python versions:

| Python Version | Supported | Notes |
|----------------|-----------|-------|
| >3.6 | Not tested | /// |
| 3.6 | Supported | Supported by original PyHula |
| 3.8 | Supported | Not tested |
| 3.9 | Supported | Not tested |
| 3.10 | Supported | Not tested |
| 3.11 | Supported | Not tested |
| 3.12 | Supported | Not tested |
| 3.13 | Supported | Latest tested |

## Files in this Package

- `setup.py` - Main build configuration
- `build.py` - Automated build script  
- `test_installation.py` - Installation test script
- `requirements.txt` - Dependencies list
- `README.md` - Comprehensive documentation
- `LICENSE` - MIT License
- `PKG-INFO` - Package metadata
- `src/` - All the source code
  - `pyhula/` - Main Python package
    - `pypack/` - Core functionality
      - `fylo/` - Flight control modules (C extensions)
      - `system/` - System modules (C extensions)
    - `f09-lite-trans/` - FFmpeg libraries for video processing

## Getting Help

If you run into issues that aren't covered here:

1. Check the troubleshooting section above first
2. Run `python test_installation.py` to get detailed diagnostic info
3. Look at the GitHub issues page to see if someone else had the same problem
4. Make sure all the dependencies are properly installed

