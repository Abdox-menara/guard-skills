# Input Blocker v3.0 - PowerShell Fallback (simple version)
param([int]$Countdown = 10)

if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`" -Countdown $Countdown" -Verb RunAs
    exit
}

$code = @"
using System;
using System.Runtime.InteropServices;
public class InputBlocker {
    [DllImport("user32.dll")]
    public static extern bool BlockInput(bool fBlockIt);
}
"@
Add-Type -TypeDefinition $code -Language CSharp

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INPUT BLOCKER v3.0 (PowerShell)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Unblock: Ctrl+Alt+Del" -ForegroundColor Yellow
Write-Host ""

Write-Host "  PREPARING..." -ForegroundColor Green
for ($i = $Countdown; $i -ge 1; $i--) {
    Write-Host "  $i" -ForegroundColor White -NoNewline
    Start-Sleep -Seconds 1
    Write-Host ""
}

Write-Host ""
Write-Host "  [BLOCKED] Input locked!" -ForegroundColor Red
$null = [InputBlocker]::BlockInput($true)
while ($true) { Start-Sleep -Seconds 1 }
