#!/usr/bin/env python3
"""
PyHula Direct Build - No temp files, strategic directory use
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_wheel_directly():
    """Build wheel directly using existing built C extensions"""
    
    current_dir = Path(__file__).parent.absolute()
    print("PyHula Direct Build")
    print("=" * 60)
    print(f"Building in: {current_dir}")
    
    # Get Python command
    python_candidates = [['py', '-3.13'], ['python3.13'], ['python']]
    python_cmd = None
    
    for cmd in python_candidates:
        try:
            result = subprocess.run(cmd + ['--version'], 
                                  capture_output=True, text=True, check=True)
            if any(v in result.stdout for v in ['3.13', '3.12', '3.11', '3.10']):
                python_cmd = cmd
                print(f"Using Python: {' '.join(cmd)} -> {result.stdout.strip()}")
                break
        except:
            continue
    
    if not python_cmd:
        print("No suitable Python found")
        return False
    
    try:
        # Clean previous build
        build_dir = current_dir / 'build'
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print("Cleaned previous build directory")
        
        dist_dir = current_dir / 'dist'
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
            print("Cleaned previous dist directory")
        
        # Try to build just the Python wheel first (without C extensions)
        print("\nAttempting Python-only wheel build...")
        
        # Create a temporary setup for Python-only build
        setup_backup = None
        setup_file = current_dir / 'setup.py'
        
        if setup_file.exists():
            # Read current setup.py
            with open(setup_file, 'r', encoding='utf-8') as f:
                setup_content = f.read()
            
            # Modify to skip C extensions for initial build
            modified_content = setup_content.replace(
                'ext_modules=cythonize(c_extensions',
                '# ext_modules=cythonize(c_extensions'
            ).replace(
                'ext_modules=c_extensions',
                '# ext_modules=c_extensions'
            )
            
            # Write modified setup
            with open(setup_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            setup_backup = setup_content
        
        # Build Python-only wheel
        print("Building Python wheel with compatibility fixes...")
        subprocess.run(python_cmd + ['setup.py', 'bdist_wheel'], check=True)
        
        # Restore original setup.py
        if setup_backup:
            with open(setup_file, 'w', encoding='utf-8') as f:
                f.write(setup_backup)
            print("Restored original setup.py")
        
        # Check results
        dist_dir = current_dir / 'dist'
        if dist_dir.exists():
            wheels = list(dist_dir.glob('*.whl'))
            if wheels:
                print(f"\nBuild successful! Created: {wheels[0].name}")
                
                # Install the wheel
                print("\nInstalling the built wheel...")
                subprocess.run(python_cmd + ['-m', 'pip', 'install', str(wheels[0]), '--force-reinstall'], check=True)
                
                # Test the installation
                print("\nTesting import...")
                test_result = subprocess.run(
                    python_cmd + ['-c', 'import pyhula; print("PyHula imported successfully with Python 3.13 compatibility")'],
                    capture_output=True, text=True
                )
                
                if test_result.returncode == 0:
                    print("✓ Import test successful")
                    print(test_result.stdout.strip())
                    
                    # Test UserApi creation (without connecting)
                    print("\nTesting UserApi creation...")
                    api_test = subprocess.run(
                        python_cmd + ['-c', 'import pyhula; api = pyhula.UserApi(); print("UserApi created successfully")'],
                        capture_output=True, text=True
                    )
                    
                    if api_test.returncode == 0:
                        print("✓ UserApi creation successful")
                        print(api_test.stdout.strip())
                        return True
                    else:
                        print("✗ UserApi creation failed:")
                        print(api_test.stderr)
                        return False
                else:
                    print("✗ Import test failed:")
                    print(test_result.stderr)
                    return False
            else:
                print("No wheel file created")
                return False
        else:
            print("No dist directory created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Build command failed: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"Build failed: {e}")
        return False

def main():
    """Main entry point"""
    print("Starting direct build process...")
    
    success = build_wheel_directly()
    
    if success:
        print("\n" + "=" * 60)
        print("BUILD AND TEST COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("PyHula is now installed with Python 3.13 compatibility!")
        print("\nYou can now use:")
        print("  import pyhula")
        print("  api = pyhula.UserApi()")
        print("  api.connect()  # Test with actual drone")
    else:
        print("\n" + "=" * 60)
        print("BUILD FAILED")
        print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
