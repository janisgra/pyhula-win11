#!/usr/bin/env python3
"""
PyHula Production Build Script
Robust path handling, no emojis, handles Windows path length issues
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

class PyHulaProductionBuild:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.python_cmd = self.detect_python()
        self.setup_environment()
    
    def detect_python(self):
        """Detect best Python command"""
        candidates = [
            ['py', '-3.13'],
            ['py', '-3.12'],
            ['python3.13'],
            ['python3.12'],
            ['python'],
        ]
        
        for cmd in candidates:
            try:
                result = subprocess.run(cmd + ['--version'], 
                                      capture_output=True, text=True, check=True)
                version = result.stdout.strip()
                if any(v in version for v in ['3.13', '3.12', '3.11', '3.10', '3.9', '3.8']):
                    print(f"Python detected: {' '.join(cmd)} -> {version}")
                    return cmd
            except:
                continue
        
        raise RuntimeError("No suitable Python 3.8+ found")
    
    def setup_environment(self):
        """Setup build environment with path length handling"""
        # Check path length
        path_len = len(str(self.project_root))
        if path_len > 200:
            print(f"WARNING: Long project path ({path_len} chars) may cause build issues")
            print("Consider moving to shorter path like c:\\dev\\pyhula")
        
        # Setup short temp directory to avoid path length issues
        short_temp = Path("c:/temp/pyhula_build")
        try:
            short_temp.mkdir(parents=True, exist_ok=True)
            os.environ['TEMP'] = str(short_temp)
            os.environ['TMP'] = str(short_temp)
            print(f"Temp directory: {short_temp}")
        except Exception as e:
            print(f"Warning: Could not set short temp directory: {e}")
    
    def check_dependencies(self):
        """Check and install build dependencies"""
        print("Checking dependencies...")
        
        required = ['setuptools>=50.0', 'wheel>=0.36.0', 'numpy>=1.19.0']
        missing = []
        
        # Check what's already installed
        for pkg in ['setuptools', 'wheel', 'numpy']:
            try:
                __import__(pkg)
                print(f"  Found: {pkg}")
            except ImportError:
                print(f"  Missing: {pkg}")
                missing.append(pkg)
        
        # Install missing packages
        if missing:
            print(f"Installing missing dependencies...")
            try:
                cmd = self.python_cmd + ['-m', 'pip', 'install', '--upgrade'] + required
                subprocess.run(cmd, check=True, capture_output=True)
                print("  Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"  Failed to install dependencies: {e}")
                return False
        
        return True
    
    def build_extensions(self):
        """Build C extensions with error handling"""
        print("Building C extensions...")
        
        try:
            result = subprocess.run(
                self.python_cmd + ['setup.py', 'build_ext', '--inplace'],
                cwd=self.project_root,
                check=True,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes max
            )
            
            # Show build progress
            if result.stdout:
                lines = result.stdout.split('\n')
                build_lines = [l for l in lines if any(keyword in l.lower() 
                              for keyword in ['building', 'creating', 'compiling'])]
                for line in build_lines[:10]:  # Show first 10 build messages
                    if line.strip():
                        print(f"  {line}")
            
            print("  C extensions built successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"  C extension build failed")
            self.diagnose_build_error(e)
            return False
        except subprocess.TimeoutExpired:
            print(f"  Build timed out after 10 minutes")
            return False
    
    def diagnose_build_error(self, error):
        """Diagnose common build errors"""
        print("  Diagnosing build error...")
        
        if error.stderr:
            stderr = error.stderr.lower()
            stdout = error.stdout.lower() if error.stdout else ""
            
            # Path length issues
            if 'lnk1104' in stderr or 'cannot open file' in stderr:
                print("  DIAGNOSIS: Path length issue detected")
                print("  SOLUTION: Move project to shorter path (e.g., c:\\dev\\pyhula)")
                print("           or enable Windows long path support")
            
            # Missing Visual Studio
            elif 'microsoft visual studio' in stderr or 'vcvarsall.bat' in stderr:
                print("  DIAGNOSIS: Visual Studio Build Tools missing")
                print("  SOLUTION: Install Visual Studio Build Tools 2022")
            
            # Missing compiler
            elif 'error: Microsoft Visual C++' in stderr:
                print("  DIAGNOSIS: C++ compiler not found")
                print("  SOLUTION: Install Microsoft C++ Build Tools")
            
            # Permission issues
            elif 'permission denied' in stderr or 'access denied' in stderr:
                print("  DIAGNOSIS: Permission error")
                print("  SOLUTION: Run as administrator or check file permissions")
            
            else:
                print("  Error details:")
                print(f"    {error.stderr[-500:]}")  # Last 500 chars
    
    def create_distributions(self):
        """Create distribution packages"""
        print("Creating distributions...")
        
        dist_commands = [
            (['setup.py', 'sdist'], 'source distribution'),
            (['setup.py', 'bdist_wheel'], 'wheel distribution'),
        ]
        
        for cmd_args, description in dist_commands:
            print(f"  Creating {description}...")
            try:
                result = subprocess.run(
                    self.python_cmd + cmd_args,
                    cwd=self.project_root,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                print(f"    {description} created successfully")
            except subprocess.CalledProcessError as e:
                print(f"    Failed to create {description}: {e}")
                return False
            except subprocess.TimeoutExpired:
                print(f"    {description} creation timed out")
                return False
        
        return True
    
    def verify_build(self):
        """Verify build outputs"""
        print("Verifying build...")
        
        # Check dist directory
        dist_dir = self.project_root / 'dist'
        if not dist_dir.exists():
            print("  No dist directory found")
            return False
        
        files = list(dist_dir.glob('*'))
        if not files:
            print("  No files in dist directory")
            return False
        
        print("  Created files:")
        for file in files:
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"    {file.name} ({size_mb:.1f} MB)")
        
        # Test basic import
        return self.test_import()
    
    def test_import(self):
        """Test if built package can be imported"""
        print("  Testing import...")
        
        test_script = f'''
import sys
sys.path.insert(0, r"{self.project_root / 'src'}")
try:
    import pyhula
    print("SUCCESS: pyhula module imported")
    print(f"Location: {{pyhula.__file__}}")
    
    # Test pyhula_py313 integration if available
    try:
        import pyhula_py313
        print("SUCCESS: pyhula_py313 integration available")
    except ImportError:
        print("INFO: pyhula_py313 integration not available")
        
except Exception as e:
    print(f"FAILED: {{type(e).__name__}}: {{e}}")
    sys.exit(1)
'''
        
        try:
            result = subprocess.run(
                self.python_cmd + ['-c', test_script],
                check=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            for line in result.stdout.strip().split('\n'):
                print(f"    {line}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"    Import test failed: {e}")
            if e.stdout:
                print(f"    Output: {e.stdout}")
            return False
        except subprocess.TimeoutExpired:
            print(f"    Import test timed out")
            return False
    
    def show_summary(self):
        """Show build summary and installation instructions"""
        print("\n" + "=" * 60)
        print("BUILD COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        dist_dir = self.project_root / 'dist'
        if dist_dir.exists():
            print("\nCreated packages:")
            wheels = []
            for file in dist_dir.glob('*'):
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"  {file.name} ({size_mb:.1f} MB)")
                if file.suffix == '.whl':
                    wheels.append(file)
            
            # Installation instructions
            if wheels:
                print(f"\nInstallation:")
                print(f"  {' '.join(self.python_cmd)} -m pip install {wheels[0]}")
        
        # pyhula_py313 integration info
        pyhula_py313 = self.project_root / 'pyhula_py313.py'
        if pyhula_py313.exists():
            print(f"\nPython 3.13 Integration:")
            print(f"  import pyhula_py313")
            print(f"  api = pyhula_py313.UserApi()")
    
    def build(self):
        """Main build process"""
        print("PyHula Production Build System")
        print("=" * 60)
        print(f"Project: {self.project_root}")
        print(f"Python: {' '.join(self.python_cmd)}")
        print(f"Platform: {sys.platform}")
        print("=" * 60)
        
        try:
            steps = [
                ("Dependency Check", self.check_dependencies),
                ("C Extension Build", self.build_extensions),
                ("Distribution Creation", self.create_distributions),
                ("Build Verification", self.verify_build),
            ]
            
            for step_name, step_func in steps:
                print(f"\nStep: {step_name}")
                print("-" * 40)
                
                if not step_func():
                    print(f"\nBUILD FAILED at: {step_name}")
                    return False
            
            self.show_summary()
            return True
            
        except KeyboardInterrupt:
            print("\nBuild interrupted by user")
            return False
        except Exception as e:
            print(f"\nUnexpected build error: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main entry point"""
    try:
        builder = PyHulaProductionBuild()
        return 0 if builder.build() else 1
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
