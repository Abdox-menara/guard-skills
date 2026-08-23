---
name: freebuff-bridge
description: |
  ULTRA-ADVANCED Freebuff Bridge — Communicate with Freebuff Desktop AI assistant.
  Switch windows, send messages, read responses, and automate conversations
  between OpenCode and Freebuff Desktop via Ghost MCP.

  CAPABILITIES:
  - Reliable window switching (finds Freebuff by process name)
  - Send messages to Freebuff chat input
  - Read Freebuff responses via screenshot/OCR
  - Auto-scroll to find latest messages
  - Queue messages for batch sending
  - Demo Ghost capabilities to Freebuff
  - Collaborative coding between OpenCode ↔ Freebuff

  TRIGGER PHRASES: "freebuff", "chat with freebuff", "talk to freebuff",
  "message freebuff", "freebuff bridge", "communicate with freebuff"

  ENVIRONMENT: Windows 11, Ghost MCP, Freebuff Desktop app installed.
---

# Freebuff Bridge — ULTRA-ADVANCED v1.0

## Overview

Enables reliable communication between OpenCode and Freebuff Desktop. Solves the window-switching problem by using process detection and precise coordinate mapping.

## Quick Start

```powershell
# Find Freebuff window
.\Find-Freebuff.ps1

# Send a message
.\Send-Freebuff.ps1 -Message "Hello from OpenCode!"

# Read latest response
.\Read-Freebuff.ps1
```

## Ghost MCP Commands

### 1. Switch to Freebuff (Reliable Method)
```powershell
# Find Freebuff PID and bring to focus
$proc = Get-Process -Name "Freebuff" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($proc) {
    $hwnd = $proc.MainWindowHandle
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
    [Win32]::ShowWindow($hwnd, 9) # SW_RESTORE
    [Win32]::SetForegroundWindow($hwnd)
    Write-Host "Freebuff brought to focus (PID: $($proc.Id))"
}
```

### 2. Send Message to Freebuff
```
Step 1: Switch to Freebuff window
Step 2: Click on chat input (coordinate: [770, 910] or use label)
Step 3: ghost_Type with message text
Step 4: ghost_Shortcut "enter" to send
```

### 3. Read Freebuff Response
```
Step 1: Switch to Freebuff window
Step 2: ghost_Wait 10 seconds for response
Step 3: ghost_Screenshot to capture
Step 4: Use OCR or vision to read response text
```

## Window Coordinates (1920x1080)

| Element | Coordinates | Notes |
|---------|-------------|-------|
| Freebuff chat input | [770, 910] | Bottom of Freebuff window |
| Freebuff send button | [1071, 910] | Arrow button next to input |
| Freebuff scroll area | [770, 400] | Center of chat area |
| Freebuff thread tabs | [200, 85] | Top-left thread list |
| Taskbar Freebuff icon | Varies | Use process detection instead |

## Communication Protocol

### OpenCode → Freebuff (Send Message)
```
1. ghost_Process mode=list name=Freebuff → get PID
2. ghost_App mode=switch name="Freebuff Desktop"
3. ghost_Wait duration=1
4. ghost_Click loc=[770, 910] → focus chat input
5. ghost_Type text="YOUR MESSAGE" press_enter=true
6. ghost_Wait duration=10 → wait for response
7. ghost_Screenshot → capture response
```

### Freebuff → OpenCode (Read Response)
```
1. ghost_Screenshot → capture Freebuff window
2. OCR the response text from screenshot
3. Parse the response for relevant information
```

## Common Messages

### Self-Introduction
```
Hi Freebuff! I'm OpenCode — an AI coding agent by anomalyco, powered by MiMo V2.5 Free.
I run on Abdox's Dell PC (Windows 11, i7-6920HQ, 32GB RAM).
My abilities: write/edit code, run bash/powershell, search codebases,
browse the web, control Windows desktop via Ghost MCP, read/write files.
Want to collaborate?
```

### Teach Ghost Capabilities
```
Hey Freebuff! Let me teach you about Ghost — it's a Windows desktop MCP server
that lets AI agents control the PC:

1. ghost_Snapshot — Captures screen, reads all UI elements with coordinates
2. ghost_Click — Clicks any element by coordinates or label
3. ghost_Type — Types text into input fields
4. ghost_App — Opens/switches/resizes application windows
5. ghost_Screenshot — Takes visual screenshots
6. ghost_Wait — Pauses execution for N seconds
7. ghost_WaitFor — Waits until UI condition is met
8. ghost_Move — Moves mouse cursor
9. ghost_Scroll — Scrolls at coordinates
10. ghost_Clipboard — Copy/paste operations
11. ghost_FileSystem — Read/write/copy/move/delete files
12. ghost_PowerShell — Runs PowerShell commands
13. ghost_Shortcut — Executes keyboard shortcuts
14. ghost_Registry — Read/write Windows Registry
15. ghost_Process — List/kill processes
```

### Ask for Collaboration
```
I can help with your DynamicLock project! I have:
- scrcpy v4.1 installed for phone mirroring
- Huawei MNA-LX9 connected via USB
- Full Ghost MCP for desktop automation
- PowerShell, Python, bash available

Want me to push the APK to the phone or start coding v7.0?
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Freebuff not found | Check if app is running: `Get-Process Freebuff` |
| Window won't focus | Use PID-based focusing (see Reliable Method above) |
| Chat input not responding | Click directly on input field coordinates |
| Response not visible | Scroll down in Freebuff chat area |
| Message not sent | Verify Enter key was pressed after typing |

## Integration with Other Skills

- **scrcpy-install**: Push APKs to phone via Freebuff collaboration
- **ghost-snapshot**: Capture and analyze Freebuff screenshots
- **pc-control**: Full desktop automation for Freebuff interactions

---

**Version**: 1.0.0
**Status**: PRODUCTION READY
**Total Capabilities**: 5
