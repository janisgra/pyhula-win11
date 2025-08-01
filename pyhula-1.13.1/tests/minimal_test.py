#!/usr/bin/env python3
"""
Minimal PyHula Test - Debug Version
"""

import sys
import os

# Add PyHula to path
pyhula_path = r"C:\Users\janis\AppData\Local\Programs\Python\Python313\Lib\site-packages"
if pyhula_path not in sys.path:
    sys.path.insert(0, pyhula_path)

print("Python version:", sys.version)
print("Python path includes:")
for p in sys.path[:5]:  # First 5 paths
    print(f"  {p}")

try:
    print("\nTrying to import pyhula...")
    import pyhula
    print("✓ pyhula imported successfully")
    
    print("\nTrying to create UserApi...")
    api = pyhula.UserApi()
    print("✓ UserApi created successfully")
    
    print("\nTrying to connect...")
    result = api.connect()
    print(f"Connect result: {result}")
    
    if result:
        print("✓ Connection successful!")
        
        print("\nTrying to get battery...")
        battery = api.get_battery()
        print(f"Battery: {battery}")
    else:
        print("✗ Connection failed")

except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete")
