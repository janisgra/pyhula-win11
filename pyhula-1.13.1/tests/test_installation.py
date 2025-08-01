#!/usr/bin/env python3
"""
PyHula Installation Test Script

This script tests the PyHula installation and verifies all modules work correctly.
Cross-platform compatible for Python 3.8+ (tested on Windows, (Linux, macOS)).
"""

import sys
import traceback
import platform
import os

def test_basic_import():
    print("Testing basic PyHula import...")
    try:
        import pyhula
        print("  [OK] pyhula imported successfully")
        
        # Try PyHula's official version method first
        try:
            version = pyhula.get_version()
            print(f"  Version: {version.strip()}")
        except Exception as e:
            # Fallback to __version__ if available (suppress Pylance warning)
            try:
                version_attr = getattr(pyhula, '__version__', None)
                if version_attr:
                    print(f"  Version: {version_attr}")
                else:
                    print(f"  Version: Could not retrieve version ({e})")
            except Exception:
                print(f"  Version: Could not retrieve version ({e})")
        
        print(f"  Location: {pyhula.__file__}")
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to import pyhula: {e}")
        traceback.print_exc()
        return False

def test_module_imports():
    print("\nTesting PyHula module imports...")
    
    # Core modules that should always be available
    core_modules = [
        ('pyhula.pypack.fylo.commandprocessor', 'Command Processor'),
        ('pyhula.pypack.fylo.config', 'Configuration'),
        ('pyhula.pypack.system.buffer', 'Buffer'),
        ('pyhula.pypack.system.command', 'Command'),
        ('pyhula.pypack.system.datacenter', 'Data Center'),
        ('pyhula.pypack.system.network', 'Network'),
        ('pyhula.pypack.system.state', 'State'),
        ('pyhula.pypack.system.system', 'System'),
    ]
    
    # Extended modules (may not be available in all builds)
    extended_modules = [
        ('pyhula.pypack.fylo.mavlink', 'MAVLink'),
        ('pyhula.pypack.fylo.mavanalyzer', 'MAV Analyzer'),
        ('pyhula.pypack.fylo.msganalyzer', 'Message Analyzer'),
        ('pyhula.pypack.fylo.stateprocessor', 'State Processor'),
        ('pyhula.pypack.fylo.taskprocessor', 'Task Processor'),
        ('pyhula.pypack.fylo.uwb', 'UWB'),
    ]
    
    def test_module_group(modules, group_name):
        print(f"  {group_name}:")
        successful = 0
        for module_name, description in modules:
            try:
                __import__(module_name)
                print(f"    [OK] {description} ({module_name.split('.')[-1]})")
                successful += 1
            except ImportError as e:
                print(f"    [MISSING] {description}: {e}")
            except Exception as e:
                print(f"    [ERROR] {description}: {e}")
        return successful, len(modules)
    
    # Test core modules
    core_successful, core_total = test_module_group(core_modules, "Core modules")
    
    # Test extended modules
    extended_successful, extended_total = test_module_group(extended_modules, "Extended modules")
    
    total_successful = core_successful + extended_successful
    total_modules = core_total + extended_total
    
    print(f"\nModule Import Results:")
    print(f"  Core modules: {core_successful}/{core_total} successful")
    print(f"  Extended modules: {extended_successful}/{extended_total} successful")
    print(f"  Total: {total_successful}/{total_modules} successful")
    
    # Consider the test successful if core modules work
    success_threshold = 0.7  # 70% of core modules should work
    core_success_rate = core_successful / core_total if core_total > 0 else 0
    
    if core_success_rate >= success_threshold:
        print(f"  Status: GOOD (core functionality available)")
        return total_successful, total_modules, True
    else:
        print(f"  Status: POOR (core functionality incomplete)")
        return total_successful, total_modules, False

def test_network_permissions():
    """Test network permissions for UDP/TCP sockets"""
    print("\nTesting network permissions...")
    
    try:
        import socket
        
        # Test UDP socket creation (what PyHula needs)
        print("  Testing UDP socket creation...")
        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.bind(('0.0.0.0', 0))  # Bind to any available port
            port = udp_socket.getsockname()[1]
            print(f"    [OK] UDP socket created on port {port}")
            udp_socket.close()
        except PermissionError as e:
            print(f"    [ERROR] UDP permission denied: {e}")
            print(f"    This is the same error PyHula encounters!")
            return False
        except Exception as e:
            print(f"    [WARNING] UDP test failed: {e}")
        
        # Test TCP socket creation
        print("  Testing TCP socket creation...")
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.bind(('0.0.0.0', 0))
            port = tcp_socket.getsockname()[1]
            print(f"    [OK] TCP socket created on port {port}")
            tcp_socket.close()
        except Exception as e:
            print(f"    [WARNING] TCP test failed: {e}")
        
        print("  [OK] Network permissions appear to be working")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Network test failed: {e}")
        return False

def test_functionality():
    """Test basic PyHula functionality"""
    print("\nTesting basic functionality...")
    
    try:
        # Test UserApi class creation
        import pyhula
        print("  Creating UserApi instance...")
        api = pyhula.UserApi()
        print("  [OK] UserApi created successfully")
        
        # Test if we can access basic methods (without calling them)
        basic_methods = ['connect', 'disconnect']
        available_methods = []
        
        for method_name in basic_methods:
            if hasattr(api, method_name):
                available_methods.append(method_name)
                print(f"  [OK] Method '{method_name}' available")
            else:
                print(f"  [MISSING] Method '{method_name}' not found")
        
        # Test accessing some modules without hardware
        try:
            from pyhula.pypack.fylo import commandprocessor
            print("  [OK] Command processor module accessible")
        except Exception as e:
            print(f"  [WARNING] Command processor issue: {e}")
        
        # Check if essential components are available
        essential_methods = len(available_methods)
        if essential_methods >= 1:  # At least connect method should be available
            print("  [OK] Essential functionality appears to be available")
            return True
        else:
            print("  [ERROR] Essential methods missing")
            return False
            
    except Exception as e:
        print(f"  [ERROR] Functionality test failed: {e}")
        traceback.print_exc()
        return False
    """Test basic PyHula functionality"""
    print("\nTesting basic functionality...")
    
    try:
        # Test UserApi class creation
        import pyhula
        print("  Creating UserApi instance...")
        api = pyhula.UserApi()
        print("  [OK] UserApi created successfully")

        # Test if basic methods can be accessed (without calling them)
        basic_methods = ['connect', 'disconnect']
        available_methods = []
        
        for method_name in basic_methods:
            if hasattr(api, method_name):
                available_methods.append(method_name)
                print(f"  [OK] Method '{method_name}' available")
            else:
                print(f"  [MISSING] Method '{method_name}' not found")
        
        # Test accessing some modules without hardware
        try:
            from pyhula.pypack.fylo import commandprocessor
            print("  [OK] Command processor module accessible")
        except Exception as e:
            print(f"  [WARNING] Command processor issue: {e}")
        
        # Check if essential components are available
        essential_methods = len(available_methods)
        if essential_methods >= 1:  # At least connect method should be available
            print("  [OK] Essential functionality appears to be available")
            return True
        else:
            print("  [ERROR] Essential methods missing")
            return False
            
    except Exception as e:
        print(f"  [ERROR] Functionality test failed: {e}")
        traceback.print_exc()
        return False

def test_dependencies():
    print("\nTesting dependencies...")
    
    # Define dependencies with platform-specific alternatives
    dependencies = [
        ('numpy', 'NumPy', 'numpy'),
        ('cv2', 'OpenCV', 'opencv-python'),
        ('serial', 'PySerial', 'pyserial'),
        ('pymavlink', 'PyMAVLink', 'pymavlink'),
        ('scipy', 'SciPy', 'scipy'),
    ]
    
    # Optional dependencies (not critical for basic functionality)
    optional_dependencies = [
        ('matplotlib', 'Matplotlib', 'matplotlib'),
        ('PIL', 'Pillow', 'pillow'),
    ]
    
    successful = 0
    total = len(dependencies)
    
    print("  Required dependencies:")
    for module_name, description, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"    [OK] {description} ({module_name})")
            successful += 1
        except Exception as e:
            print(f"    [ERROR] {description} ({module_name}): {e}")
            print(f"           Install with: pip install {package_name}")
    
    print("  Optional dependencies:")
    optional_successful = 0
    for module_name, description, package_name in optional_dependencies:
        try:
            __import__(module_name)
            print(f"    [OK] {description} ({module_name})")
            optional_successful += 1
        except Exception:
            print(f"    [MISSING] {description} ({module_name}) - optional")
    
    print(f"\nDependency Results:")
    print(f"  Required: {successful}/{total} available")
    print(f"  Optional: {optional_successful}/{len(optional_dependencies)} available")
    
    return successful, total

def print_system_info():
    print("System Information:")
    print(f"  Python Version: {sys.version}")
    print(f"  Python Executable: {sys.executable}")
    print(f"  Platform: {sys.platform}")
    
    try:
        print(f"  OS: {platform.platform()}")
        print(f"  Architecture: {platform.architecture()[0]}")
        print(f"  Machine: {platform.machine()}")
        print(f"  Processor: {platform.processor()}")
        print(f"  Node: {platform.node()}")
    except Exception as e:
        print(f"  Platform details unavailable: {e}")
    
    # Python version compatibility check
    version_info = sys.version_info
    print(f"  Python {version_info.major}.{version_info.minor}.{version_info.micro}")
    
    if version_info.major == 3:
        if version_info.minor >= 8:
            print("Python version compatible with modern PyHula")
        elif version_info.minor == 6:
            print("Python 3.6 - Original PyHula target version")
        else:
            print("Python version may have compatibility issues")
    else:
        print("Python 2 is not supported")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("  Environment: Virtual environment detected ✓")
    else:
        print("  Environment: System Python (consider using virtual environment)")
        
    # Display path separator for cross-platform awareness
    print(f"  Path separator: '{os.sep}' (Platform: {os.name})")

def main():
    print("PyHula Installation Test")
    print("=" * 50)
    
    print_system_info()
    print("\n" + "=" * 50)
    
    # Run all tests
    tests = [
        ("Basic Import", test_basic_import),
        ("Module Imports", test_module_imports),
        ("Network Permissions", test_network_permissions),
        ("Functionality", test_functionality),
        ("Dependencies", test_dependencies),
    ]
    
    all_passed = True
    results = {}
    core_functionality_ok = True
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            if isinstance(result, tuple):
                if len(result) == 3:  # Module test returns (successful, total, core_ok)
                    successful, total, core_ok = result
                    passed = successful > 0  # At least some modules should work
                    core_functionality_ok = core_functionality_ok and core_ok
                    results[test_name] = f"{successful}/{total}"
                elif len(result) == 2:  # Dependency test returns (successful, total)
                    successful, total = result
                    passed = successful == total
                    results[test_name] = f"{successful}/{total}"
                else:
                    passed = False
                    results[test_name] = "[ERROR] Unexpected result"
            else:
                # For tests that return boolean
                passed = result
                results[test_name] = "[OK]" if passed else "[ERROR]"
            
            if not passed:
                all_passed = False
                
        except Exception as e:
            print(f"  [ERROR] Test {test_name} crashed: {e}")
            traceback.print_exc()
            all_passed = False
            results[test_name] = "[ERROR] CRASHED"
    
    # Final summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    for test_name, result in results.items():
        print(f"  {test_name}: {result}")
    
    # Determine overall status
    if all_passed and core_functionality_ok:
        print("\nALL TESTS PASSED!")
        print("PyHula is properly installed and ready to use!")
        print("\nNext steps:")
        print("- Connect to your drone's WiFi network")
        print("- Run: python -c \"import pyhula; api = pyhula.UserApi(); print('PyHula ready!')\"")
        return 0
    elif core_functionality_ok:
        print("\nPARTIAL SUCCESS")
        print("PyHula core functionality is available but some components may be missing.")
        print("This is often normal - not all modules are required for basic operation.")
        print("\nRecommendations:")
        print("- Install missing dependencies if needed")
        print("- Test basic drone connection")
        return 0
    else:
        print("\nTESTS FAILED")
        print("PyHula may not be fully functional. Check the errors above.")
        print("\nTroubleshooting:")
        
        # Platform-specific recommendations
        if sys.platform.startswith('win'):
            print("- Windows: Ensure Visual C++ Redistributables are installed")
            print("- Try: pip install --upgrade --force-reinstall pyhula")
        elif sys.platform.startswith('linux'):
            print("- Linux: Install build essentials: sudo apt-get install build-essential")
            print("- Try: pip install --upgrade --force-reinstall pyhula")
        elif sys.platform.startswith('darwin'):
            print("- macOS: Install Xcode command line tools: xcode-select --install")
            print("- Try: pip install --upgrade --force-reinstall pyhula")
        
        print(f"- Check Python version compatibility (current: {sys.version_info.major}.{sys.version_info.minor})")
        print("- Consider using a virtual environment")
        print("- Verify all dependencies are installed")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
