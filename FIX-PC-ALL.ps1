#Requires -RunAsAdministrator
<#
.SYNOPSIS
  PC security & performance fix (PS1-native twin of FIX-PC-ALL.bat).
  Runs cleanup, security, update and bluetooth fix scripts in order.
#>
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($s in @('cleanup.ps1', 'security-fix.ps1', 'update-and-threats.ps1', 'bluetooth-fix.ps1')) {
  $p = Join-Path $root $s
  Write-Host "=== $s ===" -ForegroundColor Green
  & $p
}
Write-Host '[DONE] PC fix complete.' -ForegroundColor Green
