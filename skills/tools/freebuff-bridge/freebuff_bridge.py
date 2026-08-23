"""
Freebuff Bridge - Communicate with Freebuff Desktop via Ghost MCP
Usage:
    python freebuff_bridge.py send "Your message here"
    python freebuff_bridge.py switch
    python freebuff_bridge.py status
"""

import subprocess
import sys
import time
import json

POWERSHELL = r"C:\Program Files\PowerShell\7\pwsh.exe"


def run_powershell(command):
    """Run a PowerShell command and return output."""
    result = subprocess.run([POWERSHELL, "-NoProfile", "-Command", command], capture_output=True, text=True, timeout=30)
    return result.stdout.strip(), result.stderr.strip()


def find_freebuff():
    """Find Freebuff process and return PID."""
    cmd = """
    $proc = Get-Process -Name "Freebuff" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($proc) {
        @{ PID = $proc.Id; Title = $proc.MainWindowTitle; Handle = $proc.MainWindowHandle }
    } else {
        $null
    }
    """
    out, err = run_powershell(cmd)
    if out and "PID" in out:
        return True, out
    return False, "Freebuff not running"


def switch_to_freebuff():
    """Bring Freebuff window to focus."""
    cmd = """
    Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class Win32 {
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    }
"@
    $proc = Get-Process -Name "Freebuff" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
    if ($proc) {
        [Win32]::ShowWindow($proc.MainWindowHandle, 9) | Out-Null
        [Win32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
        "OK:Switched to Freebuff (PID: $($proc.Id))"
    } else {
        "ERROR:No Freebuff window found"
    }
    """
    out, err = run_powershell(cmd)
    return out


def send_message(message):
    """Send a message to Freebuff chat input."""
    switch_result = switch_to_freebuff()
    if "ERROR" in switch_result:
        return switch_result

    time.sleep(1)

    escaped_msg = message.replace('"', '`"').replace("'", "''")
    cmd = f'''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{escaped_msg}")
    Start-Sleep -Milliseconds 500
    [System.Windows.Forms.SendKeys]::SendWait("{{ENTER}}")
    "OK:Message sent"
    '''
    out, err = run_powershell(cmd)
    return out if out else f"ERROR:{err}"


def get_status():
    """Get Freebuff status."""
    running, info = find_freebuff()
    if running:
        return f"Running: {info}"
    return "Not running"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "switch":
        print(switch_to_freebuff())
    elif action == "send":
        if len(sys.argv) < 3:
            print("Usage: freebuff_bridge.py send 'message'")
            sys.exit(1)
        message = " ".join(sys.argv[2:])
        print(send_message(message))
    elif action == "status":
        print(get_status())
    else:
        print(f"Unknown action: {action}")
        print(__doc__)


if __name__ == "__main__":
    main()
