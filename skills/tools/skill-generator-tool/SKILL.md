---
name: skill-generator-tool
description: ULTRA-ADVANCED Batch Skill Generator — creates, improves, and manages AI coding agent skill files at scale. Commands: list, create, improve, inventory, stats, find, template, dedupe, clean. Based on the methodology used to build a 292-skill ecosystem.
---

# Skill Generator Tool

Batch generator and manager for coding-agent skill files.

## Usage

```powershell
python generate_batch.py <command> [options]
```

## Commands

| Command | Purpose |
|---------|---------|
| `list` | List all existing skills with category and count |
| `create <json_file>` | Create skills from JSON definition file |
| `improve <json_file>` | Update existing skills with richer content (v2.0+) |
| `inventory` | Show full inventory report |
| `stats` | Show statistics across all skills |
| `find <pattern>` | Find skills matching pattern in name/description |
| `template` | Generate a JSON template for new skill definitions |
| `dedupe` | Find and report duplicate skills |
| `clean` | Remove empty skill directories |

## Workflow

1. `python generate_batch.py template > defs.json` — scaffold definitions
2. Edit `defs.json` with skill name/category/description
3. `python generate_batch.py create defs.json` — generate SKILL.md files
4. `python generate_batch.py dedupe` — check for overlaps
5. `python ..\..\tools\build_index.py` — regenerate the master index
