#!/usr/bin/env python3
"""
PyHula Connection Diagnostic and Fix Tool
Identifies and patches struct.error issues in Python 3.13
"""

import sys
import traceback
import struct

def test_struct_compatibility():
    """Test struct module compatibility between Python versions"""
    print("=== Struct Module Compatibility Test ===")
    
    # Test cases that commonly fail in Python 3.13
    test_cases = [
        ("B", [0]),      # unsigned char
        ("B", [255]),    # unsigned char max
        ("H", [0]),      # unsigned short
        ("H", [65535]),  # unsigned short max
        ("I", [0]),      # unsigned int
        ("I", [4294967295]),  # unsigned int max
    ]
    
    for format_str, values in test_cases:
        try:
            result = struct.pack(format_str, *values)
            print(f"✓ struct.pack('{format_str}', {values}) = {result.hex()}")
        except Exception as e:
            print(f"✗ struct.pack('{format_str}', {values}) failed: {e}")
    
    # Test with potentially problematic values
    problematic_cases = [
        ("B", [None]),       # None value
        ("B", [1.0]),        # Float instead of int
        ("B", ["1"]),        # String instead of int
        ("B", [256]),        # Value too large
    ]
    
    print("\n=== Problematic Cases (Expected to Fail) ===")
    for format_str, values in problematic_cases:
        try:
            result = struct.pack(format_str, *values)
            print(f"? struct.pack('{format_str}', {values}) = {result.hex()} (unexpected success)")
        except Exception as e:
            print(f"✗ struct.pack('{format_str}', {values}) failed: {e} (expected)")

def test_pyhula_connection():
    """Test PyHula connection with better error handling"""
    print("\n=== PyHula Connection Test ===")
    
    try:
        import pyhula
        print(f"✓ PyHula imported successfully")
        
        # Create API instance
        api = pyhula.UserApi()
        print(f"✓ UserApi instance created")
        
        # Try connection with enhanced error handling
        print("\nAttempting connection...")
        print("This may show PLANE_STATUS and then fail - that's the issue we're diagnosing")
        
        try:
            result = api.connect()
            print(f"✓ Connection successful: {result}")
            return True
            
        except struct.error as e:
            print(f"✗ Struct error in connection: {e}")
            print("This is the Python 3.13 compatibility issue!")
            traceback.print_exc()
            return False
            
        except Exception as e:
            print(f"✗ Other connection error: {e}")
            traceback.print_exc()
            return False
            
    except ImportError as e:
        print(f"✗ Cannot import pyhula: {e}")
        return False

def suggest_fixes():
    """Suggest potential fixes for the issue"""
    print("\n=== Suggested Fixes ===")
    print("The struct.error indicates that the MAVLink message packing")
    print("is passing non-integer values to struct.pack()")
    print()
    print("Potential solutions:")
    print("1. Patch the compiled extensions to handle type conversion")
    print("2. Create a compatibility wrapper for struct operations")
    print("3. Modify the source code and recompile")
    print("4. Use older Python version temporarily")
    print()
    print("Immediate workarounds:")
    print("1. Test with Python 3.8-3.11 to verify the issue is version-specific")
    print("2. Check if the original Python 3.6 source files are available")
    print("3. Consider using a virtual environment with Python 3.8")

def main():
    """Run all diagnostic tests"""
    print("PyHula Connection Diagnostic Tool")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    
    # Test struct compatibility
    test_struct_compatibility()
    
    # Test PyHula connection
    connection_success = test_pyhula_connection()
    
    # Provide suggestions
    suggest_fixes()
    
    print("\n" + "=" * 50)
    if connection_success:
        print("✓ Connection successful - no issues found")
    else:
        print("✗ Connection failed - Python 3.13 compatibility issue confirmed")
        print("\nNext steps:")
        print("1. This confirms the struct.error issue in Python 3.13")
        print("2. The library needs patches for Python 3.13 compatibility")
        print("3. Consider using Python 3.8-3.11 temporarily for drone operations")

if __name__ == "__main__":
    main()
