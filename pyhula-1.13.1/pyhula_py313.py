#!/usr/bin/env python3
"""
PyHula Python 3.13 Integration
Easy-to-use module that automatically applies all compatibility patches

Usage:
    import pyhula_py313
    api = pyhula_py313.UserApi()
    api.connect()
"""

import sys
import os

# Add utils directory to path
_utils_path = os.path.join(os.path.dirname(__file__), 'utils')
if _utils_path not in sys.path:
    sys.path.insert(0, _utils_path)

# Apply all Python 3.13 compatibility patches BEFORE importing pyhula
import python313_compat
python313_compat.apply_all_patches()

# Now safely import pyhula
import pyhula

# Re-export the main API for convenience
UserApi = pyhula.UserApi
get_version = pyhula.get_version

def create_api():
    """
    Create a PyHula UserApi instance with Python 3.13 compatibility
    
    Returns:
        pyhula.UserApi: Ready-to-use drone API instance
    """
    return UserApi()

def test_connection():
    """
    Test PyHula connection with a simple example
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        api = create_api()
        result = api.connect()
        if result:
            print("✅ PyHula connection successful!")
            print(f"✅ Drone detected - {len([m for m in dir(api) if not m.startswith('_')])} API methods available")
            return True
        else:
            print("⚠ API created but no drone detected")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("PyHula Python 3.13 Integration Test")
    print("=" * 40)
    print(f"Python version: {sys.version}")
    print(f"PyHula version: {get_version()}")
    print()
    
    # Test the integration
    test_connection()
