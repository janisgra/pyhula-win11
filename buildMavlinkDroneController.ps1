#!/usr/bin/env pwsh
# Build script for C++ MAVLink drone controller

param(
    [string]$Configuration = "Release",
    [switch]$Clean = $false
)

$ErrorActionPreference = "Stop"

# Paths
$RepoRoot = $PSScriptRoot
$CppControllerPath = Join-Path $RepoRoot "cpp-mavlink-controller"
$BuildPath = Join-Path $CppControllerPath "build"

Write-Host "Building C++ MAVLink Drone Controller" -ForegroundColor Cyan
Write-Host "Repository: $RepoRoot" -ForegroundColor Gray
Write-Host "Controller: $CppControllerPath" -ForegroundColor Gray
Write-Host "Build Dir: $BuildPath" -ForegroundColor Gray

# Clean if requested
if ($Clean -and (Test-Path $BuildPath)) {
    Write-Host "Cleaning build directory..." -ForegroundColor Yellow
    Remove-Item $BuildPath -Recurse -Force
}

# Create build directory
if (-not (Test-Path $BuildPath)) {
    New-Item -ItemType Directory -Path $BuildPath -Force | Out-Null
}

# Change to build directory
Push-Location $BuildPath

try {
    # Configure
    Write-Host "Configuring with CMake..." -ForegroundColor Green
    cmake ..
    
    if ($LASTEXITCODE -ne 0) {
        throw "CMake configuration failed"
    }
    
    # Build
    Write-Host "Building with configuration: $Configuration" -ForegroundColor Green
    cmake --build . --config $Configuration
    
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed"
    }
    
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "Executables are in: $BuildPath\bin" -ForegroundColor Gray
    
    # List built executables
    $BinPath = Join-Path $BuildPath "bin"
    if (Test-Path $BinPath) {
        Write-Host "`nBuilt executables:" -ForegroundColor Cyan
        Get-ChildItem $BinPath -Filter "*.exe" | ForEach-Object {
            Write-Host "  - $($_.Name)" -ForegroundColor White
        }
    }
    
} finally {
    Pop-Location
}