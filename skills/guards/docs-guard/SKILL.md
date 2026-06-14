---
name: docs-guard
description: Review generated or changed documentation before it ships — READMEs, API references, docstrings, changelogs, tutorials. Best used reactively after an agent writes or edits docs. Core job: verify every referenced symbol, flag, endpoint, config key, and code sample against the source; catch docs-vs-code drift; strip filler and unverifiable claims.
---

# Docs Guard

You are reviewing generated or changed documentation before it ships. Apply the rules below as a guard pass. The core principle: documentation is a set of claims about a codebase, and every claim is checkable. Your job is to check them.

These rules exist because AI agents document from memory of how APIs usually look, not from the code in front of them. Half of AI answers to programming questions contain incorrect information, yet the prose sounds authoritative either way. You can verify; readers cannot.

## How to use this skill

**Guard-pass mode** (recommended): after documentation has been generated or edited, verify every claim against the source and run the self-check before delivery.

**Review mode** (the user asks you to review, audit, or fact-check docs): walk the rules against the target docs and produce a findings report with file:line evidence. Do not rewrite in review mode unless asked.

## The Rules

### Accuracy — must fix

1. **Every referenced symbol must exist.** Every function, method, class, hook, CLI command, flag, endpoint, config key, env var, and file path mentioned in the docs gets verified against the actual source — by reading it, not recalling it.

2. **Every code sample must work.** Imports resolve, APIs exist with the documented signatures, and the sample runs outside the author's machine — no hardcoded local paths, no real credentials, no implicit prior state.

3. **Document the code's actual behavior, not its intended behavior.** Read the implementation before describing it. Where code and comments/specs disagree, the code is the truth — flag the disagreement to the user.

4. **No unverifiable claims.** Performance numbers, compatibility matrices, scale limits, and "production-ready" assertions require a source in the repository. "Fast" is marketing; "O(n log n), benchmarked in bench/sort.md" is documentation.

### Versioning and drift

5. **Versions are explicit.** Features, flags, and behaviors state the version that introduced them. Prerequisites are pinned or ranged, never "latest". Deprecated items say so, with the replacement.

6. **A code change owes a docs change.** When editing code whose behavior is documented — rename, signature change, new default, removed flag — update every doc surface that mentions it in the same change.

### Substance — should fix

7. **No filler, no slop.** Delete: docstrings that paraphrase the signature ("Gets the user by ID" above `get_user_by_id`), sections that restate their heading, marketing adjectives in technical prose ("powerful", "seamless", "blazingly fast"), and intro padding ("In this section, we will explore…").

8. **Don't paraphrase upstream docs.** Link to external documentation instead of restating it. Document only your project's relationship to the external thing.

9. **Examples cover the failure path too.** A tutorial that only shows the happy path documents half the API. Show what the error looks like and what the caller should do.

### Structure — worth noting

10. **Navigation tells the truth.** Headings describe their sections, internal links resolve, and there are no TODO stubs or "coming soon" sections in published docs.

## Self-Check Before Delivery

1. List every symbol, flag, endpoint, config key, and path your docs mention. Did you verify each one against the source in this session?
2. Would every code sample run on a clean machine?
3. Any number, compatibility claim, or superlative without a repo-verifiable source?
4. If this change touched code: did you grep all docs surfaces for the old names?
5. Any docstring that just restates the signature? Any section that restates its heading?
6. Do all internal links resolve?

## Reporting Format (Review Mode)

```
**Rule N violation** in `docs/path.md:<line or section>`
- Claim: <what the docs say>
- Reality: <what the code actually has, with file:line>
- Fix: <one sentence>
```

Lead with Rule 1–4 findings (false claims), then drift, then substance.

## Severity Guide

- **Must fix:** Rules 1–4 — false documentation is worse than no documentation
- **Should fix:** Rules 5–9 — drift debt and noise
- **Worth noting:** Rule 10 — navigation and polish
