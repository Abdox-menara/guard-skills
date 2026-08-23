@echo off
title ADVANCED PC OPTIMIZATION - Dell Precision 7520
color 0A
echo ========================================
echo   ADVANCED PC OPTIMIZATION
echo   Dell Precision 7520 - i7-6920HQ
echo ========================================
echo.
echo This script requires Administrator privileges.
echo Right-click this file and select "Run as administrator"
echo.
pause

:: Set execution policy
powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force"

:: Step 1: Fix specific issues
echo.
echo [1/5] Fixing specific issues (RAVBg64, Dell telemetry, netcut)...
powershell -ExecutionPolicy Bypass -File "%~dp0fix-specific-issues.ps1"
pause

:: Step 2: Run advanced optimization
echo.
echo [2/5] Running advanced optimization...
powershell -ExecutionPolicy Bypass -File "%~dp0advanced-optimize.ps1"
pause

:: Step 3: Run disk cleanup
echo.
echo [3/5] Running disk cleanup...
powershell -ExecutionPolicy Bypass -File "%~dp0cleanup.ps1"
pause

:: Step 4: Run security hardening
echo.
echo [4/5] Running security hardening...
powershell -ExecutionPolicy Bypass -File "%~dp0security-fix.ps1"
pause

:: Step 5: Run Windows Update check
echo.
echo [5/5] Checking Windows updates and threats...
powershell -ExecutionPolicy Bypass -File "%~dp0update-and-threats.ps1"
pause

echo.
echo ========================================
echo   ALL OPTIMIZATIONS COMPLETE!
echo ========================================
echo.
echo Changes applied:
echo   - Disabled bloatware services
echo   - Disabled unnecessary scheduled tasks
echo   - Optimized network stack
echo   - Optimized memory management
echo   - Disabled telemetry
echo   - Fixed RAVBg64 handle leak
echo   - Disabled Dell telemetry
echo   - Secured exposed ports
echo   - Freed disk space
echo   - Enabled Defender protections
echo.
echo RECOMMENDED: Reboot your PC now
echo.
echo For VT-x (WSL2/Hyper-V):
echo   1. Restart PC
echo   2. Press F2 at Dell logo
echo   3. Advanced > CPU Configuration
echo   4. Enable VT-x and VT-d
echo   5. Save and Exit
echo.
pause