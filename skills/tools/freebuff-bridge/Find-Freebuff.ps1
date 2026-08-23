param(
    [switch]$Focus,
    [switch]$List
)

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
}
"@

$procs = Get-Process -Name "Freebuff" -ErrorAction SilentlyContinue

if (-not $procs) {
    Write-Host "Freebuff is not running." -ForegroundColor Red
    exit 1
}

Write-Host "Freebuff processes found:" -ForegroundColor Cyan
$procs | ForEach-Object {
    $hwnd = $_.MainWindowHandle
    $title = if ($_.MainWindowTitle) { $_.MainWindowTitle } else { "(no title)" }
    Write-Host "  PID: $($_.Id) | Handle: $hwnd | Title: $title | Memory: $([math]::Round($_.WorkingSet64/1MB,1))MB"
}

if ($Focus) {
    $target = $procs | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
    if (-not $target) {
        $target = $procs | Select-Object -First 1
    }
    $hwnd = $target.MainWindowHandle
    if ($hwnd -ne 0) {
        [Win32]::ShowWindow($hwnd, 9) | Out-Null
        [Win32]::SetForegroundWindow($hwnd) | Out-Null
        Write-Host "`nFreebuff brought to focus (PID: $($target.Id))" -ForegroundColor Green
    } else {
        Write-Host "`nFreebuff has no main window handle. Try Alt+Tab." -ForegroundColor Yellow
    }
}

if ($List) {
    Write-Host "`nAll Freebuff windows:" -ForegroundColor Cyan
    $procs | ForEach-Object {
        Write-Host "  $($_.Id) - $($_.MainWindowTitle)"
    }
}
