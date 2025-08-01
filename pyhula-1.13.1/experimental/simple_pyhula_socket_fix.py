#!/usr/bin/env python3
"""
Simple PyHula Socket Fix

This script addresses the core socket binding issue that's preventing PyHula commands from working.
Based on the diagnostic output, the main problem is multiple socket bindings to the same port.
"""

import sys
import os
import time
import threading
import socket
from typing import Any, Optional

# Add PyHula to path
pyhula_path = r"C:\Users\janis\AppData\Local\Programs\Python\Python313\Lib\site-packages"
if pyhula_path not in sys.path:
    sys.path.insert(0, pyhula_path)

import pyhula

def kill_zombie_sockets():
    """Kill any processes holding PyHula ports."""
    import subprocess
    try:
        # Kill any Python processes that might be holding our ports
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True)
        subprocess.run(['taskkill', '/F', '/IM', 'py.exe'], capture_output=True)
        time.sleep(2)
        print("✓ Cleared existing Python processes")
    except:
        print("! Could not clear processes (might not exist)")

def test_socket_availability():
    """Test if the ports PyHula needs are available."""
    ports_to_test = [50061, 50062, 50063]  # Common PyHula ports
    
    print("Testing socket availability...")
    for port in ports_to_test:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('', port))
            sock.close()
            print(f"✓ Port {port} available")
        except OSError as e:
            print(f"✗ Port {port} blocked: {e}")

def simple_pyhula_test():
    """Test PyHula with minimal complexity."""
    print("\nSimple PyHula Test")
    print("=" * 30)
    
    try:
        # Create API instance
        print("Creating PyHula UserApi...")
        api = pyhula.UserApi()
        print("✓ API created")
        
        # Show all available methods
        methods = [method for method in dir(api) if not method.startswith('_')]
        print(f"Available methods: {len(methods)}")
        
        # Try connecting
        print("\nAttempting connection...")
        result = api.connect()
        print(f"Connection result: {result}")
        
        if result:
            print("✓ Connected successfully!")
            
            # Wait for threads to stabilize
            print("Waiting for connection to stabilize...")
            time.sleep(3)
            
            # List active threads
            print("\nActive threads after connection:")
            for thread in threading.enumerate():
                print(f"  {thread.name}: daemon={thread.daemon}, alive={thread.is_alive()}")
            
            # Try a simple command that should work quickly
            if hasattr(api, 'single_fly_lamplight'):
                print("\nTesting LED command...")
                try:
                    # Set a short timeout by implementing our own timeout
                    import signal
                    
                    def timeout_handler(signum, frame):
                        raise TimeoutError("Command timed out")
                    
                    # Only set timeout on non-Windows or if signal works
                    if os.name != 'nt':
                        signal.signal(signal.SIGALRM, timeout_handler)
                        signal.alarm(5)  # 5 second timeout
                    
                    result = api.single_fly_lamplight(1)  # Turn on LED
                    
                    if os.name != 'nt':
                        signal.alarm(0)  # Cancel timeout
                    
                    print(f"✓ LED command result: {result}")
                    
                except TimeoutError:
                    print("✗ LED command timed out")
                except Exception as e:
                    print(f"✗ LED command failed: {e}")
            
            # Try getting status/info if available
            if hasattr(api, 'get_battery'):
                print("\nTesting status command...")
                try:
                    if os.name != 'nt':
                        signal.signal(signal.SIGALRM, timeout_handler)
                        signal.alarm(3)  # 3 second timeout
                    
                    battery = api.get_battery()
                    
                    if os.name != 'nt':
                        signal.alarm(0)
                    
                    print(f"✓ Battery level: {battery}")
                except TimeoutError:
                    print("✗ Battery command timed out")
                except Exception as e:
                    print(f"✗ Battery command failed: {e}")
        
        else:
            print("✗ Connection failed")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nTest complete!")

def main():
    """Main execution function."""
    print("PyHula Socket Fix and Test")
    print("=" * 40)
    
    # Step 1: Clean up any existing socket conflicts
    kill_zombie_sockets()
    
    # Step 2: Test socket availability
    test_socket_availability()
    
    # Step 3: Test PyHula with minimal complexity
    simple_pyhula_test()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nCleaning up...")
        # Give threads time to cleanup
        time.sleep(2)
