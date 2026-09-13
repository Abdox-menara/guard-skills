<#
.SYNOPSIS
  Uninstall Input Blocker (PS1-native twin of uninstall.bat).
#>
$ErrorActionPreference = 'Continue'
Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'InputBlocker' -ErrorAction SilentlyContinue
Remove-Item -LiteralPath "$env:APPDATA\InputBlocker" -Recurse -Force -ErrorAction SilentlyContinue
foreach ($f in @('block_input.py', 'block_input.bat', 'block_input.ps1', 'block_config.json')) {
  Remove-Item -LiteralPath (Join-Path ([Environment]::GetFolderPath('Desktop')) $f) -Force -ErrorAction SilentlyContinue
}
Write-Host '[DONE] Uninstalled!' -ForegroundColor Green
