@echo off
REM Video Analyzer - Quick Launch
REM Usage: analyze-video.bat "C:\path\to\video.mp4" [options]
REM Options: -ExtractFrames -ExtractAudio -GenerateThumbnails -Detailed -All

if "%~1"=="" (
    echo Usage: analyze-video.bat "C:\path\to\video.mp4" [options]
    echo Options:
    echo   -ExtractFrames      Extract keyframes
    echo   -ExtractAudio       Extract audio track
    echo   -GenerateThumbnails Generate preview thumbnails
    echo   -Detailed           Generate detailed analysis
    echo   -All                Enable all options
    echo.
    echo Example: analyze-video.bat "C:\video.mp4" -All
    pause
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%~dp0Analyze-Video.ps1" -VideoPath "%~1" %2 %3 %4 %5 %6