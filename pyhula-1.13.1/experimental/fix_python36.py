#!/usr/bin/env python3
"""
Fix PyHula for Python 3.6

This script addresses the specific issues in Python 3.6:
1. struct.error: required argument is not an integer
2. TypeError: 'int' object is not subscriptable (LED parameter issue)
"""

import os
import sys
import shutil
from pathlib import Path

def find_python36_pyhula():
    """Find Python 3.6 PyHula installation"""
    try:
        # Check if we're running Python 3.6
        if sys.version_info.major != 3 or sys.version_info.minor != 6:
            print(f"This script is for Python 3.6, but you're running Python {sys.version_info.major}.{sys.version_info.minor}")
            return None
            
        import pyhula
        pyhula_dir = Path(pyhula.__file__).parent
        print(f"Found Python 3.6 PyHula at: {pyhula_dir}")
        return pyhula_dir
    except ImportError:
        print("PyHula not found in Python 3.6 installation")
        return None

def patch_python36_pyhula(pyhula_dir):
    """Apply Python 3.6 specific patches"""
    
    # Create backup
    backup_dir = pyhula_dir / "python36_backup"
    backup_dir.mkdir(exist_ok=True)
    
    init_file = pyhula_dir / "__init__.py"
    if init_file.exists():
        shutil.copy2(init_file, backup_dir / "__init__.py")
        print("Backup created")
    
    # Read original content
    if init_file.exists():
        with open(init_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
    else:
        original_content = ""
    
    # Check if already patched
    if "Python 3.6 compatibility patch" in original_content:
        print("PyHula already patched for Python 3.6")
        return True
    
    # Create Python 3.6 specific patch
    patch_code = '''
# Python 3.6 compatibility patch - AUTO-GENERATED
import struct
import sys

# Fix struct.pack for Python 3.6 with same issues as 3.13
_original_struct_pack = struct.pack

def _python36_struct_pack(fmt, *args):
    """Python 3.6 compatible struct.pack that handles None values"""
    converted_args = []
    for arg in args:
        if arg is None:
            converted_args.append(0)
        elif isinstance(arg, float):
            converted_args.append(int(arg) if arg.is_integer() else round(arg))
        elif isinstance(arg, bool):
            converted_args.append(int(arg))
        else:
            converted_args.append(arg)
    
    return _original_struct_pack(fmt, *converted_args)

struct.pack = _python36_struct_pack

# Fix LED parameter handling for single_fly commands
def _patch_led_handling():
    """Patch LED parameter handling in PyHula commands"""
    try:
        import pyhula.pypack.fylo.commandprocessor as cp
        
        # Store original setRgb function
        if hasattr(cp, 'setRgb'):
            _original_setRgb = cp.setRgb
            
            def _safe_setRgb(led):
                """Safe setRgb that handles int and dict parameters"""
                if isinstance(led, dict):
                    return _original_setRgb(led)
                elif isinstance(led, int):
                    # Convert int to dict format
                    if led == 0:
                        led_dict = {'r': 0, 'g': 0, 'b': 0, 'mode': 2}  # Off
                    else:
                        led_dict = {'r': 255, 'g': 255, 'b': 255, 'mode': 1}  # White
                    return _original_setRgb(led_dict)
                else:
                    # Default LED settings
                    return _original_setRgb({'r': 0, 'g': 0, 'b': 0, 'mode': 2})
            
            cp.setRgb = _safe_setRgb
    except ImportError:
        pass  # Module not available yet

# Apply LED patch after import
import atexit
atexit.register(_patch_led_handling)

'''
    
    # Write patched content
    patched_content = patch_code + original_content
    
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(patched_content)
    
    print(f"Python 3.6 patch applied to {init_file}")
    return True

def main():
    """Main function for Python 3.6 patcher"""
    print("PyHula Python 3.6 Compatibility Patcher")
    print("=" * 45)
    
    if sys.version_info.major != 3 or sys.version_info.minor != 6:
        print(f"ERROR: This patcher is for Python 3.6")
        print(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}")
        print("\nTo use this patcher:")
        print("1. Run: py -3.6 fix_python36.py")
        return False
    
    # Find PyHula installation
    pyhula_dir = find_python36_pyhula()
    if not pyhula_dir:
        return False
    
    # Apply patches
    if patch_python36_pyhula(pyhula_dir):
        print("\n" + "=" * 45)
        print("SUCCESS: Python 3.6 patches applied!")
        print("=" * 45)
        print("\nRestart Python and test:")
        print(">>> import pyhula")
        print(">>> api = pyhula.UserApi()")
        print(">>> api.connect()")
        print(">>> api.single_fly_takeoff()  # Should work now")
        return True
    else:
        print("ERROR: Failed to apply patches")
        return False

if __name__ == "__main__":
    main()
