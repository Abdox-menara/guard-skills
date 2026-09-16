---
name: suivi-tanks
description: Fill and drift-check the Tanks tracking sheet from SUIVI ANAL1.xlsx. Mapping LAB=LABORATOIRE, TR=CAPTEUR. Use for Les Tanks updates.
---

# Suivi Tanks

## Source layout (SUIVI ANAL1.xlsx, sheet Analyse)

- Row 5: dates (`date: DD/MM/YYYY`, note 02/08 + 03/08 typos mean 02/09, 03/09).
- Row 6: `CAPTEUR | LABORATOIRE` pairs per date.
- Rows 29–32: `SORTIE TANK A | SORTIE TANK B | RETOUR | ANCIEN LAVERIE`.
- Mapping: **LAB = LABORATOIRE (odd col), TR = CAPTEUR (even col)**.

## Rules

1. Correct known incident: RETOUR 31/08 is LAB 64 / TR 54 (never copy SORTIE-A values there).
2. `-` or empty in source → empty cell, never 0.
3. Drift check: compare filled sheet vs source per label; print DIFFs or `in sync`.
4. Never overwrite a user-edited filled file without a diff review
   (2026-09-16: v2-full diverged with user August data — codes fixed to
   TB/TA/AU/RO original scheme, values left untouched).

## Log usage

After each real invocation:
\\powershell
python C:/opencodes/guard skills/tools/skill_usage_hook.py suivi-tanks use
\