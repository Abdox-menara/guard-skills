#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Comprehensive disk cleanup script for Dell-pc
.DESCRIPTION
    Targets safe-to-remove items to free space on C: drive
    Current status: 47.71 GB free of 599.9 GB (92% full)
.NOTES
    Run as Administrator: Right-click PowerShell > Run as Administrator
    Then: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\cleanup.ps1
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " DISK CLEANUP SCRIPT" -ForegroundColor Cyan
Write-Host " Target: Free 60+ GB on C: drive" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$before = (Get-PSDrive C).Used
Write-Host "Starting C: drive used: $([math]::Round($before/1GB, 2)) GB" -ForegroundColor Yellow
Write-Host ""

# ============================================================
# 1. Windows.old (39.76 GB) - SAFE TO REMOVE
# ============================================================
Write-Host "[1/10] Removing Windows.old folder..." -ForegroundColor Green
if (Test-Path "C:\Windows.old") {
    try {
        Remove-Item -Path "C:\Windows.old" -Recurse -Force -ErrorAction Stop
        Write-Host "  SUCCESS: Removed Windows.old (~40 GB freed)" -ForegroundColor Green
    } catch {
        Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "  SKIPPED: Windows.old not found" -ForegroundColor Yellow
}

# ============================================================
# 2. Claude vm_bundles (11.38 GB) - Can be re-downloaded
# ============================================================
Write-Host "[2/10] Cleaning Claude vm_bundles cache..." -ForegroundColor Green
$claudePath = "$env:LOCALAPPDATA\Claude-3p\vm_bundles"
if (Test-Path $claudePath) {
    try {
        Remove-Item -Path $claudePath -Recurse -Force -ErrorAction Stop
        Write-Host "  SUCCESS: Removed Claude vm_bundles (~11 GB freed)" -ForegroundColor Green
    } catch {
        Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "  SKIPPED: Claude vm_bundles not found" -ForegroundColor Yellow
}

# ============================================================
# 3. uv cache (10.56 GB) - Can be re-downloaded
# ============================================================
Write-Host "[3/10] Cleaning uv cache..." -ForegroundColor Green
$uvPath = "$env:LOCALAPPDATA\uv\cache"
if (Test-Path $uvPath) {
    try {
        Remove-Item -Path $uvPath -Recurse -Force -ErrorAction Stop
        Write-Host "  SUCCESS: Removed uv cache (~10.5 GB freed)" -ForegroundColor Green
    } catch {
        Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "  SKIPPED: uv cache not found" -ForegroundColor Yellow
}

# ============================================================
# 4. Arduino15 staging (3.89 GB) - Safe to remove
# ============================================================
Write-Host "[4/10] Cleaning Arduino15 staging..." -ForegroundColor Green
$arduinoStaging = "$env:LOCALAPPDATA\Arduino15\staging"
if (Test-Path $arduinoStaging) {
    try {
        Remove-Item -Path $arduinoStaging -Recurse -Force -ErrorAction Stop
        Write-Host "  SUCCESS: Removed Arduino15 staging (~3.9 GB freed)" -ForegroundColor Green
    } catch {
        Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "  SKIPPED: Arduino15 staging not found" -ForegroundColor Yellow
}

# ============================================================
# 5. npm cache (1.34 GB) - Safe to remove
# ============================================================
Write-Host "[5/10] Cleaning npm cache..." -ForegroundColor Green
try {
    npm cache clean --force 2>$null
    Write-Host "  SUCCESS: Cleaned npm cache (~1.3 GB freed)" -ForegroundColor Green
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================
# 6. Crash dumps (36.62 MB) - Safe to remove
# ============================================================
Write-Host "[6/10] Cleaning crash dumps..." -ForegroundColor Green
$dumpPath = "$env:LOCALAPPDATA\CrashDumps"
if (Test-Path $dumpPath) {
    try {
        Remove-Item -Path "$dumpPath\*" -Recurse -Force -ErrorAction Stop
        Write-Host "  SUCCESS: Removed crash dumps" -ForegroundColor Green
    } catch {
        Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# ============================================================
# 7. Temp files cleanup
# ============================================================
Write-Host "[7/10] Cleaning temp files..." -ForegroundColor Green
$tempPaths = @(
    "$env:TEMP",
    "$env:LOCALAPPDATA\Temp",
    "C:\WINDOWS\Temp"
)
foreach ($path in $tempPaths) {
    if (Test-Path $path) {
        Remove-Item -Path "$path\*" -Recurse -Force -ErrorAction SilentlyContinue
    }
}
Write-Host "  SUCCESS: Cleaned temp files" -ForegroundColor Green

# ============================================================
# 8. Downloads folder (check for installers)
# ============================================================
Write-Host "[8/10] Cleaning Downloads folder..." -ForegroundColor Green
$downloads = "C:\Users\Abdox\Downloads"
$oldInstallers = Get-ChildItem -Path $downloads -Filter "*.exe" -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }
if ($oldInstallers) {
    foreach ($file in $oldInstallers) {
        Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
        Write-Host "  Removed: $($file.Name)" -ForegroundColor Gray
    }
    Write-Host "  SUCCESS: Cleaned old installers from Downloads" -ForegroundColor Green
} else {
    Write-Host "  SKIPPED: No old installers found" -ForegroundColor Yellow
}

# ============================================================
# 9. Brave browser cache
# ============================================================
Write-Host "[9/10] Cleaning Brave browser cache..." -ForegroundColor Green
$braveCache = "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\Cache"
$braveCodeCache = "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\Code Cache"
$braveGPUCache = "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default\GPUCache"
foreach ($path in @($braveCache, $braveCodeCache, $braveGPUCache)) {
    if (Test-Path $path) {
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}
Write-Host "  SUCCESS: Cleaned Brave browser caches" -ForegroundColor Green

# ============================================================
# 10. Windows Update cleanup (via DISM)
# ============================================================
Write-Host "[10/10] Running Windows Update cleanup..." -ForegroundColor Green
try {
    Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase 2>$null
    Write-Host "  SUCCESS: Windows Update component cleanup complete" -ForegroundColor Green
} catch {
    Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================
# Summary
# ============================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " CLEANUP COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
$after = (Get-PSDrive C).Used
$freed = $before - $after
Write-Host "Before: $([math]::Round($before/1GB, 2)) GB used" -ForegroundColor Yellow
Write-Host "After:  $([math]::Round($after/1GB, 2)) GB used" -ForegroundColor Green
Write-Host "Freed:  $([math]::Round($freed/1GB, 2)) GB" -ForegroundColor Green
Write-Host ""
Write-Host "RECOMMENDED: Run 'cleanmgr' for additional Windows-managed cleanup" -ForegroundColor Cyan