# Recommended Tasks 101–200 (v2) — Generated 2026-08-24

> Successor to TASKS_100.md (35/100 done there). This list = 65 carried-over + 35 new from session discoveries.
> Legend: [P1] urgent · [P2] valuable · [P3] nice-to-have · [A] automatable · [U] needs user

## G1. Immediate / Blocked-on-user (8)
1. [P1][U] Run chkdsk C: /f /r (admin, reboot, ~45 min) — fixes NTFS delete/rename faults
2. [P1][A] Concat TIA Portal V18 DVD2 .P1+.P2 → verify ISO mounts
3. [P2][A] Concat StartDrive V18 SP2 .P1+.P2 → verify ISO
4. [P2][U] Verdict: delete 2×20GB OneDrive zips in H:\Recovered\API-SFO?
5. [P2][U] Test Input Blocker v69 Windows Hello unlock manually
6. [P2][A] TeraBox upload _recovered_stale_20260823 (~51 GB)
7. [P2][A] After upload OK: delete local copy → D: +51 GB
8. [P3][A] Check first CI run on github.com/Abdox-menara/guard-skills/actions

## G2. Storage & Recovery (14)
9. [P2][A] #53-carry: diff semi-uniques (106.8 GB) vs root Desktop_Sync → merge or archive plan
10. [P2][A] #57-carry: H: recovery plan (23.2 GB free — what can move to D: post-cleanup?)
11. [P3][A] Verify rebuilt V18 ISOs install-clean in mounted test OR archive to H:\Software
12. [P2][A] Organize H:\Recovered into final tree (API-SFO/installers/software) + README manifest
13. [P3][A] arduino folder (2.1 GB): active? archive if stale
14. [P3][A] Books/CV/Cursor/Pc Apps on D:: quick size+date audit
15. [P3][A] D:\freebuff audit (size unknown — classify)
16. [P3][A] D:\Module Retargetable Folder — legacy? purge candidate review
17. [P2][A] Set up monthly scheduled backup verification (test-restore bundle)
18. [P3][A] Phone folder (6.8 GB): dedupe photos vs cloud copies report
19. [P3][A] Terabox client sync-root health re-check (terabox-sync skill pre-flight)
20. [P2][A] Create D: space dashboard script (weekly report to task folder)
21. [P3][A] OneDrive desktop redirect decision doc (keep local vs sync)
22. [P3][A] $RECYCLE.BIN residual check after Storage Sense week

## G3. Guard Skills Repo (16)
23. [P2][A] #12-carry: test 5 guards against real sample code (fixtures + walkthrough)
24. [P2][A] #14-carry: add/normalize version field across all frontmatter (script)
25. [P2][A] #15-carry: skill usage analytics hook (log invocations to local jsonl)
26. [P2][A] #17-carry: CONTRIBUTING.md (submission flow, validator gate)
27. [P3][A] #20-carry: BAT wrappers → PS1-native equivalents
28. [P3][A] Skill search CLI: fuzzy finder over skills_index.json (prototype)
29. [P2][A] Disambiguate top-10 shared trigger phrases (guard vs tool twins get distinct verbs)
30. [P3][A] Add category badge + see-also rendering check to CI
31. [P2][A] GitHub Release page for v1.0.0 with notes + stats
32. [P3][A] Split mega-skills (>300 lines: video-processing 1093) into SKILL.md + references/
33. [P2][A] Dedupe references/testing-patterns.md (5 copies exist) → shared/references single source
34. [P3][A] Add examples/ dir convention + one example per guard family
35. [P3][A] Skill-of-the-week rotation doc (drive real usage testing)
36. [P2][A] Quarterly anti-drift: counts + index hash check script (cron-able)
37. [P3][A] README: add badges (CI status, skill count, license)
38. [P3][A] Convert maintain.ps1 weekly run into Task Scheduler verified trigger

## G4. Projects (16)
39. [P2][A] OpenDex exe: replace pythonw startup with dist\OpenDex.exe shortcut
40. [P3][A] OpenDex: version info resource in exe (name/company/version)
41. [P2][U] OpenDex DeX end-to-end live test (needs phone plugged)
42. [P2][A] OpenDex: auto-update mechanism (check repo tag, self-replace)
43. [P3][A] OpenDex own repo publish + README + screenshots
44. [P2][A] Input Blocker v70 roadmap draft from v69 retro notes
45. [P3][A] Input Blocker: triage _archive_pre_v69 EXEs (delete 1 GB?)
46. [P3][A] PC DIAGNOSTIQUE: refresh checks for build 29648 + save report
47. [P3][A] instrumentation-list REV4: closeout checklist + archive
48. [P3][A] plc/: ABB simulator smoke-run verification
49. [P3][A] Eplan VEGAMET: generate PDF preview sheet from symbols
50. [P2][A] LIFE-OS weekly review automation script
51. [P3][A] knowledge-base/: prune snapshots >6 months old
52. [P2][A] problems/: convert top 5 entries to KB searchable format
53. [P3][A] reports/: zip old HTML reports (137 files)

## G5. System Health (12)
54. [P2][A] Install pending updates: PS 7.6.5 + Defender sig (reboot cycle)
55. [P2][A] Startup disable candidates: NeatDM, Wondershare PE×2 (confirm w/ user)
56. [P3][A] SFC /scannow baseline
57. [P3][A] DISM RestoreHealth
58. [P2][A] GPU driver audit (Quadro M1200 — last driver date?)
59. [P3][A] Pagefile review (32 GB RAM — fixed size recommendation)
60. [P3][A] Hibernation file: keep or disable decision (hiberfil GB?)
61. [P2][A] Event log weekly triage script (auto-report criticals)
62. [P3][A] Brave cache/profile cleanup routine
63. [P3][A] DNS benchmark + set fastest resolver
64. [P3][A] Battery wear analysis from powercfg report
65. [P3][A] Installed bloatware inventory + removal list

## G6. Memory & Automation (10)
66. [P2][A] Fix mojibake â† artifacts in shared-abdox.md (encoding pass)
67. [P3][A] Session-summary auto-writer (git log + disk + tasks → digest md)
68. [P3][A] Daily standup digest scheduled task
69. [P2][A] Auto-update AGENTS.md counts weekly (Task Scheduler + build_index)
70. [P3][A] Model bench: flash vs ultra on 5 repo QA questions
71. [P2][A] Ghost memory.json schema validation + auto-backup weekly
72. [P3][A] TS port spike: ghost tooling module (Vercel Labs pattern study)
73. [P2][A] NTFS lock recovery playbook as formal skill (force-delete is seed)
74. [P3][A] Token rotation calendar + secrets inventory doc
75. [P2][A] opencode-env-check: add OPENCODE_API_KEY fix instructions alert

## G7. New Discoveries (24) ← from this session
76. [P1][A] Write verify_parts.ps1 runner for all 4 split parts (checksum before concat)
77. [P2][A] After ISO rebuilds: move finished ISOs to H:\Software\PLC\ catalog
78. [P2][A] ESA training zips: extract index of courses → knowledge-base entry
79. [P3][A] "+a Drive" folder: rename to readable name + document contents
80. [P2][A] Build OpenDex release zip (exe + Taskbar.apk + README) → H:\Backups
81. [P3][A] OpenDex crash-log file watcher (opendex.log tail widget)
82. [P2][A] Weekly TASKS progress automation (script marks done items from git log)
83. [P3][A] Create restore point now (#100-carry) before WU installs
84. [P2][A] Defender custom scan of H:\Recovered (files came from old backups)
85. [P3][A] Photo of desktop icons audit → remove dead shortcuts
86. [P3][A] Default apps: PDF/browser associations review
87. [P2][A] Clipboard history enable + pinned snippets setup
88. [P3][A] Night light schedule config
89. [P2][A] Backup C:\Users\Abdox\.agents\skills (custom skills!) to H:\Backups
90. [P2][A] Inventory ~/.opencode/skills vs repo skills — sync unique ones INTO repo
91. [P3][A] Document H:\ai\ task-folder convention in AGENTS.md (rule exists — add example links)
92. [P2][A] Scan repo for hardcoded paths (C:\Users\Abdox) — portability report
93. [P3][A] License headers consistency check across tools/*.py
94. [P2][A] requirements.txt for tools/ (PyInstaller, PIL versions pinned)
95. [P3][A] GitHub repo topics/description polish (seo for discoverability)
96. [P2][A] Mirror repo bundle to TeraBox cloud as offsite copy
97. [P3][A] Explore agent-browser skill for automated CI-badge screenshot in README
98. [P3][A] Test npx skills add Abdox-menara/guard-skills in clean VM/container
99. [P2][A] Write POST-CHKDSK checklist (retry git rm purges, old gitdir cleanup)
100. [P3][A] Celebrate: v1.0.1 tag after next milestone batch 🎯

---
Carried-over originals already done: #1,2,3,4,5(via#4),6,7,8,9,11(partial),12(partial),13,16,18,21,22(no-op),23,25,26(no-op),28,29,30,31,33,34,36,38,50,59,62,63,64,88(done via #31),93,100 → tracked in TASKS_100.md progress log.
