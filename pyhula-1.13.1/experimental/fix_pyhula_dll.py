#!/usr/bin/env python3
"""
Fix PyHula DLL Loading Issues

This script fixes the missing DLL problem that prevents PyHula commands from working.
"""

import os
import sys
from pathlib import Path

def fix_dll_path():
    """Add PyHula DLL directory to system PATH"""
    try:
        import pyhula
        pyhula_dir = Path(pyhula.__file__).parent
        dll_dir = pyhula_dir / "f09-lite-trans"
        
        if dll_dir.exists():
            dll_path = str(dll_dir)
            
            # Add to PATH if not already there
            if dll_path not in os.environ.get('PATH', ''):
                os.environ['PATH'] = dll_path + os.pathsep + os.environ.get('PATH', '')
                print(f"Added DLL directory to PATH: {dll_path}")
                return True
            else:
                print("DLL directory already in PATH")
                return True
        else:
            print(f"ERROR: DLL directory not found: {dll_dir}")
            return False
            
    except ImportError:
        print("ERROR: PyHula not found")
        return False

def test_dll_loading():
    """Test if DLLs can be loaded after fix"""
    try:
        import ctypes
        import pyhula
        
        # Get DLL path
        pyhula_dir = Path(pyhula.__file__).parent
        dll_path = pyhula_dir / "f09-lite-trans" / "f09-ffmpeg-lib.dll"
        
        if dll_path.exists():
            # Try to load the problematic DLL
            lib = ctypes.CDLL(str(dll_path))
            print(f"SUCCESS: f09-ffmpeg-lib.dll loaded successfully")
            return True
        else:
            print(f"ERROR: DLL not found at {dll_path}")
            return False
            
    except Exception as e:
        print(f"ERROR loading DLL: {e}")
        return False

def create_permanent_fix():
    """Create a permanent fix by patching PyHula __init__.py"""
    try:
        import pyhula
        pyhula_dir = Path(pyhula.__file__).parent
        init_file = pyhula_dir / "__init__.py"
        
        # Read current content
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if "DLL path fix" in content:
            print("PyHula already has DLL path fix")
            return True
        
        # Add DLL path fix to the beginning
        dll_fix_code = '''
# DLL path fix for PyHula - AUTO-GENERATED
import os
from pathlib import Path

# Add DLL directory to PATH for ctypes to find libraries
_pyhula_dir = Path(__file__).parent
_dll_dir = _pyhula_dir / "f09-lite-trans"
if _dll_dir.exists():
    _dll_path = str(_dll_dir)
    if _dll_path not in os.environ.get('PATH', ''):
        os.environ['PATH'] = _dll_path + os.pathsep + os.environ.get('PATH', '')

'''
        
        # Insert at the beginning (after any existing patches)
        if "Python 3.13 compatibility patch" in content:
            # Insert after existing patch
            insert_pos = content.find("array.array = _CompatibleArray") + len("array.array = _CompatibleArray")
            new_content = content[:insert_pos] + "\n" + dll_fix_code + content[insert_pos:]
        else:
            # Insert at the very beginning
            new_content = dll_fix_code + content
        
        # Write the patched file
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"DLL path fix applied to {init_file}")
        return True
        
    except Exception as e:
        print(f"ERROR applying permanent fix: {e}")
        return False

def test_pyhula_commands():
    """Test that PyHula commands work after DLL fix"""
    print("\nTesting PyHula commands after DLL fix...")
    
    try:
        # Clear module cache to reload with DLL fix
        modules_to_clear = [name for name in sys.modules if name.startswith('pyhula')]
        for module_name in modules_to_clear:
            del sys.modules[module_name]
        
        # Import fresh PyHula
        import pyhula
        
        # Create API
        api = pyhula.UserApi()
        print("✓ UserApi created")
        
        # Connect
        result = api.connect()
        if result:
            print("✓ Connection successful")
            
            # Test a simple LED command (should respond quickly)
            print("Testing LED command...")
            led_result = api.single_fly_lamplight(255, 0, 0, 1000, 1)
            print(f"LED command result: {led_result}")
            
            # Test takeoff (should at least attempt)
            print("Testing takeoff command...")
            import time
            start_time = time.time()
            takeoff_result = api.single_fly_takeoff()
            end_time = time.time()
            
            print(f"Takeoff command result: {takeoff_result}")
            print(f"Command took: {end_time - start_time:.2f} seconds")
            
            if end_time - start_time < 10:  # Should respond within 10 seconds
                print("✓ Commands responding normally")
                return True
            else:
                print("✗ Commands still hanging")
                return False
        else:
            print("✗ Connection failed")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("PyHula DLL Loading Fix")
    print("=" * 30)
    
    # Step 1: Fix DLL path for current session
    if fix_dll_path():
        print("✓ DLL path fixed for current session")
    else:
        print("✗ Failed to fix DLL path")
        return False
    
    # Step 2: Test DLL loading
    if test_dll_loading():
        print("✓ DLL loading test passed")
    else:
        print("✗ DLL loading test failed")
        return False
    
    # Step 3: Apply permanent fix
    if create_permanent_fix():
        print("✓ Permanent DLL fix applied")
    else:
        print("✗ Failed to apply permanent fix")
        return False
    
    # Step 4: Test PyHula commands
    if test_pyhula_commands():
        print("\n" + "=" * 40)
        print("SUCCESS: PyHula commands should work now!")
        print("=" * 40)
        print("\nRestart Python and test:")
        print(">>> import pyhula")
        print(">>> api = pyhula.UserApi()")
        print(">>> api.connect()")
        print(">>> api.single_fly_lamplight(0, 255, 0, 2000, 1)")
        return True
    else:
        print("\n" + "=" * 40)
        print("PARTIAL SUCCESS: DLL fixed but commands may still have issues")
        print("=" * 40)
        return False

if __name__ == "__main__":
    main()
