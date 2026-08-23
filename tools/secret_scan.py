import os, re, subprocess

tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.splitlines()
pats = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),  # openai-style
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),  # github PAT
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[A-Z0-9]{16}"),  # aws
    re.compile(r"(?i)(api[_-]?key|apikey|secret|passwd|password)\s*[:=]\s*['\"][A-Za-z0-9_\-\.]{16,}['\"]"),
]
hits = []
for f in tracked:
    p = f.replace("/", os.sep)
    if not os.path.isfile(p) or os.path.getsize(p) > 2_000_000:
        continue
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    for pat in pats:
        m = pat.search(t)
        if m:
            hits.append((f, m.group(0)[:40]))
print(f"scanned {len(tracked)} tracked files")
if hits:
    print("POTENTIAL SECRETS:")
    for h in hits[:15]:
        print("  ", h)
else:
    print("no secrets found - public repo is safe")
