# Guard Skills Weekly Maintenance
# Runs: index rebuild, git commit+push, offsite bundle backup.
# FIX 2026-09-20: exit 64 (ERROR_NETNAME_DELETED) when H: was unmounted at fire time.
#   Root cause: every Log() call wrote to H:\Backups\maintain-log.txt via Tee-Object,
#   so a missing H: killed the whole run before it could record anything.
#   Now: local-first logging (always succeeds) + H: mirror when reachable + guarded bundle.
#
# Log: C:\opencodes\guard skills\maintain-fallback.log  (always   — gitignored)
#      H:\Backups\maintain-log.txt                       (offsite  — when H: is mounted)

$ErrorActionPreference = "Continue"
$repo = "C:\opencodes\guard skills"
$hLog = "H:\Backups\maintain-log.txt"
$localLog = "$repo\maintain-fallback.log"

function Log($m) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m"
    # Local-first: this always works, guarantees an audit trail even if H: is gone.
    try { Add-Content -LiteralPath $localLog -Value $line -Encoding UTF8 } catch {}
    # Offsite mirror: best-effort, never breaks the run.
    try { Add-Content -LiteralPath $hLog -Value $line -Encoding UTF8 } catch {}
}

Set-Location $repo

$H_up = Test-Path -LiteralPath "H:\Backups"
Log "--- maintenance start (H: $(if ($H_up) {'mounted -> offsite log'} else {'ABSENT -> local log only'})) ---"

# 1) Rebuild skill index (detects drift)
python tools\build_index.py 2>&1 | Out-Null
Log "index rebuilt"

# 1b) Validate library (frontmatter + links) and scan for secrets
$validation = python tools\validate_skills.py 2>&1
Log ($validation | Select-Object -First 1)
if ($LASTEXITCODE -ne 0) { Log "VALIDATION FAILED:"; Log ($validation | Out-String) }
$secrets = python tools\secret_scan.py 2>&1 | Select-Object -Last 1
Log "secret scan: $secrets"

# 2) Commit + push if anything changed
git add -A 2>$null
$dirty = git status --short
if ($dirty) {
    git commit -m "Auto-maintenance: index + library sync" 2>&1 | Out-Null
    git push 2>&1 | Out-Null
    Log "committed + pushed ($(@($dirty).Count) changes)"
} else {
    Log "no changes"
}

# 3) Offsite bundle (keep last 4) — guarded: skipped gracefully when H: is absent
if ($H_up) {
    New-Item -ItemType Directory "H:\Backups" -Force | Out-Null
    $stamp = Get-Date -Format "yyyy-MM-dd"
    git bundle create "H:\Backups\guard-skills-$stamp.bundle" --all 2>$null
    Get-ChildItem "H:\Backups\guard-skills-*.bundle" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -Skip 4 |
        Remove-Item -Force -ErrorAction SilentlyContinue
    Log "bundle created: guard-skills-$stamp.bundle"
} else {
    Log "SKIP offsite bundle: H:\Backups not reachable"
}

# 4) Final sweep — build_index.py rewrites skills_index.json with a fresh UTC
#    timestamp per run, and that write can flush after step 2's git add. Retry
#    add+commit until the working tree is actually clean (bounded, so a runaway
#    writer can never hang the task).
for ($attempt = 1; $attempt -le 3; $attempt++) {
    git add -A 2>$null
    if (-not (git status --short)) { break }
    git commit -m "Auto-maintenance: index timestamp tail" 2>&1 | Out-Null
    git push 2>&1 | Out-Null
    if ($attempt -lt 3) { Start-Sleep -Seconds 2 }
}
$leftover = git status --short
if ($leftover) {
    Log "WARN: tree still dirty after 3 sweeps: $($leftover -join '; ')"
} else {
    Log "working tree clean after final sweep"
}
Log "--- done ---"
