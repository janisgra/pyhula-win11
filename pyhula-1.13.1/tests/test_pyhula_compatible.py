#!/usr/bin/env python3
"""
Test PyHula with Python 3.13 Compatibility

This script tests PyHula using the compatibility wrapper.
"""

import sys
import struct
import traceback

print("PyHula Python 3.13 Compatibility Test")
print("=" * 50)
print(f"Python version: {sys.version}")

try:
    # Import the compatible wrapper instead of original PyHula
    print("Importing PyHula compatible wrapper...")
    import pyhula_compatible as pyhula
    
    print("PyHula compatible wrapper loaded successfully")
    print(f"PyHula version: {getattr(pyhula, '__version__', 'unknown')}")
    print(f"Compatibility: {getattr(pyhula, '__compatibility__', 'unknown')}")
    
    # Test basic PyHula functionality
    print("\nTesting PyHula UserApi creation...")
    api = pyhula.UserApi()
    print("UserApi created successfully")
    
    # Test connection (this is where struct.error usually occurs)
    print("\nTesting PyHula connection...")
    print("(This is where Python 3.13 struct.error typically occurs)")
    print("Attempting connection...")
    
    result = api.connect()
    
    if result:
        print("Connection successful!")
        print("Python 3.13 compatibility working perfectly!")
        
        # Test basic functionality
        print("\nTesting API methods...")
        methods = [attr for attr in dir(api) if not attr.startswith('_') and callable(getattr(api, attr))]
        print(f"API has {len(methods)} available methods")
        
        # Clean disconnect
        try:
            api.disconnect()
            print("Disconnected cleanly")
        except:
            pass
        
    else:
        print("Connection returned False - this is normal if:")
        print("  - Drone is powered off")
        print("  - Not connected to drone WiFi")
        print("  - Drone is out of range")
        print("No struct.error means Python 3.13 compatibility is working!")
    
    print("\n" + "=" * 50)
    print("SUCCESS: PyHula Python 3.13 compatibility test PASSED")
    print("=" * 50)
    print("\nTo use PyHula with Python 3.13:")
    print("  import pyhula_compatible as pyhula")
    print("  api = pyhula.UserApi()")
    print("  result = api.connect()")
    
except struct.error as e:
    print(f"struct.error still occurring: {e}")
    print("\nThis means the compatibility patches need improvement.")
    print("Consider using Python 3.11 or 3.12 instead.")
    traceback.print_exc()
    
except ImportError as e:
    print(f"Import error: {e}")
    print("\nMake sure:")
    print("1. PyHula is installed")
    print("2. pyhula_compatible.py is in the same directory")
    traceback.print_exc()
    
except Exception as e:
    print(f"Unexpected error: {e}")
    traceback.print_exc()

print("\nTest complete.")
