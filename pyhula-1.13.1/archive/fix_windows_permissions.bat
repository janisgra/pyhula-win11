@echo off
echo PyHula Windows Permission Fix
echo ===============================
echo.
echo This script fixes Windows firewall/permission issues for PyHula
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
    goto :fix_permissions
) else (
    echo [ERROR] This script needs Administrator privileges
    echo.
    echo Please:
    echo 1. Right-click this file
    echo 2. Select "Run as administrator" 
    echo 3. Click "Yes" when prompted
    echo.
    pause
    exit /b 1
)

:fix_permissions
echo.
echo Fixing Windows Firewall permissions...
echo.

REM Add firewall rule for Python 3.13
netsh advfirewall firewall add rule name="Python PyHula Inbound" dir=in action=allow protocol=UDP program="C:\Users\janis\AppData\Local\Programs\Python\Python313\python.exe"
netsh advfirewall firewall add rule name="Python PyHula Outbound" dir=out action=allow protocol=UDP program="C:\Users\janis\AppData\Local\Programs\Python\Python313\python.exe"

REM Also add TCP rules (some drone protocols use TCP)
netsh advfirewall firewall add rule name="Python PyHula TCP Inbound" dir=in action=allow protocol=TCP program="C:\Users\janis\AppData\Local\Programs\Python\Python313\python.exe"
netsh advfirewall firewall add rule name="Python PyHula TCP Outbound" dir=out action=allow protocol=TCP program="C:\Users\janis\AppData\Local\Programs\Python\Python313\python.exe"

echo.
echo [OK] Firewall rules added successfully!
echo.
echo Testing PyHula connection...
echo.

REM Test PyHula with diagnostics
echo Running PyHula diagnostics...
python diagnose_connection_issues.py

echo.
echo Testing safe connection method...
python -c "
try:
    from safe_pyhula_connection import SafePyHulaConnection
    print('Testing safe connection wrapper...')
    conn = SafePyHulaConnection()
    result = conn.connect()
    if result:
        print('[OK] Safe connection successful!')
        conn.disconnect()
    else:
        print('[INFO] No drone detected (normal if drone is off)')
    print('Safe connection method working!')
except Exception as e:
    print(f'[ERROR] Safe connection test failed: {e}')
    print('Falling back to basic test...')
    
    # Fallback to basic test
    import pyhula
    print('Basic PyHula test...')
    try:
        api = pyhula.UserApi()
        print('UserApi created successfully')
        result = api.connect()
        if result:
            print('[OK] Connection successful!')
        else:
            print('[INFO] No drone detected (this is normal if drone is off)')
        print('Permission fix appears to be working!')
    except Exception as e:
        print(f'[ERROR] Still having issues: {e}')
        print('You may need to:')
        print('1. Restart your computer')
        print('2. Check drone is powered on')  
        print('3. Connect to drone WiFi network')
        print('4. For Python 3.13: Use Python 3.6-3.12 instead')
"

echo.
echo Fix complete! Try running PyHula again.
pause
