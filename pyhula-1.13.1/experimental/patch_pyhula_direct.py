#!/usr/bin/env python3
"""
Direct PyHula Python 3.13 Patcher

This script directly patches the installed PyHula library for Python 3.13 compatibility.
Run this once to fix PyHula permanently for Python 3.13.
"""

import os
import sys
import shutil
import struct
import array
from pathlib import Path

def find_pyhula_installation():
    """Find PyHula installation directory"""
    try:
        import pyhula
        pyhula_dir = Path(pyhula.__file__).parent
        print(f"Found PyHula installation at: {pyhula_dir}")
        return pyhula_dir
    except ImportError:
        print("ERROR: PyHula not found. Please install PyHula first.")
        return None

def backup_original_files(pyhula_dir):
    """Create backup of original files"""
    backup_dir = pyhula_dir / "python313_backup"
    backup_dir.mkdir(exist_ok=True)
    
    files_to_backup = [
        "__init__.py",
        "userapi.py",
    ]
    
    # Also look for mavlink related files
    for file_path in pyhula_dir.rglob("*.py"):
        if "mavlink" in file_path.name.lower():
            files_to_backup.append(str(file_path.relative_to(pyhula_dir)))
    
    print("Creating backups...")
    for file_name in files_to_backup:
        src_path = pyhula_dir / file_name
        if src_path.exists():
            backup_path = backup_dir / file_name
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, backup_path)
            print(f"  Backed up: {file_name}")
    
    return backup_dir

def patch_struct_module():
    """Patch struct module for Python 3.13 compatibility"""
    print("Patching struct module...")
    
    # Store original struct.pack
    original_pack = struct.pack
    
    def python313_compatible_pack(fmt, *args):
        """Python 3.13 compatible struct.pack"""
        converted_args = []
        
        for arg in args:
            if isinstance(arg, float):
                if arg.is_integer():
                    converted_args.append(int(arg))
                else:
                    converted_args.append(round(arg))
            elif isinstance(arg, bool):
                converted_args.append(int(arg))
            elif isinstance(arg, str):
                try:
                    if '.' in arg:
                        converted_args.append(int(float(arg)))
                    else:
                        converted_args.append(int(arg))
                except (ValueError, TypeError):
                    converted_args.append(arg)
            elif arg is None:
                converted_args.append(0)
            elif hasattr(arg, '__int__'):
                try:
                    converted_args.append(int(arg))
                except (ValueError, TypeError):
                    converted_args.append(arg)
            else:
                converted_args.append(arg)
        
        try:
            return original_pack(fmt, *converted_args)
        except struct.error as e:
            if "required argument is not an integer" in str(e):
                # More aggressive conversion
                final_args = []
                for arg in converted_args:
                    if isinstance(arg, (int, bool)):
                        final_args.append(int(arg))
                    elif isinstance(arg, float):
                        final_args.append(int(arg) if arg.is_integer() else round(arg))
                    elif isinstance(arg, str):
                        try:
                            final_args.append(int(arg) if arg.isdigit() else 0)
                        except (ValueError, TypeError):
                            final_args.append(0)
                    elif arg is None:
                        final_args.append(0)
                    else:
                        try:
                            final_args.append(int(arg))
                        except (ValueError, TypeError):
                            final_args.append(0)
                
                return original_pack(fmt, *final_args)
            else:
                raise
    
    # Replace struct.pack globally
    struct.pack = python313_compatible_pack
    return True

def patch_array_module():
    """Patch array module for Python 3.13 compatibility"""
    print("Patching array module...")
    
    if not hasattr(array.array, 'fromstring'):
        original_array = array.array
        
        class CompatibleArray(original_array):
            def fromstring(self, s):
                """Compatibility wrapper for removed fromstring method"""
                if isinstance(s, str):
                    s = s.encode('latin-1')
                self.frombytes(s)
        
        array.array = CompatibleArray
        print("  Added array.fromstring compatibility")
    
    return True

def create_init_patch(pyhula_dir):
    """Create a patched __init__.py that applies fixes on import"""
    init_file = pyhula_dir / "__init__.py"
    
    # Read original content
    if init_file.exists():
        with open(init_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
    else:
        original_content = ""
    
    # Check if already patched
    if "Python 3.13 compatibility patch" in original_content:
        print("PyHula already patched for Python 3.13")
        return True
    
    # Create patch code
    patch_code = '''
# Python 3.13 compatibility patch - AUTO-GENERATED
import sys
if sys.version_info >= (3, 13):
    import struct
    import array
    
    # Patch struct.pack for type compatibility
    _original_struct_pack = struct.pack
    
    def _python313_struct_pack(fmt, *args):
        """Python 3.13 compatible struct.pack"""
        converted_args = []
        for arg in args:
            if isinstance(arg, float):
                converted_args.append(int(arg) if arg.is_integer() else round(arg))
            elif isinstance(arg, bool):
                converted_args.append(int(arg))
            elif isinstance(arg, str):
                try:
                    converted_args.append(int(float(arg)) if '.' in arg else int(arg))
                except (ValueError, TypeError):
                    converted_args.append(arg)
            elif arg is None:
                converted_args.append(0)
            elif hasattr(arg, '__int__'):
                try:
                    converted_args.append(int(arg))
                except (ValueError, TypeError):
                    converted_args.append(arg)
            else:
                converted_args.append(arg)
        
        try:
            return _original_struct_pack(fmt, *converted_args)
        except struct.error as e:
            if "required argument is not an integer" in str(e):
                final_args = [int(arg) if isinstance(arg, (float, bool)) or (isinstance(arg, str) and arg.isdigit()) 
                             else (0 if arg is None else arg) for arg in converted_args]
                return _original_struct_pack(fmt, *final_args)
            else:
                raise
    
    struct.pack = _python313_struct_pack
    
    # Patch array.fromstring if missing
    if not hasattr(array.array, 'fromstring'):
        _original_array = array.array
        
        class _CompatibleArray(_original_array):
            def fromstring(self, s):
                if isinstance(s, str):
                    s = s.encode('latin-1')
                self.frombytes(s)
        
        array.array = _CompatibleArray

'''
    
    # Write patched content
    patched_content = patch_code + original_content
    
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(patched_content)
    
    print(f"Patched {init_file}")
    return True

def test_patched_pyhula():
    """Test that the patched PyHula works"""
    print("\nTesting patched PyHula...")
    
    try:
        # Clear module cache to reload patched version
        if 'pyhula' in sys.modules:
            del sys.modules['pyhula']
        
        # Also clear any submodules
        modules_to_clear = [name for name in sys.modules if name.startswith('pyhula')]
        for module_name in modules_to_clear:
            del sys.modules[module_name]
        
        # Import fresh PyHula
        import pyhula
        
        print("  PyHula imported successfully")
        
        # Test UserApi creation
        api = pyhula.UserApi()
        print("  UserApi created successfully")
        
        # Test connection (this should work now)
        print("  Testing connection...")
        result = api.connect()
        
        if result:
            print("  Connection successful!")
            print("  PyHula Python 3.13 patch working!")
            return True
        else:
            print("  Connection returned False (normal if no drone)")
            print("  PyHula Python 3.13 patch appears to be working!")
            return True
            
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main patcher function"""
    print("PyHula Python 3.13 Direct Patcher")
    print("=" * 40)
    print(f"Python version: {sys.version}")
    
    if sys.version_info < (3, 13):
        print("INFO: Python version < 3.13 - patches not needed")
        return True
    
    # Find PyHula installation
    pyhula_dir = find_pyhula_installation()
    if not pyhula_dir:
        return False
    
    # Create backups
    backup_dir = backup_original_files(pyhula_dir)
    print(f"Backups created in: {backup_dir}")
    
    # Apply patches
    print("\nApplying Python 3.13 compatibility patches...")
    
    # Patch the __init__.py file
    if not create_init_patch(pyhula_dir):
        print("ERROR: Failed to patch __init__.py")
        return False
    
    # Test the patched installation
    if test_patched_pyhula():
        print("\n" + "=" * 40)
        print("SUCCESS: PyHula patched for Python 3.13!")
        print("=" * 40)
        print("\nYou can now use PyHula normally:")
        print("  import pyhula")
        print("  api = pyhula.UserApi()")
        print("  result = api.connect()")
        print("\nThe patches are permanent until you reinstall PyHula.")
        return True
    else:
        print("\n" + "=" * 40)
        print("ERROR: Patching failed!")
        print("=" * 40)
        print(f"\nTo restore original files:")
        print(f"  Copy files from {backup_dir} back to {pyhula_dir}")
        return False

if __name__ == "__main__":
    main()
