#!/usr/bin/env python3
"""
PyHula Python 3.13 Import Hook

This module provides an import hook that automatically patches PyHula for Python 3.13 compatibility.
Just import this module before importing PyHula.

Usage:
    import pyhula_py313_fix
    import pyhula  # Will be automatically patched
"""

import sys
import struct
import importlib.util
from importlib.machinery import ModuleSpec
from importlib.abc import Loader, MetaPathFinder
import types

class PyHulaCompatibilityFinder(MetaPathFinder):
    """Import hook finder for PyHula compatibility"""
    
    def find_spec(self, fullname, path, target=None):
        """Find module spec and apply patches if needed"""
        if fullname == 'pyhula' and sys.version_info >= (3, 13):
            print("🔧 Python 3.13+ detected - applying PyHula compatibility patches...")
            
            # Find the original module
            spec = importlib.util.find_spec(fullname)
            if spec is None:
                return None
            
            # Create a wrapper loader
            original_loader = spec.loader
            spec.loader = PyHulaCompatibilityLoader(original_loader)
            
            return spec
        
        return None

class PyHulaCompatibilityLoader(Loader):
    """Import hook loader that applies compatibility patches"""
    
    def __init__(self, original_loader):
        self.original_loader = original_loader
    
    def create_module(self, spec):
        """Create module using original loader"""
        return self.original_loader.create_module(spec)
    
    def exec_module(self, module):
        """Execute module and apply patches"""
        # Execute the original module
        self.original_loader.exec_module(module)
        
        # Apply compatibility patches
        self._apply_patches(module)
        
        print("✅ PyHula Python 3.13 compatibility patches applied")
    
    def _apply_patches(self, module):
        """Apply Python 3.13 compatibility patches to the module"""
        
        # Patch MAVLinkHeader if it exists
        if hasattr(module, 'MAVLinkHeader'):
            self._patch_mavlink_header(module.MAVLinkHeader)
        
        # Patch MAVLinkMessage if it exists
        if hasattr(module, 'MAVLinkMessage'):
            self._patch_mavlink_message(module.MAVLinkMessage)
        
        # Look for these classes in submodules too
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, types.ModuleType):
                if hasattr(attr, 'MAVLinkHeader'):
                    self._patch_mavlink_header(attr.MAVLinkHeader)
                if hasattr(attr, 'MAVLinkMessage'):
                    self._patch_mavlink_message(attr.MAVLinkMessage)
    
    def _patch_mavlink_header(self, cls):
        """Patch MAVLinkHeader for Python 3.13 compatibility"""
        if not hasattr(cls, '_original_pack'):
            # Store original method
            cls._original_pack = cls.pack if hasattr(cls, 'pack') else None
            
            def safe_pack(self):
                """Python 3.13 compatible pack method"""
                try:
                    # Convert all numeric values to proper types
                    attrs = {}
                    for name in ['magic', 'length', 'sequence', 'sysid', 'compid', 'msgid']:
                        if hasattr(self, name):
                            value = getattr(self, name)
                            if isinstance(value, float):
                                attrs[name] = int(value)
                            elif isinstance(value, (int, bool)):
                                attrs[name] = int(value)
                            else:
                                attrs[name] = value
                    
                    # Create format string for header
                    fmt = '<BBBBBB'  # Common MAVLink header format
                    values = [
                        attrs.get('magic', 0xFE),
                        attrs.get('length', 0),
                        attrs.get('sequence', 0),
                        attrs.get('sysid', 0),
                        attrs.get('compid', 0),
                        attrs.get('msgid', 0)
                    ]
                    
                    return struct.pack(fmt, *values)
                    
                except Exception as e:
                    print(f"⚠️ Header pack fallback: {e}")
                    if cls._original_pack:
                        return cls._original_pack(self)
                    return b'\xFE\x00\x00\x00\x00\x00'  # Minimal header
            
            cls.pack = safe_pack
    
    def _patch_mavlink_message(self, cls):
        """Patch MAVLinkMessage for Python 3.13 compatibility"""
        if not hasattr(cls, '_original_pack'):
            # Store original method
            cls._original_pack = cls.pack if hasattr(cls, 'pack') else None
            
            def safe_pack(self):
                """Python 3.13 compatible pack method"""
                try:
                    if cls._original_pack:
                        # Try original first with type conversion
                        return cls._original_pack(self)
                    else:
                        # Fallback implementation
                        return b''
                        
                except struct.error as e:
                    if "required argument is not an integer" in str(e):
                        # Convert float values to integers where needed
                        for attr_name in dir(self):
                            if not attr_name.startswith('_'):
                                value = getattr(self, attr_name)
                                if isinstance(value, float) and value.is_integer():
                                    setattr(self, attr_name, int(value))
                        
                        # Retry with converted values
                        if cls._original_pack:
                            return cls._original_pack(self)
                    
                    print(f"⚠️ Message pack error: {e}")
                    return b''  # Return empty bytes as fallback
            
            cls.pack = safe_pack

# Install the import hook
def install_hook():
    """Install the PyHula compatibility import hook"""
    if sys.version_info >= (3, 13):
        # Check if hook is already installed
        for finder in sys.meta_path:
            if isinstance(finder, PyHulaCompatibilityFinder):
                return  # Already installed
        
        # Install at the beginning of meta_path
        sys.meta_path.insert(0, PyHulaCompatibilityFinder())
        print("🔧 PyHula Python 3.13 compatibility hook installed")

# Auto-install when module is imported
install_hook()

print("✅ PyHula Python 3.13 compatibility module loaded")
print("   Import PyHula normally - patches will be applied automatically")
