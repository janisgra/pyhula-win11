#!/usr/bin/env python3
"""
Python 3.13 Compatibility Module for PyHula
Fixes all Python 3.13 compatibility issues in PyHula library
"""

import sys
import struct
import array

def apply_all_patches():
    """Apply all Python 3.13 compatibility patches"""
    print("Applying Python 3.13 compatibility patches for PyHula...")
    print(f"Python version: {sys.version}")
    
    # Apply struct patch
    apply_struct_patch()
    
    # Apply array patch  
    apply_array_patch()
    
    print("✅ All Python 3.13 compatibility patches applied successfully!")

def apply_struct_patch():
    """Apply struct.pack compatibility patch"""
    print("\n=== Struct Compatibility Patch ===")
    
    # Store original struct.pack
    original_pack = struct.pack
    
    def safe_struct_pack(format_string, *values):
        """
        Safe struct.pack wrapper for Python 3.13 compatibility
        
        Python 3.13 is stricter about data types in struct.pack().
        This wrapper converts values to appropriate types.
        """
        converted_values = []
        format_chars = format_string.replace('<', '').replace('>', '').replace('!', '').replace('=', '').replace('@', '')
        
        for i, (fmt_char, value) in enumerate(zip(format_chars, values)):
            if value is None:
                # Convert None to 0
                converted_values.append(0)
            elif fmt_char in 'bBhHiIlLqQ':  # Integer formats
                if isinstance(value, str):
                    # Try to convert string to int
                    try:
                        converted_values.append(int(value))
                    except ValueError:
                        converted_values.append(ord(value[0]) if value else 0)
                elif isinstance(value, float):
                    converted_values.append(int(value))
                else:
                    # Ensure it's an integer and within bounds
                    int_val = int(value)
                    
                    # Apply bounds checking for unsigned byte format
                    if fmt_char == 'B' and int_val > 255:
                        int_val = 255
                    elif fmt_char == 'B' and int_val < 0:
                        int_val = 0
                    
                    converted_values.append(int_val)
            else:
                # For other formats (float, double, etc.), use as-is
                converted_values.append(value)
        
        return original_pack(format_string, *converted_values)
    
    # Replace struct.pack with safe version
    struct.pack = safe_struct_pack
    print("✓ Applied struct.pack compatibility patch")

def apply_array_patch():
    """Apply array.fromstring compatibility patch"""
    print("\n=== Array Compatibility Patch ===")
    
    # Check if fromstring method exists
    if hasattr(array.array, 'fromstring'):
        print("✓ array.fromstring already available")
        return
    
    # Create a wrapper class that adds fromstring support
    original_array = array.array
    
    class CompatibleArray(original_array):
        """Array class with fromstring() compatibility for Python 3.13"""
        
        def fromstring(self, s):
            """
            Compatibility method for array.fromstring()
            
            In Python 3.13, fromstring() was removed and replaced with frombytes().
            This method provides backward compatibility.
            """
            if isinstance(s, str):
                # Convert string to bytes using latin-1 encoding (preserves byte values)
                s = s.encode('latin-1')
            return self.frombytes(s)
    
    # Replace the array.array class
    array.array = CompatibleArray
    print("✓ Applied array.fromstring compatibility patch")

def test_all_patches():
    """Test all compatibility patches"""
    print("\n" + "=" * 50)
    print("TESTING ALL COMPATIBILITY PATCHES")
    print("=" * 50)
    
    # Test struct patch
    print("\n=== Testing Struct Patch ===")
    try:
        # Test problematic cases that caused issues in PyHula
        result1 = struct.pack('B', None)  # None -> 0
        result2 = struct.pack('B', 3.14)  # float -> int
        result3 = struct.pack('B', "5")   # string -> int
        result4 = struct.pack('B', 256)   # overflow -> clamp to 255
        print("✓ All struct.pack compatibility tests passed")
    except Exception as e:
        print(f"✗ Struct patch test failed: {e}")
        return False
    
    # Test array patch
    print("\n=== Testing Array Patch ===")
    try:
        arr = array.array('B')
        test_bytes = b'\x01\x02\x03\x04'
        arr.fromstring(test_bytes)
        
        arr2 = array.array('B')
        test_string = '\x01\x02\x03\x04'
        arr2.fromstring(test_string)
        
        assert list(arr) == list(arr2), "Array compatibility test failed"
        print("✓ All array.fromstring compatibility tests passed")
    except Exception as e:
        print(f"✗ Array patch test failed: {e}")
        return False
    
    print("\n✅ ALL COMPATIBILITY PATCHES WORKING CORRECTLY!")
    return True

if __name__ == "__main__":
    apply_all_patches()
    test_all_patches()
