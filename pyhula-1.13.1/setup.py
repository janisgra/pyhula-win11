#!/usr/bin/env python3
"""
PyHula setup.py - Python 3.8+ compatible version
Ported to support Python 3.13+ and modern build tools

Original library by HighGreat
Python 3.13+ port

Build instructions:
    python setup.py build_ext --inplace
    python setup.py bdist_wheel

Install instructions:
    pip install dist/pyhula-1.13.1-cp313-cp313-win_amd64.whl
"""

import os
import sys
from pathlib import Path
from setuptools import setup, Extension, find_packages

# Package metadata
name = 'pyhula'
version = '1.13.1'  # Version indicating Python 3.13+ compatibility
description = "PyHula - Hula drone control library (Python 3.8+ compatible)"
long_description = """
PyHula - Python 3.8+ Compatible Drone Control Library

This is a modernized version of the PyHula library, originally designed for Python 3.6,
now fully compatible with Python 3.8 through Python 3.13+ and future versions.

Features:
- Drone flight control and command processing
- MAVLink communication protocol support
- Formation flying capabilities
- LED control and visual effects
- Real-time data processing
- Cross-platform compatibility (Windows, Linux)

Requirements:
- Python 3.8 or higher
- OpenCV (cv2)
- NumPy
- PySerial
- PyMAVLink
- SciPy

This port maintains full API compatibility with the original library while
adding support for modern Python versions and improved build systems.
"""

author = 'HighGreat'
author_email = 'highgreat@hg-fly.com'

def find_c_files():
    """Find C source files with robust path handling"""
    project_root = Path(__file__).parent.absolute()
    src_dir = project_root / 'src'
    
    if not src_dir.exists():
        print(f"WARNING: Source directory not found: {src_dir}")
        return []
    
    c_extensions = []
    
    # Use pathlib for robust cross-platform path handling
    module_mappings = {
        src_dir / 'pyhula/pypack/fylo/commandprocessor.c': 'pyhula.pypack.fylo.commandprocessor',
        src_dir / 'pyhula/pypack/fylo/config.c': 'pyhula.pypack.fylo.config',
        src_dir / 'pyhula/pypack/fylo/controlserver.c': 'pyhula.pypack.fylo.controlserver',
        src_dir / 'pyhula/pypack/fylo/mavanalyzer.c': 'pyhula.pypack.fylo.mavanalyzer',
        src_dir / 'pyhula/pypack/fylo/mavlink.c': 'pyhula.pypack.fylo.mavlink',
        src_dir / 'pyhula/pypack/fylo/msganalyzer.c': 'pyhula.pypack.fylo.msganalyzer',
        src_dir / 'pyhula/pypack/fylo/stateprocessor.c': 'pyhula.pypack.fylo.stateprocessor',
        src_dir / 'pyhula/pypack/fylo/taskprocessor.c': 'pyhula.pypack.fylo.taskprocessor',
        src_dir / 'pyhula/pypack/fylo/uwb.c': 'pyhula.pypack.fylo.uwb',
        
        src_dir / 'pyhula/pypack/system/buffer.c': 'pyhula.pypack.system.buffer',
        src_dir / 'pyhula/pypack/system/command.c': 'pyhula.pypack.system.command',
        src_dir / 'pyhula/pypack/system/communicationcontroller.c': 'pyhula.pypack.system.communicationcontroller',
        src_dir / 'pyhula/pypack/system/communicationcontrollerfactory.c': 'pyhula.pypack.system.communicationcontrollerfactory',
        src_dir / 'pyhula/pypack/system/dancecontroller.c': 'pyhula.pypack.system.dancecontroller',
        src_dir / 'pyhula/pypack/system/dancefileanalyzer.c': 'pyhula.pypack.system.dancefileanalyzer',
        src_dir / 'pyhula/pypack/system/datacenter.c': 'pyhula.pypack.system.datacenter',
        src_dir / 'pyhula/pypack/system/event.c': 'pyhula.pypack.system.event',
        src_dir / 'pyhula/pypack/system/mavcrc.c': 'pyhula.pypack.system.mavcrc',
        src_dir / 'pyhula/pypack/system/network.c': 'pyhula.pypack.system.network',
        src_dir / 'pyhula/pypack/system/networkcontroller.c': 'pyhula.pypack.system.networkcontroller',
        src_dir / 'pyhula/pypack/system/serialcontroller.c': 'pyhula.pypack.system.serialcontroller',
        src_dir / 'pyhula/pypack/system/state.c': 'pyhula.pypack.system.state',
        src_dir / 'pyhula/pypack/system/system.c': 'pyhula.pypack.system.system',
        src_dir / 'pyhula/pypack/system/taskcontroller.c': 'pyhula.pypack.system.taskcontroller',
    }
    
    print(f"Scanning for C source files in: {src_dir}")
    found_count = 0
    missing_count = 0
    
    for c_file_path, module_name in module_mappings.items():
        if c_file_path.exists():
            found_count += 1
            print(f" Found: {module_name}")
            ext = Extension(
                module_name,
                [str(c_file_path)],  # Convert Path to string for setuptools
                include_dirs=[str(src_dir)],  # Use absolute path
                # Python 3.13+ compatibility defines
                define_macros=[
                    ('PY_SSIZE_T_CLEAN', None),  # Required for Python 3.13+
                    ('CYTHON_USE_DICT_VERSIONS', '0'),  # Compatibility with older Cython
                ],
                # Compiler optimization flags
                extra_compile_args=['/O2'] if sys.platform == 'win32' else ['-O2'],
                # Linker flags for better compatibility
                extra_link_args=[] if sys.platform == 'win32' else ['-Wl,--strip-all'],
            )
            c_extensions.append(ext)
        else:
            missing_count += 1
            print(f" Missing: {c_file_path}")
    
    print(f"C source file summary: {found_count} found, {missing_count} missing")
    return c_extensions

def get_existing_data_files():
    """Get data files with robust path handling"""
    project_root = Path(__file__).parent.absolute()
    data_files = []
    
    # Check for dance files
    dance_files = []
    dance_dir = project_root / 'src/pyhula/pypack/system/dance'
    if dance_dir.exists():
        for file_path in dance_dir.glob('*.matxt'):
            dance_files.append(str(file_path))
        print(f"Found {len(dance_files)} dance files")
    
    if dance_files:
        data_files.append(('Lib/site-packages/pyhula/pypack/system/dance', dance_files))
    
    # Check for ini files
    ini_files = []
    ini_candidates = [
        project_root / 'src/pyhula/pypack/log.ini',
        project_root / 'src/pyhula/pypack/version.ini'
    ]
    
    for ini_file in ini_candidates:
        if ini_file.exists():
            ini_files.append(str(ini_file))
    
    if ini_files:
        data_files.append(('Lib/site-packages/pyhula/pypack', ini_files))
    
    print(f"Found {len(data_files)} data file groups")
    return data_files

# Updated classifiers for modern Python versions (removed deprecated License classifier)
classifiers = [
    "Intended Audience :: Education",
    "Intended Audience :: Developers", 
    "Intended Audience :: Science/Research",
    "Development Status :: 4 - Beta",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9", 
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: C",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Hardware :: Hardware Drivers",
]

# Define dependencies
install_requires = [
    'numpy>=1.19.0',
    'opencv-python>=4.5.0',
    'pyserial>=3.4',
    'pymavlink>=2.4.0',
    'scipy>=1.6.0',
]

# Optional dependencies for development and extended features
extras_require = {
    'dev': [
        'pytest>=6.0',
        'pytest-cov>=2.10',
        'black>=21.0',
        'flake8>=3.8',
    ],
    'visualization': [
        'matplotlib>=3.3.0',
        'pillow>=8.0.0',
    ],
    'docs': [
        'sphinx>=3.0.0',
        'sphinx-rtd-theme>=0.5.0',
    ],
    'all': [
        'pytest>=6.0',
        'pytest-cov>=2.10', 
        'matplotlib>=3.3.0',
        'pillow>=8.0.0',
        'sphinx>=3.0.0',
        'sphinx-rtd-theme>=0.5.0',
    ]
}

# Read requirements from file if it exists
project_root = Path(__file__).parent.absolute()
try:
    requirements_file = project_root / "docs/requirements.txt"
    if requirements_file.exists():
        with open(requirements_file, "r", encoding="utf-8") as f:
            file_requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')] 
            # Merge with default requirements, preferring file versions
            install_requires.extend([req for req in file_requirements if req not in install_requires])
except FileNotFoundError:
    print("No docs/requirements.txt found, using default dependencies")

# Read long description from README
long_description_content_type = 'text/markdown'
readme_candidates = [project_root / 'README.md', project_root / 'README.rst']
for readme_file in readme_candidates:
    try:
        with open(readme_file, encoding='utf-8') as f:
            long_description = f.read()
            if readme_file.suffix == '.rst':
                long_description_content_type = 'text/x-rst'
            break
    except FileNotFoundError:
        continue
else:
    long_description = description  # Fallback to short description

# Find packages automatically
packages = find_packages(where='src')
package_dir = {'': 'src'}

print(f"Found packages: {packages}")
print(f"Package directory: {package_dir}")

# Create C extensions
ext_modules = find_c_files()
print(f"Created {len(ext_modules)} C extensions")

# Print Python version info
print(f"Building for Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print(f"Platform: {sys.platform}")

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    license='MIT',  # SPDX license expression
    author=author,
    author_email=author_email,
    url='https://github.com/janisgra/pyhula-win11',
    project_urls={
        'Bug Reports': 'https://github.com/janisgra/pyhula-win11/issues',
        'Source': 'https://github.com/janisgra/pyhula-win11',
        'Documentation': 'https://github.com/janisgra/pyhula-win11/blob/main/README.md',
    },
    packages=packages,
    package_dir=package_dir,
    ext_modules=ext_modules,
    data_files=get_existing_data_files(),
    install_requires=install_requires,
    extras_require=extras_require,
    package_data={
        'pyhula': ['f09-lite-trans/*'],
        '': ['utils/*.py'] if (Path(__file__).parent / 'utils').exists() else [],  # Include utils if exists
    },
    # Include pyhula_py313.py as a standalone module if it exists
    py_modules=['pyhula_py313'] if (Path(__file__).parent / 'pyhula_py313.py').exists() else [],
    python_requires='>=3.8',
    classifiers=classifiers,
    zip_safe=False,
    # setuptools configuration
    options={
        'build_ext': {
            'include_dirs': [str(Path(__file__).parent / 'src')],  # Use absolute path
        },
        'bdist_wheel': {
            'universal': False,  # Platform-specific wheel due to C extensions
        }
    },
    # Entry points for command-line tools (if any)
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here if needed
            # 'pyhula-cli=pyhula.cli:main',
        ],
    },
)
