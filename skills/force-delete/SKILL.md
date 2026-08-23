---
name: force-delete
description: Automates the removal of protected directories that throw **"Access is denied"** by: - Taking ownership (`takeown /A`) - Granting Administrators full control (`icacls /grant`) - Clearing restrictive attributes (`attrib`) - Deleting recursively (`Remove-Item -Recurse -Force`)
---

# Force‑Delete & Disk‑Cleanup Skill

## Description
Automates the removal of protected directories that throw **"Access is denied"** by:
- Taking ownership (`takeown /A`)
- Granting Administrators full control (`icacls /grant`)
- Clearing restrictive attributes (`attrib`)
- Deleting recursively (`Remove-Item -Recurse -Force`)

Also provides **drive‑space analysis** and **scheduled‑task automation** for recurring cleanups.

**Learned from a real Windows 11 session** where folders were owned by TrustedInstaller and blocked by `ModifiableWindowsApps` ACLs.

---

## Workflow Map (AI / Human can follow this exactly)

```
1. ANALYSE (optional)
   ├─ Get-PSDrive -Name <drive>             → used / free / total
   ├─ Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue
   │    Sort-Object Length -Descending       → top 20 largest files
   └─ Get-ChildItem -Directory -Recurse     → folder‑size summary

2. DELETE PROTECTED FOLDER
   ├─ Test-Path -LiteralPath <path>         → exists?
   ├─ if NOT Admin:
   │    Start-Process -Verb RunAs           → UAC prompt → user clicks Yes
   ├─ takeown /F <path> /A /R /D Y          → ownership → Administrators group
   ├─ icacls <path> /grant:r Administrators:(F) /T /C
   │                                         → full control recursively
   ├─ attrib -R -S -H <path> /S /D          → clear readonly, system, hidden
   └─ Remove-Item -LiteralPath <path> -Recurse -Force

3. VERIFY
   └─ Test-Path -LiteralPath <path>         → must return $false

4. AUTOMATE (optional)
   ├─ Register-ScheduledTask -UserId SYSTEM -RunLevel Highest
   ├─ Triggers: AtLogOn / Once / Daily
   └─ Run immediately: Start-ScheduledTask -TaskName <name>
```

---

## Scripts

| Script | Purpose | Parameters |
|--------|---------|------------|
| `ForceDelete.ps1` | Elevates, takes ownership, grants full control, deletes. | `-Paths` (mandatory, array) |
| `CreateForceDeleteTask.ps1` | Registers a scheduled‑task as SYSTEM that runs `ForceDelete.ps1`. | `-TaskName`, `-TriggerType` (AtLogOn/Once/Daily) |
| `StorageAnalyze.ps1` | Reports used/free space, top 20 largest files, folder sizes. | `-Drive` (string, e.g. "H") |
| `FindAndDelete.ps1` | Searches a whole drive for folders by name pattern, then deletes them. | `-Pattern` (wildcard), `-Drive` |

All scripts:
- Detect if running as Administrator; if not, they **self‑elevate** via UAC.
- Use `-ErrorAction Stop` and try/catch for robust error handling.
- Print colored success/failure messages.
- Can be called from any PowerShell window.

---

## Quick‑start

```powershell
# 1. Analyse drive H:
.\StorageAnalyze.ps1 -Drive H

# 2. Force‑delete protected folders
.\ForceDelete.ps1 -Paths "D:\FolderA","D:\FolderB"

# 3. Schedule the deletion to run on every log‑on
.\CreateForceDeleteTask.ps1

# 4. Run the task immediately
Start-ScheduledTask -TaskName "ForceDeleteProtectedFolders"
```

---

## Prompt triggers (for any AI / agent)

| Category | Phrases |
|----------|---------|
| Analyse | `"analyse drive X"`, `"free space on H:"`, `"disk usage"`, `"largest files"` |
| Force delete | `"delete protected folder"`, `"access denied"`, `"force delete path"`, `"can't remove directory"` |
| Automate | `"schedule deletion"`, `"run at boot"`, `"cleanup task"`, `"register scheduled task"` |
| Combined | `"clean storage"`, `"free up space"`, `"remove locked files"`, `"storage guard"` |

An AI agent should follow the **Workflow Map** above. If a step fails, consult the **Common errors** table.

---

## Common errors and fixes

| Error | Root cause | Fix |
|-------|------------|-----|
| `Access is denied` | Not elevated / protected ACL | `takeown /A /R /D Y` then `icacls /grant administrators:F /T /C` |
| `File or Directory not found` | Path removed or hidden | Use `Get-ChildItem -Force -ErrorAction SilentlyContinue` to rediscover |
| `Group used for deny only` | User in Administrators but **not elevated** | Run PowerShell **as Administrator** or accept UAC prompt |
| `Invalid parameter "\Administrators:(F)"` | Quoting error in `icacls` | Use double quotes: `icacls path /grant "Administrators:(F)" /T /C` |
| `ModifiableWindowsApps: Access is denied` | Windows‑protected subfolder | Run `takeown /F path /A /R /D Y` **before** `icacls` |
| `The current logged on user does not have administrative privileges` | `takeown` refuses because token is not elevated | Relaunch script with `-Verb RunAs` |
| `Remove-Item: Access to the path is denied` | Still not enough rights | Reset ACL first with `icacls /reset /T /C`, then `icacls /grant …` |
| `Attempted to perform an unauthorized operation` on `Get-Acl` | No read‑permission | Take ownership first, then retry |

---

## What this skill learned from the real session

1. **`Remove-Item -Force -Recurse` alone never works** on system‑protected directories.  
2. The correct order is **takeown → icacls → attrib → remove-item**; swapping or skipping any step fails.  
3. **`takeown /A`** gives ownership to the Administrators group, not the current user. This is crucial because the current session may have deny‑only group membership.  
4. **`icacls /grant:r "Administrators:(F)"`** must be quoted around the parenthesis or the colon is misparsed.  
5. Folders containing **`ModifiableWindowsApps`** (Windows Store) require ownership first, or even `icacls /grant` will return `Access is denied`.  
6. The **`whoami /groups`** output showing `Group used for deny only` for `BUILTIN\Administrators` means the process token is **not elevated** and will block all admin operations.  
7. **Self‑elevating** via `Start-Process -Verb RunAs` works, but requires the user to click the UAC prompt – the AI cannot auto‑confirm it.  
8. Creating a **scheduled task as `SYSTEM`** (`-UserId SYSTEM -LogonType ServiceAccount -RunLevel Highest`) runs the deletion without any further UAC prompts on subsequent log‑ons.  
9. The **parentheses** inside `icacls` permission strings must be escaped with double quotes around the whole argument: `"/grant:r Administrators:(F)"`.  
10. Multi‑step `foreach` loop works but potential file‑not‑found errors after `removal` need to be caught with `-ErrorAction SilentlyContinue` and re‑check with `Test-Path`.

---

## Tested on

| Environment | Details |
|-------------|---------|
| **OS** | Windows 11 Pro, build 22621 |
| **Drive** | D: (NTFS) |
| **Folders** | Contained `ModifiableWindowsApps`, recursive `.dll` files, `.png`, `.json`, `.xml` – all owned by TrustedInstaller |
| **User** | Member of Administrators group but **not elevated** (`Mandatory Label\Medium Mandatory Level`) |
| **Powershell** | 7+ (pwsh.exe) |

All steps in this skill were executed against actual **"Access is denied"** errors and verified as successful.

---

## Integration with opencode

To make this skill automatically available to opencode agents, add the following to your `opencode.json` (inside the `skills` array):

```json
{
  "name": "force-delete",
  "description": "Capacity to analyse drives, force‑delete protected folders, and schedule cleanup tasks.",
  "location": "C:\\opencodes\\guard skills\\skills\\force-delete\\SKILL.md"
}
```

Then any opencode agent can be instructed to "use the force-delete skill" to handle these tasks.

---

## Future improvements (ideas)

- [ ] Add `-Analyze` switch to `ForceDelete.ps1` to run storage analysis before deletion.  
- [ ] Add `-LogPath` parameter to write a timestamped log of all actions.  
- [ ] Add `-WhatIf` / `-Confirm` for dry‑runs and user confirmation.  
- [ ] Add a `Recover-Storage` cmdlet that automatically removes junk from common locations (Temp, Recycle Bin, etc.).  
- [ ] Support remote machines via `Invoke-Command`.  
- [ ] Embed the skill as a PowerShell module (`GuardSkills.psm1`).  
