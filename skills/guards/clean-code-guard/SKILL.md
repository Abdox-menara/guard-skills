---
name: clean-code-guard
description: Review generated or changed production code before it ships, using Clean Code, SOLID, DRY, KISS, YAGNI, and LLM-specific failure-mode checks in any programming language. Best used reactively after an agent writes, edits, refactors, or fixes code, before presenting, committing, or merging the result.
---

# Clean Code Guard

You are reviewing generated or changed code before it ships. Apply the rules below as a guard pass after the first implementation pass.

## How to use this skill

**Guard-pass mode** (recommended): after code has been generated, edited, refactored, or fixed, check the diff or target files against the imperatives below. Fix violations before presenting, committing, or merging.

**Review mode** (triggered when the user asks you to review, audit, or rate code): walk the rules against the target file(s) and produce a structured findings report. Do not edit code in review mode unless asked.

## Adapt to the project first

1. Read the project's agent instructions (CLAUDE.md, AGENTS.md) and coding conventions. Project-specific rules win when they conflict.
2. Identify the language and framework, then read the matching reference for language-specific patterns.
3. Read the file you're editing and at least one neighbor before writing. Mirror the existing style.

## The Imperatives

### Functions and Names

1. **Names reveal intent.** Never use `data`, `result`, `item`, `temp`, `value`, `obj`, `info`, `helper`, `manager`, `utils`, or `handle_*`/`process_*`/`do_*` without a qualifier. A name must answer why it exists and what it does.

2. **Functions stay small.** Target ≤20 lines, one level of abstraction, one thing. If you can extract a function with a name that doesn't restate the body, the parent was doing more than one thing.

3. **Four arguments is the hard ceiling.** At five, introduce a request/config object. Never use boolean flag arguments — split into two functions instead.

4. **No output arguments.** A function either returns a value (query) or has a side effect (command). Never both.

### Comments and Structure

5. **Comments explain WHY, never WHAT.** Delete any comment that paraphrases the line below it. Delete step-number scaffolding comments. Delete commented-out code — version control exists.

6. **Match the file's existing style.** Mirror the casing, import order, error handling, logging, and HTTP/DB client choices. Do not introduce a second pattern.

### SOLID

7. **One actor per module.** A class should be answerable to one stakeholder group. If two unrelated subsystems both reach into the same class, split it.

8. **Extension via new code, not edits.** If adding a new variant requires another type-tag branch in an existing function, refactor to a registry, strategy, or polymorphic dispatch first.

9. **No subclass refuses its parent's contract.** Never override a method to signal "not implemented" or "unsupported operation."

10. **Abstractions live with the client, not the implementation.** Put interfaces in the package that consumes them, not next to the concrete class.

### DRY, KISS, YAGNI

11. **Delete duplicated knowledge, not duplicated text.** Two functions that look alike but encode different rules are not a DRY violation.

12. **The wrong abstraction is worse than duplication.** If an abstraction has accumulated branches for each caller's special case, re-inline it.

13. **Complexity ceiling: cyclomatic ≤10, nesting depth ≤5.** Refactor before exceeding.

14. **No speculative anything.** No optional parameter, config flag, feature toggle, interface, factory, or base class without a present-day caller.

### AI-Specific Guardrails

15. **Never swallow errors with broad catch-all handling.** Catch only the specific error type you can recover from. Returning null/none/empty success from a catch handler is forbidden unless documented.

16. **No defensive guards for impossible cases.** Do not add null checks for values whose declared type already excludes null.

17. **Verify every import and external call.** Before calling a method on a library, confirm it exists in the version installed. Do not generate code based on what the API "should" look like.

18. **No hardcoded "success" returns.** Never return `{"status": "ok"}` or canned data from a function whose spec says it does real work.

19. **Re-derive, do not copy from similar.** When tempted to copy a function and modify it, stop. Re-derive from the spec.

20. **Strip dead code before delivery.** Remove unused imports, unused symbols, unreachable branches, and "just in case" exports.

## Self-Check Before Delivery

1. Walk imperatives 1–20 against your diff. Fix every violation.
2. For new functions: lines ≤ 20? params ≤ 4? complexity ≤ 10? names reveal intent?
3. For new comments: does this explain WHY? If it explains WHAT, delete it.
4. For new error handling: is the caught error type specific? Does the handler do something other than silently return?
5. For new abstractions: is there a second concrete user today? If no, inline it.
6. Did you read the file you edited and at least one neighbor? Did your style match?
7. Is there any hardcoded "ok" return or fixture data? Replace with real implementation.

## Reporting Format (Review Mode)

```
**Rule N violation** in `path/to/file.ext:line`
- What: <description>
- Fix: <what to do instead>
```

Group violations by file. Lead with Rule 15–19 findings (AI-specific), then SOLID/DRY, then style.

## Severity Guide

- **Must fix:** Rules 15, 17, 18, 19 — these hide real bugs
- **Should fix:** Rules 1–14 — these cause maintenance drag
- **Worth noting:** Style inconsistencies

## References

- [references/ai-failure-modes.md](references/ai-failure-modes.md) — the systematic ways LLMs produce bad code
- [references/solid-principles.md](references/solid-principles.md) — SOLID with detection smells
- [references/testing-patterns.md](references/testing-patterns.md) — universal testing patterns
