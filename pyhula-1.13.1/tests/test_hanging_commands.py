#!/usr/bin/env python3
"""
Test Specific Hanging Commands

Now that we know basic PyHula functionality works perfectly,
let's test the specific commands that were hanging before.
"""

import sys
import time
import threading

sys.path.insert(0, r"C:\Users\janis\AppData\Local\Programs\Python\Python313\Lib\site-packages")

def test_with_timeout(func, timeout_seconds=10):
    """Execute a function with a timeout."""
    result = {'value': None, 'error': None, 'completed': False}
    
    def target():
        try:
            result['value'] = func()
            result['completed'] = True
        except Exception as e:
            result['error'] = e
            result['completed'] = True
    
    thread = threading.Thread(target=target, daemon=True)
    start_time = time.time()
    thread.start()
    thread.join(timeout_seconds)
    duration = time.time() - start_time
    
    if result['completed']:
        if result['error']:
            return f"ERROR: {result['error']} ({duration:.2f}s)"
        else:
            return f"SUCCESS: {result['value']} ({duration:.2f}s)"
    else:
        return f"TIMEOUT after {duration:.2f}s"

def test_previously_hanging_commands():
    """Test the commands that were hanging in previous tests."""
    import pyhula
    
    print("Testing Previously Hanging Commands")
    print("=" * 40)
    
    # Connect
    api = pyhula.UserApi()
    if not api.connect():
        print("Failed to connect")
        return
    
    print("✓ Connected")
    print(f"✓ Battery: {api.get_battery()}%")
    
    # Test the commands that were problematic
    hanging_commands = [
        ("Takeoff", lambda: api.single_fly_takeoff()),
        ("Up Movement", lambda: api.single_fly_up(20)),
        ("Down Movement", lambda: api.single_fly_down(20)),
        ("Forward Movement", lambda: api.single_fly_forward(20)),
        ("Landing", lambda: api.single_fly_touchdown()),
        ("Turn Left", lambda: api.single_fly_turnleft(45)),
        ("Turn Right", lambda: api.single_fly_turnright(45)),
    ]
    
    print("\nTesting with 10-second timeout per command:")
    print("-" * 40)
    
    for cmd_name, cmd_func in hanging_commands:
        print(f"{cmd_name:20} ", end="", flush=True)
        result = test_with_timeout(cmd_func, 10)
        print(result)
        
        # Check if drone is still responsive after each command
        try:
            battery = api.get_battery()
            print(f"{'':20} Responsive: ✓ (Battery: {battery}%)")
        except:
            print(f"{'':20} Responsive: ✗")
            break
        
        time.sleep(1)  # Brief pause between commands
    
    print("\n" + "=" * 40)
    print("ANALYSIS:")
    print("- Commands that complete quickly are working")
    print("- Commands that timeout may require drone to be in specific state")
    print("- For example: takeoff might require armed state or specific conditions")
    print("- The drone remains responsive even after timeouts")

def test_flight_sequence():
    """Test a proper flight sequence."""
    import pyhula
    
    print("\n\nTesting Proper Flight Sequence")
    print("=" * 35)
    
    api = pyhula.UserApi()
    if not api.connect():
        print("Failed to connect")
        return
    
    print("✓ Connected")
    
    # Proper sequence for flight
    sequence = [
        ("Check Battery", lambda: api.get_battery()),
        ("Arm Drone", lambda: api.plane_fly_arm()),
        ("Wait 2s", lambda: time.sleep(2)),
        ("Takeoff", lambda: api.single_fly_takeoff()),
        ("Wait 3s", lambda: time.sleep(3)),
        ("Check Position", lambda: api.get_coordinate()),
        ("Small Up", lambda: api.single_fly_up(10)),
        ("Wait 2s", lambda: time.sleep(2)),
        ("Small Down", lambda: api.single_fly_down(10)),
        ("Wait 2s", lambda: time.sleep(2)),
        ("Land", lambda: api.single_fly_touchdown()),
        ("Wait 3s", lambda: time.sleep(3)),
        ("Disarm", lambda: api.plane_fly_disarm()),
    ]
    
    print("Executing flight sequence...")
    for step_name, step_func in sequence:
        print(f"  {step_name}...", end="", flush=True)
        
        if "Wait" in step_name:
            step_func()
            print(" ✓")
        else:
            result = test_with_timeout(step_func, 15)  # Longer timeout for flight commands
            print(f" {result}")
            
            # If a command fails, stop the sequence
            if "ERROR" in result or "TIMEOUT" in result:
                print(f"  Sequence stopped due to {step_name} failure")
                break

if __name__ == "__main__":
    try:
        test_previously_hanging_commands()
        test_flight_sequence()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
