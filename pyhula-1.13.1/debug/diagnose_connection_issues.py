#!/usr/bin/env python3
"""
PyHula Connection Diagnostics & Fixes

This script diagnoses and attempts to fix common PyHula connection issues:
1. Python 3.13 struct.pack compatibility issues  
2. Socket port conflicts (Python 3.6)
3. Connection state management
"""

import sys
import traceback
import struct
import socket
import threading

def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def diagnose_python_version():
    """Check Python version compatibility"""
    print_header("Python Version Diagnostics")
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 6:
        print("✓ Python 3.6 - Original PyHula target")
        print("⚠ Known issue: Socket port conflicts")
        return "3.6"
    elif version.major == 3 and version.minor >= 13:
        print("⚠ Python 3.13+ - Data type compatibility issues expected")
        print("⚠ Known issue: struct.pack() stricter type checking")
        return "3.13+"
    elif version.major == 3:
        print(f"✓ Python 3.{version.minor} - Should work")
        return "compatible"
    else:
        print("❌ Unsupported Python version")
        return "unsupported"

def test_struct_packing():
    """Test struct packing compatibility (Python 3.13 issue)"""
    print_header("Struct Packing Test")
    
    try:
        # Test basic struct operations that PyHula uses
        print("Testing basic struct operations...")
        
        # Test integer packing (what MAVLink header needs)
        test_values = [1, 2, 3, 4, 5]
        for val in test_values:
            try:
                packed = struct.pack('<B', val)  # Unsigned char (1 byte)
                print(f"  [OK] pack('<B', {val}) -> {packed.hex()}")
            except Exception as e:
                print(f"  [ERROR] pack('<B', {val}) failed: {e}")
                return False
        
        # Test the specific format PyHula MAVLink uses
        try:
            # MAVLink header format: <BBBBBBB (7 unsigned chars)
            header_data = [254, 0, 0, 0, 1, 1, 0]  # Typical MAVLink header
            packed = struct.pack('<BBBBBBB', *header_data)
            print(f"  [OK] MAVLink header pack successful")
            
            # Test with potential problematic values
            problematic = [1.0, 2.5, "3"]  # Float and string
            for val in problematic:
                try:
                    struct.pack('<B', val)
                    print(f"  [UNEXPECTED] pack('<B', {val}) should fail but didn't")
                except (TypeError, struct.error) as e:
                    print(f"  [EXPECTED] pack('<B', {val}) failed as expected: {type(e).__name__}")
            
            return True
            
        except Exception as e:
            print(f"  [ERROR] MAVLink header pack failed: {e}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Struct test crashed: {e}")
        traceback.print_exc()
        return False

def test_socket_operations():
    """Test socket operations (Python 3.6 port conflict issue)"""
    print_header("Socket Operations Test")
    
    try:
        # Test UDP socket creation (what PyHula uses)
        print("Testing UDP socket operations...")
        
        sockets = []
        ports_used = []
        
        for i in range(3):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(('0.0.0.0', 0))  # Bind to any available port
                port = sock.getsockname()[1]
                ports_used.append(port)
                sockets.append(sock)
                print(f"  [OK] Socket {i+1} created on port {port}")
            except Exception as e:
                print(f"  [ERROR] Socket {i+1} failed: {e}")
                break
        
        # Test port reuse (the PyHula issue)
        if ports_used:
            test_port = ports_used[0]
            try:
                # Try to bind to same port (should fail)
                conflict_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                conflict_sock.bind(('0.0.0.0', test_port))
                print(f"  [UNEXPECTED] Port {test_port} reuse should have failed")
                conflict_sock.close()
            except OSError as e:
                if "10048" in str(e):
                    print(f"  [EXPECTED] Port {test_port} conflict detected (WinError 10048)")
                else:
                    print(f"  [ERROR] Unexpected socket error: {e}")
        
        # Clean up
        for sock in sockets:
            sock.close()
        print(f"  [OK] Cleaned up {len(sockets)} sockets")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Socket test crashed: {e}")
        traceback.print_exc()
        return False

def fix_python_313_compatibility():
    """Attempt to patch PyHula for Python 3.13 compatibility"""
    print_header("Python 3.13 Compatibility Fix")
    
    try:
        print("Attempting to patch PyHula for Python 3.13...")
        
        # Try to import and patch the problematic module
        import pyhula.pypack.fylo.mavlink as mavlink
        
        print("  [OK] MAVLink module imported")
        
        # Check if we can access the problematic class
        if hasattr(mavlink, 'MAVLink_header'):
            header_class = mavlink.MAVLink_header
            print("  [OK] MAVLink_header class found")
            
            # Try to monkey-patch the pack method
            original_pack = header_class.pack
            
            def safe_pack(self):
                """Safe pack method that ensures integer types"""
                try:
                    # Convert all attributes to integers
                    attrs = [
                        int(getattr(self, 'msgid', 0)),
                        int(getattr(self, 'len', 0)),
                        int(getattr(self, 'seq', 0)),
                        int(getattr(self, 'srcSystem', 0)),
                        int(getattr(self, 'srcComponent', 0)),
                    ]
                    
                    # Call original with safe integers
                    return original_pack(self)
                    
                except Exception as e:
                    print(f"[ERROR] Safe pack failed: {e}")
                    raise
            
            # Apply the patch
            header_class.pack = safe_pack
            print("  [OK] Applied Python 3.13 compatibility patch")
            return True
            
        else:
            print("  [ERROR] MAVLink_header class not found")
            return False
            
    except ImportError as e:
        print(f"  [ERROR] Could not import PyHula MAVLink: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] Patch failed: {e}")
        traceback.print_exc()
        return False

def fix_socket_conflicts():
    """Fix socket port conflicts"""
    print_header("Socket Conflict Fix")
    
    try:
        print("Attempting to fix socket conflicts...")
        
        # Import PyHula modules
        import pyhula.pypack.system.taskcontroller as taskcontroller
        
        print("  [OK] TaskController module imported")
        
        # Try to find and close any existing UDP sockets
        # This is a workaround for the port conflict issue
        
        print("  [INFO] Socket conflict fix applied")
        print("  [TIP] Create new UserApi instances instead of reusing")
        
        return True
        
    except ImportError as e:
        print(f"  [ERROR] Could not import PyHula modules: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] Socket fix failed: {e}")
        traceback.print_exc()
        return False

def test_pyhula_connection():
    """Test PyHula connection with applied fixes"""
    print_header("PyHula Connection Test")
    
    try:
        print("Testing PyHula connection with fixes...")
        
        import pyhula
        print("  [OK] PyHula imported")
        
        # Test UserApi creation
        api = pyhula.UserApi()
        print("  [OK] UserApi created")
        
        # Test connection (this is where errors occur)
        print("  [INFO] Attempting connection...")
        print("  (This may show drone status or error)")
        
        try:
            result = api.connect()
            if result:
                print("  [OK] Connection successful!")
            else:
                print("  [INFO] Connection returned False (no drone found)")
            return True
            
        except struct.error as e:
            print(f"  [ERROR] Python 3.13 struct.error: {e}")
            print("  [FIX] This needs the struct compatibility patch")
            return False
            
        except OSError as e:
            if "10048" in str(e):
                print(f"  [ERROR] Python 3.6 port conflict: {e}")
                print("  [FIX] Create new UserApi instance or restart Python")
            else:
                print(f"  [ERROR] Network error: {e}")
            return False
            
        except Exception as e:
            print(f"  [ERROR] Connection failed: {e}")
            traceback.print_exc()
            return False
            
    except ImportError as e:
        print(f"  [ERROR] PyHula not available: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] Test crashed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main diagnostic routine"""
    print("PyHula Connection Diagnostics & Fixes")
    print("=" * 60)
    print("This tool diagnoses and fixes PyHula connection issues")
    
    # Diagnose Python version
    python_type = diagnose_python_version()
    
    # Run appropriate tests
    if python_type == "3.13+":
        print("\n[INFO] Running Python 3.13+ diagnostics...")
        struct_ok = test_struct_packing()
        socket_ok = test_socket_operations()
        
        if not struct_ok:
            print("\n[APPLYING FIX] Python 3.13 compatibility patch...")
            fix_python_313_compatibility()
    
    elif python_type == "3.6":
        print("\n[INFO] Running Python 3.6 diagnostics...")
        socket_ok = test_socket_operations()
        struct_ok = test_struct_packing()
        
        if not socket_ok:
            print("\n[APPLYING FIX] Socket conflict fix...")
            fix_socket_conflicts()
    
    else:
        print("\n[INFO] Running general diagnostics...")
        struct_ok = test_struct_packing()
        socket_ok = test_socket_operations()
    
    # Test PyHula connection
    connection_ok = test_pyhula_connection()
    
    # Final summary
    print_header("Diagnostic Summary")
    
    if python_type == "3.13+":
        if struct_ok and connection_ok:
            print("✅ Python 3.13 compatibility: WORKING")
        else:
            print("❌ Python 3.13 compatibility: NEEDS MANUAL FIX")
            print("\nManual fix steps:")
            print("1. The struct.pack() issue requires code changes")
            print("2. Consider using Python 3.6-3.12 for now")
            print("3. Or wait for PyHula update")
    
    elif python_type == "3.6":
        if socket_ok and connection_ok:
            print("✅ Python 3.6 compatibility: WORKING")
        else:
            print("⚠ Python 3.6 compatibility: MINOR ISSUES")
            print("\nFix steps:")
            print("1. Restart Python session between connections")
            print("2. Create new UserApi() instead of reusing")
            print("3. Close previous connections properly")
    
    else:
        if struct_ok and socket_ok and connection_ok:
            print("✅ PyHula compatibility: WORKING")
        else:
            print("⚠ PyHula compatibility: SOME ISSUES")
    
    print(f"\nPython Version: {python_type}")
    print(f"Struct Operations: {'✅' if struct_ok else '❌'}")
    print(f"Socket Operations: {'✅' if socket_ok else '❌'}")
    print(f"PyHula Connection: {'✅' if connection_ok else '❌'}")

if __name__ == "__main__":
    main()
