---
name: schematic-review
description: Review a schematic image with @vision using the standard report format. Use for DOL starters, panels, symbol sheets, DXF renders.
---

# Schematic Review (report format — always use)

## Components

List every device with tag + rating (Q breakers, KM contactors, F overloads,
M motors, S buttons, H lamps, X terminals, PLC I/O).

## Wiring

Power path order (inlet → protection → switching → load). Control path
(L → stops → starts → coils → N). Cable/wire numbers if drawn.

## Anomalies vs IEC

Functional issues first; cosmetics second. Reference symbols:
Q1 = IEC 60617 S00288, KM1 = S00287, M = S00305 (circle + M).
Check: overload setting vs motor FLA, PE drawn, wire numbers present,
cross-references present.

## Verdict

PASS / PASS-with-notes / FAIL, one line, with evidence.

## Log usage

After each real invocation:
\\powershell
python C:/opencodes/guard skills/tools/skill_usage_hook.py schematic-review use
\