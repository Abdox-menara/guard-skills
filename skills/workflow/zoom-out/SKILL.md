---
name: zoom-out
description: Tell the agent to zoom out and give broader context or a higher-level perspective on an unfamiliar section of code. Use when user says "zoom out", "explain the architecture", "what's going on here", or is lost in the codebase.
---

# Zoom Out

When the user is lost in the codebase or wants broader context, zoom out and explain what's happening at a higher level.

## How to Execute

1. **Start at the entry point.** Find the main entry point of the application, module, or feature under discussion. Trace the flow from there.

2. **Map the architecture.** Identify:
   - What are the major modules/packages?
   - What does each one do?
   - How do they communicate? (HTTP, queues, function calls, events)
   - What are the key data flows?

3. **Explain the "why."** Don't just describe the structure — explain why it's structured this way. What problem does this architecture solve?

4. **Highlight the key decisions.** What are the non-obvious choices? What tradeoffs were made? What would change if requirements changed?

5. **Connect to the user's question.** Relate the high-level view back to whatever they're working on. "This matters because..."

## Output Format

```
## Architecture Overview

### What This System Does
[One paragraph: the purpose]

### Key Components
- **Component A**: [what it does, why it exists]
- **Component B**: [what it does, why it exists]
- **Component C**: [what it does, why it exists]

### Data Flow
[How data moves through the system]

### Key Design Decisions
1. [Decision] → [Reason] → [Tradeoff]
2. [Decision] → [Reason] → [Tradeoff]

### What You're Looking At
[Connect the architecture back to the user's specific question]
```

## When to Use This

- User says "zoom out" or "explain the architecture"
- User is working on a file they don't fully understand
- User is about to make a change that affects multiple modules
- User is debugging and needs to understand the system context
- After a long debugging session, to document what was learned
