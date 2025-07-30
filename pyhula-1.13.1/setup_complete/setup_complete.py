#!/usr/bin/env python3
"""
Complete PyHula Setup Script

This script installs all dependencies AND builds/installs PyHula itself.
It's a complete one-stop solution for PyHula installation.
"""

import subprocess
import sys
import os
import importlib
import shutil

def run_command(cmd, description, check=True):
    """Run a command and handle output"""
    print(f"\n{description}...")
    print("=" * len(description))
    
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, check=check, text=True)
        else:
            result = subprocess.run(cmd, check=check, text=True)
        
        if result.returncode == 0:
            print(f"[OK] {description} completed successfully")
            return True
        else:
            print(f"[ERROR] {description} failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed with error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error during {description}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"[OK] Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"[ERROR] Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("PyHula requires Python 3.8 or higher")
        return False

def install_build_tools():
    """Install required build tools"""
    print("\nInstalling build tools...")
    print("=" * 25)
    
    build_tools = [
        "setuptools>=50.0",
        "wheel>=0.36.0", 
        "Cython>=0.29.0"
    ]
    
    success = 0
    for tool in build_tools:
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", tool
            ], capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                print(f"  [OK] {tool.split('>=')[0]} installed")
                success += 1
            else:
                print(f"  [ERROR] Failed to install {tool}")
                
        except Exception as e:
            print(f"  [ERROR] Error installing {tool}: {e}")
    
    return success == len(build_tools)

def install_dependencies():
    """Install PyHula dependencies using the dependency installer"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    installer_path = os.path.join(parent_dir, "install_dependencies", "install_dependencies.py")
    
    if os.path.exists(installer_path):
        print("\nRunning dependency installer...")
        result = subprocess.run([sys.executable, installer_path], 
                            capture_output=False, text=True)
        return result.returncode == 0
    else:
        print("[WARNING] Dependency installer not found, installing manually...")
        
        # Manual installation
        dependencies = [
            "numpy>=1.19.0",
            "opencv-python>=4.5.0",
            "pyserial>=3.4", 
            "pymavlink>=2.4.0",
            "scipy>=1.6.0",
            "matplotlib>=3.3.0",
            "pillow>=8.0.0"
        ]
        
        for dep in dependencies:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep],
                            check=True, capture_output=True, text=True)
                print(f"  [OK] {dep.split('>=')[0]} installed")
            except:
                print(f"  [ERROR] Failed to install {dep}")
        
        return True

def build_pyhula():
    """Build PyHula from source"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)  # Go up one level from setup_complete/
    
    # Check if setup.py exists
    setup_py = os.path.join(parent_dir, "setup.py")
    if not os.path.exists(setup_py):
        print("[ERROR] setup.py not found in parent directory")
        return False
    
    # Change to parent directory for build
    original_dir = os.getcwd()
    os.chdir(parent_dir)
    
    try:
        # Build wheel
        print("\nBuilding PyHula wheel...")
        build_cmd = [sys.executable, "setup.py", "bdist_wheel"]
        if not run_command(build_cmd, "Building PyHula wheel"):
            return False
        
        # Find the built wheel
        dist_dir = os.path.join(parent_dir, "dist")
        if not os.path.exists(dist_dir):
            print("[ERROR] dist directory not found after build")
            return False
        
        wheel_files = [f for f in os.listdir(dist_dir) if f.endswith('.whl')]
        if not wheel_files:
            print("[ERROR] No wheel file found after build")
            return False
        
        # Install the wheel
        wheel_path = os.path.join(dist_dir, wheel_files[-1])  # Use latest wheel
        print(f"\nInstalling PyHula wheel: {wheel_files[-1]}")
        
        # Check if PyHula is already installed to decide if we need upgrade or install
        try:
            import pyhula
            # If already installed, use upgrade to avoid unnecessary dependency reinstallation
            install_cmd = [sys.executable, "-m", "pip", "install", wheel_path, "--upgrade"]
            print("PyHula already installed, upgrading...")
        except ImportError:
            # If not installed, do a clean install
            install_cmd = [sys.executable, "-m", "pip", "install", wheel_path]
            print("Installing PyHula for the first time...")
        
        return run_command(install_cmd, "Installing PyHula")
    
    finally:
        # Always return to original directory
        os.chdir(original_dir)

def test_installation():
    """Test if PyHula is properly installed"""
    print("\nTesting PyHula installation...")
    print("=" * 30)
    
    try:
        import pyhula
        print("[OK] PyHula import successful")
        
        # Test basic functionality
        api = pyhula.UserApi()
        print("[OK] UserApi creation successful")
        
        # Check version if available
        if hasattr(pyhula, '__version__'):
            print(f"[OK] PyHula version: {pyhula.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] PyHula import failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] PyHula test failed: {e}")
        return False

def main():
    """Main installation function"""
    print("PyHula Complete Setup & Installation")
    print("=" * 50)
    print("This script will:")
    print("1. Check Python version compatibility")
    print("2. Install build tools and dependencies")
    print("3. Build PyHula from source")
    print("4. Install PyHula")
    print("5. Test the installation")
    print("=" * 50)
    
    # Step 1: Check Python version
    if not check_python_version():
        return 1
    
    # Step 2: Install build tools
    if not install_build_tools():
        print("\n[WARNING] Some build tools failed to install")
        print("You may need to install Visual Studio Build Tools on Windows")
    
    # Step 3: Install dependencies
    if not install_dependencies():
        print("\n[ERROR] Dependency installation failed")
        return 1
    
    # Step 4: Build and install PyHula
    if not build_pyhula():
        print("\n[ERROR] PyHula build/installation failed")
        return 1
    
    # Step 5: Test installation
    if not test_installation():
        print("\n[ERROR] PyHula installation test failed")
        return 1
    
    # Success message
    print("\n" + "=" * 50)
    print("INSTALLATION COMPLETE!")
    print("=" * 50)
    print("[OK] PyHula has been successfully installed!")
    print("\nYou can now:")
    print("• Run 'python pyhula_import.py' to test drone operations")
    print("• Run 'python test_installation.py' for comprehensive testing")
    print("• Import pyhula in your own Python scripts")
    print("\nFor drone connection:")
    print("• Ensure drone is powered on")
    print("• Connect to drone WiFi network")
    print("• Use standard IPs: 192.168.1.118, 192.168.4.1, or 192.168.10.1")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[INFO] Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
