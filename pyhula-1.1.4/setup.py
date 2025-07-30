
#!/usr/bin/env python3
"""
Fixed setup.py for PyHula Python 3.13+ compatibility
"""

import os
import glob
from setuptools import setup, Extension, find_packages

name = 'pyhula'
version = '1.1.7'  # Bump version for Python 3.13 compatibility
description = "Hula package - Python 3.13+ compatible"
author = 'HighGreat'
author_email = 'highgreat@hg-fly.com'

def find_c_files():
    """Find all C source files and create proper module mappings"""
    c_extensions = []
    
    # Manually define the correct module mappings to avoid path parsing issues
    module_mappings = {
        './src/pyhula/pypack/fylo/commandprocessor.c': 'pyhula.pypack.fylo.commandprocessor',
        './src/pyhula/pypack/fylo/config.c': 'pyhula.pypack.fylo.config',
        './src/pyhula/pypack/fylo/controlserver.c': 'pyhula.pypack.fylo.controlserver',
        './src/pyhula/pypack/fylo/mavanalyzer.c': 'pyhula.pypack.fylo.mavanalyzer',
        './src/pyhula/pypack/fylo/mavlink.c': 'pyhula.pypack.fylo.mavlink',
        './src/pyhula/pypack/fylo/msganalyzer.c': 'pyhula.pypack.fylo.msganalyzer',
        './src/pyhula/pypack/fylo/stateprocessor.c': 'pyhula.pypack.fylo.stateprocessor',
        './src/pyhula/pypack/fylo/taskprocessor.c': 'pyhula.pypack.fylo.taskprocessor',
        './src/pyhula/pypack/fylo/uwb.c': 'pyhula.pypack.fylo.uwb',
        
        './src/pyhula/pypack/system/buffer.c': 'pyhula.pypack.system.buffer',
        './src/pyhula/pypack/system/command.c': 'pyhula.pypack.system.command',
        './src/pyhula/pypack/system/communicationcontroller.c': 'pyhula.pypack.system.communicationcontroller',
        './src/pyhula/pypack/system/communicationcontrollerfactory.c': 'pyhula.pypack.system.communicationcontrollerfactory',
        './src/pyhula/pypack/system/dancecontroller.c': 'pyhula.pypack.system.dancecontroller',
        './src/pyhula/pypack/system/dancefileanalyzer.c': 'pyhula.pypack.system.dancefileanalyzer',
        './src/pyhula/pypack/system/datacenter.c': 'pyhula.pypack.system.datacenter',
        './src/pyhula/pypack/system/event.c': 'pyhula.pypack.system.event',
        './src/pyhula/pypack/system/mavcrc.c': 'pyhula.pypack.system.mavcrc',
        './src/pyhula/pypack/system/network.c': 'pyhula.pypack.system.network',
        './src/pyhula/pypack/system/networkcontroller.c': 'pyhula.pypack.system.networkcontroller',
        './src/pyhula/pypack/system/serialcontroller.c': 'pyhula.pypack.system.serialcontroller',
        './src/pyhula/pypack/system/state.c': 'pyhula.pypack.system.state',
        './src/pyhula/pypack/system/system.c': 'pyhula.pypack.system.system',
        './src/pyhula/pypack/system/taskcontroller.c': 'pyhula.pypack.system.taskcontroller',
    }
    
    for c_file, module_name in module_mappings.items():
        if os.path.exists(c_file):
            print(f"✅ Found: {module_name} -> {c_file}")
            ext = Extension(
                module_name,
                [c_file],
                include_dirs=['./src'],
                define_macros=[('PY_SSIZE_T_CLEAN', None)],  # For Python 3.13 compatibility
            )
            c_extensions.append(ext)
        else:
            print(f"❌ Missing: {c_file}")
    
    return c_extensions

# Only include data files that actually exist
def get_existing_data_files():
    data_files = []
    
    # Check for dance files
    dance_files = []
    dance_dir = 'src/pyhula/pypack/system/dance'
    if os.path.exists(dance_dir):
        for file in os.listdir(dance_dir):
            if file.endswith('.matxt'):
                dance_files.append(os.path.join(dance_dir, file))
    
    if dance_files:
        data_files.append(('Lib/site-packages/pyhula/pypack/system/dance', dance_files))
    
    # Check for ini files
    ini_files = []
    for ini_file in ['src/pyhula/pypack/log.ini', 'src/pyhula/pypack/version.ini']:
        if os.path.exists(ini_file):
            ini_files.append(ini_file)
    
    if ini_files:
        data_files.append(('Lib/site-packages/pyhula/pypack', ini_files))
    
    return data_files

# Updated classifiers for modern Python
classifiers = [
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
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
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

# Read requirements
try:
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    requirements = []

# Read readme
try:
    with open('./README.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    try:
        with open('./readmewhl.md', encoding='utf-8') as f:
            long_description = f.read()
    except FileNotFoundError:
        long_description = description

# Find packages
packages = find_packages(where='src')
package_dir = {'': 'src'}

print(f"Found packages: {packages}")
print(f"Package directory: {package_dir}")

# Create extensions
ext_modules = find_c_files()
print(f"Created {len(ext_modules)} extensions")

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=author,
    author_email=author_email,
    packages=packages,
    package_dir=package_dir,
    ext_modules=ext_modules,
    data_files=get_existing_data_files(),
    install_requires=requirements,
    package_data={'pyhula': ['f09-lite-trans/*']},
    python_requires='>=3.8',  # Modern Python versions
    classifiers=classifiers,
    zip_safe=False,
    # Modern setuptools configuration
    options={
        'build_ext': {
            'include_dirs': ['./src'],
        }
    },
)
