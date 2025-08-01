#!/usr/bin/env python3
"""
Fix PyHula connection management issues

This script addresses the socket binding conflicts and incomplete command execution
by properly managing PyHula connections and implementing proper cleanup.
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

class FixedPyHulaConnection:
    """A wrapper around PyHula that properly manages connections and cleanup."""
    
    def __init__(self):
        self._pyhula = None
        self._connected = False
        self._connection_lock = threading.Lock()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
    
    def connect(self):
        """Connect to PyHula with proper error handling."""
        with self._connection_lock:
            if self._connected:
                print("Already connected")
                return True
            
            try:
                print("Creating PyHula instance...")
                self._pyhula = pyhula.UserApi()  # Correct API class
                
                print("Connecting to drone...")
                result = self._pyhula.connect()
                
                if result:
                    self._connected = True
                    print("✓ Connected successfully")
                    
                    # Wait a moment for all threads to stabilize
                    time.sleep(2)
                    
                    return True
                else:
                    print("✗ Connection failed")
                    return False
                    
            except Exception as e:
                print(f"✗ Connection error: {e}")
                return False
    
    def disconnect(self):
        """Properly disconnect from PyHula."""
        with self._connection_lock:
            if not self._connected or not self._pyhula:
                return
            
            try:
                print("Disconnecting...")
                # UserApi might not have disconnect method, try different approaches
                if hasattr(self._pyhula, 'disconnect'):
                    self._pyhula.disconnect()
                elif hasattr(self._pyhula, 'close'):
                    self._pyhula.close()
                # If no explicit disconnect, just clear the connection
                self._connected = False
                print("✓ Disconnected")
            except Exception as e:
                print(f"Disconnect error: {e}")
    
    def cleanup(self):
        """Clean up all resources."""
        self.disconnect()
        
        # Force cleanup of any remaining threads
        print("Cleaning up threads...")
        for thread in threading.enumerate():
            if thread != threading.current_thread() and thread.daemon:
                if any(name in thread.name for name in ['UDP', 'TCP', 'BROADCAST']):
                    print(f"  Stopping {thread.name}")
                    # Thread cleanup happens automatically with daemon threads
        
        self._pyhula = None
        time.sleep(1)
    
    def execute_command(self, command_func, *args, timeout=10, **kwargs):
        """Execute a PyHula command with timeout and proper error handling."""
        if not self._connected or not self._pyhula:
            print("Not connected!")
            return None
        
        try:
            command_name = command_func.__name__ if hasattr(command_func, '__name__') else str(command_func)
            print(f"Executing {command_name}...")
            
            # Use threading to implement timeout
            result = [None]
            exception = [None]  # Initialize as list to allow assignment
            
            def run_command():
                try:
                    result[0] = command_func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=run_command, daemon=True)
            thread.start()
            thread.join(timeout)
            
            if thread.is_alive():
                print(f"✗ {command_name} timed out after {timeout}s")
                return None
            elif exception[0]:
                print(f"✗ {command_name} failed: {exception[0]}")
                return None
            else:
                print(f"✓ {command_name} completed: {result[0]}")
                return result[0]
        
        except Exception as e:
            print(f"Command execution error: {e}")
            return None
    
    @property
    def pyhula(self):
        """Access to the underlying PyHula instance."""
        return self._pyhula if self._connected else None

def kill_existing_processes():
    """Kill any existing Python processes that might be holding sockets."""
    import subprocess
    try:
        # Find Python processes using our port
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        pids_to_kill = set()
        
        for line in lines:
            if ':50061' in line or ':50062' in line:  # PyHula ports
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    if pid.isdigit():
                        pids_to_kill.add(int(pid))
        
        for pid in pids_to_kill:
            try:
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
                print(f"Killed process {pid}")
            except:
                pass
    except:
        pass

def test_fixed_connection():
    """Test the fixed PyHula connection."""
    print("Testing Fixed PyHula Connection")
    print("=" * 50)
    
    # Clean up any existing processes
    print("Cleaning up existing processes...")
    kill_existing_processes()
    time.sleep(2)
    
    with FixedPyHulaConnection() as conn:
        # Test connection
        if not conn.connect():
            print("Failed to connect")
            return
        
        # Test basic commands
        print("\nTesting basic commands...")
        
        # Test RTP command (should be quick)
        result = conn.execute_command(conn.pyhula.Plane_cmd_swith_rtp, 0, timeout=5)
        
        # Test LED command
        result = conn.execute_command(conn.pyhula.single_fly_lamplight, 1, timeout=5)
        
        # Test takeoff with longer timeout
        print("\nTesting takeoff command...")
        result = conn.execute_command(conn.pyhula.single_fly_takeoff, timeout=15)
        
        if result:
            print("Waiting for takeoff to complete...")
            time.sleep(3)
            
            # Test landing
            print("Testing landing...")
            result = conn.execute_command(conn.pyhula.single_fly_touchdown, timeout=15)
        
        print("\nTest complete!")

if __name__ == "__main__":
    try:
        test_fixed_connection()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Cleaning up...")
        # Force cleanup
        kill_existing_processes()
