# 100 Recommended Tasks — Abdox Master List (2026-08-23)

> Generated from verified system state + project memory. Check off as completed.
> Legend: [P1] urgent/high · [P2] valuable · [P3] nice-to-have · [A] automatable by agent

## PROGRESS LOG
**Session 2026-08-23 — 14 done:**✅ #1 validate (225/225 clean) · ✅ #2 secret scan (0 secrets) · ✅ #3 index sync (225)
✅ #6+#8 committed+pushed `5ed07de` · ✅ #28 TEMP audited (8.7 GB active files remain)
✅ #31 Recycle emptied (**C: +18 GB**) · ✅ #33 Defender healthy · ✅ #34 startup flagged (NeatDM, Wondershare×2)
✅ #40 event log OK · ✅ #50 battery report generated · ✅ #59 task Ready · ✅ #62 junk folders purged
⚠️ #63 UnityProTemp locked (0 MB, ignore) · ⏳ #27 zips await user verdict
**Next up:** #26 chkdsk (admin+reboot) · #51 TeraBox upload (~51 GB) · #57 H: recovery plan · #53 semi-uniques merge

**Session 2026-08-23 (2) — #4 DONE:** Dedup analysis executed. Findings: 0 exact-duplicate bodies in 222 skills; dedupe_report.json pairs were template false-positives. Real issue = 5 trigger collisions (identical phrases, stub vs rich twin). Merged: deleted 5 skeleton stubs (tools/seo, workflow/api-design, chaos-engineering, database-design, feature-flags), kept rich twins. Library: **225 → 220** (72G/82T/63W/3S). NTFS lock hit during delete — force-delete method worked. Commit `99fbc12` pushed ✅

## A. Guard Skills Repo (25)
1. [P1][A] Run validate_skills.py — full library validation
2. [P1][A] Run secret_scan.py — no leaked keys in 225 skills
3. [P1][A] Re-run build_index.py — confirm 225 sync (done today ✅)
4. [P2][A] Act on validator v2 dedup analysis — merge duplicate skills
5. [P2][A] Process deprecation list — remove/archive deprecated skills
6. [P2][A] Push latest commits to github.com/Abdox-menara/guard-skills
7. [P2][A] Weekly bundle → H:\Backups (done today 01:54 ✅ — repeat weekly)
8. [P2] Verify GitHub remote == local HEAD (a045b07)
9. [P2][A] Add GitHub Actions CI: validate on every push
10. [P3][A] Skill description quality pass — improve trigger phrases
11. [P3][A] Fill empty "Purpose" fields in skill index (many are ".")
12. [P2] Test 5 random guard skills against real code samples
13. [P3][A] Generate SKILL.md template consistency report
14. [P2] Add version field to all skill frontmatter
15. [P3] Create skill usage analytics hook
16. [P2][A] Tag release v225 on GitHub
17. [P3] Write CONTRIBUTING.md for skill submissions
18. [P3][A] Cross-link related skills (see-also sections)
19. [P2] Review tools/ scripts for Windows PowerShell 7 compat
20. [P3][A] Convert BAT wrappers to PS1-native equivalents
21. [P2] Prune stale branches on GitHub remote
22. [P3][A] Add changelog.md auto-generation from commits
23. [P2] Audit .gitignore for remaining over-blocking patterns
24. [P3] Document skill authoring guide in README
25. [P3][A] Quarterly: re-verify counts vs filesystem (anti-drift)

## B. System Health & Cleanup (25)
26. [P1] chkdsk C: /f /r — fix NTFS corruption at C:\opencodes (admin+reboot)
27. [P1][A] Delete corrupt OneDrive zips after review (H:\Recovered\API-SFO)
28. [P2][A] Windows Temp cleanup (%TEMP% size audit + purge)
29. [P2][A] C:\Windows\Temp cleanup
30. [P2][A] Delivery Optimization cache purge
31. [P2][A] Recycle Bin empty (all drives)
32. [P2][A] Windows Update — check + install pending
33. [P2][A] Defender quick scan; schedule weekly full scan
34. [P2][A] Startup apps audit — disable junk
35. [P2][A] Services audit — disable unnecessary
36. [P3][A] SFC /scannow system file check
37. [P3][A] DISM /Online /Cleanup-Image /RestoreHealth
38. [P2][A] Driver audit — outdated/nvidia quadro driver check
39. [P3][A] Power plan optimization (high perf for workstation)
40. [P2][A] Event Log error triage (last 7 days criticals)
41. [P2][A] Browser cache purge (Brave)
42. [P3][A] DNS flush + faster DNS test (1.1.1.1)
43. [P3][A] Network adapter power management fix
44. [P2][A] Pagefile sizing review (32 GB RAM)
45. [P3][A] Hibernation file review (hiberfil vs RAM)
46. [P2][A] Installed apps inventory — flag bloatware
47. [P3][A] Font cache rebuild if slow
48. [P2][A] Task Scheduler hygiene — dead tasks cleanup
49. [P3][A] WMI repository health check
50. [P2][A] Battery/thermal report (powercfg /batteryreport)

## C. Storage & Backups (15)
51. [P1][A] Upload _recovered_stale_20260823 (~51 GB) to TeraBox
52. [P2][A] After upload: delete local copy → D: gains ~51 GB more
53. [P2][A] Diff D:\A\Desktop_Sync uniques (106.8 GB) vs root — merge or archive
54. [P2][A] Terabox folder audit on D: (11.8 GB — dedupe candidates?)
55. [P2][A] D:\Downloads audit (6.2 GB — old installers purge)
56. [P3][A] arduino folder (2.1 GB) — archive if inactive
57. [P2][A] H: free-space recovery plan (only 23.2 GB left)
58. [P2][A] Monthly backup verification: test-restore one bundle
59. [P2][A] Automate GuardSkills-Maintenance task (verify Ready state works)
60. [P3][A] Cloud photo backup audit (phone folder 6.8 GB)
61. [P2][A] OneDrive desktop redirect config review
62. [P3][A] Old D:\h + D:\tmp folders — investigate/purge
63. [P2][A] UnityProTemp (D:) — safe to delete?
64. [P3][A] $RECYCLE.BIN deep clean on D:
65. [P2][A] Set storage-sense auto-cleanup on C:

## D. Projects (20)
66. [P2] OpenDex v2.2: DeX wallpaper picker polish + keyguard UX note
67. [P2] OpenDex: test DeX mode end-to-end (phone reconnect needed)
68. [P2][A] OpenDex: package as exe (PyInstaller) + icon
69. [P3][A] OpenDex: publish to own repo with README
70. [P2] Input Blocker v70: plan next features (from v69 retro)
71. [P2] Input Blocker: verify Hello biometrics manually (user action)
72. [P2][A] Input Blocker: archive pre-v69 EXEs decision (1 GB)
73. [P3][A] PC DIAGNOSTIQUE: refresh 100-point suite for Win11 29648
74. [P3][A] instrumentation-list: close out 19094-02 REV4 deliverables
75. [P3][A] plc/: ABB conductivity simulator — verify still runs
76. [P3][A] Eplan VEGAMET symbols: export PDF preview sheet
77. [P2][A] LIFE-OS: weekly review automation
78. [P3][A] knowledge-base: prune read-only snapshots >6 months
79. [P2][A] problems/: convert top 5 to searchable KB entries
80. [P3][A] reports/: archive old HTML reports to zip

## E. Memory / Knowledge / Automation (15)
81. [P2][A] Sync knowledge_base_v2.json with today's session
82. [P2][A] Update HANDOFF.md for next session continuity
83. [P2][A] Fix mojibake encoding in shared-abdox.md (â€” artifacts)
84. [P2][A] AGENTS.md: update PC specs (D:/H: changed today)
85. [P3][A] Build session-summary auto-writer script
86. [P2][A] opencode-env-check.ps1 — verify all API keys valid
87. [P3][A] Model benchmark: deepseek-v4-flash vs nemotron-3-ultra on repo QA
88. [P2][A] Ghost MCP health check + memory.json backup
89. [P3][A] Create daily standup digest script (git log + disk + tasks)
90. [P2][A] Auto-update AGENTS.md skill counts via scheduled task
91. [P3][A] Explore: TS port of ghost tooling (Vercel Labs pattern)
92. [P3][A] Prototype skill-search CLI (fuzzy find across 225 skills)
93. [P2][A] Backup .config/opencode configs to H:\Backups
94. [P3][A] Document recovery procedures (NTFS lock playbook)
95. [P2][A] Quarterly security review: rotate exposed tokens

## F. Quick Wins / Misc (5)
96. [P3][A] Desktop shortcut audit (C:\Users\Abdox\Desktop)
97. [P3][A] Default app associations review
98. [P3][A] Clipboard history enable/configure
99. [P3][A] Night light + display calibration check
100. [P3][A] Create restore point before major changes
