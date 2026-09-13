<#
.SYNOPSIS
  Input Blocker admin launcher (PS1-native twin of Run-As-Admin.bat). Auto-elevates.
#>
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
  Start-Process pwsh -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
  exit
}
Write-Host 'Input Blocker v3.0 - Admin Mode' -ForegroundColor Green
& python (Join-Path $PSScriptRoot 'app.py')
