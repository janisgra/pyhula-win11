# PyHula Import & Dependencies Test Script
import time
import os
import sys

print("PyHula Import Test")
print("=" * 20)

# Auto-install dependencies if needed
print("Checking dependencies...")
try:
    # Run dependency installer if available
    current_dir = os.path.dirname(os.path.abspath(__file__))
    installer_path = os.path.join(current_dir, "install_dependencies", "install_dependencies.py")
    
    if os.path.exists(installer_path):
        print("Dependency installer available (run install_dependencies/install_dependencies.py if needed)")
    else:
        print("No dependency installer found in current directory")
        
except Exception as e:
    print(f"[WARNING] Could not check for dependency installer: {e}")

print("\n" + "=" * 40)

# Test PyHula imports
print("Testing PyHula imports...")
try:
    import pyhula
    print("[OK] PyHula imported successfully")
    
    # Test API initialization
    api = pyhula.UserApi()
    print("[OK] UserApi initialized")
    
except ImportError as e:
    print(f"[ERROR] PyHula import failed: {e}")
    print("Run the setup scripts to install PyHula first")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] PyHula initialization failed: {e}")
    sys.exit(1)

# Test dependency imports
print("\nTesting dependencies...")
dependencies = [
    ("numpy", "np"),
    ("cv2", "cv2"), 
    ("serial", "serial"),
    ("scipy", "scipy")
]

missing_deps = []
for dep_name, import_name in dependencies:
    try:
        __import__(import_name)
        print(f"[OK] {dep_name}")
    except ImportError:
        print(f"[MISSING] {dep_name}")
        missing_deps.append(dep_name)

if missing_deps:
    print(f"\n[WARNING] Missing dependencies: {', '.join(missing_deps)}")
    print("Run install_dependencies/install_dependencies.py to install missing packages")
else:
    print("\n[OK] All dependencies are available!")

print("\n" + "=" * 40)
print("PyHula Import Test Complete!")
print("\nTo use PyHula:")
print("1. Connect to your drone's WiFi network")
print("2. Use pyhula.UserApi() to create an API instance")
print("3. Call api.connect() to establish connection")
print("4. Use flight commands safely and responsibly")
print("\nAlways follow local drone regulations and safety guidelines!")