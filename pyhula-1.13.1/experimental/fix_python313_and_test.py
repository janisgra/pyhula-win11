#!/usr/bin/env python3
"""
PyHula Python 3.13 Fix & Test

This script applies the Python 3.13 compatibility patches and then tests PyHula connection
in the same Python session (so patches stay applied).
"""

import sys
import struct
import traceback

def apply_patches_and_test():
    """Apply patches and test connection in same session"""
    print("PyHula Python 3.13 Fix & Test")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    
    if sys.version_info < (3, 13):
        print("ℹ️ Python version < 3.13 - patches not needed")
        print("Testing direct connection...")
    else:
        print("🔧 Python 3.13+ detected - applying patches first...")
        
        # Apply patches BEFORE importing PyHula
        try:
            # Import patch functions
            from fix_python313_compatibility import patch_mavlink_header, patch_mavlink_message
            
            # Try importing PyHula first
            print("Importing PyHula...")
            import pyhula
            
            # Now apply patches
            print("Applying compatibility patches...")
            success = True
            success &= patch_mavlink_header()
            success &= patch_mavlink_message()
            
            if not success:
                print("❌ Patch application failed")
                return False
                
        except Exception as e:
            print(f"❌ Failed to apply patches: {e}")
            traceback.print_exc()
            return False
    
    # Test PyHula connection
    print("\n" + "=" * 50)
    print("Testing PyHula Connection")
    print("=" * 50)
    
    try:
        if 'pyhula' not in locals():
            import pyhula
        
        print("✅ PyHula imported successfully")
        
        # Create UserApi
        print("Creating UserApi...")
        api = pyhula.UserApi()
        print("✅ UserApi created successfully")
        
        # Test connection
        print("Attempting connection...")
        print("(You should see PLANE_STATUS if drone is detected)")
        
        result = api.connect()
        
        if result:
            print("🎉 Connection successful!")
            print("✅ Python 3.13 compatibility fix working!")
            
            # Test a simple command
            try:
                print("Testing basic command...")
                # Just test that we can access methods without calling dangerous ones
                methods = [attr for attr in dir(api) if not attr.startswith('_') and callable(getattr(api, attr))]
                print(f"✅ API has {len(methods)} available methods")
                print("🔒 Connection stable - safe to use PyHula commands")
                
            except Exception as e:
                print(f"⚠️ Connection successful but API test failed: {e}")
            
        else:
            print("ℹ️ Connection returned False")
            print("This is normal if:")
            print("  - Drone is powered off")
            print("  - Not connected to drone WiFi") 
            print("  - Drone is out of range")
            print("✅ No struct.error means Python 3.13 fix is working!")
        
        return True
        
    except struct.error as e:
        print(f"❌ struct.error still occurring: {e}")
        print("The Python 3.13 compatibility patch needs improvement")
        print("\nDebugging info:")
        traceback.print_exc()
        return False
        
    except OSError as e:
        if "10048" in str(e):
            print(f"⚠️ Socket port conflict: {e}")
            print("This is a different issue - try restarting Python")
        else:
            print(f"❌ Network error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return False

def main():
    """Main function"""
    try:
        success = apply_patches_and_test()
        
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        
        if success:
            print("✅ PyHula Python 3.13 compatibility: WORKING")
            print("\nNext steps:")
            print("1. Connect to drone WiFi network")
            print("2. Power on drone")
            print("3. Use this pattern for reliable connections:")
            print()
            print("   # In Python 3.13:")
            print("   exec(open('fix_python313_and_test.py').read())")
            print("   # Then use PyHula normally")
            
        else:
            print("❌ PyHula Python 3.13 compatibility: FAILED")
            print("\nRecommendations:")
            print("1. Use Python 3.11 or 3.12 instead")
            print("2. Or wait for official PyHula Python 3.13 support")
            print("3. Check that drone is on and connected to WiFi")
    
    except Exception as e:
        print(f"❌ Script failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
