#!/usr/bin/env python3
"""
PyHula Quick Setup Script

This script installs dependencies and PyHula only if needed,
without forcing reinstallation of existing working components.
"""

import subprocess
import sys
import os
import importlib

def check_pyhula_installation():
    """Check if PyHula is properly installed and working"""
    try:
        import pyhula
        api = pyhula.UserApi()
        print("[OK] PyHula is already installed and working!")
        if hasattr(pyhula, '__version__'):
            print(f"[OK] PyHula version: {pyhula.__version__}")
        return True
    except ImportError:
        print("[INFO] PyHula is not installed")
        return False
    except Exception as e:
        print(f"[WARNING] PyHula is installed but has issues: {e}")
        return False

def run_dependency_installer():
    """Run the dependency installer"""
    # Go up one directory to find install_dependencies subfolder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    installer_path = os.path.join(parent_dir, "install_dependencies", "install_dependencies.py")
    
    if not os.path.exists(installer_path):
        print("[ERROR] install_dependencies.py not found")
        return False
        
    print("Running dependency installer...")
    result = subprocess.run([sys.executable, installer_path], 
                          capture_output=False, text=True)
    return result.returncode == 0

def install_pyhula_if_needed():
    """Install PyHula only if it's not already working"""
    if check_pyhula_installation():
        return True
        
    print("\nPyHula needs to be installed...")
    
    # Go up one directory to access parent project files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    dist_dir = os.path.join(parent_dir, "dist")
    
    if os.path.exists(dist_dir):
        wheel_files = [f for f in os.listdir(dist_dir) if f.endswith('.whl')]
        if wheel_files:
            wheel_path = os.path.join(dist_dir, wheel_files[-1])
            print(f"Installing existing wheel: {wheel_files[-1]}")
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", wheel_path
                ], capture_output=True, text=True, check=True)
                
                print("[OK] PyHula installed from existing wheel")
                return check_pyhula_installation()
            except subprocess.CalledProcessError as e:
                print(f"[WARNING] Failed to install from wheel: {e}")
    
    # If no wheel or wheel installation failed, build from source
    print("Building PyHula from source...")
    setup_py = os.path.join(parent_dir, "setup.py")
    if not os.path.exists(setup_py):
        print("[ERROR] setup.py not found - cannot build PyHula")
        return False
    
    try:
        # Build wheel (run from parent directory)
        subprocess.run([
            sys.executable, "setup.py", "bdist_wheel"
        ], check=True, capture_output=True, text=True, cwd=parent_dir)
        
        # Install the newly built wheel
        wheel_files = [f for f in os.listdir(dist_dir) if f.endswith('.whl')]
        if wheel_files:
            wheel_path = os.path.join(dist_dir, wheel_files[-1])
            subprocess.run([
                sys.executable, "-m", "pip", "install", wheel_path
            ], check=True, capture_output=True, text=True)
            
            print("[OK] PyHula built and installed successfully")
            return check_pyhula_installation()
        else:
            print("[ERROR] No wheel file created during build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to build/install PyHula: {e}")
        return False

def main():
    """Main function"""
    print("PyHula Quick Setup")
    print("=" * 30)
    print("This script installs only what's needed without disrupting existing packages.")
    print("=" * 30)
    
    # Check Python version
    version = sys.version_info
    if not (version.major == 3 and version.minor >= 8):
        print(f"[ERROR] Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("PyHula requires Python 3.8 or higher")
        return 1
    
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro} is compatible")
    
    # Install dependencies (only missing ones)
    if not run_dependency_installer():
        print("[ERROR] Dependency installation failed")
        return 1
    
    # Install PyHula if needed
    if not install_pyhula_if_needed():
        print("[ERROR] PyHula installation failed")
        return 1
    
    # Final test
    if check_pyhula_installation():
        print("\n" + "=" * 40)
        print("SUCCESS! PyHula is ready to use!")
        print("=" * 40)
        print("\nYou can now:")
        print("• Run 'python pyhula_import.py' to test drone operations")
        print("• Run 'python test_installation.py' for comprehensive testing")
        print("• Import pyhula in your own Python scripts")
        return 0
    else:
        print("\n" + "=" * 40)
        print("ERROR! PyHula installation test failed")
        print("=" * 40)
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[INFO] Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
