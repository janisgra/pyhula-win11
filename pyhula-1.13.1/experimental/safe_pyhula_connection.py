#!/usr/bin/env python3
"""
PyHula Safe Connection Helper

This module provides safe connection methods that handle:
- Python 3.13 struct.pack compatibility issues
- Python 3.6 socket port conflicts
- Proper connection cleanup
"""

import sys
import time
import threading
import traceback

class SafePyHulaConnection:
    """Safe PyHula connection wrapper that handles version-specific issues"""
    
    def __init__(self):
        self.api = None
        self.connected = False
        self.python_version = sys.version_info
        
        print(f"SafePyHulaConnection initialized for Python {self.python_version.major}.{self.python_version.minor}")
        
        # Apply compatibility patches if needed
        if self.python_version >= (3, 13):
            self._apply_python313_patches()
    
    def _apply_python313_patches(self):
        """Apply Python 3.13 compatibility patches"""
        try:
            print("Applying Python 3.13 compatibility patches...")
            
            # Import the fix module and apply patches
            import fix_python313_compatibility
            fix_python313_compatibility.apply_all_patches()
            
        except Exception as e:
            print(f"Warning: Could not apply Python 3.13 patches: {e}")
    
    def create_api(self):
        """Create a new UserApi instance with proper cleanup"""
        try:
            # Clean up previous instance
            if self.api is not None:
                self.disconnect()
                time.sleep(0.5)  # Give time for cleanup
            
            # Import PyHula
            import pyhula
            
            # Create new API instance
            self.api = pyhula.UserApi()
            print("✅ UserApi created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create UserApi: {e}")
            traceback.print_exc()
            return False
    
    def connect(self, server_ip=None, retries=3):
        """Safe connection with retry logic and error handling"""
        if self.api is None:
            if not self.create_api():
                return False
        
        for attempt in range(retries):
            try:
                print(f"Connection attempt {attempt + 1}/{retries}...")
                
                if server_ip:
                    result = self.api.connect(server_ip)
                else:
                    result = self.api.connect()
                
                if result:
                    self.connected = True
                    print("✅ Connection successful!")
                    return True
                else:
                    print("ℹ️ Connection returned False (no drone found)")
                    return False
                    
            except struct.error as e:
                print(f"❌ Python 3.13 struct.error (attempt {attempt + 1}): {e}")
                if attempt < retries - 1:
                    print("Retrying with fresh API instance...")
                    self.create_api()  # Create fresh instance
                    time.sleep(1)
                else:
                    print("💡 This is a Python 3.13 compatibility issue")
                    print("   Consider using Python 3.6-3.12 or wait for PyHula update")
                    return False
            
            except OSError as e:
                if "10048" in str(e):
                    print(f"❌ Python 3.6 port conflict (attempt {attempt + 1}): {e}")
                    if attempt < retries - 1:
                        print("Creating new API instance to fix port conflict...")
                        self.create_api()  # Create fresh instance
                        time.sleep(1)
                    else:
                        print("💡 Port conflict - try restarting Python or use new session")
                        return False
                else:
                    print(f"❌ Network error: {e}")
                    return False
            
            except Exception as e:
                print(f"❌ Unexpected error (attempt {attempt + 1}): {e}")
                if attempt < retries - 1:
                    time.sleep(1)
                else:
                    traceback.print_exc()
                    return False
        
        return False
    
    def disconnect(self):
        """Safe disconnection with cleanup"""
        try:
            if self.api and self.connected:
                # Try to disconnect gracefully
                if hasattr(self.api, 'disconnect'):
                    self.api.disconnect()
                self.connected = False
                print("✅ Disconnected successfully")
            
            # Additional cleanup for socket issues
            if self.python_version.major == 3 and self.python_version.minor == 6:
                # Give extra time for socket cleanup
                time.sleep(1)
            
        except Exception as e:
            print(f"Warning: Disconnect cleanup failed: {e}")
    
    def __del__(self):
        """Cleanup on destruction"""
        try:
            self.disconnect()
        except:
            pass

def safe_connect(server_ip=None, retries=3):
    """Simple function for safe PyHula connection"""
    conn = SafePyHulaConnection()
    return conn.connect(server_ip, retries)

def demo_usage():
    """Demonstrate safe connection usage"""
    print("PyHula Safe Connection Demo")
    print("=" * 40)
    
    # Method 1: Using the class
    print("\nMethod 1: Using SafePyHulaConnection class")
    conn = SafePyHulaConnection()
    
    if conn.create_api():
        result = conn.connect()
        if result:
            print("Demo: Connection successful! You can now send commands.")
            # Example commands would go here
            conn.disconnect()
        else:
            print("Demo: No drone found (this is normal if drone is off)")
    
    # Method 2: Using the simple function
    print("\nMethod 2: Using safe_connect() function")
    result = safe_connect()
    if result:
        print("Demo: Quick connection successful!")
    else:
        print("Demo: Quick connection failed or no drone found")

if __name__ == "__main__":
    demo_usage()
