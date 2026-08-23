import os

content = """# OpenCode Notes - Persistent Memory

> **AI: Read this file at start of EVERY session. Update it after learning something new.**

---

## Table of Contents
1. [User Profile](#user-profile)
2. [Environment](#environment)
3. [Solutions Library](#solutions-library)
4. [Installed Tools](#installed-tools)
5. [Projects History](#projects-history)
6. [Common Commands](#common-commands)
7. [Gotchas and Tips](#gotchas-and-tips)
8. [Learning Log](#learning-log)

---

## User Profile
| Field | Value |
|-------|-------|
| Name | Abdox |
| OS | Windows 11 Pro |
| Workspace | C:\\opencodes\\guard skills |
| Primary Language | Python |
| Values | persistence, conciseness, automation, efficiency |
| Communication | Prefers short, direct answers |

---

## Environment
| Tool | Version/Path |
|------|--------------|
| Python | 3.11.15 |
| Python venv | C:\\Users\\Abdox\\AppData\\Local\\hermes\\hermes-agent\\venv |
| Platform | win32 |
| Shell | PowerShell 7+ |

---

## Solutions Library

### Extract Icon from EXE/DLL

```python
from icoextract import IconExtractor

exe_path = r'path\\to\\app.exe'
output = r'path\\to\\icon.ico'

e = IconExtractor(exe_path)
e.export_icon(output, 0)
```

- Install: pip install icoextract
- Note: Icon is in target exe, not in .lnk shortcut

### Read Windows Shortcuts (.lnk)

```python
from pylnk3 import Lnk

lnk = Lnk(r'path\\to\\shortcut.lnk')
print(lnk.path)        # target exe path
print(lnk.icon)        # icon path
print(lnk.work_dir)    # working directory
```

- Install: pip install pylnk3
- Note: Different Python installs need separate pip

---

## Installed Libraries
| Library | Purpose | Install |
|---------|---------|---------|
| icoextract | Extract icons from PE files | pip install icoextract |
| pylnk3 | Read Windows .lnk shortcuts | pip install pylnk3 |
| Pillow | Image processing | pip install Pillow |
| pefile | PE file parsing | pip install pefile |
| pywin32 | Windows API access | pip install pywin32 |

---

## Projects History

### 1. Drive Composer Icon Extraction
- **Date:** 2026-06-30
- **Goal:** Extract .ico from desktop shortcut
- **Source:** C:\\Users\\Public\\Desktop\\Drive Composer pro 2.9.0.1.lnk
- **Target:** C:\\Program Files (x86)\\DriveWare\\Drive Composer pro\\2.9\\Drive Composer pro.exe
- **Output:** C:\\opencodes\\guard skills\\drive_composer.ico (285 KB)
- **Solution:** Used icoextract library
- **Status:** COMPLETED

---

## Common Commands

### Python (in venv)
```
python --version
python -m pip install <package>
python -m pip list
```

### File Operations
```
dir
Test-Path "path\\to\\file"
(Get-Item "path").Length
```

---

## Gotchas and Tips
1. **$ signs stripped** - The write tool strips $ signs. Use python or cmd echo instead.
2. **Multiple Pythons** - User has Python 3.11 (venv) and 3.14 (system). Use correct pip.
3. **LNK vs EXE** - Shortcut (.lnk) files do not contain icons directly; they point to exe.
4. **Path escaping** - In Python strings, use double backslashes or raw strings (r"...").

---

## Learning Log

| Date | What I Learned |
|------|----------------|
| 2026-06-30 | pylnk3 reads .lnk files, icoextract pulls icons from exes |
| 2026-06-30 | User values persistent memory - created this notes file |
| 2026-06-30 | $ signs get stripped in write tool - use python instead |
"""

output_path = r'C:\opencodes\guard skills\opencode_notes.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Notes file created: {output_path}')
print(f'Size: {os.path.getsize(output_path)} bytes')
