# Guard Skills

**225 skills for coding agents: quality gates that catch AI-generated failure modes, workflow skills that prevent them, plus infrastructure tools.**

> 72 guards · 83 tools · 67 workflow skills · 3 special (desktop-control-mcp, force-delete, self-learning)

Best use: let your agent do the work, then invoke the relevant guard on the diff before you present, commit, or merge it. Or use the workflow skills to shape how the agent works from the start.

## Install

```bash
# Install all skills
npx skills add Abdox-menara/guard-skills

# Install individual skills
npx skills add Abdox-menara/guard-skills --skill clean-code-guard
npx skills add Abdox-menara/guard-skills --skill test-guard
npx skills add Abdox-menara/guard-skills --skill grill-me

# Install for a specific agent
npx skills add Abdox-menara/guard-skills --skill clean-code-guard --agent claude-code
npx skills add Abdox-menara/guard-skills --skill '*' --agent cursor
```

Works with Claude Code, Codex, Cursor, OpenCode, and other supported agents via the [Skills CLI](https://github.com/vercel-labs/skills).

## Philosophy

This repository combines two approaches:

1. **Guard Skills** — Quality gates that run AFTER the agent produces work. They catch systematic AI failure modes: hallucinated APIs, mock abuse, broad error swallowing, docs-vs-code drift.

2. **Workflow Skills** — Process skills that shape HOW the agent works. Planning alignment, test-driven development, disciplined debugging, architecture awareness.

Use guards as a safety net. Use workflow skills to build right from the start.

## Skills Reference

### Guards (Post-Review Quality Gates)

| Skill | Use After | Catches |
|---|---|---|
| `clean-code-guard` | Agent wrote/edited production code | LLM code smells, over-abstraction, error swallowing, SOLID/DRY/KISS/YAGNI violations |
| `test-guard` | Agent wrote/edited tests | Mock abuse, duplicate tests, implementation-detail assertions, tests that catch nothing |
| `docs-guard` | Agent wrote/edited docs | Hallucinated symbols, broken samples, docs-vs-code drift, unverifiable claims |

### Workflow (Engineering Process)

| Skill | Use When | What It Does |
|---|---|---|
| `grill-me` | Starting a new feature/fix | Interview the user relentlessly until every decision is resolved |
| `tdd` | Writing code | Red-green-refactor loop with vertical slices |
| `diagnose` | Debugging a hard bug | Disciplined reproduce → hypothesize → instrument → fix loop |
| `zoom-out` | Lost in the codebase | Explain code in context of the whole system |
| `handoff` | Switching sessions/agents | Compact conversation into a handoff document |

## How to Use

### As a Guard (After the Agent Writes)

```
Use $clean-code-guard on the diff you just produced.
Use $test-guard on the tests you just wrote.
Use $docs-guard on this README update before we ship it.
```

### As a Workflow Skill (Before/During)

```
Use $grill-me before we start implementing.
Use $tdd while building this feature.
Use $diagnose to find what's causing this bug.
Use $zoom-out to understand this module.
```

## Repository Shape

```
skills/
├── guards/                          # Post-review quality gates
│   ├── clean-code-guard/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── test-guard/
│   │   ├── SKILL.md
│   │   └── references/
│   └── docs-guard/
│       ├── SKILL.md
│       └── references/
├── workflow/                        # Engineering process skills
│   ├── grill-me/
│   │   └── SKILL.md
│   ├── tdd/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── diagnose/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── zoom-out/
│   │   └── SKILL.md
│   └── handoff/
│       └── SKILL.md
└── references/                      # Shared knowledge base
    ├── ai-failure-modes.md
    ├── solid-principles.md
    └── testing-patterns.md
```

## Trust and Validation

This package is intentionally inspectable:

- Skill content is Markdown — no executable scripts, no network calls, no MCP server dependencies, no credentials
- Each guard references published research on AI failure modes
- Progressive disclosure: SKILL.md stays small, deeper guidance loads only when needed

## License

MIT
