#!/usr/bin/env python3
"""
PyHula Command Execution Analysis

This script specifically investigates why some commands (like takeoff) hang
while others (like get_battery) work perfectly.
"""

import sys
import os
import time
import threading
import signal
from contextlib import contextmanager

# Add PyHula to path
pyhula_path = r"C:\Users\janis\AppData\Local\Programs\Python\Python313\Lib\site-packages"
if pyhula_path not in sys.path:
    sys.path.insert(0, pyhula_path)

import pyhula

@contextmanager
def timeout_context(seconds):
    """Context manager for command timeout."""
    def timeout_handler():
        raise TimeoutError(f"Command timed out after {seconds} seconds")
    
    timer = threading.Timer(seconds, timeout_handler)
    timer.start()
    try:
        yield
    finally:
        timer.cancel()

def test_command_execution():
    """Test different types of commands to understand the hanging issue."""
    print("PyHula Command Execution Analysis")
    print("=" * 40)
    
    # Create API and connect
    api = pyhula.UserApi()
    print("Connecting...")
    if not api.connect():
        print("Failed to connect")
        return
    
    print("✓ Connected successfully")
    
    # Test commands in order of complexity
    commands_to_test = [
        # Quick status commands (these work)
        ("Battery Status", lambda: api.get_battery()),
        ("Plane ID", lambda: api.get_plane_id()),
        ("Coordinate", lambda: api.get_coordinate()),
        
        # Simple control commands  
        ("RTP Switch", lambda: api.Plane_cmd_swith_rtp(0)),
        
        # LED command with proper parameters
        ("LED Red", lambda: api.single_fly_lamplight(255, 0, 0, 1, 1)),
        
        # Movement commands (these might hang)
        ("Arm Drone", lambda: api.plane_fly_arm()),
        ("Simple Up Movement", lambda: api.single_fly_up(20)),
        ("Takeoff", lambda: api.single_fly_takeoff()),
    ]
    
    results = {}
    
    for cmd_name, cmd_func in commands_to_test:
        print(f"\nTesting: {cmd_name}")
        print("-" * 20)
        
        try:
            start_time = time.time()
            
            # Use timeout context for each command
            with timeout_context(10):  # 10 second timeout
                result = cmd_func()
            
            duration = time.time() - start_time
            print(f"✓ {cmd_name}: {result} (took {duration:.2f}s)")
            results[cmd_name] = {'status': 'success', 'result': result, 'duration': duration}
            
            # Small delay between commands
            time.sleep(1)
            
        except TimeoutError as e:
            duration = time.time() - start_time
            print(f"⏱ {cmd_name}: TIMEOUT after {duration:.2f}s")
            results[cmd_name] = {'status': 'timeout', 'duration': duration}
            
            # If a command times out, let's see what threads are doing
            print("  Active threads during timeout:")
            for thread in threading.enumerate():
                if thread != threading.current_thread():
                    print(f"    {thread.name}: alive={thread.is_alive()}, daemon={thread.daemon}")
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"✗ {cmd_name}: ERROR - {e} (after {duration:.2f}s)")
            results[cmd_name] = {'status': 'error', 'error': str(e), 'duration': duration}
        
        # If we hit a timeout or error on movement commands, let's try to continue
        # but first check if the drone is still responsive
        if cmd_name in ["Simple Up Movement", "Takeoff"] and results[cmd_name]['status'] != 'success':
            print("  Checking if drone is still responsive...")
            try:
                with timeout_context(3):
                    battery = api.get_battery()
                print(f"  ✓ Drone still responsive (battery: {battery})")
            except:
                print("  ✗ Drone not responsive after failed command")
                break
    
    # Summary
    print("\n" + "=" * 40)
    print("COMMAND EXECUTION SUMMARY")
    print("=" * 40)
    
    for cmd_name, result in results.items():
        status = result['status']
        duration = result.get('duration', 0)
        
        if status == 'success':
            print(f"✓ {cmd_name}: SUCCESS ({duration:.2f}s)")
        elif status == 'timeout':
            print(f"⏱ {cmd_name}: TIMEOUT ({duration:.2f}s)")
        elif status == 'error':
            print(f"✗ {cmd_name}: ERROR ({duration:.2f}s)")
    
    print("\nAnalysis:")
    successes = [name for name, result in results.items() if result['status'] == 'success']
    timeouts = [name for name, result in results.items() if result['status'] == 'timeout']
    
    if successes:
        print(f"Working commands ({len(successes)}): {', '.join(successes)}")
    if timeouts:
        print(f"Hanging commands ({len(timeouts)}): {', '.join(timeouts)}")
    
    # Pattern analysis
    if successes and timeouts:
        print("\nPATTERN DETECTED:")
        print("- Status/info commands work immediately")
        print("- Movement/action commands hang indefinitely")
        print("- This suggests the command pipeline is partially working")
        print("- The issue may be in the command acknowledgment or completion detection")

if __name__ == "__main__":
    try:
        test_command_execution()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nTest complete")
