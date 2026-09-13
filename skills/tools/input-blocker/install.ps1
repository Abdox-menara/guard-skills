<#
.SYNOPSIS
  Install Input Blocker dependencies (PS1-native twin of install.bat).
#>
$ErrorActionPreference = 'Stop'
try { python --version | Out-Null } catch {
  Write-Error 'Python not found! Install from https://python.org'
}
Write-Host '[OK] Python found' -ForegroundColor Green
pip install keyboard pystray Pillow pyttsx3 --quiet
Write-Host '[DONE] All dependencies installed!' -ForegroundColor Green
