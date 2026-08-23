#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Advanced PC Optimization Script
.DESCRIPTION
    Deep system optimization: services, startup, network, memory, registry
.NOTES
    Run as Administrator
#>

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " ADVANCED PC OPTIMIZATION" -ForegroundColor Cyan
Write-Host " Dell Precision 7520 - i7-6920HQ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$totalFreed = 0

# ============================================================
# 1. DISABLE BLOATWARE SERVICES
# ============================================================
Write-Host "[1/10] Disabling bloatware services..." -ForegroundColor Green

$bloatServices = @(
    "DiagTrack"           # Connected User Experiences and Telemetry
    "dmwappushservice"    # WAP Push Message Routing Service
    "MapsBroker"          # Downloaded Maps Manager
    "lfsvc"               # Geolocation Service
    "SharedAccess"        # Internet Connection Sharing
    "TrkWks"              # Distributed Link Tracking Client
    "SysMain"             # Superfetch (SSD not needed)
    "Fax"                 # Fax Service
    "RetailDemo"          # Retail Demo Service
    "XblAuthManager"      # Xbox Live Auth Manager
    "XblGameSave"         # Xbox Live Game Save
    "XboxNetApiSvc"       # Xbox Live Networking Service
    "XboxGipSvc"          # Xbox Accessory Management Service
    "BDESVC"              # BitLocker Drive Encryption Service
    "wbengine"            # Block Level Backup Engine
    "ScDeviceEnum"        # Smart Card Device Enumeration
    "SCardSvr"            # Smart Card
    "AJRouter"            # AllJoyn Router Service
    "MSiSCSI"             # Microsoft iSCSI Initiator
    "RpcLocator"          # Remote Procedure Call Locator
    "RemoteRegistry"      # Remote Registry
    "RemoteAccess"        # Routing and Remote Access
    "SNMPTRAP"            # SNMP Trap
    "TapiSrv"             # Telephony
    "TlntSvr"             # Telnet
    "WpcMonSvc"           # Parental Controls
    "icssvc"              # Windows Mobile Hotspot
    "SEMgrSvc"            # Payments and NFC/SE Manager
    "PhoneSvc"            # Phone Service
    "QWAVE"               # Quality Windows Audio Video
)

$disabledCount = 0
foreach ($svc in $bloatServices) {
    $service = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($service -and $service.Status -eq 'Running') {
        try {
            Stop-Service -Name $svc -Force -ErrorAction Stop
            Set-Service -Name $svc -StartupType Disabled -ErrorAction Stop
            Write-Host "  Disabled: $($service.DisplayName)" -ForegroundColor Yellow
            $disabledCount++
        } catch {
            Write-Host "  Failed to disable: $($service.DisplayName) - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}
Write-Host "  Disabled $disabledCount bloatware services" -ForegroundColor Green

# ============================================================
# 2. DISABLE UNNECESSARY SCHEDULED TASKS
# ============================================================
Write-Host "[2/10] Disabling unnecessary scheduled tasks..." -ForegroundColor Green

$bloatTasks = @(
    "\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser"
    "\Microsoft\Windows\Application Experience\ProgramDataUpdater"
    "\Microsoft\Windows\Autochk\Proxy"
    "\Microsoft\Windows\CloudExperienceHost\CreateObjectTask"
    "\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector"
    "\Microsoft\Windows\Feedback\Siuf\DmClient"
    "\Microsoft\Windows\Feedback\Siuf\DmClientOnScenarioDownload"
    "\Microsoft\Windows\Maps\MapsToastTask"
    "\Microsoft\Windows\Maps\MapsUpdateTask"
    "\Microsoft\Windows\Windows Error Reporting\QueueReporting"
    "\Microsoft\Windows\WindowsErrorReporting\SystemSoundsService"
)

$disabledTaskCount = 0
foreach ($task in $bloatTasks) {
    try {
        $t = Get-ScheduledTask -TaskPath ($task.Substring(0, $task.LastIndexOf('\') + 1)) -TaskName ($task.Substring($task.LastIndexOf('\') + 1)) -ErrorAction SilentlyContinue
        if ($t -and $t.State -ne 'Disabled') {
            Disable-ScheduledTask -TaskPath $t.TaskPath -TaskName $t.TaskName -ErrorAction Stop | Out-Null
            Write-Host "  Disabled: $($t.TaskName)" -ForegroundColor Yellow
            $disabledTaskCount++
        }
    } catch {}
}
Write-Host "  Disabled $disabledTaskCount scheduled tasks" -ForegroundColor Green

# ============================================================
# 3. OPTIMIZE NETWORK SETTINGS
# ============================================================
Write-Host "[3/10] Optimizing network settings..." -ForegroundColor Green

# Optimize TCP/IP stack
$netParams = "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
$netSettings = @{
    "TcpTimedWaitDelay" = 30           # Reduce TIME_WAIT (default 120)
    "MaxUserPort" = 65534               # Max ephemeral ports
    "TcpMaxDataRetransmissions" = 3     # Reduce retransmissions
    "DefaultTTL" = 64                   # Optimal TTL
    "Tcp1323Opts" = 3                   # Enable timestamps and window scaling
    "SackOpts" = 1                      # Enable SACK
    "TcpWindowSize" = 65535             # Optimal window size
    "GlobalMaxTcpWindowSize" = 65535    # Global window size
}

foreach ($key in $netSettings.Keys) {
    try {
        Set-ItemProperty -Path $netParams -Name $key -Value $netSettings[$key] -Type DWord -ErrorAction Stop
    } catch {}
}

# Disable Nagle's Algorithm (already set from previous analysis)
Write-Host "  Network stack optimized" -ForegroundColor Green

# ============================================================
# 4. OPTIMIZE MEMORY MANAGEMENT
# ============================================================
Write-Host "[4/10] Optimizing memory management..." -ForegroundColor Green

$memParams = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
$memSettings = @{
    "DisablePagingExecutive" = 1        # Keep kernel in RAM
    "LargeSystemCache" = 0              # Optimize for workstation
    "IoPageLockLimit" = 0               # Let Windows manage
    "SessionPoolSize" = 48              # MB
    "NonPagedPoolSize" = 0              # Let Windows manage
    "PagedPoolSize" = 0                 # Let Windows manage
}

foreach ($key in $memSettings.Keys) {
    try {
        Set-ItemProperty -Path $memParams -Name $key -Value $memSettings[$key] -Type DWord -ErrorAction Stop
    } catch {}
}

Write-Host "  Memory management optimized" -ForegroundColor Green

# ============================================================
# 5. OPTIMIZE VISUAL EFFECTS
# ============================================================
Write-Host "[5/10] Optimizing visual effects..." -ForegroundColor Green

$visualParams = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
$visualSettings = @{
    "VisualFXSetting" = 2               # Adjust for best performance
    "ListviewAlphaSelect" = 0           # Disable alpha selection
    "ListviewShadow" = 0                # Disable listview shadow
    "TaskbarAnimations" = 0             # Disable taskbar animations
    "IconSpacing" = -1128               # Compact icon spacing
    "IconVerticalSpacing" = -1128       # Compact vertical spacing
}

foreach ($key in $visualSettings.Keys) {
    try {
        Set-ItemProperty -Path $visualParams -Name $key -Value $visualSettings[$key] -Type DWord -ErrorAction Stop
    } catch {}
}

# Disable transparency
try {
    Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "EnableTransparency" -Value 0 -Type DWord -ErrorAction Stop
} catch {}

Write-Host "  Visual effects optimized" -ForegroundColor Green

# ============================================================
# 6. DISABLE TELEMETRY
# ============================================================
Write-Host "[6/10] Disabling telemetry..." -ForegroundColor Green

$telemetryPaths = @(
    "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection"
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection"
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
)

foreach ($path in $telemetryPaths) {
    if (-not (Test-Path $path)) {
        New-Item -Path $path -Force | Out-Null
    }
}

try {
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name "AllowTelemetry" -Value 0 -Type DWord -ErrorAction Stop
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection" -Name "MaxTelemetryAllowed" -Value 0 -Type DWord -ErrorAction Stop
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection" -Name "AllowTelemetry" -Value 0 -Type DWord -ErrorAction Stop
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection" -Name "MaxTelemetryAllowed" -Value 0 -Type DWord -ErrorAction Stop
} catch {}

Write-Host "  Telemetry disabled" -ForegroundColor Green

# ============================================================
# 7. DISABLE BACKGROUND APPS
# ============================================================
Write-Host "[7/10] Disabling background apps..." -ForegroundColor Green

try {
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" -Name "GlobalUserDisabled" -Value 1 -Type DWord -ErrorAction Stop
    Write-Host "  Background apps disabled" -ForegroundColor Green
} catch {
    Write-Host "  Failed to disable background apps" -ForegroundColor Red
}

# ============================================================
# 8. OPTIMIZE POWER SETTINGS
# ============================================================
Write-Host "[8/10] Optimizing power settings..." -ForegroundColor Green

# Set High Performance power plan
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2>$null

# Disable USB selective suspend
powercfg /setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0 2>$null

# Disable PCI Express Link State Power Management
powercfg /setacvalueindex SCHEME_CURRENT 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0 2>$null

# Disable processor parking
powercfg /setacvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 0cc5b647-c1df-4637-891a-dec35c318583 100 2>$null

# Set minimum processor state to 100%
powercfg /setacvalueindex SCHEME_CURRENT 54533251-82be-4824-96c1-47b60b740d00 893dee8e-2bef-41e0-89c6-b55d0929964c 100 2>$null

powercfg /setactive SCHEME_CURRENT 2>$null
Write-Host "  Power settings optimized" -ForegroundColor Green

# ============================================================
# 9. CLEAN UP SYSTEM FILES
# ============================================================
Write-Host "[9/10] Cleaning up system files..." -ForegroundColor Green

# Clean Windows Update cache
Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\WINDOWS\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service -Name wuauserv -ErrorAction SilentlyContinue

# Clean Windows Installer cache (orphaned patches only)
$installerPath = "C:\WINDOWS\Installer"
$orphanedMsp = Get-ChildItem -Path $installerPath -Filter "*.msp" -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-90) }
if ($orphanedMsp) {
    $freedMB = [math]::Round(($orphanedMsp | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
    $orphanedMsp | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "  Removed $freedMB MB of orphaned patches" -ForegroundColor Green
}

# Clean Delivery Optimization cache
Stop-Service -Name DoSvc -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\WINDOWS\ServiceProfiles\NetworkService\AppData\Local\Microsoft\Windows\DeliveryOptimization\Cache\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service -Name DoSvc -ErrorAction SilentlyContinue

Write-Host "  System files cleaned" -ForegroundColor Green

# ============================================================
# 10. OPTIMIZE PAGEFILE
# ============================================================
Write-Host "[10/10] Optimizing pagefile..." -ForegroundColor Green

# Remove custom pagefiles and set optimal configuration
$pagefile = Get-WmiObject Win32_ComputerSystem -ErrorAction SilentlyContinue
if ($pagefile) {
    try {
        $pagefile.AutomaticManagedPagefile = $false
        $pagefile.Put() | Out-Null

        # Set optimal pagefile size (1.5x RAM)
        $ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1MB, 0)
        $pagefileSize = [math]::Round($ram * 1.5, 0)

        # Remove existing pagefiles
        Get-WmiObject Win32_PageFileSetting -ErrorAction SilentlyContinue | Remove-WmiObject -ErrorAction SilentlyContinue

        # Create new optimal pagefile
        Set-WmiInstance -Class Win32_PageFileSetting -Arguments @{
            Name = "C:\pagefile.sys"
            InitialSize = $pagefileSize
            MaximumSize = $pagefileSize
        } -ErrorAction Stop | Out-Null

        Write-Host "  Pagefile optimized: ${pagefileSize} MB" -ForegroundColor Green
    } catch {
        Write-Host "  Failed to optimize pagefile: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# ============================================================
# SUMMARY
# ============================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " OPTIMIZATION COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Applied optimizations:" -ForegroundColor Yellow
Write-Host "  - Disabled $disabledCount bloatware services" -ForegroundColor Green
Write-Host "  - Disabled $disabledTaskCount scheduled tasks" -ForegroundColor Green
Write-Host "  - Optimized network stack" -ForegroundColor Green
Write-Host "  - Optimized memory management" -ForegroundColor Green
Write-Host "  - Optimized visual effects" -ForegroundColor Green
Write-Host "  - Disabled telemetry" -ForegroundColor Green
Write-Host "  - Disabled background apps" -ForegroundColor Green
Write-Host "  - Optimized power settings" -ForegroundColor Green
Write-Host "  - Cleaned system files" -ForegroundColor Green
Write-Host "  - Optimized pagefile" -ForegroundColor Green
Write-Host ""
Write-Host "REBOOT REQUIRED for all changes to take effect" -ForegroundColor Cyan
Write-Host ""
Write-Host "Additional recommendations:" -ForegroundColor Yellow
Write-Host "  - Disable VT-x in BIOS for WSL2/Hyper-V performance" -ForegroundColor Gray
Write-Host "  - Replace thermal paste on CPU (9 years old)" -ForegroundColor Gray
Write-Host "  - Consider disabling netcut_windows if not needed" -ForegroundColor Gray