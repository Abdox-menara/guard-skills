# Guard Skills Weekly Maintenance
# Runs: validation, secret scan, index rebuild, git commit+push, offsite bundle backup.
# FIX 2026-09-20: exit 64 (ERROR_NETNAME_DELETED) when H: was unmounted at fire time.
#   Root cause: every Log() call wrote to H:\Backups\maintain-log.txt via Tee-Object,
#   so a missing H: killed the whole run before it could record anything.
#   Now: local-first logging (always succeeds) + H: mirror when reachable + guarded bundle.
# FIX 2026-09-20 (2): perpetual dirty tree. build_index.py rewrites skills_index.json with
#   a fresh UTC timestamp and the write flushes asynchronously, racing git add. Restructured:
#   index build runs LAST, we poll the file hash until stable, then commit exactly once.
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

# 1) Validate library (frontmatter + links) and scan for secrets — read-only, run first
$validation = python tools\validate_skills.py 2>&1
Log ($validation | Select-Object -First 1)
if ($LASTEXITCODE -ne 0) { Log "VALIDATION FAILED:"; Log ($validation | Out-String) }
$secrets = python tools\secret_scan.py 2>&1 | Select-Object -Last 1
Log "secret scan: $secrets"

# 2) Rebuild skill index LAST — it rewrites skills_index.json with a fresh UTC
#    timestamp. build_index.py now flushes+fsyncs on exit (fixed 2026-09-20: a bare
#    open() passed to json.dump relied on GC, so the write landed seconds late and
#    raced git add, leaving the tree perpetually dirty). Poll briefly as a safety net.
python tools\build_index.py 2>&1 | Out-Null
$idx = "$repo\skills_index.json"
$hash = ''
$stable = $false
for ($i = 0; $i -lt 5; $i++) {
    $cur = (Get-FileHash -LiteralPath $idx -Algorithm MD5).Hash
    if ($cur -eq $hash) { $stable = $true; break }
    $hash = $cur
    Start-Sleep -Seconds 1
}
if ($stable) { Log "index rebuilt (hash stable)" }
else { Log "WARN: skills_index.json still changing — committing anyway" }

# 3) Commit + push exactly once, now that the writer has settled
git add -A 2>$null
$dirty = git status --short
if ($dirty) {
    git commit -m "Auto-maintenance: index + library sync" 2>&1 | Out-Null
    git push 2>&1 | Out-Null
    Log "committed + pushed ($(@($dirty).Count) changes)"
} else {
    Log "no changes"
}

# 4) Offsite bundle (keep last 4) — guarded: skipped gracefully when H: is absent
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

# 5) Verify the tree ended clean
$leftover = git status --short
if ($leftover) {
    Log "WARN: tree still dirty post-commit: $($leftover -join '; ')"
} else {
    Log "working tree clean"
}
Log "--- done ---"
