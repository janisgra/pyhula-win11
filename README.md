# PyHula Python 3.13 Port

A modernized port of the PyHula drone control library from Python 3.6 to Python 3.13+.

## Project Status

- **Import**: Working - Library can be imported successfully
- **Connection**: Working - Can establish connection to drone  
- **API Commands**: Not working - Flight commands hang or fail
- **Target**: Full functionality restoration for Python 3.13+

## Quick Start

```bash
cd pyhula-1.13.1
python setup.py build_ext --inplace
python -m tests.test_installation
```

## Repository Structure

```
pyhula-win11/
├── pyhula-1.13.1/           # Main development version (Python 3.13 port)
│   ├── src/pyhula/          # Core library source code
│   ├── setup.py             # Package build configuration  
│   ├── build.py             # Build automation
│   ├── tests/               # Test files and examples
│   ├── experimental/        # Fix attempts and prototypes
│   ├── debug/               # Diagnostic and analysis tools
│   ├── docs/                # Documentation
│   └── README.md            # Detailed documentation
├── pyhula-1.1.4/            # Original Python 3.6 version (reference)
└── README.md                # This file
```

## Development Focus

The main issue is that while the library imports and connects successfully, the API commands for drone control (takeoff, landing, movement) do not execute properly. This appears to be related to changes in Python's socket handling and threading between versions 3.6 and 3.13.

## Key Files

- `pyhula-1.13.1/src/pyhula/` - Main library code
- `pyhula-1.13.1/setup.py` - Build configuration
- `pyhula-1.13.1/tests/test_installation.py` - Basic functionality test
- `pyhula-1.13.1/PYTHON_313_COMPATIBILITY_GUIDE.md` - Porting notes

## Contributing

Focus development on the `pyhula-1.13.1/` directory. The other folders contain reference materials and archived attempts.


## Submodules

We pull in [pyhula-install-wrapper](https://github.com/janisgra/pyhula-install-wrapper.git) as a Git submodule under `submoduls/` so its code stays separate and easy to update.

### 1. Adding the Submodule

Run this once (or skip if it’s already there):

```bash

git config -f .gitmodules submodule.submoduls/pyhula-install-wrapper.branch master
git add .gitmodules submoduls/pyhula-install-wrapper
git commit -m "Add pyhula-install-wrapper submodule"
```

### 2. Cloning the Repo (with Submodules)

After you git clone the main repo, initialize and fetch submodules in one go:
```bash
git submodule update --init --recursive
```

### 3. Pulling In Upstream Updates

Whenever `pyhula-install-wrapper` sees new commits, run:
```bash
git submodule update --remote --merge
git add submoduls/pyhula-install-wrapper
git commit -m "Update pyhula-install-wrapper to latest"
```

*Optional:* set an alias in your `~/.gitconfig` for one-liner updates:

```ini
[alias]
  smu = "!git submodule update --init --remote --merge && git add . && git commit -m 'Update submodules'"
```

# PyHula Win11 Project Structure

This repository contains a comprehensive collection of tools and analysis for the PyHula drone control library.

## Directory Structure

```
pyhula-win11/
├── cpp-mavlink-controller/          # C++ MAVLink drone controller
│   ├── src/                         # C++ source files
│   ├── include/                     # MAVLink headers
│   ├── build/                       # Build directory (created by cmake)
│   ├── wiresharkdump/              # Network captures for analysis
│   └── CMakeLists.txt              # Build configuration
├── reverse-engineering/             # Reverse engineering analysis
│   ├── pyhula-wheel-analysis/      # Decompiled PyHula wheel contents
│   └── ghidra-decompiled/          # Ghidra analysis results
├── pyhula-1.1.4/                  # PyHula source package
├── pyhula-1.13.1/                 # Enhanced PyHula version
├── submoduls/                      # Git submodules
│   └── pyhula-install-wrapper/     # Installation utilities
├── wiresharkRec/                   # Additional network recordings
├── build-cpp-controller.ps1       # Build script for C++ controller
└── PROJECT_STRUCTURE.md           # This file
```

## Quick Start

### 1. Build C++ Controller
```powershell
.\build-cpp-controller.ps1
```

### 2. Install PyHula Environment
```powershell
cd submoduls\pyhula-install-wrapper
.\INSTALL_PYHULA.bat
```

### 3. Run Network Analysis
```powershell
cd cpp-mavlink-controller\build
.\bin\raw-analyzer.exe
```

## Components

### C++ MAVLink Controller
- **Purpose**: Direct MAVLink communication with drone
- **Features**: TCP connection, message parsing, command sending
- **Build**: Uses CMake, compatible with Windows
- **Tools**: Message analyzer, working replayer, connection tester

### PyHula Analysis
- **Wheel Analysis**: Decompiled Python wheel for protocol understanding
- **Ghidra Results**: Reverse engineered binary analysis
- **Network Captures**: Wireshark recordings of successful drone operations

### Installation Wrapper
- **Submodule**: Automated PyHula environment setup
- **Features**: Python 3.6 installation, virtual environment, examples
- **Target**: Students and educational use

## Development Workflow

### Protocol Analysis
1. Use Wireshark captures in `cpp-mavlink-controller/wiresharkdump/`
2. Analyze with `raw-analyzer.exe`
3. Compare with PyHula wheel analysis in `reverse-engineering/`
4. Test protocols with `working-replayer.exe`

### Code Development
1. Modify C++ sources in `cpp-mavlink-controller/src/`
2. Build with `.\build-cpp-controller.ps1`
3. Test with drone using built executables
4. Document findings in network captures

### Integration Testing
1. Use PyHula environment from submodule
2. Compare C++ implementation with Python behavior
3. Validate protocol compatibility

## Git Submodules

This repository uses Git submodules for modular development:

```bash
# Initialize submodules (after clone)
git submodule update --init --recursive

# Update submodules
git submodule update --remote --merge
git add submoduls/pyhula-install-wrapper
git commit -m "Update pyhula-install-wrapper to latest"
```

