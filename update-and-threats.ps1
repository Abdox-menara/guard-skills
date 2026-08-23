#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Windows Update and threat investigation script
.DESCRIPTION
    Checks for missing updates and investigates Kepavll/DefenderTamperingRestore threats
.NOTES
    Run as Administrator: Right-click PowerShell > Run as Administrator
    Then: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\update-and-threats.ps1
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " WINDOWS UPDATE & THREAT INVESTIGATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# PART 1: Windows Update
# ============================================================
Write-Host "=== PART 1: WINDOWS UPDATE ===" -ForegroundColor Yellow
Write-Host ""

Write-Host "[1/3] Checking for available updates..." -ForegroundColor Green
try {
    $updateSession = New-Object -ComObject Microsoft.Update.Session
    $updateSearcher = $updateSession.CreateUpdateSearcher()
    $searchResult = $updateSearcher.Search("IsInstalled=0")

    if ($searchResult.Updates.Count -gt 0) {
        Write-Host "  Found $($searchResult.Updates.Count) available updates:" -ForegroundColor Yellow
        foreach ($update in $searchResult.Updates) {
            Write-Host "    - $($update.Title)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  No updates available" -ForegroundColor Green
    }
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "[2/3] Checking installed updates..." -ForegroundColor Green
try {
    $installedUpdates = $updateSearcher.Search("IsInstalled=1")
    Write-Host "  Installed updates: $($installedUpdates.Updates.Count)" -ForegroundColor Gray

    # Check for critical/security updates
    $criticalUpdates = @()
    foreach ($update in $installedUpdates.Updates) {
        if ($update.MsrcSeverity -eq "Critical" -or $update.MsrcSeverity -eq "Important") {
            $criticalUpdates += $update
        }
    }
    Write-Host "  Critical/Important updates: $($criticalUpdates.Count)" -ForegroundColor Gray
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "[3/3] Checking hotfix history..." -ForegroundColor Green
try {
    $hotfixes = Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5
    foreach ($hf in $hotfixes) {
        Write-Host "  $($hf.HotFixID) - $($hf.InstalledOn.ToString('yyyy-MM-dd')) - $($hf.Description)" -ForegroundColor Gray
    }
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================
# PART 2: Threat Investigation
# ============================================================
Write-Host ""
Write-Host "=== PART 2: THREAT INVESTIGATION ===" -ForegroundColor Yellow
Write-Host ""

Write-Host "[1/4] Checking Defender threat history..." -ForegroundColor Green
try {
    $threatHistory = Get-MpThreatDetection | Sort-Object InitialDetectionTime -Descending | Select-Object -First 10
    if ($threatHistory) {
        foreach ($threat in $threatHistory) {
            Write-Host "  Threat: $($threat.ThreatID) - $($threat.InitialDetectionTime)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  No recent threats detected" -ForegroundColor Green
    }
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "[2/4] Checking threat catalog..." -ForegroundColor Green
try {
    $threats = Get-MpThreat | Sort-Object IsActive -Descending
    if ($threats) {
        foreach ($threat in $threats) {
            $status = if ($threat.IsActive) { "ACTIVE" } else { "INACTIVE" }
            Write-Host "  [$status] $($threat.ThreatName) - Severity: $($threat.SeverityID)" -ForegroundColor $(if ($threat.IsActive) { "Red" } else { "Gray" })
        }
    } else {
        Write-Host "  No threats in catalog" -ForegroundColor Green
    }
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "[3/4] Checking protection history..." -ForegroundColor Green
try {
    $protectionHistory = Get-MpProtectionStatus
    Write-Host "  Real-time protection: $($protectionHistory.RealTimeProtectionEnabled)" -ForegroundColor $(if ($protectionHistory.RealTimeProtectionEnabled) { "Green" } else { "Red" })
    Write-Host "  Behavior monitor: $($protectionHistory.BehaviorMonitorEnabled)" -ForegroundColor $(if ($protectionHistory.BehaviorMonitorEnabled) { "Green" } else { "Red" })
    Write-Host "  Anti-spyware: $($protectionHistory.AntiSpywareEnabled)" -ForegroundColor $(if ($protectionHistory.AntiSpywareEnabled) { "Green" } else { "Red" })
    Write-Host "  Antivirus enabled: $($protectionHistory.AntivirusEnabled)" -ForegroundColor $(if ($protectionHistory.AntivirusEnabled) { "Green" } else { "Red" })
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "[4/4] Scanning for Kepavll remnants..." -ForegroundColor Green
try {
    # Check common locations for Kepavll
    $kepavllPaths = @(
        "$env:TEMP",
        "$env:LOCALAPPDATA\Temp",
        "$env:APPDATA",
        "$env:LOCALAPPDATA",
        "C:\WINDOWS\Temp",
        "C:\WINDOWS\Prefetch"
    )

    $found = $false
    foreach ($path in $kepavllPaths) {
        if (Test-Path $path) {
            $items = Get-ChildItem -Path $path -Recurse -Force -ErrorAction SilentlyContinue |
                Where-Object { $_.Name -like "*kepavll*" -or $_.Name -like "*Kepavll*" }
            if ($items) {
                foreach ($item in $items) {
                    Write-Host "  FOUND: $($item.FullName)" -ForegroundColor Red
                    $found = $true
                }
            }
        }
    }

    if (-not $found) {
        Write-Host "  No Kepavll files found in common locations" -ForegroundColor Green
    }
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================
# PART 3: Recommendations
# ============================================================
Write-Host ""
Write-Host "=== RECOMMENDATIONS ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Install all available Windows updates" -ForegroundColor Cyan
Write-Host "   Run: Start-Process ms-settings:windowsupdate" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Run full Defender scan" -ForegroundColor Cyan
Write-Host "   Run: Start-MpScan -ScanType FullScan" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Check Kepavll in Defender quarantine" -ForegroundColor Cyan
Write-Host "   Run: Get-MpThreatDetection | Where-Object { \$_.ThreatName -like '*Kepavll*' }" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Monitor for recurrence" -ForegroundColor Cyan
Write-Host "   Run: Get-MpThreatDetection | Sort-Object InitialDetectionTime -Descending" -ForegroundColor Gray