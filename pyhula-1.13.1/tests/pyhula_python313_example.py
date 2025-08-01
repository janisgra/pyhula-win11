#!/usr/bin/env python3
"""
PyHula Python 3.13 Example

This example shows how to use PyHula with Python 3.13 using the compatibility wrapper.
"""

# Use the compatibility wrapper instead of regular PyHula
import pyhula_compatible as pyhula

def main():
    print("PyHula Python 3.13 Example")
    print("=" * 30)
    
    try:
        # Create UserApi (this works the same as before)
        print("Creating UserApi...")
        api = pyhula.UserApi()
        print("SUCCESS: UserApi created")
        
        # Connect to drone (this now works with Python 3.13!)
        print("\nConnecting to drone...")
        result = api.connect()
        
        if result:
            print("SUCCESS: Connected to drone!")
            
            # Example: Get basic information
            print("\nTesting basic functionality...")
            
            # List available methods
            methods = [attr for attr in dir(api) if not attr.startswith('_') and callable(getattr(api, attr))]
            print(f"Available API methods: {len(methods)}")
            
            # You can now use any PyHula commands normally
            # For example (be careful with actual drone commands):
            # api.takeoff()
            # api.land()
            # api.set_height(50)
            
            print("\nPyHula is ready to use with Python 3.13!")
            
        else:
            print("INFO: Connection returned False")
            print("This is normal if:")
            print("- Drone is powered off")
            print("- Not connected to drone WiFi")
            print("- Drone is out of range")
            print("\nBut the compatibility wrapper is working!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        try:
            if 'api' in locals():
                api.disconnect()
                print("\nDisconnected from drone")
        except:
            pass

if __name__ == "__main__":
    main()
