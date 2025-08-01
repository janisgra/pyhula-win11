#!/usr/bin/env python3
"""
PyHula Setup - Direct Build Handler
Builds directly in the current directory without temp files
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_short_path_build():
    """Return current directory for direct build"""
    
    # Build directly in current directory
    current_dir = Path.cwd()
    print(f"Building directly in: {current_dir}")
    
    return current_dir

def copy_project_to_short_path(source_dir, target_dir):
    """No copying needed - building directly"""
    print("Building directly in current directory - no copying needed")
    return

def build_in_short_path():
    """Build PyHula directly in current directory"""
    
    current_dir = Path(__file__).parent.absolute()
    original_cwd = os.getcwd()  # Get this first
    
    print("PyHula Build - Direct Build Handler")
    print("=" * 60)
    print(f"Building in: {current_dir}")
    print(f"Path length: {len(str(current_dir))} characters")
    
    # Use current directory
    build_dir = current_dir
    print(f"Build directory: {build_dir}")
    
    try:
        # No copying needed
        print("\nBuilding directly in current directory...")
        
        # Get Python command
        python_candidates = [['py', '-3.13'], ['python3.13'], ['python']]
        python_cmd = None
        
        for cmd in python_candidates:
            try:
                result = subprocess.run(cmd + ['--version'], 
                                      capture_output=True, text=True, check=True)
                if any(v in result.stdout for v in ['3.13', '3.12', '3.11', '3.10', '3.9', '3.8']):
                    python_cmd = cmd
                    print(f"Using Python: {' '.join(cmd)} -> {result.stdout.strip()}")
                    break
            except:
                continue
        
        if not python_cmd:
            raise RuntimeError("No suitable Python found")
        
        # Install dependencies
        print("\nInstalling dependencies...")
        subprocess.run(
            python_cmd + ['-m', 'pip', 'install', 'setuptools', 'wheel', 'numpy'],
            check=True
        )
        
        # Build C extensions
        print("\nBuilding C extensions...")
        result = subprocess.run(
            python_cmd + ['setup.py', 'build_ext', '--inplace'],
            check=True, capture_output=True, text=True
        )
        print("  C extensions built successfully")
        
        # Build distributions
        print("\nBuilding distributions...")
        subprocess.run(python_cmd + ['setup.py', 'sdist'], check=True)
        subprocess.run(python_cmd + ['setup.py', 'bdist_wheel'], check=True)
        
        # Results are already in current directory
        print("\nBuild completed in current directory...")
        dist_dir = current_dir / 'dist'
        
        if dist_dir.exists():
            # Show results
            print("\nBuild results:")
            for file in dist_dir.glob('*'):
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"  {file.name} ({size_mb:.1f} MB)")
        
        print("\n" + "=" * 60)
        print("BUILD COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Files available in: {dist_dir}")
        
        # Installation instructions
        wheels = list(dist_dir.glob('*.whl'))
        if wheels:
            print(f"\nTo install:")
            print(f"  {' '.join(python_cmd)} -m pip install {wheels[0]}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error output: {e.stderr}")
        return False
        
    except Exception as e:
        print(f"\nBuild failed: {e}")
        return False
        
    finally:
        # Restore original directory
        os.chdir(original_cwd)
        print("Build process completed")

def install_and_test():
    """Install the built package and test it"""
    
    current_dir = Path(__file__).parent.absolute()
    dist_dir = current_dir / 'dist'
    
    if not dist_dir.exists():
        print("No dist directory found. Run build first.")
        return False
    
    # Find wheel file
    wheels = list(dist_dir.glob('*.whl'))
    if not wheels:
        print("No wheel file found")
        return False
    
    wheel_file = wheels[0]
    print(f"\nInstalling: {wheel_file.name}")
    
    # Get Python command
    python_candidates = [['py', '-3.13'], ['python3.13'], ['python']]
    python_cmd = None
    
    for cmd in python_candidates:
        try:
            result = subprocess.run(cmd + ['--version'], 
                                  capture_output=True, text=True, check=True)
            if any(v in result.stdout for v in ['3.13', '3.12', '3.11', '3.10', '3.9', '3.8']):
                python_cmd = cmd
                break
        except:
            continue
    
    if not python_cmd:
        print("No suitable Python found")
        return False
    
    try:
        # Uninstall old version
        print("Uninstalling old versions...")
        subprocess.run(
            python_cmd + ['-m', 'pip', 'uninstall', 'pyhula', '-y'],
            capture_output=True
        )
        
        # Install new version
        subprocess.run(
            python_cmd + ['-m', 'pip', 'install', str(wheel_file), '--force-reinstall'],
            check=True
        )
        print("Installation completed")
        
        # Test import
        print("\nTesting import...")
        test_script = '''
import pyhula
print("SUCCESS: PyHula imported")
print(f"Version: {getattr(pyhula, '__version__', 'unknown')}")
print(f"Location: {pyhula.__file__}")

# Test API availability
if hasattr(pyhula, 'UserApi'):
    print("SUCCESS: UserApi available")
    api = pyhula.UserApi()
    print("UserApi instance created")
else:
    print("WARNING: UserApi not found")
'''
        
        result = subprocess.run(
            python_cmd + ['-c', test_script],
            check=True, capture_output=True, text=True
        )
        print(result.stdout)
        
        print("\n" + "=" * 60)
        print("INSTALLATION AND TEST COMPLETED")
        print("=" * 60)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Installation/test failed: {e}")
        return False

def test_drone_connection():
    """Test connection to Hula drone"""
    
    print("\nTesting drone connection...")
    
    # Get Python command
    python_candidates = [['py', '-3.13'], ['python3.13'], ['python']]
    python_cmd = None
    
    for cmd in python_candidates:
        try:
            result = subprocess.run(cmd + ['--version'], 
                                  capture_output=True, text=True, check=True)
            if any(v in result.stdout for v in ['3.13', '3.12', '3.11', '3.10', '3.9', '3.8']):
                python_cmd = cmd
                break
        except:
            continue
    
    if not python_cmd:
        print("No suitable Python found")
        return False
    
    connection_script = '''
import time
try:
    import pyhula
    print("Creating API instance...")
    api = pyhula.UserApi()
    
    print("Attempting drone connection...")
    result = api.connect()
    
    if result:
        print("SUCCESS: Connected to drone")
        print("Connection test passed")
        
        # Basic cleanup
        time.sleep(1)
        print("Disconnected from drone")
    else:
        print("FAILED: Could not connect to drone")
        print("Check: Drone powered on, WLAN connected, no firewall blocking")
        
except Exception as e:
    print(f"Connection test error: {e}")
'''
    
    try:
        result = subprocess.run(
            python_cmd + ['-c', connection_script],
            capture_output=True, text=True, timeout=30
        )
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Connection test failed: {e}")
        if e.stdout:
            print(e.stdout)
        return False
    except subprocess.TimeoutExpired:
        print("Connection test timed out")
        return False

def main():
    """Main entry point"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'install':
            success = install_and_test()
        elif command == 'test':
            success = test_drone_connection()
        elif command == 'complete':
            # Run complete process
            success = build_in_short_path()
            if success:
                success = install_and_test()
                if success:
                    success = test_drone_connection()
        else:
            print("Usage:")
            print("  python build_complete.py        - Build only")
            print("  python build_complete.py install - Install and test")
            print("  python build_complete.py test    - Test drone connection")
            print("  python build_complete.py complete - Complete process")
            return 1
    else:
        success = build_in_short_path()
        
        if success:
            print("\nNext steps:")
            print("  python build_complete.py install  - Install and test")
            print("  python build_complete.py test     - Test drone connection")
            print("  python build_complete.py complete - Run everything")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
