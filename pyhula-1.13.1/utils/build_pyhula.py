#!/usr/bin/env python3
"""
Simple build script for PyHula - Python 3.13 Version
Handles the common build tasks with proper commands using Python 3.13
"""

import sys
import subprocess
import os
import shutil

# Force Python 3.13 usage
PYTHON_CMD = 'py'
PYTHON_ARGS = ['-3.13']

def get_python_cmd():
    """Get the correct Python 3.13 command"""
    # Try py -3.13 first (Windows)
    try:
        result = subprocess.run([PYTHON_CMD] + PYTHON_ARGS + ['--version'], 
                              capture_output=True, text=True, check=True)
        if '3.13' in result.stdout:
            return [PYTHON_CMD] + PYTHON_ARGS
    except:
        pass
    
    # Try python3.13 direct
    try:
        result = subprocess.run(['python3.13', '--version'], 
                              capture_output=True, text=True, check=True)
        if '3.13' in result.stdout:
            return ['python3.13']
    except:
        pass
    
    print("ERROR: Python 3.13 not found!")
    print("Please install Python 3.13 or ensure it's available as 'py -3.13'")
    return None

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n=== {description} ===")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("SUCCESS")
        if result.stdout:
            # Only show important output, not the verbose scanning
            lines = result.stdout.split('\n')
            important_lines = [line for line in lines if not line.strip().startswith('Found:') and not line.strip().startswith('Scanning')]
            if important_lines:
                print("Output:", '\n'.join(important_lines[:10]))  # Show first 10 important lines
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: {e}")
        if e.stdout:
            print("Stdout:", e.stdout)
        if e.stderr:
            print("Stderr:", e.stderr)
        return False

def main():
    """Main build process"""
    print("PyHula Build Script - Python 3.13")
    print("=" * 50)
    
    # Get correct Python command
    python_cmd = get_python_cmd()
    if not python_cmd:
        return False
    
    print(f"Using Python command: {' '.join(python_cmd)}")
    
    # Check if we're in the right directory
    if not os.path.exists('setup.py'):
        print("ERROR: setup.py not found. Run this script from the pyhula-1.13.1 directory.")
        return False
    
    # Uninstall old versions first
    print("\nUninstalling old PyHula versions...")
    run_command(python_cmd + ['-m', 'pip', 'uninstall', 'pyhula', '-y'], 
                "Uninstalling old PyHula")
    
    # Check and install wheel if needed
    print("\nChecking for wheel package...")
    try:
        result = subprocess.run(python_cmd + ['-c', 'import wheel'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Wheel package found")
        else:
            raise ImportError()
    except:
        print("Installing wheel package...")
        if not run_command(python_cmd + ['-m', 'pip', 'install', 'wheel'], 
                          "Installing wheel"):
            print("WARNING: Could not install wheel, skipping wheel build")
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}")
            try:
                # Try multiple methods to remove stubborn directories
                if os.name == 'nt':  # Windows
                    subprocess.run(['rmdir', '/s', '/q', dir_name], shell=True, check=False)
                else:
                    shutil.rmtree(dir_name)
            except Exception as e:
                print(f"Warning: Could not remove {dir_name}: {e}")
                print("Continuing anyway...")
    
    # Remove egg-info directories
    for item in os.listdir('.'):
        if item.endswith('.egg-info') and os.path.isdir(item):
            print(f"Removing {item}")
            try:
                if os.name == 'nt':  # Windows
                    subprocess.run(['rmdir', '/s', '/q', item], shell=True, check=False)
                else:
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Warning: Could not remove {item}: {e}")
    
    # Build C extensions in place
    if not run_command(python_cmd + ['setup.py', 'build_ext', '--inplace'], 
                      "Building C extensions"):
        return False
    
    # Build source distribution
    if not run_command(python_cmd + ['setup.py', 'sdist'], 
                      "Building source distribution"):
        return False
    
    # Try to build wheel if wheel package is available
    try:
        result = subprocess.run(python_cmd + ['-c', 'import wheel'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            if not run_command(python_cmd + ['setup.py', 'bdist_wheel'], 
                              "Building wheel"):
                print("WARNING: Wheel build failed, but source distribution was created")
        else:
            raise ImportError()
    except:
        print("SKIPPED: Wheel build (wheel package not available)")
    
    print("\n" + "=" * 50)
    print("Build completed!")
    print("\nFiles created in dist/:")
    if os.path.exists('dist'):
        for file in os.listdir('dist'):
            print(f"  {file}")
    
    print(f"\nTo install:")
    print(f"  {' '.join(python_cmd)} -m pip install dist/pyhula-1.13.1.tar.gz")
    print("  or")
    print(f"  {' '.join(python_cmd)} -m pip install dist/pyhula-1.13.1-*.whl  (if wheel was built)")
    print(f"\nTo test installation:")
    print(f"  {' '.join(python_cmd)} diagnostic.py")
    print(f"  {' '.join(python_cmd)} simple_test.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
