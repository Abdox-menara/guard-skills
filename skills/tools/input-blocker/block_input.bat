@echo off
title Input Blocker v3.0
echo ========================================
echo   INPUT BLOCKER v3.0
echo   Block until manual unblock
echo ========================================
echo.
echo   Unblock: Ctrl+Shift+B
echo   Or: Ctrl+Alt+Del
echo.

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo   Requesting Admin...
    powershell -Command "Start-Process cmd -ArgumentList '/c python \"%~dp0block_input.py\"' -Verb RunAs"
    exit /b
)

echo   [OK] Running as Admin
echo.
python "%~dp0block_input.py"
