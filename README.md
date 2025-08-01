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

