@echo off
title Input Blocker - Uninstall
echo ========================================
echo   INPUT BLOCKER - UNINSTALL
echo ========================================
echo.

echo   Removing startup entry...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "InputBlocker" /f >nul 2>&1

echo   Removing config files...
del "%APPDATA%\InputBlocker\config.json" >nul 2>&1
del "%APPDATA%\InputBlocker\block_log.txt" >nul 2>&1
del "%APPDATA%\InputBlocker\block_history.json" >nul 2>&1
rmdir "%APPDATA%\InputBlocker" >nul 2>&1

echo   Removing desktop files...
del "%USERPROFILE%\Desktop\block_input.py" >nul 2>&1
del "%USERPROFILE%\Desktop\block_input.bat" >nul 2>&1
del "%USERPROFILE%\Desktop\block_input.ps1" >nul 2>&1
del "%USERPROFILE%\Desktop\block_config.json" >nul 2>&1

echo.
echo   [DONE] Uninstalled!
echo.
pause
