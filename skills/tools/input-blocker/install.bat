@echo off
title Input Blocker - Install Dependencies
echo ========================================
echo   INSTALLING DEPENDENCIES
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [ERROR] Python not found!
    echo   Install Python from: https://python.org
    pause
    exit /b
)

echo   [OK] Python found
echo.

echo   Installing packages...
pip install keyboard --quiet
pip install pystray --quiet
pip install Pillow --quiet
pip install pyttsx3 --quiet

echo.
echo   [DONE] All dependencies installed!
echo.
pause
