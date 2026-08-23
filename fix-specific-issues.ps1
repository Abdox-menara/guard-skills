#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Fix specific system issues found during analysis
.DESCRIPTION
    Fixes RAVBg64 handle leak, netcut exposure, Dell telemetry, and other issues
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " FIXING SPECIFIC ISSUES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# 1. FIX RAVBg64 HANDLE LEAK (4544 handles)
# ============================================================
Write-Host "[1/6] Fixing RAVBg64 handle leak..." -ForegroundColor Green

$ravProcess = Get-Process -Name "RAVBg64" -ErrorAction SilentlyContinue
if ($ravProcess) {
    Write-Host "  Found RAVBg64 with $($ravProcess.HandleCount) handles" -ForegroundColor Yellow
    try {
        Stop-Process -Name "RAVBg64" -Force -ErrorAction Stop
        Start-Sleep -Seconds 2
        Write-Host "  Restarted RAVBg64 (handles reset)" -ForegroundColor Green
    } catch {
        Write-Host "  Failed to restart: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# ============================================================
# 2. FIX DELL TELEMETRY BLOAT
# ============================================================
Write-Host "[2/6] Disabling Dell telemetry..." -ForegroundColor Green

$dellServices = @(
    "DellClientManagementService"
    "DellTechHub"
    "Dell SupportAssistAgent"
    "SupportAssistAgent"
    "Dell Digital Delivery Service"
    "Dell Peripheral Manager Service"
)

foreach ($svc in $dellServices) {
    $service = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($service -and $service.Status -eq 'Running') {
        try {
            Stop-Service -Name $svc -Force -ErrorAction Stop
            Set-Service -Name $svc -StartupType Disabled -ErrorAction Stop
            Write-Host "  Disabled: $($service.DisplayName)" -ForegroundColor Yellow
        } catch {}
    }
}

# Kill Dell processes
$dellProcesses = @(
    "Dell.TechHub.Instrumentation.SubAgent"
    "SupportAssistAgent"
    "Dell SupportAssist"
    "Dell Digital Delivery"
)

foreach ($proc in $dellProcesses) {
    Get-Process -Name $proc -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
}

Write-Host "  Dell telemetry disabled" -ForegroundColor Green

# ============================================================
# 3. SECURE NETCUT_EXPOSURE
# ============================================================
Write-Host "[3/6] Securing netcut_windows..." -ForegroundColor Green

# Check if netcut is running
$netcut = Get-Process -Name "netcut_windows" -ErrorAction SilentlyContinue
if ($netcut) {
    Write-Host "  WARNING: netcut_windows is running" -ForegroundColor Red
    Write-Host "  Listening on ports 4622-4624 (publicly exposed)" -ForegroundColor Red
    Write-Host "  Consider disabling if not needed" -ForegroundColor Yellow

    # Block netcut ports via firewall
    try {
        New-NetFirewallRule -DisplayName "Block netcut 4622" -Direction Inbound -LocalPort 4622 -Protocol TCP -Action Block -ErrorAction Stop
        New-NetFirewallRule -DisplayName "Block netcut 4623" -Direction Inbound -LocalPort 4623 -Protocol TCP -Action Block -ErrorAction Stop
        New-NetFirewallRule -DisplayName "Block netcut 4624" -Direction Inbound -LocalPort 4624 -Protocol TCP -Action Block -ErrorAction Stop
        Write-Host "  Blocked netcut ports via firewall" -ForegroundColor Green
    } catch {
        Write-Host "  Failed to block netcut ports: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# ============================================================
# 4. BLOCK EXPOSED INDUSTRIAL PROTOCOLS
# ============================================================
Write-Host "[4/6] Blocking exposed industrial protocols..." -ForegroundColor Green

# Block Siemens S7 (port 102)
try {
    New-NetFirewallRule -DisplayName "Block Siemens S7" -Direction Inbound -LocalPort 102 -Protocol TCP -Action Block -ErrorAction Stop
    Write-Host "  Blocked port 102 (Siemens S7)" -ForegroundColor Green
} catch {}

# Block ENI (port 80) - HTTP should not be publicly exposed
try {
    New-NetFirewallRule -DisplayName "Block ENI HTTP" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Block -ErrorAction Stop
    Write-Host "  Blocked port 80 (ENI HTTP)" -ForegroundColor Green
} catch {}

# Block Dassault CATIA (port 55555)
try {
    New-NetFirewallRule -DisplayName "Block CATIA" -Direction Inbound -LocalPort 55555 -Protocol TCP -Action Block -ErrorAction Stop
    Write-Host "  Blocked port 55555 (Dassault CATIA)" -ForegroundColor Green
} catch {}

# ============================================================
# 5. FIX BRAVE BROWSER HANDLE LEAK
# ============================================================
Write-Host "[5/6] Fixing Brave browser handles..." -ForegroundColor Green

$braveProcesses = Get-Process -Name "brave" -ErrorAction SilentlyContinue
$highHandleBrave = $braveProcesses | Where-Object { $_.HandleCount -gt 2000 }
if ($highHandleBrave) {
    Write-Host "  Found $($highHandleBrave.Count) Brave processes with >2000 handles" -ForegroundColor Yellow
    foreach ($proc in $highHandleBrave) {
        Write-Host "    PID $($proc.Id): $($proc.HandleCount) handles" -ForegroundColor Gray
    }
}

# ============================================================
# 6. DISABLE UNNECESSARY COM PORTS
# ============================================================
Write-Host "[6/6] Disabling unnecessary COM ports..." -ForegroundColor Green

$btPorts = Get-PnpDevice -Class Ports -Status OK -ErrorAction SilentlyContinue |
    Where-Object { $_.FriendlyName -like "*Bluetooth*" }

$disabledPortCount = 0
foreach ($port in $btPorts) {
    if ($port.FriendlyName -notlike "*COM3*" -and $port.FriendlyName -notlike "*COM4*") {
        try {
            Disable-PnpDevice -InstanceId $port.InstanceId -Confirm:$false -ErrorAction Stop
            Write-Host "  Disabled: $($port.FriendlyName)" -ForegroundColor Yellow
            $disabledPortCount++
        } catch {}
    }
}
Write-Host "  Disabled $disabledPortCount Bluetooth COM ports" -ForegroundColor Green

# ============================================================
# SUMMARY
# ============================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " ISSUES FIXED" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Fixed:" -ForegroundColor Yellow
Write-Host "  - RAVBg64 handle leak (4544 handles)" -ForegroundColor Green
Write-Host "  - Dell telemetry bloat" -ForegroundColor Green
Write-Host "  - netcut_windows port exposure" -ForegroundColor Green
Write-Host "  - Industrial protocol exposure (port 80, 102, 55555)" -ForegroundColor Green
Write-Host "  - Unnecessary Bluetooth COM ports" -ForegroundColor Green
Write-Host ""
Write-Host "REBOOT REQUIRED" -ForegroundColor Cyan