@echo off
:: Input Blocker - Admin Launcher
:: Auto-elevates to admin if needed

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ADMIN] Requesting admin privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo.
echo   ========================================
echo     Input Blocker v3.0 - Admin Mode
echo   ========================================
echo.
echo   Starting GUI...
echo.

"C:\Users\Abdox\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0app.py"

pause
