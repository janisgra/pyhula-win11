#!/usr/bin/env python3
"""
PyHula 1.13.1 Local Build Script
Builds directly in current directory with shorter paths
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("PyHula 1.13.1 Local Build")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"Building in: {current_dir}")
    
    # Create short build directory
    build_dir = current_dir / "b"
    if build_dir.exists():
        print("Removing existing build directory...")
        try:
            shutil.rmtree(build_dir)
        except:
            print("Warning: Could not remove build directory")
    
    # Create short dist directory  
    dist_dir = current_dir / "d"
    if dist_dir.exists():
        print("Removing existing dist directory...")
        try:
            shutil.rmtree(dist_dir)
        except:
            print("Warning: Could not remove dist directory")
    
    # Set environment variables for short paths
    env = os.environ.copy()
    env['TMPDIR'] = str(current_dir / "tmp")
    env['TEMP'] = str(current_dir / "tmp")
    env['TMP'] = str(current_dir / "tmp")
    
    # Create temp directory
    tmp_dir = current_dir / "tmp"
    tmp_dir.mkdir(exist_ok=True)
    
    print("Building wheel...")
    try:
        # Run build with custom build and dist directories
        cmd = [
            sys.executable, "setup.py", 
            "bdist_wheel",
            "--build-base", str(build_dir),
            "--dist-dir", str(dist_dir)
        ]
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Build successful!")
            
            # List created wheels
            if dist_dir.exists():
                wheels = list(dist_dir.glob("*.whl"))
                if wheels:
                    print(f"Created wheel: {wheels[0]}")
                    
                    # Copy to main dist directory
                    main_dist = current_dir / "dist"
                    main_dist.mkdir(exist_ok=True)
                    shutil.copy2(wheels[0], main_dist)
                    print(f"Copied to: {main_dist / wheels[0].name}")
                else:
                    print("No wheel files found")
            else:
                print("Dist directory not created")
        else:
            print("Build failed:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return 1
            
    except Exception as e:
        print(f"Error during build: {e}")
        return 1
    finally:
        # Cleanup
        print("Cleaning up...")
        for cleanup_dir in [build_dir, dist_dir, tmp_dir]:
            if cleanup_dir.exists():
                try:
                    shutil.rmtree(cleanup_dir)
                except:
                    print(f"Warning: Could not remove {cleanup_dir}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
