#!/usr/bin/env python3
"""
Python 3.13 Array Compatibility Patch for PyHula
Fixes array.fromstring() deprecation in Python 3.13
"""

import array
import sys
import builtins

def patch_array_module():
    """
    Patch array module to restore fromstring() method for Python 3.13 compatibility
    
    In Python 3.9+, array.fromstring() was deprecated and removed in Python 3.13.
    It was replaced with array.frombytes(). This patch adds backward compatibility
    by replacing the array.array class with a compatible version.
    """
    print("Applying Python 3.13 array compatibility patch...")
    
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
            
            Args:
                s: String or bytes to convert to array
            """
            if isinstance(s, str):
                # Convert string to bytes using latin-1 encoding (preserves byte values)
                s = s.encode('latin-1')
            return self.frombytes(s)
    
    # Replace the array.array class
    array.array = CompatibleArray
    print("✓ Replaced array.array with compatible version")

def test_array_patch():
    """Test the array compatibility patch"""
    print("\n=== Testing Array Patch ===")
    
    # Test with bytes
    arr = array.array('B')  # unsigned char array
    test_bytes = b'\x01\x02\x03\x04'
    arr.fromstring(test_bytes)
    print(f"✓ fromstring with bytes: {list(arr)}")
    
    # Test with string (legacy behavior)
    arr2 = array.array('B')
    test_string = '\x01\x02\x03\x04'  # String with byte values
    arr2.fromstring(test_string)
    print(f"✓ fromstring with string: {list(arr2)}")
    
    # Verify compatibility
    arr3 = array.array('B')
    arr3.frombytes(test_bytes)
    print(f"✓ frombytes comparison: {list(arr3)}")
    
    assert list(arr) == list(arr2) == list(arr3), "Compatibility test failed"
    print("✓ All array compatibility tests passed")

if __name__ == "__main__":
    patch_array_module()
    test_array_patch()
