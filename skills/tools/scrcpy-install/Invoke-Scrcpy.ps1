param(
    [switch]$Mirror,
    [switch]$NoBorder,
    [switch]$Fullscreen,
    [switch]$ListDevices,
    [string]$Record,
    [string]$ConnectWireless,
    [string]$Push,
    [string]$Pull,
    [string]$ScreenShot,
    [int]$MaxSize = 0,
    [int]$MaxFps = 0,
    [string]$BitRate = "",
    [switch]$TurnScreenOff,
    [switch]$Help
)

$ScrcpyDir = "$env:ProgramFiles\scrcpy"
$Adb = "$ScrcpyDir\adb.exe"
$Scrcpy = "$ScrcpyDir\scrcpy.exe"

function Show-Help {
    Write-Host @"
Invoke-Scrcpy.ps1 — Scrcpy wrapper for Android screen mirroring

USAGE:
  .\Invoke-Scrcpy.ps1 -Mirror                    # Standard USB mirror
  .\Invoke-Scrcpy.ps1 -Mirror -NoBorder          # Borderless window
  .\Invoke-Scrcpy.ps1 -Mirror -Fullscreen        # Fullscreen mode
  .\Invoke-Scrcpy.ps1 -Mirror -MaxSize 1024 -MaxFps 30  # Low bandwidth
  .\Invoke-Scrcpy.ps1 -Record "out.mp4"          # Record screen
  .\Invoke-Scrcpy.ps1 -ConnectWireless "192.168.1.100"  # WiFi connect
  .\Invoke-Scrcpy.ps1 -ListDevices               # Show connected devices
  .\Invoke-Scrcpy.ps1 -Push "file" "/sdcard/"    # Push file to device
  .\Invoke-Scrcpy.ps1 -Pull "/sdcard/file" "."   # Pull file from device
  .\Invoke-Scrcpy.ps1 -ScreenShot "shot.png"     # Take screenshot
  .\Invoke-Scrcpy.ps1 -Help                      # This help

FLAGS for -Mirror:
  -NoBorder          Remove window border
  -Fullscreen        Start in fullscreen
  -TurnScreenOff     Turn off device screen while mirroring
  -MaxSize N         Limit resolution (e.g. 1024)
  -MaxFps N          Limit frame rate (e.g. 30)
  -BitRate "4M"      Limit bandwidth (e.g. "2M", "4M", "8M")

ADB wireless setup (one-time):
  Connect USB → adb tcpip 5555 → disconnect USB → adb connect <IP>:5555
"@
    exit
}

if ($Help) { Show-Help }

if (-not (Test-Path $Scrcpy)) {
    Write-Host "ERROR: scrcpy not found. Run Install-Scrcpy.ps1 first." -ForegroundColor Red
    exit 1
}

if ($ListDevices) {
    Write-Host "Connected devices:" -ForegroundColor Cyan
    & $Adb devices -l
    exit
}

if ($ConnectWireless) {
    Write-Host "Setting up wireless connection to $ConnectWireless ..." -ForegroundColor Yellow
    & $Adb connect "$ConnectWireless`:5555"
    Write-Host "Done. Run with -Mirror to start." -ForegroundColor Green
    exit
}

if ($Push) {
    $target = if ($Pull) { $Pull } else { "/sdcard/" }
    Write-Host "Pushing $Push to $target ..." -ForegroundColor Yellow
    & $Adb push $Push $target
    exit
}

if ($Pull) {
    $target = if ($Push) { $Push } else { "." }
    Write-Host "Pulling $Pull to $target ..." -ForegroundColor Yellow
    & $Adb pull $Pull $target
    exit
}

if ($ScreenShot) {
    Write-Host "Taking screenshot -> $ScreenShot ..." -ForegroundColor Yellow
    & $Adb exec-out screencap -p > $ScreenShot
    Write-Host "  ✓ Saved" -ForegroundColor Green
    exit
}

if ($Mirror) {
    $args = @()
    if ($NoBorder) { $args += "--no-border" }
    if ($Fullscreen) { $args += "--fullscreen" }
    if ($TurnScreenOff) { $args += "--turn-screen-off" }
    if ($MaxSize -gt 0) { $args += "--max-size", $MaxSize }
    if ($MaxFps -gt 0) { $args += "--max-fps", $MaxFps }
    if ($BitRate) { $args += "--bit-rate", $BitRate }
    if ($Record) { $args += "--record", $Record }

    Write-Host "Starting scrcpy mirror ..." -ForegroundColor Cyan
    Write-Host "  Press Ctrl+C to stop" -ForegroundColor Gray
    & $Scrcpy $args
    exit
}

if ($Record -and -not $Mirror) {
    Write-Host "Recording screen to $Record (no window)..." -ForegroundColor Yellow
    & $Scrcpy --no-window --record $Record
    exit
}

Write-Host "No action specified. Use -Help to see options." -ForegroundColor Yellow
