---
name: diagnose
description: Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user says "diagnose this" / "debug this", reports a bug, says something is broken/throwing/failing, or describes a performance regression.
---

# Diagnose

A discipline for hard bugs. Skip phases only when explicitly justified.

## Phase 1 — Build a Feedback Loop

**This is the skill.** Everything else is mechanical. If you have a fast, deterministic, agent-runnable pass/fail signal for the bug, you will find the cause. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to Construct One (try in this order)

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states, automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version and diff outputs.

Build the right feedback loop, and the bug is 90% fixed.

### Iterate on the Loop Itself

Treat the loop as a product:
- Can I make it faster?
- Can I make the signal sharper?
- Can I make it more deterministic?

A 2-second deterministic loop is a debugging superpower.

### Non-Deterministic Bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100x, parallelise, add stress, narrow timing windows. A 50%-flake bug is debuggable; 1% is not — keep raising the rate.

### When You Genuinely Cannot Build a Loop

Stop and say so explicitly. List what you tried. Ask the user for:
- Access to whatever environment reproduces it
- A captured artifact (HAR file, log dump, screen recording)
- Permission to add temporary production instrumentation

Do not proceed to Phase 2 without a loop.

## Phase 2 — Reproduce

Run the loop. Watch the bug appear.

Confirm:
- The loop produces the failure mode the **user** described — not a different failure nearby
- The failure is reproducible across multiple runs
- You have captured the exact symptom (error message, wrong output, slow timing)

Do not proceed until you reproduce the bug.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear."

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:
1. **Debugger / REPL inspection** — one breakpoint beats ten logs
2. **Targeted logs** at the boundaries that distinguish hypotheses
3. Never "log everything and grep"

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup becomes a single grep.

**Perf branch.** For performance regressions: establish a baseline measurement, then bisect. Measure first, fix second.

## Phase 5 — Fix + Regression Test

Write the regression test **before the fix** — but only if there is a correct seam for it.

A correct seam exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow, a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Flag this for the next phase.

If a correct seam exists:
1. Turn the minimised repro into a failing test
2. Watch it fail
3. Apply the fix
4. Watch it pass
5. Re-run the Phase 1 feedback loop against the original scenario

## Phase 6 — Cleanup + Post-Mortem

Required before declaring done:
- [ ] Original repro no longer reproduces
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed
- [ ] Throwaway prototypes deleted
- [ ] The hypothesis that turned out correct is stated in the commit/PR message

**Then ask: what would have prevented this bug?** If the answer involves architectural change, hand off to architecture improvement skills with the specifics.

## References

- [references/testing-patterns.md](references/testing-patterns.md) — for writing regression tests
