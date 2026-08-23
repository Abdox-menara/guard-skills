@echo off
REM GitHub Publisher - Quick Launch
REM Usage: publish-github.bat "C:\path\to\folder" [options]
REM Options: -RepoName "name" -Description "desc" -Private -AutoOpen

if "%~1"=="" (
    echo Usage: publish-github.bat "C:\path\to\folder" [options]
    echo Options:
    echo   -RepoName "name"     GitHub repo name
    echo   -Description "desc"  Repo description
    echo   -Private              Make repo private
    echo   -AutoOpen            Open in browser after publish
    echo.
    echo Example: publish-github.bat "C:\my-skill" -RepoName "my-skill" -AutoOpen
    pause
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%~dp0Publish-GitHub.ps1" -Path "%~1" %2 %3 %4 %5 %6 %7 %8