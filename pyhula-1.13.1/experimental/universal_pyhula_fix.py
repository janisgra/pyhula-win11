#!/usr/bin/env python3
"""
Universal PyHula Python 3.13 Fix
==================================

This script automatically detects PyHula installations in any Python environment
and applies the necessary fixes for Python 3.13 compatibility.

Works for:
- Conda environments  
- Standard Python installations
- Virtual environments
- Any PyHula installation location
"""

import sys
import os
import shutil
import importlib.util
import subprocess
import platform

def find_pyhula_installations():
    """Find all PyHula installations in current environment."""
    installations = []
    
    # Method 1: Try importing pyhula to get its location
    try:
        import pyhula
        pyhula_path = os.path.dirname(pyhula.__file__)
        installations.append(pyhula_path)
        print(f"✓ Found PyHula via import: {pyhula_path}")
    except ImportError:
        print("! PyHula not importable in current environment")
    
    # Method 2: Search sys.path for pyhula
    for path in sys.path:
        if os.path.exists(path):
            pyhula_candidate = os.path.join(path, 'pyhula')
            if os.path.exists(pyhula_candidate) and os.path.isdir(pyhula_candidate):
                if pyhula_candidate not in installations:
                    installations.append(pyhula_candidate)
                    print(f"✓ Found PyHula in sys.path: {pyhula_candidate}")
    
    # Method 3: Check common conda locations
    if 'conda' in sys.executable.lower() or 'anaconda' in sys.executable.lower():
        conda_base = os.path.dirname(os.path.dirname(sys.executable))
        conda_site_packages = os.path.join(conda_base, 'Lib', 'site-packages', 'pyhula')
        if os.path.exists(conda_site_packages) and conda_site_packages not in installations:
            installations.append(conda_site_packages)
            print(f"✓ Found PyHula in conda: {conda_site_packages}")
    
    return installations

def backup_file(file_path):
    """Create a backup of the original file."""
    backup_path = f"{file_path}.backup"
    if not os.path.exists(backup_path):
        shutil.copy2(file_path, backup_path)
        print(f"  Created backup: {backup_path}")
    else:
        print(f"  Backup already exists: {backup_path}")

def apply_mavlink_fix(pyhula_path):
    """Apply the struct.pack fix to mavlink.py."""
    mavlink_path = os.path.join(pyhula_path, 'pypack', 'fylo', 'mavlink.py')
    
    if not os.path.exists(mavlink_path):
        print(f"  ! mavlink.py not found at {mavlink_path}")
        return False
    
    print(f"  Applying mavlink.py fix...")
    backup_file(mavlink_path)
    
    try:
        with open(mavlink_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix 1: struct.pack in MAVLink_header.pack()
        old_pack_line = "return struct.pack(self.native_format, self.msgId, self.len, self.seq, self.srcSystem, self.srcComponent)"
        new_pack_line = "return struct.pack(self.native_format, int(self.msgId), int(self.len), int(self.seq), int(self.srcSystem), int(self.srcComponent))"
        
        if old_pack_line in content:
            content = content.replace(old_pack_line, new_pack_line)
            print("    ✓ Fixed MAVLink_header.pack() struct.pack issue")
        else:
            print("    ! MAVLink_header.pack() fix not needed or already applied")
        
        # Fix 2: struct.pack in MAVLink_message.pack()  
        old_msg_pack = "return struct.pack(self.native_format,"
        if old_msg_pack in content:
            # Find the full pack statement and fix it
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if old_msg_pack in line and "self.msgId" in line:
                    # Convert numpy types to int
                    if "int(self.msgId)" not in line:
                        lines[i] = line.replace("self.msgId", "int(self.msgId)")
                        lines[i] = lines[i].replace("self.len", "int(self.len)")
                        print("    ✓ Fixed MAVLink_message.pack() struct.pack issue")
                        break
            content = '\n'.join(lines)
        
        with open(mavlink_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("  ✓ mavlink.py fixes applied successfully")
        return True
        
    except Exception as e:
        print(f"  ✗ Error applying mavlink.py fix: {e}")
        return False

def apply_array_fix(pyhula_path):
    """Apply the array.fromstring fix."""
    # Look for files that might use array.fromstring
    files_to_check = []
    
    # Search for Python files that might contain array.fromstring
    for root, dirs, files in os.walk(pyhula_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'fromstring' in content and 'array' in content:
                            files_to_check.append(file_path)
                except:
                    continue
    
    print(f"  Checking {len(files_to_check)} files for array.fromstring...")
    
    fixes_applied = 0
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '.fromstring(' in content:
                backup_file(file_path)
                
                # Replace array.fromstring with array.frombytes
                content = content.replace('.fromstring(', '.frombytes(')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                rel_path = os.path.relpath(file_path, pyhula_path)
                print(f"    ✓ Fixed array.fromstring in {rel_path}")
                fixes_applied += 1
        
        except Exception as e:
            print(f"    ! Error fixing {file_path}: {e}")
    
    if fixes_applied > 0:
        print(f"  ✓ Applied array.fromstring fixes to {fixes_applied} files")
    else:
        print("  ! No array.fromstring fixes needed")
    
    return fixes_applied > 0

def apply_dll_fix(pyhula_path):
    """Apply the DLL loading fix."""
    init_path = os.path.join(pyhula_path, '__init__.py')
    
    if not os.path.exists(init_path):
        print(f"  ! __init__.py not found at {init_path}")
        return False
    
    print(f"  Applying DLL loading fix...")
    backup_file(init_path)
    
    try:
        with open(init_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add DLL path fix at the beginning
        dll_fix_code = '''# PyHula Python 3.13 DLL Fix
import os
import sys

# Add DLL directory to PATH for ctypes loading
pyhula_dir = os.path.dirname(__file__)
dll_dir = os.path.join(pyhula_dir, 'f09-lite-trans')
if os.path.exists(dll_dir) and dll_dir not in os.environ.get('PATH', ''):
    os.environ['PATH'] = dll_dir + os.pathsep + os.environ.get('PATH', '')

'''
        
        # Only add if not already present
        if 'PyHula Python 3.13 DLL Fix' not in content:
            content = dll_fix_code + content
            
            with open(init_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  ✓ DLL loading fix applied to __init__.py")
            return True
        else:
            print("  ! DLL fix already applied")
            return True
            
    except Exception as e:
        print(f"  ✗ Error applying DLL fix: {e}")
        return False

def test_pyhula_installation(pyhula_path):
    """Test if PyHula works after fixes."""
    print(f"  Testing PyHula installation...")
    
    try:
        # Test basic import
        sys.path.insert(0, os.path.dirname(pyhula_path))
        import pyhula
        print("    ✓ Import successful")
        
        # Test API creation
        api = pyhula.UserApi()
        print("    ✓ UserApi creation successful")
        
        # Test method availability
        methods = [m for m in dir(api) if not m.startswith('_')]
        print(f"    ✓ {len(methods)} API methods available")
        
        return True
        
    except Exception as e:
        print(f"    ✗ Test failed: {e}")
        return False

def main():
    """Main fix application function."""
    print("Universal PyHula Python 3.13 Fix")
    print("=" * 40)
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Find all PyHula installations
    print("\nSearching for PyHula installations...")
    installations = find_pyhula_installations()
    
    if not installations:
        print("✗ No PyHula installations found!")
        print("\nTry installing PyHula first:")
        print("  pip install path/to/pyhula-1.1.7-cp36-cp36m-win_amd64.whl")
        return False
    
    print(f"\nFound {len(installations)} PyHula installation(s)")
    
    # Apply fixes to each installation
    for i, pyhula_path in enumerate(installations, 1):
        print(f"\nFixing installation {i}: {pyhula_path}")
        print("-" * 50)
        
        success = True
        
        # Apply all fixes
        if not apply_mavlink_fix(pyhula_path):
            success = False
        
        if not apply_array_fix(pyhula_path):
            print("  ! Array fix failed but continuing...")
        
        if not apply_dll_fix(pyhula_path):
            print("  ! DLL fix failed but continuing...")
        
        # Test the installation
        if test_pyhula_installation(pyhula_path):
            print(f"  ✅ Installation {i} fixed and tested successfully!")
        else:
            print(f"  ❌ Installation {i} fixes applied but testing failed")
            success = False
    
    print("\n" + "=" * 40)
    print("UNIVERSAL FIX COMPLETE")
    print("=" * 40)
    
    if installations:
        print("PyHula should now work with Python 3.13 in this environment!")
        print("\nTest with:")
        print("import pyhula")
        print("api = pyhula.UserApi()")
        print("api.connect()")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nFix interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
