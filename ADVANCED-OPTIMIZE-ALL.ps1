#Requires -RunAsAdministrator
<#
.SYNOPSIS
  Advanced PC optimization suite (PS1-native twin of ADVANCED-OPTIMIZE-ALL.bat).
  Runs the five optimization scripts in order. Replaces the BAT wrapper.
#>
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($s in @('fix-specific-issues.ps1', 'advanced-optimize.ps1', 'cleanup.ps1',
                 'security-fix.ps1', 'update-and-threats.ps1')) {
  $p = Join-Path $root $s
  Write-Host "=== $s ===" -ForegroundColor Green
  & $p
}
Write-Host '[DONE] All optimizations complete.' -ForegroundColor Green
