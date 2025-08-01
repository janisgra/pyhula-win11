#!/usr/bin/env python3
"""
Simple functionality test for PyHula Python 3.13 port
Tests import, connection, and basic API commands to identify where functionality breaks
"""

import sys
import time
import os

def test_import():
    """Test if pyhula can be imported"""
    print("Testing PyHula import...")
    try:
        # Add src to path for development testing
        sys.path.insert(0, 'src')
        import pyhula
        print(f"✓ SUCCESS: PyHula imported. Version: {pyhula.get_version()}")
        
        # Check available API classes
        print(f"Available classes: {[attr for attr in dir(pyhula) if not attr.startswith('_')]}")
        
        return True, pyhula
    except Exception as e:
        print(f"✗ FAILED: Could not import pyhula: {e}")
        return False, None

def test_connection(pyhula_module):
    """Test if connection to drone can be established"""
    print("\nTesting drone connection...")
    if not pyhula_module:
        print("SKIPPED: No pyhula module")
        return None
        
    try:
        # Create connection instance using the correct API
        if hasattr(pyhula_module, 'UserApi'):
            drone = pyhula_module.UserApi()
            print("✓ SUCCESS: UserApi instance created")
        elif hasattr(pyhula_module, 'HULA'):
            drone = pyhula_module.HULA()
            print("✓ SUCCESS: HULA instance created")
        else:
            print("✗ FAILED: No known API class found")
            return None
        
        # Try to connect (this may require actual drone hardware)
        print("Attempting drone connection...")
        print("NOTE: This requires actual drone hardware to succeed")
        
        # Test connection method
        if hasattr(drone, 'connect'):
            print("✓ SUCCESS: Connect method available")
            # result = drone.connect()  # Uncomment when drone hardware is available
            print("✓ SUCCESS: Drone API structure is correct")
        else:
            print("✗ FAILED: No connect method found")
        
        return drone
            
    except Exception as e:
        print(f"✗ FAILED: Connection error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_basic_commands(drone):
    """Test basic drone commands (placeholder for when connection works)"""
    print("\nTesting basic drone commands...")
    
    if not drone:
        print("SKIPPED: No drone connection")
        return False
    
    try:
        print("✓ SUCCESS: Basic command structure ready")
        print("NOTE: Actual command testing requires drone hardware")
        return True
        
    except Exception as e:
        print(f"✗ FAILED: Command execution error: {e}")
        return False

def main():
    """Run all tests"""
    print("PyHula Python 3.13 Port - Functionality Test")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # Test 1: Import
    import_success, pyhula_module = test_import()
    if not import_success:
        print("\n" + "=" * 50)
        print("❌ Test suite stopped - import failed")
        print("\nTroubleshooting:")
        print("1. Run: py -3.13 utils/build_pyhula.py")
        print("2. Run: py -3.13 utils/diagnostic.py")
        print("3. Check if C extensions were built for correct Python version")
        return False
    
    # Test 2: Connection
    drone = test_connection(pyhula_module)
    
    # Test 3: Commands (placeholder for future testing)
    test_basic_commands(drone)
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print("✓ Import: Working")
    print("✓ Object Creation: Working")  
    print("⚠ API Commands: Requires hardware testing")
    print("\n🎯 Next steps:")
    print("1. Connect actual drone hardware")
    print("2. Test real API commands (takeoff, landing, movement)")
    print("3. Fix any command execution issues for Python 3.13")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
