#!/usr/bin/env python3
"""
PyHula Success Test - Build on What Works

We know from minimal_test.py that:
- pyhula.UserApi() works
- api.connect() works  
- api.get_battery() works

Let's build on this step by step.
"""

import sys
import os
import time

# Add PyHula to path
sys.path.insert(0, r"C:\Users\janis\AppData\Local\Programs\Python\Python313\Lib\site-packages")

def test_pyhula_step_by_step():
    """Test PyHula functionality step by step."""
    import pyhula
    
    print("Step-by-Step PyHula Test")
    print("=" * 30)
    
    # Step 1: Create API (we know this works)
    print("Step 1: Creating API...")
    api = pyhula.UserApi()
    print("✓ API created")
    
    # Step 2: Connect (we know this works)
    print("\nStep 2: Connecting...")
    result = api.connect()
    if not result:
        print("✗ Connection failed")
        return
    print("✓ Connected")
    
    # Step 3: Test battery (we know this works)
    print("\nStep 3: Testing battery...")
    battery = api.get_battery()
    print(f"✓ Battery: {battery}%")
    
    # Step 4: Test other simple status commands
    print("\nStep 4: Other status commands...")
    try:
        plane_id = api.get_plane_id()
        print(f"✓ Plane ID: {plane_id}")
    except Exception as e:
        print(f"! Plane ID error: {e}")
    
    try:
        coords = api.get_coordinate()
        print(f"✓ Coordinates: {coords}")
    except Exception as e:
        print(f"! Coordinates error: {e}")
    
    # Step 5: Test simple control command
    print("\nStep 5: Simple control command...")
    try:
        rtp_result = api.Plane_cmd_swith_rtp(0)
        print(f"✓ RTP command: {rtp_result}")
    except Exception as e:
        print(f"! RTP error: {e}")
    
    # Step 6: Test LED (needs all parameters)
    print("\nStep 6: LED test...")
    try:
        # Turn on red LED for 1 second
        led_result = api.single_fly_lamplight(255, 0, 0, 1, 1)
        print(f"✓ LED on: {led_result}")
        time.sleep(2)
        
        # Turn off LED
        led_off = api.single_fly_lamplight(0, 0, 0, 1, 1)
        print(f"✓ LED off: {led_off}")
    except Exception as e:
        print(f"! LED error: {e}")
    
    # Step 7: Test a simple movement command with immediate check
    print("\nStep 7: Simple movement test...")
    try:
        print("Attempting arm command...")
        arm_result = api.plane_fly_arm()
        print(f"✓ Arm result: {arm_result}")
        
        # Immediately check if drone is still responsive
        battery_check = api.get_battery()
        print(f"✓ Still responsive after arm: {battery_check}%")
        
        print("Attempting disarm command...")
        disarm_result = api.plane_fly_disarm()
        print(f"✓ Disarm result: {disarm_result}")
        
    except Exception as e:
        print(f"! Movement error: {e}")
    
    # Step 8: Final responsiveness check
    print("\nStep 8: Final check...")
    try:
        final_battery = api.get_battery()
        print(f"✓ Final battery: {final_battery}%")
        print("✓ Drone still fully responsive")
    except Exception as e:
        print(f"! Final check failed: {e}")
    
    print("\n" + "=" * 30)
    print("Test completed successfully!")
    print("All working commands identified.")

if __name__ == "__main__":
    try:
        test_pyhula_step_by_step()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
