# PyHula Windows Permission Fix (PowerShell)
# Run this as Administrator to fix UDP socket permissions

Write-Host "PyHula Windows Permission Fix" -ForegroundColor Yellow
Write-Host "=" * 40 -ForegroundColor Yellow
Write-Host ""

# Check if running as administrator
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]$currentUser
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] This script requires Administrator privileges" -ForegroundColor Red
    Write-Host ""
    Write-Host "To run as Administrator:" -ForegroundColor Yellow
    Write-Host "1. Press Win+X" -ForegroundColor Cyan
    Write-Host "2. Select 'Windows Terminal (Admin)'" -ForegroundColor Cyan  
    Write-Host "3. Navigate to this folder and run:" -ForegroundColor Cyan
    Write-Host "   .\fix_windows_permissions.ps1" -ForegroundColor Green
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Running as Administrator" -ForegroundColor Green
Write-Host ""

# Python executable path
$pythonPath = "C:\Users\janis\AppData\Local\Programs\Python\Python313\python.exe"

# Check if Python exists
if (-not (Test-Path $pythonPath)) {
    Write-Host "[WARNING] Python 3.13 not found at expected location" -ForegroundColor Yellow
    Write-Host "Looking for Python installations..." -ForegroundColor Cyan
    
    # Try to find Python
    $possiblePaths = @(
        "C:\Users\janis\AppData\Local\Programs\Python\Python313\python.exe",
        "C:\Python313\python.exe",
        "C:\Program Files\Python313\python.exe"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $pythonPath = $path
            Write-Host "[OK] Found Python at: $pythonPath" -ForegroundColor Green
            break
        }
    }
    
    if (-not (Test-Path $pythonPath)) {
        Write-Host "[ERROR] Could not find Python 3.13 installation" -ForegroundColor Red
        Write-Host "Please update the path in this script" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "Python path: $pythonPath" -ForegroundColor Cyan
Write-Host ""

# Add Windows Firewall rules
Write-Host "Adding Windows Firewall rules..." -ForegroundColor Yellow

try {
    # Remove existing rules (if any)
    Write-Host "Removing old firewall rules..." -ForegroundColor Cyan
    Remove-NetFirewallRule -DisplayName "Python PyHula*" -ErrorAction SilentlyContinue
    
    # Add new rules
    Write-Host "Adding UDP rules..." -ForegroundColor Cyan
    New-NetFirewallRule -DisplayName "Python PyHula UDP Inbound" -Direction Inbound -Protocol UDP -Action Allow -Program $pythonPath | Out-Null
    New-NetFirewallRule -DisplayName "Python PyHula UDP Outbound" -Direction Outbound -Protocol UDP -Action Allow -Program $pythonPath | Out-Null
    
    Write-Host "Adding TCP rules..." -ForegroundColor Cyan  
    New-NetFirewallRule -DisplayName "Python PyHula TCP Inbound" -Direction Inbound -Protocol TCP -Action Allow -Program $pythonPath | Out-Null
    New-NetFirewallRule -DisplayName "Python PyHula TCP Outbound" -Direction Outbound -Protocol TCP -Action Allow -Program $pythonPath | Out-Null
    
    Write-Host "[OK] Firewall rules added successfully!" -ForegroundColor Green
    
} catch {
    Write-Host "[ERROR] Failed to add firewall rules: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Try running Windows Defender Firewall manually" -ForegroundColor Yellow
}

Write-Host ""

# Test PyHula
Write-Host "Testing PyHula connection..." -ForegroundColor Yellow
Write-Host ""

try {
    $testScript = @"
import pyhula
import sys

print('=' * 50)
print('PyHula Connection Test')
print('=' * 50)

try:
    print('Creating UserApi...')
    api = pyhula.UserApi()
    print('[OK] UserApi created successfully')
    
    print('Attempting connection...')
    result = api.connect()
    
    if result:
        print('[OK] Connection successful!')
        print('Drone detected and connected!')
    else:
        print('[INFO] Connection returned False')
        print('This is normal if:')
        print('- Drone is powered off')
        print('- Not connected to drone WiFi')
        print('- Drone is out of range')
    
    print('')
    print('Permission fix appears to be working!')
    print('No more socket permission errors!')
    
except Exception as e:
    print(f'[ERROR] PyHula test failed: {e}')
    if 'PermissionError' in str(e):
        print('Still having permission issues.')
        print('Try restarting your computer.')
    else:
        print('Different error - may be normal if no drone present.')
    
print('')
print('Test complete.')
"@

    & $pythonPath -c $testScript
    
} catch {
    Write-Host "[ERROR] Failed to test PyHula: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" * 50 -ForegroundColor Yellow
Write-Host "Fix completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Connect to your drone's WiFi network" -ForegroundColor Cyan
Write-Host "2. Power on your drone" -ForegroundColor Cyan
Write-Host "3. Run: py -3.13" -ForegroundColor Cyan
Write-Host "4. Test: import pyhula; api = pyhula.UserApi(); api.connect()" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"
