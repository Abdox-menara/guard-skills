#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Disables unnecessary Bluetooth COM ports
.DESCRIPTION
    Keeps essential Bluetooth devices (phones, earbuds) but disables serial ports
.NOTES
    Run as Administrator: Right-click PowerShell > Run as Administrator
    Then: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\bluetooth-fix.ps1
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " BLUETOOTH COM PORT CLEANUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# List all Bluetooth COM ports
$btPorts = Get-PnpDevice -Class Ports -Status OK -ErrorAction SilentlyContinue |
    Where-Object { $_.FriendlyName -like "*Bluetooth*" -or $_.FriendlyName -like "*BTH*" }

if (-not $btPorts) {
    Write-Host "No Bluetooth COM ports found" -ForegroundColor Green
    return
}

Write-Host "Found $($btPorts.Count) Bluetooth COM ports:" -ForegroundColor Yellow
Write-Host ""

# Show ports
foreach ($port in $btPorts) {
    Write-Host "  $($port.FriendlyName) - Instance: $($port.InstanceId)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Options:" -ForegroundColor Cyan
Write-Host "  1. Disable ALL Bluetooth COM ports (recommended)" -ForegroundColor White
Write-Host "  2. Keep COM3/COM4 (common for phones), disable others" -ForegroundColor White
Write-Host "  3. Keep all, no changes" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Disabling ALL Bluetooth COM ports..." -ForegroundColor Green
        foreach ($port in $btPorts) {
            try {
                Disable-PnpDevice -InstanceId $port.InstanceId -Confirm:$false -ErrorAction Stop
                Write-Host "  Disabled: $($port.FriendlyName)" -ForegroundColor Yellow
            } catch {
                Write-Host "  FAILED to disable: $($port.FriendlyName) - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        Write-Host ""
        Write-Host "SUCCESS: All Bluetooth COM ports disabled" -ForegroundColor Green
    }
    "2" {
        Write-Host ""
        Write-Host "Keeping COM3/COM4, disabling others..." -ForegroundColor Green
        foreach ($port in $btPorts) {
            if ($port.FriendlyName -notlike "*COM3*" -and $port.FriendlyName -notlike "*COM4*") {
                try {
                    Disable-PnpDevice -InstanceId $port.InstanceId -Confirm:$false -ErrorAction Stop
                    Write-Host "  Disabled: $($port.FriendlyName)" -ForegroundColor Yellow
                } catch {
                    Write-Host "  FAILED to disable: $($port.FriendlyName) - $($_.Exception.Message)" -ForegroundColor Red
                }
            } else {
                Write-Host "  Kept: $($port.FriendlyName)" -ForegroundColor Green
            }
        }
        Write-Host ""
        Write-Host "SUCCESS: Non-essential Bluetooth COM ports disabled" -ForegroundColor Green
    }
    default {
        Write-Host ""
        Write-Host "No changes made" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "NOTE: Bluetooth devices will still work for audio/calls." -ForegroundColor Cyan
Write-Host "Only serial port profiles are disabled." -ForegroundColor Cyan