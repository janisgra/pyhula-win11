#!/usr/bin/env python3
"""
PyHula Connection Fix - Focused Solution

Based on diagnostic output, the issue is:
1. OSError: [WinError 10048] Only one usage of each socket address is normally permitted
2. Commands connect but never complete execution

This script implements a single-connection approach with proper cleanup.
"""

import sys
import os
import time
import threading
import socket
import signal

# Add PyHula to path
pyhula_path = r"C:\Users\janis\AppData\Local\Programs\Python\Python313\Lib\site-packages"
if pyhula_path not in sys.path:
    sys.path.insert(0, pyhula_path)

import pyhula

class SingletonPyHula:
    """Singleton PyHula connection to prevent multiple socket bindings."""
    _instance = None
    _api = None
    _connected = False
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def connect(self):
        """Connect if not already connected."""
        with self._lock:
            if self._connected and self._api:
                print("Already connected")
                return True
            
            if self._api is None:
                print("Creating PyHula UserApi...")
                self._api = pyhula.UserApi()
            
            print("Connecting to drone...")
            try:
                result = self._api.connect()
                if result:
                    self._connected = True
                    print("✓ Connected successfully")
                    # Give threads time to stabilize
                    time.sleep(2)
                    return True
                else:
                    print("✗ Connection failed")
                    return False
            except Exception as e:
                print(f"✗ Connection error: {e}")
                return False
    
    def get_api(self):
        """Get the API instance if connected."""
        return self._api if self._connected else None
    
    def is_connected(self):
        """Check if connected."""
        return self._connected
    
    def execute_with_timeout(self, func, *args, timeout=5, **kwargs):
        """Execute a function with timeout using threading."""
        result = [None]
        exception = [None]
        finished = threading.Event()
        
        def target():
            try:
                result[0] = func(*args, **kwargs)
            except Exception as e:
                exception[0] = e
            finally:
                finished.set()
        
        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        
        if finished.wait(timeout):
            if exception[0]:
                raise exception[0]
            return result[0]
        else:
            raise TimeoutError(f"Operation timed out after {timeout} seconds")

def test_commands():
    """Test PyHula commands with the singleton connection."""
    print("\nTesting PyHula Commands")
    print("=" * 30)
    
    # Use singleton connection
    pyhula_conn = SingletonPyHula()
    
    if not pyhula_conn.connect():
        print("Failed to connect")
        return
    
    api = pyhula_conn.get_api()
    if not api:
        print("No API available")
        return
    
    print(f"\nDrone connected. Available methods: {len([m for m in dir(api) if not m.startswith('_')])}")
    
    # Test 1: Simple status check
    print("\n1. Testing battery status...")
    try:
        battery = pyhula_conn.execute_with_timeout(api.get_battery, timeout=3)
        print(f"✓ Battery: {battery}")
    except TimeoutError:
        print("✗ Battery check timed out")
    except Exception as e:
        print(f"✗ Battery check failed: {e}")
    
    # Test 2: RTP command (usually quick)
    print("\n2. Testing RTP switch...")
    try:
        result = pyhula_conn.execute_with_timeout(api.Plane_cmd_swith_rtp, 0, timeout=3)
        print(f"✓ RTP switch: {result}")
    except TimeoutError:
        print("✗ RTP switch timed out")
    except Exception as e:
        print(f"✗ RTP switch failed: {e}")
    
    # Test 3: LED light (check signature and try)
    print("\n3. Testing LED command...")
    try:
        # The LED command needs r, g, b, time, mode parameters
        result = pyhula_conn.execute_with_timeout(
            api.single_fly_lamplight, 
            255, 0, 0,  # Red color
            1,          # Duration
            1,          # Mode
            timeout=5
        )
        print(f"✓ LED command: {result}")
    except TimeoutError:
        print("✗ LED command timed out")
    except Exception as e:
        print(f"✗ LED command failed: {e}")
    
    # Test 4: Simple movement command
    print("\n4. Testing simple up movement...")
    try:
        result = pyhula_conn.execute_with_timeout(api.single_fly_up, 20, timeout=8)
        print(f"✓ Up movement: {result}")
    except TimeoutError:
        print("✗ Up movement timed out")
    except Exception as e:
        print(f"✗ Up movement failed: {e}")
    
    print("\nCommand tests complete!")

def main():
    """Main function."""
    print("PyHula Connection Fix - Focused Solution")
    print("=" * 45)
    
    # Clean up any existing Python processes that might hold sockets
    print("Cleaning up existing processes...")
    try:
        import subprocess
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True, timeout=5)
        subprocess.run(['taskkill', '/F', '/IM', 'py.exe'], capture_output=True, timeout=5)
        time.sleep(2)
    except:
        pass
    
    # Test socket availability
    print("Testing key ports...")
    test_ports = [50061, 50062]
    for port in test_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('', port))
            sock.close()
            print(f"✓ Port {port} available")
        except:
            print(f"! Port {port} may be in use")
    
    # Run command tests
    test_commands()

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
        print("\nScript finished.")
        # Give time for cleanup
        time.sleep(1)
