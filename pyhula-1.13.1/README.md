# PyHula - Python 3.8+ Compatible Drone Control Library

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org) [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](README.md)


<span style="color: red;">DISCLAIMER: PyHula and the original PyHula library are separate projects. This version is a modernized fork. We are not affiliated with the original authors. When in question, all rights belong to the original authors.</span>

## Overview

PyHula is a modernized Python library for controlling Hula drones, originally designed for Python 3.6 and now fully compatible with Python 3.8 through Python 3.13+ and future versions.

## Features

-  **Drone Flight Control**: Complete flight control API for takeoff, landing, and maneuvering
-  **MAVLink Communication**: Full MAVLink protocol support for robust drone communication
-  **Formation Flying**: Advanced algorithms for coordinated multi-drone operations
-  **LED Control**: RGB LED control for visual effects and status indication
-  **Real-time Data**: Live telemetry and sensor data processing
-  **Cross-platform**: Windows, Linux, and macOS support
-  **Modern Python**: Python 3.8+ compatibility with future-proof design

## Installation

### Quick Setup (Recommended - Safe)

For a conservative installation that only installs missing components:

**Windows:**
```cmd
cd setup_quick
setup_quick.bat
```

**Linux/macOS:**
```bash
cd setup_quick
chmod +x setup_quick.sh
./setup_quick.sh
```

**Any platform with Python:**
```bash
cd setup_quick
python setup_quick.py
```

### Complete Setup (Advanced Users)

For a complete one-click installation that builds from source:

**Windows:**
```cmd
# Complete rebuild (may reinstall dependencies)
cd setup_complete
setup_complete.bat
```

**Linux/macOS:**
```bash
cd setup_complete
chmod +x setup_complete.sh
./setup_complete.sh
```

**Cross-platform:**
```bash
# Complete setup including PyHula build
cd setup_complete
python setup_complete/setup_complete.py
```
```

### Manual Installation Options

#### Option 1: Dependencies Only

**Windows:**
```cmd
install_dependencies.bat
```

**Linux/macOS:**
```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

**Cross-platform:**
```bash
python install_dependencies/install_dependencies.py
```

#### Option 2: Build from Source
```bash
# Install with all dependencies
pip install pyhula[all]

# Install with visualization support
pip install pyhula[visualization]

# Install development dependencies
pip install pyhula[dev]
```

### Build from Source

```bash
# Clone the repository
git clone https://github.com/janisgra/pyhula-win11.git
cd pyhula-win11/pyhula-1.13.1

# Install dependencies
pip install -r requirements.txt

# Build the C extensions
python setup.py build_ext --inplace

# Create a wheel file
python setup.py bdist_wheel

# Install
pip install dist/pyhula-1.13.1-*.whl
```

## Quick Start

```python
import pyhula
from pyhula.pypack.fylo import commandprocessor, config, mavlink
from pyhula.pypack.system import buffer, command, datacenter, network

# Initialize drone communication
drone = commandprocessor.CommandProcessor()

# Take off
takeoff_cmd = commandprocessor.SFTakeoffCP()
drone.send_command(takeoff_cmd)

# LED control
led_cmd = commandprocessor.SFLamplight()
led_cmd.set_color(255, 0, 0)  # RGB values
drone.send_command(led_cmd)

# Landing
landing_cmd = commandprocessor.SFTouchdownCP()
drone.send_command(landing_cmd)
```

## API Documentation

### Core Modules

- **`pyhula.pypack.fylo.commandprocessor`**: Main command processing and drone control
- **`pyhula.pypack.fylo.mavlink`**: MAVLink protocol implementation
- **`pyhula.pypack.fylo.config`**: Configuration management
- **`pyhula.pypack.system.buffer`**: Data buffering and management
- **`pyhula.pypack.system.network`**: Network communication
- **`pyhula.pypack.system.datacenter`**: Central data processing

### Command Classes

- **`CommandProcessor`**: Main command interface
- **`SFTakeoffCP`**: Takeoff command
- **`SFTouchdownCP`**: Landing command
- **`SFLamplight`**: LED control
- **`SFForwardCP`**: Movement commands



## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Windows 10/11 |  Fully Supported | Primary development platform |
| Linux |  Supported | Ubuntu 20.04+ tested |
| macOS |  Experimental | Intel and Apple Silicon |

## Building for Different Platforms

### Windows
```bash
python setup.py build_ext --inplace
python setup.py bdist_wheel
```

### Linux
```bash
sudo apt-get install python3-dev build-essential
python setup.py build_ext --inplace
python setup.py bdist_wheel
```

### macOS
```bash
xcode-select --install
python setup.py build_ext --inplace
python setup.py bdist_wheel
```

## Changelog

### v1.13.1 (Python 3.13+ Compatible)
-  **BREAKING**: Dropped Python 3.6/3.7 support
-  **NEW**: Full Python 3.8-3.13+ compatibility
-  **FIXED**: Cython import compatibility issues
-  **FIXED**: Module name parsing corruption
-  **IMPROVED**: Modern setuptools configuration
-  **IMPROVED**: Better error handling and logging
-  **IMPROVED**: Cross-platform build support
-  **ADDED**: Comprehensive dependency management
-  **ADDED**: Development and testing tools

### v1.1.7 (Previous)
- Original Python 3.6 version with compatibility patches

### Version 1.1.4 (Legacy)
- Original HighGreat release

## Troubleshooting

### Common Issues

**"No module named 'cv2'"**
```bash
pip install opencv-python
```

2. **Import Error: No module named 'pymavlink'**
   ```bash
   pip install pymavlink
   ```

3. **Build Errors on Windows**
   - Install Visual Studio Build Tools 2022
   - Ensure Windows SDK is installed

4. **Build Errors on Linux**
   ```bash
   sudo apt-get install python3-dev build-essential
   ```



## Contributing

If you want to help improve PyHula:

1. Fork this repository
2. Create a branch for your feature
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **HighGreat**: Original PyHula library developers

## Original Library Information

This is a modernized version of the PyHula library originally created by HighGreat for Python 3.6. The original library has been ported to support modern Python versions while maintaining full API compatibility.

**Original Author**: HighGreat  
**Original Email**: highgreat@hg-fly.com 

---

**Note**: This library is designed for educational and development purposes. Always follow local regulations and safety guidelines when operating drones.
**Note**: The code was commented by GitHub Copilot. The print functions were partly written by Copilot. 

