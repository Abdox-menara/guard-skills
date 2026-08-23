# Guard Skills Weekly Maintenance
# Runs: index rebuild, git commit+push, offsite bundle backup.
# Log: H:\Backups\maintain-log.txt

$ErrorActionPreference = "Continue"
$repo = "C:\opencodes\guard skills"
$log = "H:\Backups\maintain-log.txt"

function Log($m) {
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m" | Tee-Object -FilePath $log -Append
}

Set-Location $repo

# 1) Rebuild skill index (detects drift)
python tools\build_index.py 2>&1 | Out-Null
Log "index rebuilt"

# 2) Commit + push if anything changed
git add -A 2>$null
$dirty = git status --short
if ($dirty) {
    git commit -m "Auto-maintenance: index + library sync" 2>&1 | Out-Null
    $pushed = git push 2>&1
    Log "committed + pushed ($(@($dirty).Count) changes)"
} else {
    Log "no changes"
}

# 3) Offsite bundle (keep last 4)
New-Item -ItemType Directory "H:\Backups" -Force | Out-Null
$stamp = Get-Date -Format "yyyy-MM-dd"
git bundle create "H:\Backups\guard-skills-$stamp.bundle" --all 2>$null
Get-ChildItem "H:\Backups\guard-skills-*.bundle" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -Skip 4 |
    Remove-Item -Force -ErrorAction SilentlyContinue
Log "bundle created: guard-skills-$stamp.bundle"
Log "--- done ---"
