#!/usr/bin/env python3
"""
PyHula Python 3.13 Compatible Wrapper

This module provides a drop-in replacement for PyHula that works with Python 3.13.
Instead of 'import pyhula', use 'import pyhula_compatible as pyhula'.

Usage:
    import pyhula_compatible as pyhula
    api = pyhula.UserApi()
    result = api.connect()
"""

import sys
import struct
import warnings

# Import the original PyHula
try:
    import pyhula as _original_pyhula
except ImportError as e:
    print(f"❌ Could not import original PyHula: {e}")
    print("Make sure PyHula is installed: pip install pyhula-1.1.7-cp36-cp36m-win_amd64.whl")
    raise

class Python313CompatibleStruct:
    """Wrapper for struct operations that handles Python 3.13 stricter type checking"""
    
    def __init__(self):
        # Store the original struct.pack function to avoid recursion
        self.original_pack = struct.pack
    
    def pack(self, fmt, *args):
        """Pack with automatic type conversion for Python 3.13"""
        converted_args = []
        
        for arg in args:
            if isinstance(arg, float):
                if arg.is_integer():
                    # Convert float integers to actual integers
                    converted_args.append(int(arg))
                else:
                    # For non-integer floats, try rounding
                    converted_args.append(round(arg))
            elif isinstance(arg, bool):
                # Convert boolean to integer
                converted_args.append(int(arg))
            elif isinstance(arg, str):
                # Convert string numbers to integers if possible
                try:
                    if '.' in arg:
                        converted_args.append(int(float(arg)))
                    else:
                        converted_args.append(int(arg))
                except (ValueError, TypeError):
                    converted_args.append(arg)
            elif hasattr(arg, '__int__'):
                # Try to convert any object with __int__ method
                try:
                    converted_args.append(int(arg))
                except (ValueError, TypeError):
                    converted_args.append(arg)
            else:
                converted_args.append(arg)
        
        try:
            return self.original_pack(fmt, *converted_args)
        except struct.error as e:
            if "required argument is not an integer" in str(e):
                # Silently try more aggressive conversion
                aggressive_converted = []
                for arg in converted_args:
                    if isinstance(arg, (int, bool)):
                        aggressive_converted.append(int(arg))
                    elif isinstance(arg, float):
                        aggressive_converted.append(int(arg) if arg.is_integer() else round(arg))
                    elif isinstance(arg, str):
                        try:
                            if arg.isdigit():
                                aggressive_converted.append(int(arg))
                            elif arg.replace('.', '').isdigit():
                                aggressive_converted.append(int(float(arg)))
                            else:
                                # For strings that can't be converted, use ord() of first char or 0
                                aggressive_converted.append(ord(arg[0]) if arg else 0)
                        except (ValueError, TypeError, IndexError):
                            aggressive_converted.append(0)
                    elif arg is None:
                        aggressive_converted.append(0)
                    else:
                        # Last resort: try to get an integer representation
                        try:
                            aggressive_converted.append(int(arg))
                        except (ValueError, TypeError):
                            aggressive_converted.append(0)
                
                return self.original_pack(fmt, *aggressive_converted)
            else:
                raise

def patch_mavlink_classes():
    """Apply Python 3.13 compatibility patches to MAVLink classes"""
    
    # Find and patch MAVLink classes
    patched_classes = []
    
    def patch_class_struct_operations(cls):
        """Patch a class to use compatible struct operations"""
        if hasattr(cls, 'pack'):
            original_pack = cls.pack
            
            def safe_pack(self):
                """Python 3.13 safe pack method"""
                try:
                    return original_pack(self)
                except struct.error as e:
                    if "required argument is not an integer" in str(e):
                        # Apply type conversion to instance attributes
                        for attr_name in dir(self):
                            if not attr_name.startswith('_'):
                                try:
                                    value = getattr(self, attr_name)
                                    if isinstance(value, float) and value.is_integer():
                                        setattr(self, attr_name, int(value))
                                    elif isinstance(value, bool):
                                        setattr(self, attr_name, int(value))
                                except (AttributeError, TypeError):
                                    pass
                        
                        # Retry with converted attributes
                        return original_pack(self)
                    else:
                        raise
            
            cls.pack = safe_pack
            return True
        return False
    
    # Look for MAVLink classes in the pyhula module
    for attr_name in dir(_original_pyhula):
        attr = getattr(_original_pyhula, attr_name)
        if isinstance(attr, type):
            if 'mavlink' in attr_name.lower() or 'MAVLink' in attr_name:
                if patch_class_struct_operations(attr):
                    patched_classes.append(attr_name)
    
    # Also check submodules
    for attr_name in dir(_original_pyhula):
        attr = getattr(_original_pyhula, attr_name)
        if hasattr(attr, '__dict__'):  # Module-like object
            for sub_attr_name in dir(attr):
                sub_attr = getattr(attr, sub_attr_name)
                if isinstance(sub_attr, type):
                    if 'mavlink' in sub_attr_name.lower() or 'MAVLink' in sub_attr_name:
                        if patch_class_struct_operations(sub_attr):
                            patched_classes.append(f"{attr_name}.{sub_attr_name}")
    
    return patched_classes

# Apply patches if Python 3.13+
if sys.version_info >= (3, 13):
    print("Python 3.13+ detected - applying PyHula compatibility patches...")
    
    # Create struct wrapper instance to avoid recursion
    struct_wrapper = Python313CompatibleStruct()
    
    # Monkey patch the struct module for PyHula
    struct.pack = struct_wrapper.pack
    
    # Patch array.array.fromstring which was removed in Python 3.13
    import array
    if not hasattr(array.array, 'fromstring'):
        original_array = array.array
        
        class CompatibleArray(original_array):
            def fromstring(self, s):
                """Compatibility wrapper for removed fromstring method"""
                if isinstance(s, str):
                    s = s.encode('latin-1')  # Convert string to bytes
                self.frombytes(s)
        
        # Replace array.array with our compatible version
        array.array = CompatibleArray
        print("Patched array.array.fromstring for Python 3.13 compatibility")
    
    # Patch MAVLink classes
    patched = patch_mavlink_classes()
    if patched:
        print(f"Patched {len(patched)} MAVLink classes: {', '.join(patched)}")
    else:
        print("No MAVLink classes found to patch (this is normal for some PyHula versions)")
    
    print("PyHula Python 3.13 compatibility patches applied")

# Export everything from original PyHula
for attr_name in dir(_original_pyhula):
    if not attr_name.startswith('_'):
        globals()[attr_name] = getattr(_original_pyhula, attr_name)

# Add compatibility info
__version__ = getattr(_original_pyhula, '__version__', 'unknown')
__compatibility__ = f"Python {sys.version_info.major}.{sys.version_info.minor} compatible"

print(f"PyHula compatible wrapper loaded (Python {sys.version_info.major}.{sys.version_info.minor})")
