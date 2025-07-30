#!/usr/bin/env python3
"""
PyHula Build Script for Cross-Platform Compatibility

This script automates the build process for different platforms and Python versions.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, description="Running command"):
    """Run a shell command and return success status"""
    print(f"\n{description}: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(cmd, check=True, shell=True if isinstance(cmd, str) else False)
        print(" Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f" Failed with exit code {e.returncode}")
        return False

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for pattern in dirs_to_clean:
        if '*' in pattern:
            import glob
            for path in glob.glob(pattern):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"  Removed directory: {path}")
        elif os.path.exists(pattern):
            shutil.rmtree(pattern)
            print(f"  Removed directory: {pattern}")

def check_dependencies():
    """Check if required build dependencies are installed"""
    print(" Checking build dependencies...")
    required = ['setuptools', 'wheel', 'numpy']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"   {package}")
        except ImportError:
            print(f"   {package}")
            missing.append(package)
    
    if missing:
        print(f"\n Installing missing dependencies: {', '.join(missing)}")
        cmd = [sys.executable, "-m", "pip", "install"] + missing
        if not run_command(cmd, "Installing dependencies"):
            return False
    
    return True

def build_extensions():
    """Build C extensions"""
    print(" Building C extensions...")
    cmd = [sys.executable, "setup.py", "build_ext", "--inplace"]
    return run_command(cmd, "Building extensions")

def create_wheel():
    """Create wheel package"""
    print(" Creating wheel package...")
    cmd = [sys.executable, "setup.py", "bdist_wheel"]
    return run_command(cmd, "Creating wheel")

def create_source_dist():
    """Create source distribution"""
    print(" Creating source distribution...")
    cmd = [sys.executable, "setup.py", "sdist"]
    return run_command(cmd, "Creating source distribution")

def test_import():
    """Test if the built package can be imported"""
    print(" Testing package import...")
    try:
        # Add the current directory to Python path
        sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
        import pyhula
        print("   pyhula imported successfully")
        
        # Test specific modules
        modules_to_test = [
            'pyhula.pypack.fylo.commandprocessor',
            'pyhula.pypack.fylo.config',
            'pyhula.pypack.system.buffer',
        ]
        
        for module in modules_to_test:
            try:
                __import__(module)
                print(f"   {module}")
            except Exception as e:
                print(f"   {module}: {e}")
        
        return True
    except Exception as e:
        print(f"   Import test failed: {e}")
        return False

def main():
    """Main build process"""
    print(" PyHula Build Script")
    print(f"Python {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('setup.py'):
        print(" setup.py not found. Please run this script from the pyhula-1.13.1 directory.")
        return 1
    
    # Build process
    steps = [
        ("Clean build artifacts", clean_build),
        ("Check dependencies", check_dependencies),
        ("Build extensions", build_extensions),
        ("Create wheel", create_wheel),
        ("Create source distribution", create_source_dist),
        ("Test import", test_import),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_func():
            print(f"\n Build failed at step: {step_name}")
            return 1
    
    # Success summary
    print("\n" + "="*60)
    print(" BUILD SUCCESSFUL! ")
    print("="*60)
    
    # List created files
    if os.path.exists('dist'):
        print("\n Created packages:")
        for file in os.listdir('dist'):
            file_path = os.path.join('dist', file)
            size = os.path.getsize(file_path) / (1024*1024)
            print(f"   {file} ({size:.1f} MB)")
    
    print("\n Installation commands:")
    if os.path.exists('dist'):
        wheels = [f for f in os.listdir('dist') if f.endswith('.whl')]
        if wheels:
            wheel_path = os.path.join('dist', wheels[0])
            print(f"  pip install {wheel_path}")
    
    print("\n PyHula is ready for distribution!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
