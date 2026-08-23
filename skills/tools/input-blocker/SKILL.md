---
name: input-blocker
description: Block keyboard and mouse input on Windows until manually unblocked.
---

# Input Blocker v3.0

Block keyboard and mouse input on Windows until manually unblocked.

## Quick Start

```
Double-click control_panel.bat  -> Open GUI to change settings
Double-click block_input.bat    -> Run blocker with current settings
```

## Files

| File | Description |
|------|-------------|
| `control_panel.bat` | **Open GUI Control Panel** |
| `control_panel.py` | GUI settings manager |
| `block_input.bat` | Run blocker |
| `block_input.py` | Main script (20 features) |
| `block_input.ps1` | PowerShell fallback |
| `block_config.json` | User settings |
| `install.bat` | Install dependencies |
| `uninstall.bat` | Remove everything |
| `SKILL.md` | This file |
| `README.md` | Quick reference |

## Control Panel Tabs

### General
- Countdown seconds
- Unlock hotkey
- Language (EN/FR/AR)
- Block mode (All/Mouse/Keyboard)

### Features
- Sound alerts
- Voice alerts
- Overlay timer
- Auto-block on idle
- Scheduled block
- Auto-unblock timer
- Repeat daily
- Block on startup

### Security
- Require password to unblock
- Set password

### Presets
- Quick (3s)
- AFK (10s)
- Sleep (30s)
- Long (60s)

## All 20 Features

| # | Feature | CLI |
|---|---------|-----|
| 1 | Hotkey unblock | `--hotkey ctrl+shift+b` |
| 2 | Sound alert | `--no-sound` to disable |
| 3 | Overlay countdown | `--no-overlay` to disable |
| 4 | Password unblock | `--password xxx` |
| 5 | Presets | `--preset afk` |
| 6 | Mouse-only block | `--mouse-only` |
| 7 | Keyboard-only block | `--keyboard-only` |
| 8 | System tray icon | Auto |
| 9 | Block log | Auto |
| 10 | Multiple durations | `--preset xxx` |
| 11 | Auto-block on idle | `--idle 5` |
| 12 | Scheduled block | `--schedule 22:00` |
| 13 | Block timer | `--timer 30` |
| 14 | Repeat daily | `--repeat 22:00` |
| 15 | Block on startup | `--startup` |
| 16 | Block history | `--history` |
| 17 | Stats dashboard | `--stats` |
| 18 | Export/import config | `--export`/`--import` |
| 19 | Multi-language | `--lang fr` |
| 20 | Voice alert | `--voice` |

## Command Line

```bash
# Default
python block_input.py

# With preset
python block_input.py --preset afk

# Idle detection
python block_input.py --idle 5

# Scheduled
python block_input.py --schedule 22:00

# Auto-unblock after 30min
python block_input.py --timer 30

# Voice + French
python block_input.py --voice --lang fr

# View stats/history
python block_input.py --stats
python block_input.py --history

# Export/import config
python block_input.py --export my_config.json
python block_input.py --import my_config.json
```

## How to Unblock

| Method | Action |
|--------|--------|
| `Ctrl+Shift+B` | Custom hotkey |
| `Ctrl+Alt+Del` | Windows emergency |
| Tray icon | Right-click → Unblock |
| Timer | Auto-unblock |
| `Ctrl+C` | Cancel in terminal |

## Config Location

```
%APPDATA%\InputBlocker\config.json
```

## Requirements

- Windows 10/11
- Python 3.10+
- Admin privileges (auto-elevates)
- Run `install.bat` to install dependencies
