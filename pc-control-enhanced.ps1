#requires -version 7.0

param(
    [string]$Action = "help",
    [string]$Target = "",
    [string]$Value = "",
    [int]$X = 0,
    [int]$Y = 0,
    [int]$W = 0,
    [int]$H = 0,
    [int]$Timeout = 30,
    [switch]$Verbose
)

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor Cyan
}

function Get-ActiveWindowInfo {
    Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        using System.Text;
        using System.Diagnostics;
        public class WinAPI {
            [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
            [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
            [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint pid);
        }
"@
    $hwnd = [WinAPI]::GetForegroundWindow()
    $sb = New-Object System.Text.StringBuilder 256
    [WinAPI]::GetWindowText($hwnd, $sb, 256) | Out-Null
    $pid = 0
    [WinAPI]::GetWindowThreadProcessId($hwnd, [ref]$pid) | Out-Null
    return @{ Handle = $hwnd; Title = $sb.ToString(); PID = $pid }
}

function Get-WindowByTitle {
    param([string]$Title)
    $windows = @()
    Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        using System.Text;
        public class WinEnum {
            public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
            [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
            [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
            [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
        }
"@
    $winList = [System.Collections.Generic.List[object]]::new()
    $callback = [WinEnum+EnumWindowsProc]{
        param($hWnd, $lParam)
        $sb = New-Object System.Text.StringBuilder 256
        [WinEnum]::GetWindowText($hWnd, $sb, 256) | Out-Null
        $visible = [WinEnum]::IsWindowVisible($hWnd)
        if ($sb.ToString().Trim() -ne "" -and $visible) {
            $winList.Add(@{ Handle = $hWnd; Title = $sb.ToString() })
        }
        return $true
    }
    [WinEnum]::EnumWindows($callback, [IntPtr]::Zero) | Out-Null
    if ($Title) {
        return $winList | Where-Object { $_.Title -like "*$Title*" }
    }
    return $winList
}

function Show-Notification {
    param([string]$Title, [string]$Text, [string]$Type = "Info")
    $icon = switch ($Type) { "Error" { "Error" } "Warning" { "Warning" } default { "Info" } }
    $baloon = New-Object System.Windows.Forms.NotifyIcon
    $baloon.Icon = [System.Drawing.SystemIcons]::Information
    $baloon.BalloonTipTitle = $Title
    $baloon.BalloonTipText = $Text
    $baloon.Visible = $true
    $baloon.ShowBalloonTip(3000)
    Start-Sleep -Milliseconds 100
    $baloon.Dispose()
}

switch ($Action) {
    "help" {
        Write-Host @"

PC Control Enhanced - PowerShell Automation Module
===================================================
Actions:
  help                          Show this help
  windows                       List all open windows
  active-window                 Show active window info
  find-window -Target <name>    Find windows by title
  activate -Target <name>       Activate a window by title
  close -Target <name>          Close a window by title
  minimize-all                  Minimize all windows
  show-desktop                  Show desktop (Win+D)
  type -Value <text>            Type text at cursor
  key -Value <key>              Press a key (enter, tab, etc.)
  hotkey -Value <combo>         Send hotkey (ctrl+c, alt+tab)
  notify -Title <t> -Value <m>  Show notification
  screenshot [-Target <path>]   Take screenshot
  process-list                  List top processes
  process-kill -Target <name>   Kill process by name
  info                          System information
  clipboard-get                 Get clipboard content
  clipboard-set -Value <text>   Set clipboard content
  monitor-list                  List all monitors
  volume-mute                   Toggle mute
  volume-set -Value <0-100>     Set volume level
  brightness -Value <0-100>     Set brightness (if supported)
  lock                          Lock workstation
  sleep                         Sleep computer
  restart                       Restart computer
  shutdown                      Shutdown computer
  run -Value <command>          Run a command/program
  reg-read -Target <path>       Read registry value
  reg-write -Target <path>      Write registry value
  service-list                  List services
  service-start -Target <name>  Start a service
  service-stop -Target <name>   Stop a service
  wifi-list                     List WiFi networks
  wifi-connect -Target <ssid>   Connect to WiFi (set -Value for password)

"@
    }

    "windows" {
        $windows = Get-WindowByTitle
        $windows | Select-Object Title | Format-Table -AutoSize -Wrap
        Write-Log "Total: $($windows.Count) windows"
    }

    "active-window" {
        $info = Get-ActiveWindowInfo
        Write-Log "Active Window: $($info.Title) (PID: $($info.PID))"
        return $info
    }

    "find-window" {
        $windows = Get-WindowByTitle -Title $Target
        $windows | Format-Table -AutoSize
        Write-Log "Found: $($windows.Count) window(s)"
    }

    "activate" {
        Add-Type -AssemblyName Microsoft.VisualBasic
        $windows = Get-WindowByTitle -Title $Target
        if ($windows.Count -eq 0) { Write-Log "No window found"; return }
        try {
            $sig = '[DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);'
            $type = Add-Type -MemberDefinition $sig -Name "WinActivate" -Namespace Win32 -PassThru
            $type::SetForegroundWindow($windows[0].Handle) | Out-Null
            Write-Log "Activated: $($windows[0].Title)"
        } catch { Write-Log "Failed: $_" }
    }

    "close" {
        $windows = Get-WindowByTitle -Title $Target
        if ($windows.Count -eq 0) { Write-Log "No window found"; return }
        $sig = '[DllImport("user32.dll")] public static extern bool PostMessage(IntPtr hWnd, uint Msg, int wParam, int lParam);'
        $type = Add-Type -MemberDefinition $sig -Name "WinClose" -Namespace Win32 -PassThru
        $type::PostMessage($windows[0].Handle, 0x0010, 0, 0) | Out-Null
        Write-Log "Closed: $($windows[0].Title)"
    }

    "minimize-all" {
        $shell = New-Object -ComObject "Shell.Application"
        $shell.MinimizeAll()
        Write-Log "Minimized all windows"
    }

    "show-desktop" {
        $shell = New-Object -ComObject "Shell.Application"
        $shell.ToggleDesktop()
        Write-Log "Toggled desktop"
    }

    "type" {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait($Value)
        Write-Log "Typed: $Value"
    }

    "key" {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait("{$($Value)}")
        Write-Log "Sent key: $Value"
    }

    "hotkey" {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait("$Value")
        Write-Log "Sent hotkey: $Value"
    }

    "notify" {
        Add-Type -AssemblyName System.Windows.Forms
        Show-Notification -Title $Target -Text $Value
    }

    "screenshot" {
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($bounds.X, $bounds.Y, 0, 0, $bounds.Size)
        $path = if ($Target) { $Target } else { Join-Path $env:TEMP "screenshot_$(Get-Date -Format yyyyMMdd_HHmmss).png" }
        $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
        $graphics.Dispose(); $bitmap.Dispose()
        Write-Log "Screenshot saved: $path"
    }

    "process-list" {
        Get-Process | Sort-Object CPU -Descending | Select-Object -First 20 Name, Id, @{N="CPU(s)";E={[math]::Round($_.CPU,1)}}, @{N="Mem(MB)";E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize
    }

    "process-kill" {
        $procs = Get-Process -Name $Target -ErrorAction SilentlyContinue
        if ($procs) { $procs | Stop-Process -Force; Write-Log "Killed $($procs.Count) process(es): $Target" }
        else { Write-Log "No process found: $Target" }
    }

    "info" {
        $os = Get-CimInstance Win32_OperatingSystem
        $cpu = Get-CimInstance Win32_Processor
        $mem = Get-CimInstance Win32_ComputerSystem
        $disk = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3"
        [PSCustomObject]@{
            ComputerName = $env:COMPUTERNAME
            OS = "$($os.Caption) $($os.Version)"
            CPU = $cpu.Name
            Cores = $cpu.NumberOfCores
            RAM_GB = [math]::Round($mem.TotalPhysicalMemory/1GB, 2)
            Disks = ($disk | ForEach-Object { "$($_.DeviceID) $([math]::Round($_.Size/1GB,1))GB" }) -join "; "
            Uptime = "$([math]::Floor((Get-Date)-$os.LastBootUpTime).TotalDays)d $((Get-Date - $os.LastBootUpTime).Hours)h"
            Users = (Get-CimInstance Win32_ComputerSystem).UserName
        } | Format-List
    }

    "clipboard-get" {
        Add-Type -AssemblyName System.Windows.Forms
        $clip = [System.Windows.Forms.Clipboard]::GetText()
        Write-Log "Clipboard: $clip"
        return $clip
    }

    "clipboard-set" {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.Clipboard]::SetText($Value)
        Write-Log "Clipboard set: $Value"
    }

    "monitor-list" {
        Add-Type -AssemblyName System.Windows.Forms
        $screens = [System.Windows.Forms.Screen]::AllScreens
        for ($i = 0; $i -lt $screens.Count; $i++) {
            $s = $screens[$i]
            Write-Log "Monitor $i: $($s.DeviceName) - $($s.Bounds.Width)x$($s.Bounds.Height) at ($($s.Bounds.X),$($s.Bounds.Y)) Primary=$($s.Primary)"
        }
    }

    "volume-mute" {
        $obj = New-Object -ComObject WScript.Shell
        $obj.SendKeys([char]174)
        Write-Log "Volume toggle"
    }

    "volume-set" {
        for ($i = 0; $i -le 50; $i++) {
            $obj = New-Object -ComObject WScript.Shell
            $obj.SendKeys([char]174)
        }
        for ($i = 0; $i -lt [math]::Min([int]$Value / 2, 50); $i++) {
            $obj = New-Object -ComObject WScript.Shell
            $obj.SendKeys([char]175)
        }
        Write-Log "Volume set to ~$Value%"
    }

    "lock" { rundll32.exe user32.dll,LockWorkStation }
    "sleep" { rundll32.exe powrprof.dll,SetSuspendState 0,1,0 }
    "restart" { Restart-Computer -Confirm }
    "shutdown" { Stop-Computer -Confirm }

    "run" {
        if ($Target) { Start-Process $Target; Write-Log "Started: $Target" }
        else { Write-Log "No target specified" }
    }

    "reg-read" {
        $parts = $Target -split '::'
        if ($parts.Count -eq 2) {
            $val = Get-ItemProperty -Path $parts[0] -Name $parts[1] -ErrorAction SilentlyContinue
            if ($val) { Write-Log "$($parts[1]) = $($val.$($parts[1]))" }
        }
    }

    "reg-write" {
        $parts = $Target -split '::'
        if ($parts.Count -eq 2) {
            Set-ItemProperty -Path $parts[0] -Name $parts[1] -Value $Value -ErrorAction SilentlyContinue
            Write-Log "Set $($parts[1]) = $Value"
        }
    }

    "service-list" {
        Get-Service | Where-Object Status -eq Running | Select-Object Name, DisplayName, Status | Format-Table -AutoSize -Wrap
    }

    "service-start" { Start-Service $Target -ErrorAction SilentlyContinue; Write-Log "Started service: $Target" }
    "service-stop" { Stop-Service $Target -ErrorAction SilentlyContinue; Write-Log "Stopped service: $Target" }

    "wifi-list" {
        $nics = Get-NetAdapter -Name "*WiFi*" -ErrorAction SilentlyContinue
        if (-not $nics) { $nics = Get-NetAdapter -Name "*Wireless*" -ErrorAction SilentlyContinue }
        if (-not $nics) { Write-Log "No WiFi adapter found"; return }
        netsh wlan show profiles | Select-String ":\s+(.+)$" | ForEach-Object { $_.Matches.Groups[1].Value } | Sort-Object -Unique
    }

    default {
        Write-Log "Unknown action: $Action"
        Write-Log "Run 'pc-control-enhanced.ps1 help' for available actions"
    }
}
