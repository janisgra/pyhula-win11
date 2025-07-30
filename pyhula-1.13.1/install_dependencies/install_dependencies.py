#!/usr/bin/env python3
"""
PyHula Dependency Installer

Installs required dependencies for PyHula.
Checks existing packages to avoid unnecessary reinstalls.
"""

import subprocess
import sys
import importlib
import os

def check_pip():
    """Check if pip is available"""
    try:
        import pip
        return True
    except ImportError:
        print("Error: pip is not installed. Please install pip first.")
        return False

def is_package_installed(package_name):
    """Check if a package is already installed"""
    try:
        # Handle special cases for package names vs import names
        import_name = package_name
        if package_name == 'opencv-python':
            import_name = 'cv2'
        elif package_name == 'pillow':
            import_name = 'PIL'
        elif package_name == 'pyserial':
            import_name = 'serial'
        
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def install_package(package):
    """Install a single package using pip"""
    try:
        print(f"Installing {package}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package
        ], capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            print(f"Successfully installed {package}")
            return True
        else:
            print(f"Failed to install {package}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error installing {package}: {e}")
        return False

def upgrade_pip():
    """Upgrade pip to latest version"""
    try:
        print("Upgrading pip...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], capture_output=True, text=True, check=True)
        print("pip upgraded successfully")
        return True
    except:
        print("Warning: Could not upgrade pip, continuing with current version")
        return False

def install_dependencies():
    """Install all PyHula dependencies"""
    print("PyHula Dependency Installer")
    print("=" * 40)
    
    if not check_pip():
        return False
    
    upgrade_pip()
    
    # Core dependencies
    core_deps = [
        "numpy>=1.19.0",
        "opencv-python>=4.5.0", 
        "pyserial>=3.4",
        "pymavlink>=2.4.0",
        "scipy>=1.6.0",
        "psutil>=5.7.0"
    ]
    
    # Optional dependencies
    optional_deps = [
        "matplotlib>=3.3.0",
        "pillow>=8.0.0"
    ]
    
    print("\nChecking core dependencies...")
    core_success = 0
    for package in core_deps:
        package_name = package.split(">=")[0].split("==")[0]
        
        if is_package_installed(package_name):
            print(f"{package_name} - already installed")
            core_success += 1
        else:
            if install_package(package):
                core_success += 1
    
    print(f"\nCore dependencies: {core_success}/{len(core_deps)} installed")
    
    print("\nChecking optional dependencies...")
    optional_success = 0
    for package in optional_deps:
        package_name = package.split(">=")[0].split("==")[0]
        
        if is_package_installed(package_name):
            print(f"{package_name} - already installed")
            optional_success += 1
        else:
            if install_package(package):
                optional_success += 1
    
    print(f"Optional dependencies: {optional_success}/{len(optional_deps)} installed")
    
    print("\n" + "=" * 40)
    print("Installation Summary")
    print("=" * 40)
    print(f"Core: {core_success}/{len(core_deps)}")
    print(f"Optional: {optional_success}/{len(optional_deps)}")
    
    if core_success == len(core_deps):
        print("\nAll core dependencies installed successfully!")
        if optional_success == len(optional_deps):
            print("All optional dependencies also installed!")
        else:
            missing = len(optional_deps) - optional_success
            print(f"Warning: {missing} optional dependencies failed")
            print("PyHula will work but some features may be limited.")
        return True
    else:
        missing = len(core_deps) - core_success
        print(f"\nError: {missing} core dependencies failed to install")
        print("PyHula may not work correctly.")
        print("\nTroubleshooting steps:")
        print("1. Check internet connection")
        print("2. Try running as administrator")
        print("3. Install Visual Studio Build Tools (Windows)")
        print("4. Try manual installation:")
        for package in core_deps:
            package_name = package.split(">=")[0]
            if not is_package_installed(package_name):
                print(f"   pip install {package}")
        return False

def main():
    """Main function"""
    try:
        success = install_dependencies()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
