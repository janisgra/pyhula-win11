#!/usr/bin/env python3
"""
PyHula Python 3.13 Compatibility Patch

This script patches PyHula to work with Python 3.13's stricter struct.pack() requirements.
The issue is that Python 3.13 no longer accepts floats where integers are expected in struct.pack().

Run this once after importing pyhula to apply the compatibility patches.
"""

import sys
import struct
import traceback

def patch_mavlink_header():
    """Patch MAVLink header for Python 3.13 compatibility"""
    try:
        # Import the problematic module
        import pyhula.pypack.fylo.mavlink as mavlink_module
        
        print("Patching MAVLink for Python 3.13 compatibility...")
        
        # Get the MAVLink_header class
        if not hasattr(mavlink_module, 'MAVLink_header'):
            print("[ERROR] MAVLink_header class not found")
            return False
        
        header_class = mavlink_module.MAVLink_header
        
        # Store original pack method
        if not hasattr(header_class, '_original_pack'):
            header_class._original_pack = header_class.pack
        
        def safe_pack(self):
            """Python 3.13 compatible pack method"""
            try:
                # Debug: Print what we're working with
                print(f"[DEBUG] Header pack called with: {dir(self)}")
                
                # Common MAVLink header attributes - ensure they're integers
                attr_names = ['msgid', 'len', 'seq', 'sysid', 'compid', 'msgid2', 'start']
                
                for name in attr_names:
                    if hasattr(self, name):
                        val = getattr(self, name)
                        print(f"[DEBUG] {name} = {val} (type: {type(val)})")
                        
                        # Convert to int, handling various types
                        if isinstance(val, (int, float)):
                            new_val = int(val)
                        elif isinstance(val, str) and val.replace('.', '').replace('-', '').isdigit():
                            new_val = int(float(val))  # Handle string floats
                        elif val is None:
                            new_val = 0
                        else:
                            print(f"[WARNING] Unknown type for {name}: {val} ({type(val)})")
                            new_val = 0
                        
                        setattr(self, name, new_val)
                        print(f"[DEBUG] {name} converted to {new_val}")
                
                # Call original pack method with fixed attributes
                return self._original_pack()
                
            except Exception as e:
                print(f"[ERROR] safe_pack failed: {e}")
                print(f"Self attributes: {[(k, getattr(self, k, 'N/A'), type(getattr(self, k, None))) for k in dir(self) if not k.startswith('_')]}")
                traceback.print_exc()
                raise
        
        # Apply the patch
        header_class.pack = safe_pack
        print("✅ MAVLink_header.pack() patched for Python 3.13")
        return True
        
    except ImportError as e:
        print(f"[ERROR] Could not import MAVLink module: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to patch MAVLink_header: {e}")
        traceback.print_exc()
        return False

def patch_mavlink_message():
    """Patch general MAVLink message packing"""
    try:
        import pyhula.pypack.fylo.mavlink as mavlink_module
        
        # Find MAVLink_message class
        if not hasattr(mavlink_module, 'MAVLink_message'):
            print("[WARNING] MAVLink_message class not found")
            return True  # Not critical
        
        message_class = mavlink_module.MAVLink_message
        
        # Store original pack method
        if not hasattr(message_class, '_original_pack'):
            message_class._original_pack = message_class.pack
        
        def safe_message_pack(self):
            """Python 3.13 compatible message pack method"""
            try:
                # Ensure all numeric attributes are proper integers/floats
                for attr_name in dir(self):
                    if not attr_name.startswith('_'):
                        attr_val = getattr(self, attr_name)
                        if isinstance(attr_val, (int, float)):
                            # Keep as-is, but ensure it's the right type
                            continue
                        elif isinstance(attr_val, str) and attr_val.replace('.', '').replace('-', '').isdigit():
                            # Convert numeric strings
                            if '.' in attr_val:
                                setattr(self, attr_name, float(attr_val))
                            else:
                                setattr(self, attr_name, int(attr_val))
                
                # Call original pack method
                return self._original_pack()
                
            except Exception as e:
                print(f"[ERROR] safe_message_pack failed: {e}")
                raise
        
        # Apply the patch
        message_class.pack = safe_message_pack
        print("✅ MAVLink_message.pack() patched for Python 3.13")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to patch MAVLink_message: {e}")
        return False

def patch_struct_operations():
    """Patch any other struct operations in PyHula"""
    try:
        # This is a more aggressive patch - monkey patch struct.pack itself
        # Only for PyHula's use
        
        original_struct_pack = struct.pack
        
        def safe_struct_pack(fmt, *args):
            """Struct pack that converts floats to ints when needed for integer formats"""
            try:
                # For formats that expect integers, convert floats
                safe_args = []
                
                # Parse format string to see what types are expected
                fmt_chars = fmt.replace('<', '').replace('>', '').replace('!', '').replace('@', '').replace('=', '')
                
                for i, (fmt_char, arg) in enumerate(zip(fmt_chars, args)):
                    if fmt_char in 'bBhHiIlLqQ':  # Integer formats
                        if isinstance(arg, float):
                            safe_args.append(int(arg))
                        elif isinstance(arg, str) and arg.isdigit():
                            safe_args.append(int(arg))
                        else:
                            safe_args.append(arg)
                    else:
                        safe_args.append(arg)
                
                return original_struct_pack(fmt, *safe_args)
                
            except Exception:
                # Fallback to original
                return original_struct_pack(fmt, *args)
        
        # Only patch if we're in PyHula context
        import sys
        if any('pyhula' in str(frame) for frame in traceback.extract_stack()):
            struct.pack = safe_struct_pack
            print("✅ struct.pack() patched for PyHula Python 3.13 compatibility")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to patch struct operations: {e}")
        return False

def apply_all_patches():
    """Apply all necessary patches for Python 3.13 compatibility"""
    print(f"Applying PyHula Python 3.13 compatibility patches...")
    print(f"Python version: {sys.version}")
    
    if sys.version_info >= (3, 13):
        print("✅ Python 3.13+ detected - applying compatibility patches")
        
        success = True
        success &= patch_mavlink_header()
        success &= patch_mavlink_message()
        # success &= patch_struct_operations()  # Commented out - too aggressive
        
        if success:
            print("✅ All patches applied successfully!")
            print("\nYou can now use PyHula:")
            print("  import pyhula")
            print("  api = pyhula.UserApi()")
            print("  api.connect()")
        else:
            print("❌ Some patches failed - PyHula may still have issues")
        
        return success
    else:
        print(f"ℹ️ Python {sys.version_info.major}.{sys.version_info.minor} - patches not needed")
        return True

if __name__ == "__main__":
    apply_all_patches()
