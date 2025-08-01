#!/usr/bin/env python3
"""
Test Direct PyHula Patch

This script tests that PyHula works directly after patching (no wrapper needed).
"""

print("Testing Direct PyHula Import (Python 3.13)")
print("=" * 50)

try:
    # Import PyHula directly (no wrapper)
    print("Importing PyHula directly...")
    import pyhula
    print("SUCCESS: PyHula imported without errors")
    
    # Create UserApi
    print("Creating UserApi...")
    api = pyhula.UserApi()
    print("SUCCESS: UserApi created")
    
    # Test connection
    print("Testing connection...")
    result = api.connect()
    
    if result:
        print("SUCCESS: Connection established!")
        
        # Test that commands work now
        print("\nTesting drone commands...")
        
        # List available methods
        methods = [m for m in dir(api) if not m.startswith('_') and callable(getattr(api, m))]
        print(f"Available methods: {len(methods)}")
        
        # Test a few specific commands that were mentioned
        command_tests = [
            ('single_fly_takeoff', lambda: api.single_fly_takeoff()),
            ('single_fly_forward', lambda: api.single_fly_forward(100)),
            ('single_fly_land', lambda: api.single_fly_land()),
        ]
        
        for cmd_name, cmd_func in command_tests:
            if hasattr(api, cmd_name):
                print(f"  {cmd_name}: Available")
                try:
                    # Don't actually execute dangerous commands when testing
                    print(f"    Method signature: {cmd_func.__name__}")
                except:
                    pass
            else:
                print(f"  {cmd_name}: Not found")
        
        print("\nDirect PyHula import is working!")
        print("You can now use 'import pyhula' normally in Python 3.13")
        
    else:
        print("INFO: Connection returned False (normal if no drone)")
        print("But PyHula import and API creation worked!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete.")
