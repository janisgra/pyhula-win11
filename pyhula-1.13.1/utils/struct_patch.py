#!/usr/bin/env python3
"""
PyHula Python 3.13 Compatibility Patch
Patches struct operations for Python 3.13 compatibility
"""

import struct
import sys
from typing import Any

# Store original struct.pack for fallback
_original_struct_pack = struct.pack

def safe_struct_pack(format_str: str, *args) -> bytes:
    """
    Safe wrapper for struct.pack that handles Python 3.13 type strictness
    Automatically converts values to appropriate integer types
    """
    try:
        # Try original pack first
        return _original_struct_pack(format_str, *args)
    except (struct.error, TypeError) as e:
        if "required argument is not an integer" in str(e) or "format requires" in str(e):
            # Convert arguments to appropriate types
            converted_args = []
            
            # Parse format string to understand expected types
            format_chars = [c for c in format_str if c in 'BbHhIiLlQqfd']
            
            for i, arg in enumerate(args):
                format_char = format_chars[i] if i < len(format_chars) else format_chars[-1] if format_chars else 'B'
                
                # Convert to integer first
                if arg is None:
                    int_arg = 0
                elif isinstance(arg, float):
                    int_arg = int(arg)
                elif isinstance(arg, str):
                    try:
                        int_arg = int(arg)
                    except ValueError:
                        int_arg = 0
                elif hasattr(arg, '__int__'):
                    int_arg = int(arg)
                else:
                    int_arg = 0 if not isinstance(arg, int) else arg
                
                # Apply bounds checking based on format character
                if format_char == 'B':  # unsigned char 0-255
                    int_arg = max(0, min(255, int_arg))
                elif format_char == 'b':  # signed char -128 to 127
                    int_arg = max(-128, min(127, int_arg))
                elif format_char == 'H':  # unsigned short 0-65535
                    int_arg = max(0, min(65535, int_arg))
                elif format_char == 'h':  # signed short -32768 to 32767
                    int_arg = max(-32768, min(32767, int_arg))
                elif format_char in 'IL':  # unsigned int/long 0 to 4294967295
                    int_arg = max(0, min(4294967295, int_arg))
                elif format_char in 'il':  # signed int/long
                    int_arg = max(-2147483648, min(2147483647, int_arg))
                elif format_char == 'Q':  # unsigned long long
                    int_arg = max(0, min(18446744073709551615, int_arg))
                elif format_char == 'q':  # signed long long
                    int_arg = max(-9223372036854775808, min(9223372036854775807, int_arg))
                
                converted_args.append(int_arg)
            
            # Try again with converted and bounded arguments
            return _original_struct_pack(format_str, *converted_args)
        else:
            # Re-raise other struct errors
            raise

def patch_struct_module():
    """Apply the struct compatibility patch"""
    struct.pack = safe_struct_pack
    print("✓ Applied Python 3.13 struct compatibility patch")

def unpatch_struct_module():
    """Remove the struct compatibility patch"""
    struct.pack = _original_struct_pack
    print("✓ Removed struct compatibility patch")

def test_patch():
    """Test the compatibility patch"""
    print("=== Testing Struct Compatibility Patch ===")
    
    # Apply patch
    patch_struct_module()
    
    # Test cases that would fail in Python 3.13
    test_cases = [
        ("B", [None]),       # None value
        ("B", [1.0]),        # Float instead of int  
        ("B", ["1"]),        # String instead of int
        ("B", [256]),        # Value too large (should be clamped)
        ("B", [-1]),         # Negative value (should be clamped)
    ]
    
    for format_str, values in test_cases:
        try:
            result = struct.pack(format_str, *values)
            print(f"✓ struct.pack('{format_str}', {values}) = {result.hex()}")
        except Exception as e:
            print(f"✗ struct.pack('{format_str}', {values}) failed: {e}")
    
    # Remove patch
    unpatch_struct_module()

def main():
    """Main function for testing"""
    print("PyHula Python 3.13 Struct Compatibility Patch")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    
    test_patch()
    
    print("\n" + "=" * 50)
    print("To use this patch:")
    print("1. Import this module before importing pyhula")
    print("2. Call patch_struct_module()")
    print("3. Use pyhula normally")
    print("\nExample:")
    print("  import struct_patch")
    print("  struct_patch.patch_struct_module()")
    print("  import pyhula")
    print("  api = pyhula.UserApi()")
    print("  api.connect()")

if __name__ == "__main__":
    main()
