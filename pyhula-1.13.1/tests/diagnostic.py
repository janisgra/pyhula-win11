#!/usr/bin/env python3
"""
PyHula Setup Diagnostic Tool - Python 3.13 Version
Identifies and fixes common setup issues using Python 3.13
"""

import os
import sys
import subprocess

# Force Python 3.13 usage
PYTHON_CMD = 'py'
PYTHON_ARGS = ['-3.13']

def get_python_info():
    """Get current Python version info"""
    print("=== Python Version Check ===")
    version = sys.version_info
    print(f"Current Python: {version.major}.{version.minor}.{version.micro}")
    
    # Check if we're running under Python 3.13
    if version.major == 3 and version.minor == 13:
        print("✓ Running on Python 3.13 (recommended)")
        return True
    else:
        print(f"⚠ Running on Python {version.major}.{version.minor} (Python 3.13 recommended)")
        print("For best results, run with: py -3.13 diagnostic.py")
        
        # Try to check if Python 3.13 is available
        try:
            result = subprocess.run(['py', '-3.13', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Python 3.13 is available: {result.stdout.strip()}")
                return True
            else:
                print("✗ Python 3.13 not found")
        except:
            print("✗ Python 3.13 not found")
        
        return False

def check_c_extensions():
    """Check if C extensions were built"""
    print("\n=== C Extensions Check ===")
    
    extensions_found = 0
    missing_extensions = []
    
    # Check for some key extensions
    key_extensions = [
        'src/pyhula/pypack/fylo/controlserver.pyd',
        'src/pyhula/pypack/system/network.pyd',
        'src/pyhula/pypack/system/command.pyd'
    ]
    
    for ext_path in key_extensions:
        # Look for any .pyd files (Windows) or .so files (Linux)
        base_path = ext_path.replace('.pyd', '')
        found = False
        
        # Check for .pyd files (Windows)
        for file in os.listdir(os.path.dirname(base_path)) if os.path.exists(os.path.dirname(base_path)) else []:
            if file.startswith(os.path.basename(base_path)) and (file.endswith('.pyd') or file.endswith('.so')):
                print(f"Found: {file}")
                extensions_found += 1
                found = True
                break
        
        if not found:
            missing_extensions.append(ext_path)
    
    if extensions_found == 0:
        print("ERROR: No C extensions found. Run 'python setup.py build_ext --inplace' first")
        return False
    
    print(f"Found {extensions_found} C extensions")
    
    if missing_extensions:
        print("Missing extensions:")
        for ext in missing_extensions:
            print(f"  {ext}")
    
    return True

def check_dependencies():
    """Check if required dependencies are available"""
    print("\n=== Dependencies Check ===")
    
    required_packages = {
        'numpy': 'numpy',
        'cv2': 'opencv-python', 
        'serial': 'pyserial',
        'pymavlink': 'pymavlink',
        'scipy': 'scipy'
    }
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} (missing)")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + ' '.join(missing_packages))
        return False
    
    return True

def test_import():
    """Test if pyhula can be imported"""
    print("\n=== Import Test ===")
    
    # Add src to path
    sys.path.insert(0, 'src')
    
    try:
        import pyhula
        print("✓ pyhula imported successfully")
        
        try:
            version = pyhula.get_version()
            print(f"✓ Version: {version}")
        except Exception as e:
            print(f"✗ Could not get version: {e}")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        
        # Try to give specific guidance
        if "DLL load failed" in str(e):
            print("\nDLL Load Error - Possible fixes:")
            print("1. Install Microsoft Visual C++ Redistributable")
            print("2. Check if all dependencies are installed")
            print("3. Try rebuilding with: python setup.py clean --all && python setup.py build_ext --inplace")
        
        return False

def main():
    """Run all diagnostic checks"""
    print("PyHula Setup Diagnostic Tool")
    print("=" * 50)
    
    checks = [
        get_python_info,
        check_c_extensions, 
        check_dependencies,
        test_import
    ]
    
    all_passed = True
    
    for check in checks:
        try:
            if not check():
                all_passed = False
        except Exception as e:
            print(f"Check failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All checks passed! PyHula should be working.")
    else:
        print("✗ Some checks failed. See above for details.")
        print("\nQuick fix attempts:")
        print("1. python setup.py build_ext --inplace")
        print("2. pip install numpy opencv-python pyserial pymavlink scipy")
        print("3. python diagnostic.py")
    
    return all_passed

if __name__ == "__main__":
    main()
