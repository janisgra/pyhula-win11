#!/usr/bin/env python3
"""
PyHula Python 3.13 Example Usage
Demonstrates how to use PyHula with Python 3.13
"""

# Easy method - use the integrated module
import pyhula_py313

def main():
    """Simple PyHula usage example"""
    print("PyHula Python 3.13 Example")
    print("=" * 30)
    
    # Create API instance (compatibility patches applied automatically)
    api = pyhula_py313.create_api()
    
    # Connect to drone
    print("Connecting to drone...")
    if api.connect():
        print("✅ Connected to drone!")
        
        # Example: Get drone status
        try:
            # List available methods
            methods = [m for m in dir(api) if not m.startswith('_') and callable(getattr(api, m))]
            print(f"\n📋 Available methods ({len(methods)}):")
            for i, method in enumerate(methods[:10]):  # Show first 10
                print(f"  {i+1:2d}. {method}")
            if len(methods) > 10:
                print(f"      ... and {len(methods) - 10} more")
                
            print("\n🎮 Ready for drone commands!")
            print("Examples:")
            print("  - api.Plane_takeoff()              # Take off")
            print("  - api.Plane_landing()              # Land")
            print("  - api.Plane_goto(x, y, z)          # Move to position")
            print("  - api.Plane_cmd_switch_video(1)    # Enable video")
            
        except Exception as e:
            print(f"⚠ Error accessing drone methods: {e}")
            
    else:
        print("⚠ No drone detected (this is normal without hardware)")
        print("✅ API created successfully - ready to use when drone is connected")

if __name__ == "__main__":
    main()
