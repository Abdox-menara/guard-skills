---
name: windows-shortcut-repair
description: ULTRA-ADVANCED Windows Shortcut Repair — GUI + CLI with monitoring, export, backup, and scheduled tasks. Scans and fixes broken .lnk shortcuts with missing icons, broken targets, or incorrect paths across Desktop, Start Menu, Taskbar, and custom folders.

CAPABILITIES:
- GUI mode with real-time scanning and visual grid
- CLI mode for automation and scripting
- Detects broken icons (empty IconLocation)
- Detects broken targets (missing .exe files)
- Auto-fixes icon paths pointing to known executables
- Export reports (CSV, JSON, HTML)
- Import known-good shortcut configurations
- Backup before fix (rollback support)
- Monitoring mode (watch for new shortcuts)
- Scheduled task integration
- System tray notifications
- Batch repair across all locations
- Multi-folder scanning with pattern filtering

TRIGGER PHRASES: "fix shortcut icon", "repair shortcut", "broken shortcut", "missing icon", "shortcut repair", "fix .lnk", "desktop icon missing", "shortcut scanner", "shortcut monitor"

ENVIRONMENT: Windows 10/11, PowerShell 5.1+, no admin required for user shortcuts.
---

## Quick Start

### GUI Mode (Interactive)
```powershell
.\Repair-Shortcuts.ps1 -GUI
```

### CLI Mode (Automation)
```powershell
# Scan only
.\Repair-Shortcuts.ps1 -ScanOnly

# Fix all broken shortcuts
.\Repair-Shortcuts.ps1

# Fix with backup
.\Repair-Shortcuts.ps1 -Backup

# Export report
.\Repair-Shortcuts.ps1 -Export "report.html"
```

### Monitor Mode (Watch for Changes)
```powershell
# Watch every 5 minutes
.\Repair-Shortcuts.ps1 -Monitor -Interval 300

# Watch specific folder
.\Repair-Shortcuts.ps1 -Monitor -Path "C:\Users\Me\Desktop"
```

## Features

### GUI Mode
- Visual grid showing all shortcuts
- Color-coded status (red=broken, green=OK)
- One-click "Fix Selected" or "Fix All Broken"
- Export to CSV/JSON/HTML
- Folder selection dropdown

### Backup System
```powershell
# Create backups before fixing
.\Repair-Shortcuts.ps1 -Backup

# Backups stored in: ~/.shortcut-backups/
# Named: backup_YYYYMMDD_HHMMSS_shortcutname.lnk
```

### Export Formats
```powershell
# CSV (Excel compatible)
.\Repair-Shortcuts.ps1 -Export "report.csv"

# JSON (API/machine readable)
.\Repair-Shortcuts.ps1 -Export "report.json"

# HTML (visual report with styling)
.\Repair-Shortcuts.ps1 -Export "report.html"
```

### Monitoring Mode
```powershell
# Auto-fix new broken shortcuts
.\Repair-Shortcuts.ps1 -Monitor -Interval 60

# Output:
# NEW: MyApp.lnk in C:\Users\Me\Desktop
#   -> BROKEN ICON, auto-fixing...
#   -> FIXED
```

## Common Scenarios

### Scenario 1: Electron App Missing Icon
```powershell
# Problem: OpenCode shortcut shows generic icon
.\Repair-Shortcuts.ps1 -Pattern "opencode" -FixExePath "C:\path\to\OpenCode.exe"
```

### Scenario 2: Batch Fix All Shortcuts
```powershell
# Fix everything on Desktop + Start Menu
.\Repair-Shortcuts.ps1 -Path "$env:USERPROFILE\Desktop","$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
```

### Scenario 3: System Health Check
```powershell
# Daily check with HTML report
.\Repair-Shortcuts.ps1 -ScanOnly -Export "health-$(Get-Date -Format 'yyyyMMdd').html"
```

### Scenario 4: Post-Installation Fix
```powershell
# After installing new app, fix its shortcuts
.\Repair-Shortcuts.ps1 -Pattern "newapp" -Backup
```

## Shortcut Locations (Windows 11)

| Location | Path | Scope |
|----------|------|-------|
| Desktop | `%USERPROFILE%\Desktop\` | Current user |
| Start Menu (User) | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\` | Current user |
| Start Menu (All) | `%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\` | All users |
| Taskbar | `%APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\` | Current user |
| Startup | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\` | Current user |

## How Windows Shortcuts Work

| Property | Description |
|----------|-------------|
| `TargetPath` | The .exe or file to open |
| `IconLocation` | Format: `path,index` — if path is empty, shows generic icon |
| `WorkingDirectory` | Starting folder for the app |
| `Arguments` | Command-line arguments |
| `Description` | Tooltip text |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Icon still missing after fix | Right-click desktop → Refresh, or restart explorer.exe |
| Shortcut target not found | Reinstall the app or update TargetPath |
| Taskbar icon not updating | Unpin and re-pin the shortcut |
| Start Menu shortcut broken | Check both User and ProgramData Start Menu folders |
| GUI not loading | Ensure .NET Framework 4.5+ is installed |
| Monitoring too frequent | Increase -Interval value (seconds) |

## Automation Examples

### Scheduled Task (Daily Scan)
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-File C:\scripts\Repair-Shortcuts.ps1 -ScanOnly -Export C:\reports\shortcuts.html"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -TaskName "ShortcutRepair" -Action $action -Trigger $trigger
```

### Post-Installer Hook
```powershell
# Run after any installer
.\Repair-Shortcuts.ps1 -Pattern "newapp" -Backup -Quiet
```

## References

- [Microsoft: IShellLink interface](https://learn.microsoft.com/en-us/windows/win32/shell/ishelllink)
- [PowerShell: WScript.Shell COM](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/automat/-automat-scripting-scsshell)
- [Windows Shortcut Properties](https://learn.microsoft.com/en-us/windows/win32/shell/shortcuts)
