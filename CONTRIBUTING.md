# Contributing Skills

## Where skills live

`skills/<category>/<name>/SKILL.md` — categories: `guards`, `tools`, `workflow`, plus top-level `special` skills.

## Frontmatter (required)

```yaml
---
name: my-skill          # kebab-case, must match folder name, unique library-wide
version: 1.0.0
author: Abdox
description: |
  One-line purpose (first line = index "Purpose", keep it specific).
  TRIGGER PHRASES: "phrase one, phrase two"
  ENVIRONMENT: Works with any codebase, any language, any framework.
---
```

Rules:
1. `name` matches folder, unique across the library.
2. First description line populates the index — specific, no marketing prefix.
3. Trigger phrases must not collide with another skill's triggers (see `outputs/trigger-dups.json` topic-family list for known intentional overlaps).
4. Keep SKILL.md under ~150 lines; put deep material in `references/` and link it (see `skills/tools/video-processing/` as the template). Flagship ULTRA-ADVANCED skills may exceed this — note the exception in your PR.
5. No executables, no network calls, no credentials — Markdown instructions only.

## Before submitting

```bash
python tools/validate_skills.py   # frontmatter, descriptions, links
python tools/secret_scan.py       # no leaked keys
python tools/build_index.py       # regenerate AGENTS.md §4 + skills_index.json
```

Commit everything the validators touch (`AGENTS.md`, `skills_index.json`).

## Cross-links

Add `See Also` links to related skills: same-category `../name`, cross-category `../../cat/name`. The validator checks for broken links.
