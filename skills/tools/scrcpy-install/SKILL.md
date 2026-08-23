---
name: scrcpy-install
description: |
  ULTRA-ADVANCED Scrcpy Install & Usage — Android screen mirroring via ADB.
  Installs scrcpy v4.1 to PATH, creates shortcuts, and provides PowerShell wrappers
  for wireless/ USB connection, recording, and automation.

  CAPABILITIES:
  - Install scrcpy to a permanent location & add to PATH
  - Desktop & Start Menu shortcut creation
  - USB connection helper (one-command mirror)
  - Wireless ADB pairing & connection
  - Screen recording with scrcpy
  - File transfer via ADB push/pull
  - PowerShell wrapper with common commands
  - Scriptable automation for testing

  TRIGGER PHRASES: "scrcpy install", "android mirror", "screen mirror android",
  "scrcpy setup", "install scrcpy", "adb wireless"

  ENVIRONMENT: Windows 11, requires ADB-enabled Android device or emulator.
---
# Scrcpy Install — ULTRA-ADVANCED v1.0

## Overview

Scrcpy (v4.1) displays and controls Android devices connected via USB or wirelessly. No root required. This skill installs it permanently and wraps it with convenience commands.

## Installation

Run once to install permanently:

```powershell
# Install: copy to Program Files, add PATH, create shortcuts
.\Install-Scrcpy.ps1
```

**What it does:**
1. Copies scrcpy to `C:\Program Files\scrcpy`
2. Adds to `PATH` (user-level)
3. Creates Desktop shortcut `🔗 Scrcpy Mirror`
4. Creates Start Menu folder `Scrcpy`
5. Verifies ADB connectivity

## Quick Start

### USB Connection
```powershell
# Enable USB debugging on Android, then:
scrcpy
```

### Wireless Connection
```powershell
# 1. Connect via ADB over TCP/IP
Invoke-Scrcpy.ps1 -ConnectWireless 192.168.1.100

# 2. Mirror the device
scrcpy
```

## Wrapper Commands

| Command | Description |
|---------|-------------|
| `Invoke-Scrcpy.ps1 -Mirror` | Standard USB mirror |
| `Invoke-Scrcpy.ps1 -Mirror -NoBorder` | Borderless window |
| `Invoke-Scrcpy.ps1 -Record "out.mp4"` | Record screen to file |
| `Invoke-Scrcpy.ps1 -ConnectWireless "IP"` | Pair & connect via WiFi |
| `Invoke-Scrcpy.ps1 -Push "file" "/sdcard/"` | Push file to device |
| `Invoke-Scrcpy.ps1 -Pull "/sdcard/file" "."` | Pull file from device |
| `Invoke-Scrcpy.ps1 -ListDevices` | List connected devices |
| `Invoke-Scrcpy.ps1 -ScreenShot "shot.png"` | Take screenshot via ADB |

## Scrcpy Options Reference

| Flag | Effect |
|------|--------|
| `--max-size 1024` | Limit resolution |
| `--max-fps 30` | Limit frame rate |
| `--bit-rate 4M` | Limit bandwidth |
| `--no-border` | Borderless window |
| `--fullscreen` | Start fullscreen |
| `--turn-screen-off` | Turn off device screen while mirroring |
| `--record file.mp4` | Record to file |
| `--no-window` | Record without displaying |
| `--display 1` | Select secondary display |
| `--crop 720:1280:0:0` | Crop the screen |
| `--lock-video-orientation 0` | Lock orientation |
| `--tcpip 192.168.1.100` | Connect wirelessly |

## Common Scenarios

### Scenario 1: First-Time USB Mirror
```powershell
# Install scrcpy
.\Install-Scrcpy.ps1

# Connect phone via USB, accept USB debugging prompt
# Then:
scrcpy --max-size 1080 --max-fps 30
```

### Scenario 2: Wireless Mirror (No USB)
```powershell
# Once phone is on same WiFi:
Invoke-Scrcpy.ps1 -ConnectWireless 192.168.1.100
# Then disconnect cable — scrcpy stays connected
```

### Scenario 3: Record Demo Video
```powershell
Invoke-Scrcpy.ps1 -Record "C:\videos\demo.mp4" -MaxSize 1080
# Press Ctrl+C to stop recording
```

### Scenario 4: App Testing Automation
```powershell
# Mirror + install APK + screenshot
Invoke-Scrcpy.ps1 -Push "app.apk" "/sdcard/Download/"
adb shell pm install -r "/sdcard/Download/app.apk"
adb shell monkey -p com.example.app 1
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `adb: no devices/emulators found` | Enable USB debugging on phone, re-plug cable |
| `ERROR: Device not found` | Try `adb kill-server` then `adb start-server` |
| `ERROR: Could not find any ADB device` | Check USB cable supports data transfer |
| Wireless: `connection failed` | Ensure phone & PC on same network; disable VPN |
| Scrcpy not recognized | Run `.\Install-Scrcpy.ps1` again or restart terminal |
| Slow performance | Use `--max-size 800 --max-fps 15 --bit-rate 2M` |

## ADB Commands

```powershell
# List devices
adb devices -l

# Restart ADB server
adb kill-server && adb start-server

# Wireless setup (prep)
adb tcpip 5555

# Connect wirelessly
adb connect 192.168.1.100:5555

# Disconnect
adb disconnect

# Push file
adb push "file" "/sdcard/"

# Pull file
adb pull "/sdcard/file"

# Install APK
adb install "app.apk"

# Take screenshot
adb exec-out screencap -p > "shot.png"

# Record screen (Ctrl+C to stop)
adb shell screenrecord /sdcard/demo.mp4
```

## File Transfer

After mirroring starts, drag & drop files from Windows Explorer into the scrcpy window to transfer them to the device.

---

**Version**: 1.0.0
**Location**: `H:\tmp\scrcpy-win64-v4.1\scrcpy-win64-v4.1`
**Source**: https://github.com/Genymobile/scrcpy
