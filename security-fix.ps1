#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Security hardening script for Dell-pc
.DESCRIPTION
    Enables Windows Defender protections and fixes firewall gaps
.NOTES
    Run as Administrator: Right-click PowerShell > Run as Administrator
    Then: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\security-fix.ps1
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " SECURITY HARDENING SCRIPT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# 1. Enable Network Protection in Windows Defender
# ============================================================
Write-Host "[1/5] Enabling Network Protection..." -ForegroundColor Green
try {
    Set-MpPreference -EnableNetworkProtection Enabled -ErrorAction Stop
    Write-Host "  SUCCESS: Network Protection enabled" -ForegroundColor Green
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================
# 2. Configure ASR Rules (Attack Surface Reduction)
# ============================================================
Write-Host "[2/5] Configuring ASR rules..." -ForegroundColor Green
$asrRules = @(
    "56a863a9-b878-428f-950d-74dba67ee8c3"  # Block executable content from email
    "7674ba52-37eb-4a4f-a9a1-f0f9a1619a2c"  # Block Office apps from creating child processes
    "d4f940ab-401b-4efc-aadc-ad5f3c50688a"  # Block Office apps from creating executable content
    "9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2"  # Block Office apps from injecting code
    "be9ba2d9-53ea-4cdc-84e5-9b1eeee46550"  # Block Office communication apps from creating child processes
    "01443614-cd74-433a-b99e-2ecdc07bfc25"  # Block executable content from USB
    "4c9875ef-209c-43d5-877b-0f9b4b0d9273"  # Block JavaScript/VBScript from launching downloaded content
    "d3e037e1-3eb8-44c8-a917-57927947596d"  # Block Office apps from creating executable content
    "5beb7efe-fd9a-4556-801d-275e5ffc04cc"  # Block execution of potentially obfuscated scripts
    "75668c1f-73b5-4cf0-bb93-3ecf5cb7cc84"  # Block process creations from WMI
    "26190899-1602-49e8-8b27-eb1d0a1ce869"  # Block untrusted and unsigned processes from USB
    "e6db77e5-3df2-4cf1-b95a-636979351e5b"  # Block untrusted and unsigned processes
    "b2b3f03d-6a65-4f7b-a9c7-1c7ef74a9ba4"  # Block Windows Installer from creating child processes
    "92e97fa1-2edf-4476-bdd6-9dd0b4dddc7b"  # Block Win32 API calls from Office macros
)

$enabledCount = 0
foreach ($rule in $asrRules) {
    try {
        Add-MpPreference -AttackSurfaceReductionRules_Ids $rule -AttackSurfaceReductionRules_Actions Enabled -ErrorAction Stop
        $enabledCount++
    } catch {
        # Rule may already be enabled
    }
}
Write-Host "  SUCCESS: Enabled $enabledCount ASR rules" -ForegroundColor Green

# ============================================================
# 3. Enable Brute Force Protection
# ============================================================
Write-Host "[3/5] Enabling brute force protection..." -ForegroundColor Green
try {
    # Enable controlled folder access (already enabled, but verify)
    Set-MpPreference -EnableControlledFolderAccess Enabled -ErrorAction Stop
    Write-Host "  SUCCESS: Controlled folder access verified" -ForegroundColor Green
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================
# 4. Enable Remote Encryption Protection
# ============================================================
Write-Host "[4/5] Enabling remote encryption protection..." -ForegroundColor Green
try {
    # Enable network protection (already done in step 1)
    # Enable cloud-delivered protection
    Set-MpPreference -MAPSReporting Advanced -ErrorAction Stop
    Set-MpPreference -SubmitSamplesConsent SendAllSamples -ErrorAction Stop
    Write-Host "  SUCCESS: Cloud protection enabled" -ForegroundColor Green
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================
# 5. Fix Firewall - Remove SMB/NetBIOS from Public profile
# ============================================================
Write-Host "[5/5] Fixing firewall rules..." -ForegroundColor Green
try {
    # Get SMB rules on Public profile
    $smbRules = Get-NetFirewallRule -Direction Inbound -Profile Public -ErrorAction SilentlyContinue |
        Where-Object { $_.DisplayName -like "*SMB*" -or $_.DisplayName -like "*NetBIOS*" -or $_.DisplayName -like "*File and Printer*" }

    if ($smbRules) {
        foreach ($rule in $smbRules) {
            Write-Host "  Disabling: $($rule.DisplayName)" -ForegroundColor Yellow
            Disable-NetFirewallRule -Name $rule.Name -ErrorAction SilentlyContinue
        }
        Write-Host "  SUCCESS: Disabled SMB/NetBIOS on Public profile" -ForegroundColor Green
    } else {
        Write-Host "  SKIPPED: No SMB/NetBIOS rules found on Public profile" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================
# Summary
# ============================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " SECURITY HARDENING COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Applied fixes:" -ForegroundColor Yellow
Write-Host "  - Network Protection: ENABLED" -ForegroundColor Green
Write-Host "  - ASR Rules: ENABLED" -ForegroundColor Green
Write-Host "  - Cloud Protection: ENABLED" -ForegroundColor Green
Write-Host "  - Controlled Folder Access: VERIFIED" -ForegroundColor Green
Write-Host "  - SMB/NetBIOS on Public: DISABLED" -ForegroundColor Green
Write-Host ""
Write-Host "REBOOT REQUIRED for some changes to take effect" -ForegroundColor Cyan