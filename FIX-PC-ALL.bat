@echo off
title PC SECURITY & PERFORMANCE FIX
color 0A
echo ========================================
echo   PC SECURITY ^& PERFORMANCE FIX
echo   Dell-pc - Dell Precision 7520
echo ========================================
echo.
echo This script requires Administrator privileges.
echo Right-click this file and select "Run as administrator"
echo.
pause

:: Set execution policy
powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force"

:: Run cleanup
echo.
echo [1/4] Running disk cleanup...
powershell -ExecutionPolicy Bypass -File "%~dp0cleanup.ps1"
pause

:: Run security fixes
echo.
echo [2/4] Running security hardening...
powershell -ExecutionPolicy Bypass -File "%~dp0security-fix.ps1"
pause

:: Run update and threats check
echo.
echo [3/4] Checking updates and threats...
powershell -ExecutionPolicy Bypass -File "%~dp0update-and-threats.ps1"
pause

:: Run Bluetooth fix
echo.
echo [4/4] Cleaning Bluetooth COM ports...
powershell -ExecutionPolicy Bypass -File "%~dp0bluetooth-fix.ps1"
pause

echo.
echo ========================================
echo   ALL DONE!
echo ========================================
echo.
echo RECOMMENDED: Reboot your PC to apply all changes
echo.
echo To enable VT-x in BIOS:
echo   1. Restart PC
echo   2. Press F2 at Dell logo
echo   3. Go to Advanced ^> CPU Configuration
echo   4. Enable VT-x and VT-d
echo   5. Save and Exit
echo.
pause