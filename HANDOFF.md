# Handoff: Library Automation + Truth Sync — 2026-08-23

## Session Context
- **Session ID**: automation-truth-sync-2026-08-23
- **Timestamp**: 2026-08-23T02:00:00+01:00
- **Agent**: opencode (ox-alpha)
- **Project**: Guard Skills — `C:\opencodes\guard skills`

## Current Verified State

### Skills Library (TRUE counts, auto-generated)
- **225 skills total** = 72 guards + 83 tools + 67 workflow + 3 special
  - Special (top-level): `desktop-control-mcp`, `force-delete`, `self-learning`
- 224 SKILL.md files on disk; `skill-generator-tool` SKILL.md was missing → created this session
- `meta-skill-generator` was an EMPTY dir → removed from indexes (dir itself NTFS-locked on disk)
- All 225 validated: frontmatter ✓ descriptions ✓ relative links ✓ (run `python tools/validate_skills.py`)

### Git / GitHub
- Repo: **github.com/Abdox-menara/guard-skills** (public, secret-scanned clean)
- Git DB relocated: `.git` is a FILE pointing to `C:\Users\Abdox\.opencode_git_storage\guard-skills-clean.git`
- Old gitdir `guard-skills.git` purged except ~627 NTFS-locked objects (~0.8 MB) — clear after chkdsk
- Backups: weekly bundle to `H:\Backups\` (auto-pruned to last 4) + GitHub remote

### Automation (NEW this session)
| Component | Path | Purpose |
|-----------|------|---------|
| Index generator | `tools/build_index.py` | Regenerates AGENTS.md §4 index + `skills_index.json` from frontmatter |
| Validator | `tools/validate_skills.py` | Frontmatter/description/link checks (exit 1 on failure) |
| Secret scanner | `tools/secret_scan.py` | Scans tracked files for credential patterns |
| Maintenance | `scripts/maintain.ps1` | index → validate → secret-scan → commit+push → bundle |
| Scheduled task | **GuardSkills-Maintenance** | Weekly Sunday 20:00, runs maintain.ps1 |

## Pending (requires user action)
1. **REBOOT** → chkdsk C: /F /X runs (scheduled) — fixes the NTFS create-ok/delete-blocked corruption that caused today's git object failures
2. After reboot: delete leftover `C:\Users\Abdox\.opencode_git_storage\guard-skills.git` remnants + locked junk files (`skills/gen*.py`, `generate_skills.py`, `skills/workflow/meta-skill-generator/`)
3. Re-run `python tools/build_index.py && python tools/validate_skills.py` to confirm clean state post-chkdsk

## Key Learnings (this session)
- **l020**: NTFS-locked files → `icacls /grant:r user:F /T` then .NET File.Delete (Remove-Item fails in NonInteractive)
- **l021**: On corrupted volumes where delete/rename is blocked but create works: `git repack -a -d` → fresh separate-git-dir from pack+refs → rewrite `.git` pointer via `Set-Content -Force`
- gh CLI fails on `.git` file pointers — use manual `git remote add` + `git push`
