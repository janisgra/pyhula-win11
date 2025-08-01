#!/usr/bin/env python3
"""
Simple PyHula LED Test

This script tests LED commands which should always work if communication is functioning.
"""

import pyhula
import time

def test_led_commands():
    """Test LED commands to verify communication"""
    print("PyHula LED Communication Test")
    print("=" * 35)
    
    try:
        # Connect
        api = pyhula.UserApi()
        result = api.connect()
        
        if result:
            print("✓ Connected to drone")
            
            # Test LED commands (these should work regardless of flight status)
            led_tests = [
                ("Red Light", 255, 0, 0),
                ("Green Light", 0, 255, 0), 
                ("Blue Light", 0, 0, 255),
                ("White Light", 255, 255, 255),
                ("Lights Off", 0, 0, 0)
            ]
            
            print("\nTesting LED commands...")
            for name, r, g, b in led_tests:
                try:
                    print(f"Setting {name}...")
                    # Use mode 1 (solid) for 1 second
                    result = api.single_fly_lamplight(r, g, b, 1000, 1)
                    print(f"  Result: {result}")
                    time.sleep(1.5)  # Wait a bit between commands
                except Exception as e:
                    print(f"  Error: {e}")
            
            print("\n✓ LED test complete")
            print("If you saw the drone lights change, communication is working perfectly!")
            
        else:
            print("✗ Failed to connect to drone")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_led_commands()
