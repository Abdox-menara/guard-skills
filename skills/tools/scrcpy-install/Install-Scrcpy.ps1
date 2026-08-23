param(
    [switch]$InstallOnly,
    [switch]$DesktopShortcut,
    [switch]$StartMenuShortcut,
    [switch]$Remove
)

$SrcDir = "H:\tmp\scrcpy-win64-v4.1\scrcpy-win64-v4.1"
$DestDir = "$env:ProgramFiles\scrcpy"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$StartMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Scrcpy"

function Write-Banner {
    Write-Host "╔══════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║     Scrcpy v4.1 Installer            ║" -ForegroundColor Cyan
    Write-Host "║     Android Screen Mirroring Tool    ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════╝" -ForegroundColor Cyan
}

function Install-Scrcpy {
    Write-Host "`n[1/5] Copying files to $DestDir ..." -ForegroundColor Yellow
    if (-not (Test-Path $SrcDir)) {
        Write-Host "ERROR: Source not found at $SrcDir" -ForegroundColor Red
        exit 1
    }
    New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
    Copy-Item "$SrcDir\*" $DestDir -Recurse -Force
    Write-Host "  ✓ Files copied" -ForegroundColor Green

    Write-Host "[2/5] Adding to user PATH ..." -ForegroundColor Yellow
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$DestDir*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$DestDir", "User")
        $env:Path = "$env:Path;$DestDir"
        Write-Host "  ✓ PATH updated" -ForegroundColor Green
    } else {
        Write-Host "  ✓ Already in PATH" -ForegroundColor Green
    }

    Write-Host "[3/5] Creating Desktop shortcut ..." -ForegroundColor Yellow
    $wshell = New-Object -ComObject WScript.Shell
    $shortcut = $wshell.CreateShortcut("$DesktopPath\Scrcpy Mirror.lnk")
    $shortcut.TargetPath = "$DestDir\scrcpy.exe"
    $shortcut.IconLocation = "$DestDir\scrcpy.exe,0"
    $shortcut.WorkingDirectory = $DestDir
    $shortcut.Description = "Android Screen Mirroring (scrcpy v4.1)"
    $shortcut.Save()
    Write-Host "  ✓ Desktop shortcut created" -ForegroundColor Green

    Write-Host "[4/5] Creating Start Menu shortcuts ..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $StartMenuPath -Force | Out-Null

    $mirrorSc = $wshell.CreateShortcut("$StartMenuPath\Scrcpy Mirror.lnk")
    $mirrorSc.TargetPath = "$DestDir\scrcpy.exe"
    $mirrorSc.IconLocation = "$DestDir\scrcpy.exe,0"
    $mirrorSc.WorkingDirectory = $DestDir
    $mirrorSc.Save()

    $shellSc = $wshell.CreateShortcut("$StartMenuPath\Scrcpy Shell.lnk")
    $shellSc.TargetPath = "powershell.exe"
    $shellSc.Arguments = "-NoExit -Command Set-Location '$DestDir'"
    $shellSc.IconLocation = "$DestDir\scrcpy.exe,0"
    $shellSc.WorkingDirectory = $DestDir
    $shellSc.Save()

    Write-Host "  ✓ Start Menu shortcuts created" -ForegroundColor Green

    Write-Host "[5/5] Verifying installation ..." -ForegroundColor Yellow
    if (Test-Path "$DestDir\scrcpy.exe") {
        $ver = & "$DestDir\scrcpy.exe" --version 2>&1 | Select-Object -First 1
        Write-Host "  ✓ scrcpy installed: $ver" -ForegroundColor Green
    }
    if (Test-Path "$DestDir\adb.exe") {
        $adbVer = & "$DestDir\adb.exe" --version 2>&1 | Select-Object -First 1
        Write-Host "  ✓ ADB available: $adbVer" -ForegroundColor Green
    }

    Write-Host "`n╔══════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  Scrcpy v4.1 Installation Complete!  ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host "`nQuick start:" -ForegroundColor White
    Write-Host "  1. Connect Android phone via USB" -ForegroundColor White
    Write-Host "  2. Enable USB debugging on phone" -ForegroundColor White
    Write-Host "  3. Run: scrcpy" -ForegroundColor Green
    Write-Host "`nFor wireless: adb tcpip 5555 then adb connect DEVICE-IP:5555" -ForegroundColor White
}

function Remove-Scrcpy {
    Write-Host "Removing scrcpy installation ..." -ForegroundColor Yellow

    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -like "*$DestDir*") {
        $newPath = ($currentPath.Split(';') | Where-Object { $_ -ne $DestDir }) -join ';'
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "  ✓ Removed from PATH" -ForegroundColor Green
    }

    if (Test-Path $DestDir) {
        Remove-Item $DestDir -Recurse -Force
        Write-Host "  ✓ Removed $DestDir" -ForegroundColor Green
    }

    if (Test-Path "$DesktopPath\Scrcpy Mirror.lnk") {
        Remove-Item "$DesktopPath\Scrcpy Mirror.lnk" -Force
        Write-Host "  ✓ Desktop shortcut removed" -ForegroundColor Green
    }
    if (Test-Path $StartMenuPath) {
        Remove-Item $StartMenuPath -Recurse -Force
        Write-Host "  ✓ Start Menu shortcuts removed" -ForegroundColor Green
    }
    Write-Host "`nScrcpy uninstalled." -ForegroundColor Cyan
}

Write-Banner

if ($Remove) {
    Remove-Scrcpy
} else {
    Install-Scrcpy
}
