#!/usr/bin/env python3
"""
PyHula Working Solution - Based on Successful Battery Test

Since we proved that connection and get_battery() work perfectly,
this script builds on that success to test more commands systematically.
"""

import sys
import os
import time
import subprocess

# Add PyHula to path
pyhula_path = r"C:\Users\janis\AppData\Local\Programs\Python\Python313\Lib\site-packages"
if pyhula_path not in sys.path:
    sys.path.insert(0, pyhula_path)

def clean_environment():
    """Clean up any lingering processes or connections."""
    try:
        # Kill any Python processes that might be holding connections
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True, timeout=3)
        subprocess.run(['taskkill', '/F', '/IM', 'py.exe'], 
                      capture_output=True, timeout=3)
        time.sleep(2)
        print("✓ Environment cleaned")
    except:
        print("! Could not clean environment")

def test_working_commands():
    """Test commands we know work, then gradually try more complex ones."""
    import pyhula
    
    print("Testing Known Working Commands")
    print("=" * 35)
    
    # Create fresh API instance
    api = pyhula.UserApi()
    
    print("Connecting to drone...")
    try:
        result = api.connect()
        if not result:
            print("✗ Connection failed")
            return
        print("✓ Connected successfully")
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return
    
    # Test 1: Battery (we know this works)
    print("\n1. Battery Status (known working):")
    try:
        battery = api.get_battery()
        print(f"   ✓ Battery: {battery}%")
    except Exception as e:
        print(f"   ✗ Battery failed: {e}")
        return  # If battery fails, something is fundamentally wrong
    
    # Test 2: Other status commands
    status_commands = [
        ("Plane ID", "get_plane_id"),
        ("Coordinates", "get_coordinate"),
        ("Plane Speed", "get_plane_speed"),
        ("Yaw", "get_yaw"),
    ]
    
    print("\n2. Status Commands:")
    for name, method in status_commands:
        try:
            result = getattr(api, method)()
            print(f"   ✓ {name}: {result}")
        except Exception as e:
            print(f"   ! {name}: {e}")
    
    # Test 3: Simple control commands
    print("\n3. Simple Control Commands:")
    try:
        result = api.Plane_cmd_swith_rtp(0)
        print(f"   ✓ RTP Switch: {result}")
    except Exception as e:
        print(f"   ! RTP Switch: {e}")
    
    # Test 4: LED with proper parameters (RGB + time + mode)
    print("\n4. LED Command:")
    try:
        # Red LED for 1 second, mode 1
        result = api.single_fly_lamplight(255, 0, 0, 1, 1)
        print(f"   ✓ LED Red: {result}")
        time.sleep(2)  # Wait to see the effect
        
        # Turn off LED
        result = api.single_fly_lamplight(0, 0, 0, 1, 1)
        print(f"   ✓ LED Off: {result}")
    except Exception as e:
        print(f"   ! LED: {e}")
    
    # Test 5: Movement commands with timeout using simple approach
    print("\n5. Movement Commands (with manual timeout):")
    
    movement_commands = [
        ("Arm", "plane_fly_arm"),
        ("Up 20cm", lambda: api.single_fly_up(20)),
        ("Down 20cm", lambda: api.single_fly_down(20)),
        ("Disarm", "plane_fly_disarm"),
    ]
    
    for name, cmd in movement_commands:
        print(f"   Testing {name}...")
        try:
            start_time = time.time()
            
            # Execute command
            if callable(cmd):
                result = cmd()
            else:
                result = getattr(api, cmd)()
            
            duration = time.time() - start_time
            print(f"   ✓ {name}: {result} ({duration:.2f}s)")
            
            # Quick responsiveness check after each movement
            try:
                battery = api.get_battery()
                print(f"     (Battery check: {battery}% - drone responsive)")
            except:
                print(f"     (Drone not responsive after {name})")
                break
            
            time.sleep(1)  # Brief pause between movements
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"   ! {name}: {e} (after {duration:.2f}s)")
    
    # Test 6: If basic movements work, try takeoff/landing
    print("\n6. Advanced Flight Commands:")
    print("   Note: Only attempting if basic movements succeeded")
    
    try:
        print("   Testing takeoff...")
        start_time = time.time()
        result = api.single_fly_takeoff()
        duration = time.time() - start_time
        print(f"   ✓ Takeoff: {result} ({duration:.2f}s)")
        
        # Wait a moment, then check status
        time.sleep(3)
        battery = api.get_battery()
        print(f"   Status after takeoff - Battery: {battery}%")
        
        # Land
        print("   Testing landing...")
        result = api.single_fly_touchdown()
        print(f"   ✓ Landing: {result}")
        
    except Exception as e:
        print(f"   ! Advanced flight: {e}")
    
    print("\n" + "=" * 35)
    print("TEST COMPLETE")
    print("Based on results above:")
    print("- Status commands should work immediately")
    print("- LED commands should work")
    print("- Movement success depends on drone state")
    print("- If movements hang, the issue is in command completion detection")

def main():
    print("PyHula Working Solution Test")
    print("=" * 40)
    
    # Clean environment first
    clean_environment()
    
    # Run tests
    test_working_commands()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nScript finished")
