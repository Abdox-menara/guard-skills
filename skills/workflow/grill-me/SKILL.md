---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

# Grill Me

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## How This Works

1. **Start broad:** What are we building? Who is it for? What problem does it solve?
2. **Drill into scope:** What's in? What's out? What are the hard constraints?
3. **Challenge assumptions:** Why this approach? What alternatives did you consider? Why did you reject them?
4. **Resolve dependencies:** What does this depend on? What depends on this? What's the order of operations?
5. **Find edge cases:** What happens when X fails? What about Y? Have you considered Z?
6. **Confirm decisions:** So we've agreed: [summary]. Anything you want to revisit?

## Rules

- One question at a time
- Provide your recommended answer for each question
- If the user is vague, push for specifics
- If the user contradicts themselves, call it out
- If a question can be answered by reading the code, read the code instead of asking
- Stop when every branch of the decision tree is resolved

## What Good Looks Like

```
Agent: What's the primary data flow for this feature?
User: Users upload a CSV, we parse it, and show results.
Agent: Recommended: streaming parse for large files, batch insert.
       What's the max file size you expect?
User: ~10MB, maybe 50K rows.
Agent: That's manageable in memory. But if you want to support 100MB+,
       streaming is the safer default. Your call?
User: Let's go with streaming.
Agent: Got it. Streaming parse, batch insert. Next: how should errors
       in individual rows be reported to the user?
```
