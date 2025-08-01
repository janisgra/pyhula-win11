# PyHula Build System

## Overview
Single build script (`build_complete.py`) handles complete PyHula setup: dependencies, build, install, and test.

## Version
- **PyHula Version**: 1.13.1
- **Python Support**: 3.8 - 3.13+
- **Platform**: Windows (with Visual Studio 2022)

## Usage

### Complete Build and Setup
```cmd
py -3.13 build_complete.py complete
```
Runs: build → install → test connection

### Individual Commands
```cmd
py -3.13 build_complete.py         # Build only
py -3.13 build_complete.py install # Install and test import
py -3.13 build_complete.py test    # Test drone connection
```

## Features

### Automatic Path Length Handling
- Builds in short temporary path (`c:\temp\pyhula`) to avoid Windows 260-character limit
- Copies results back to original location
- No manual intervention required

### Complete Dependency Management
- Installs: setuptools, wheel, numpy, opencv-python, pyserial, pymavlink, scipy
- Uninstalls old versions automatically
- Handles version conflicts

### Build Process
1. **Dependencies**: Install/verify build and runtime dependencies
2. **Build**: Compile 24 C extensions for Python 3.13
3. **Package**: Create source distribution (.tar.gz) and wheel (.whl)
4. **Install**: Clean install with dependency resolution
5. **Verify**: Test PyHula import and UserApi availability
6. **Test**: Attempt drone connection via api.connect()

## Output Files
```
dist/
├── pyhula-1.13.1-cp313-cp313-win_amd64.whl  (36.2 MB)
└── pyhula-1.13.1.tar.gz                     (34.6 MB)
```

## Integration Features

### Python 3.13 Compatibility
- Automatic integration of `pyhula_py313.py` if available
- Includes `utils/python313_compat.py` compatibility patches
- Version management via `__version__` attribute

### Robust Error Handling
- Windows file locking protection
- Path length issue detection
- Build error diagnosis
- Comprehensive logging

## System Requirements
- **Python**: 3.8+ (optimized for 3.13)
- **Compiler**: Visual Studio 2022 with C++ tools
- **Memory**: 2GB+ during build
- **Disk**: 500MB for build artifacts

## Notes
- **Emoji-free**: All code and output text without emojis per requirements
- **Single file**: Only `build_complete.py` needed in project root
- **Cross-platform paths**: Uses pathlib.Path for compatibility
- **Clean builds**: Automatic cleanup of temporary files

## Connection Testing
The drone connection test requires:
- Hula drone powered on
- WLAN connection to drone network
- No firewall blocking connection
- `api.connect()` returns `True` for success

Connection failure is normal if drone not connected but does not indicate build issues.
