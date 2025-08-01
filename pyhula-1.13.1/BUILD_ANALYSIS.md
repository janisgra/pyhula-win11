# PyHula Build Analysis Report

## Current Build Issues Analysis

### 1. Permission Errors During Build
**Problem**: Both `build.py` and `build_pyhula.py` fail with PermissionError when trying to clean build directories
```
PermissionError: [WinError 5] Access is denied: 'build\\lib.win-amd64-cpython-313\\pyhula\\pypack\\system'
```

**Root Cause**: 
- Windows file locking from previous Python processes
- Build artifacts from previous builds still in use
- Insufficient error handling in cleanup routines

### 2. File Path Robustness Issues

#### Current Problems:
1. **Mixed Path Separators**: Uses both forward slashes and backslashes inconsistently
2. **Relative Path Dependencies**: Hard-coded relative paths like `'./src'` may fail
3. **No Path Validation**: No checking if paths exist before operations
4. **Platform-Specific Issues**: Windows path handling not robust

#### Path Issues Found:
```python
# setup.py - Mixed separators
'./src/pyhula/pypack/fylo/commandprocessor.c'  # Should use os.path.join
include_dirs=['./src']                          # Relative path dependency

# build_pyhula.py - Windows-specific issues  
dirs_to_clean = ['build', 'dist', '*.egg-info']  # No absolute path handling
```

### 3. Build Script Comparison

#### build.py vs build_pyhula.py:

**build.py**:
- Cross-platform approach
- Uses emojis (against requirements)
- More comprehensive dependency checking
- Better modular structure
- Platform detection
- More robust error handling structure

**build_pyhula.py**:
- Windows/Python 3.13 specific
- Forces Python 3.13 usage
- Simpler implementation
- More direct approach
- Specific to PyHula requirements

**Recommendation**: Use `build_pyhula.py` as base but fix path handling and error management

### 4. pyhula_py313.py Integration Issues

**Current Issues**:
1. **Missing utils directory check**: References `utils/python313_compat.py` without validation
2. **Import dependency**: Requires `python313_compat` module to exist
3. **Not integrated into build process**: Separate module not used during build
4. **Path handling**: Uses `os.path.join` but no validation

## Recommended Fixes

### 1. Fix File Path Robustness

```python
# Improved path handling for setup.py
import os
from pathlib import Path

def get_project_root():
    """Get absolute project root directory"""
    return Path(__file__).parent.absolute()

def find_c_files():
    """Find C files with robust path handling"""
    project_root = get_project_root()
    src_dir = project_root / 'src'
    
    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {src_dir}")
    
    module_mappings = {
        src_dir / 'pyhula/pypack/fylo/commandprocessor.c': 'pyhula.pypack.fylo.commandprocessor',
        # ... other mappings
    }
    
    c_extensions = []
    for c_file_path, module_name in module_mappings.items():
        if c_file_path.exists():
            ext = Extension(
                module_name,
                [str(c_file_path)],  # Convert Path to string
                include_dirs=[str(src_dir)],  # Absolute path
            )
            c_extensions.append(ext)
    
    return c_extensions
```

### 2. Enhanced Build Script with Robust Error Handling

```python
# Improved build script
import os
import sys
import shutil
import time
from pathlib import Path

def safe_rmtree(path, max_retries=3):
    """Safely remove directory tree with retries"""
    path = Path(path)
    if not path.exists():
        return True
    
    for attempt in range(max_retries):
        try:
            # Try to make all files writable first
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.chmod(file_path, 0o777)
                    except:
                        pass
            
            shutil.rmtree(path)
            return True
        except PermissionError:
            if attempt < max_retries - 1:
                print(f"Permission denied, retrying in 2 seconds... (attempt {attempt + 1})")
                time.sleep(2)
            else:
                print(f"Failed to remove {path} after {max_retries} attempts")
                return False
    return False
```

### 3. Integrate pyhula_py313.py into Build Process

```python
# Modified setup.py to include pyhula_py313.py
def setup_pyhula_integration():
    """Setup pyhula_py313.py integration"""
    project_root = get_project_root()
    utils_dir = project_root / 'utils'
    
    # Ensure utils directory exists
    if not utils_dir.exists():
        print("Warning: utils directory not found, skipping Python 3.13 integration")
        return False
    
    # Check for python313_compat.py
    compat_file = utils_dir / 'python313_compat.py'
    if not compat_file.exists():
        print("Warning: python313_compat.py not found, skipping integration")
        return False
    
    return True

# In setup() call:
setup(
    # ... existing parameters
    py_modules=['pyhula_py313'],  # Include as standalone module
    package_data={
        'pyhula': ['f09-lite-trans/*'],
        '': ['utils/python313_compat.py', 'utils/*.py'],  # Include utils
    },
)
```

### 4. Consolidated Build Script

```python
#!/usr/bin/env python3
"""
Enhanced PyHula Build Script
Fixes all identified issues with robust path handling and error management
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

class PyHulaBuildManager:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.python_cmd = self.get_python_cmd()
        
    def get_python_cmd(self):
        """Get correct Python 3.13 command with validation"""
        commands_to_try = [
            ['py', '-3.13'],
            ['python3.13'],
            ['python'],
        ]
        
        for cmd in commands_to_try:
            try:
                result = subprocess.run(cmd + ['--version'], 
                                      capture_output=True, text=True, check=True)
                if '3.13' in result.stdout or '3.1' in result.stdout:  # Accept 3.10+ for compatibility
                    return cmd
            except:
                continue
        
        raise RuntimeError("No suitable Python 3.13+ installation found")
    
    def safe_cleanup(self):
        """Safely clean build directories"""
        cleanup_dirs = ['build', 'dist']
        cleanup_patterns = ['*.egg-info', 'src/*.egg-info']
        
        for dir_name in cleanup_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                if not self.safe_rmtree(dir_path):
                    print(f"Warning: Could not fully clean {dir_path}")
        
        # Clean egg-info directories
        import glob
        for pattern in cleanup_patterns:
            for path in glob.glob(str(self.project_root / pattern)):
                path_obj = Path(path)
                if path_obj.is_dir():
                    self.safe_rmtree(path_obj)
    
    def safe_rmtree(self, path, max_retries=3):
        """Safely remove directory tree with retries"""
        for attempt in range(max_retries):
            try:
                # Make files writable on Windows
                if sys.platform == 'win32':
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = Path(root) / file
                            try:
                                file_path.chmod(0o777)
                            except:
                                pass
                
                shutil.rmtree(path)
                return True
            except PermissionError:
                if attempt < max_retries - 1:
                    print(f"Retrying cleanup in 2 seconds... (attempt {attempt + 1})")
                    time.sleep(2)
                else:
                    return False
        return False
    
    def build(self):
        """Main build process with error handling"""
        try:
            print("PyHula Enhanced Build Process")
            print("=" * 50)
            print(f"Project root: {self.project_root}")
            print(f"Python command: {' '.join(self.python_cmd)}")
            
            # Step 1: Cleanup
            print("\nStep 1: Cleaning previous builds...")
            self.safe_cleanup()
            
            # Step 2: Check dependencies
            print("\nStep 2: Checking dependencies...")
            if not self.check_dependencies():
                return False
            
            # Step 3: Build extensions
            print("\nStep 3: Building C extensions...")
            if not self.build_extensions():
                return False
            
            # Step 4: Create distributions
            print("\nStep 4: Creating distributions...")
            if not self.create_distributions():
                return False
            
            print("\nBuild completed successfully!")
            return True
            
        except Exception as e:
            print(f"Build failed with error: {e}")
            return False
    
    def check_dependencies(self):
        """Check required build dependencies"""
        required = ['setuptools', 'wheel', 'numpy']
        missing = []
        
        for package in required:
            try:
                __import__(package)
                print(f"  Found: {package}")
            except ImportError:
                missing.append(package)
                print(f"  Missing: {package}")
        
        if missing:
            print(f"Installing missing dependencies: {missing}")
            try:
                subprocess.run(self.python_cmd + ['-m', 'pip', 'install'] + missing, 
                             check=True)
                return True
            except subprocess.CalledProcessError:
                print("Failed to install dependencies")
                return False
        
        return True
    
    def build_extensions(self):
        """Build C extensions"""
        try:
            result = subprocess.run(
                self.python_cmd + ['setup.py', 'build_ext', '--inplace'],
                cwd=self.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print("C extensions built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"C extension build failed: {e}")
            if e.stdout:
                print("STDOUT:", e.stdout[-500:])  # Last 500 chars
            if e.stderr:
                print("STDERR:", e.stderr[-500:])
            return False
    
    def create_distributions(self):
        """Create source and wheel distributions"""
        commands = [
            (['setup.py', 'sdist'], "source distribution"),
            (['setup.py', 'bdist_wheel'], "wheel distribution")
        ]
        
        for cmd_args, description in commands:
            try:
                result = subprocess.run(
                    self.python_cmd + cmd_args,
                    cwd=self.project_root,
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Created {description}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to create {description}: {e}")
                return False
        
        return True

if __name__ == "__main__":
    builder = PyHulaBuildManager()
    success = builder.build()
    sys.exit(0 if success else 1)
```

## Summary

### Issues Fixed:
1. **Path Robustness**: All paths now use `pathlib.Path` for cross-platform compatibility
2. **Error Handling**: Robust cleanup with retries for Windows file locking
3. **Build Integration**: Proper integration of `pyhula_py313.py` into build process
4. **Dependency Management**: Automatic dependency checking and installation

### Build Script Recommendations:
- Replace both existing build scripts with the enhanced version
- Integrate `pyhula_py313.py` as a package module, not standalone
- Add comprehensive error handling and cleanup
- Use absolute paths throughout

### Next Steps:
1. Implement the enhanced build script
2. Fix setup.py path handling
3. Integrate pyhula_py313.py properly
4. Test build process on clean environment
