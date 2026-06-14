---
name: handoff
description: Compact the current conversation into a handoff document so another agent can continue the work. Use when user says "handoff", "save progress", "switch agents", or wants to continue in a new session.
---

# Handoff

Compact the current conversation into a structured handoff document so another agent can continue the work without losing context.

## How to Execute

1. **Gather context.** Review the entire conversation and identify:
   - What was the original request?
   - What has been done so far?
   - What is the current state of the work?
   - What decisions were made and why?
   - What is blocked or pending?
   - What files were created or modified?

2. **Structure the handoff.** Use this format:

```
# Handoff: [Brief Description]

## Original Request
[What the user asked for]

## What Was Done
- [Task 1] ✅
- [Task 2] ✅
- [Task 3] ⏳ (in progress)

## Current State
[Where things stand right now — what's working, what's not]

## Key Decisions
- [Decision 1]: [Why] (affects [what])
- [Decision 2]: [Why] (affects [what])

## Files Modified
- `path/to/file1.ts` — [what changed]
- `path/to/file2.ts` — [what changed]

## What's Next
- [ ] [Immediate next step]
- [ ] [Following step]
- [ ] [Blocker to resolve]

## Context for Next Agent
[Anything the next agent needs to know that isn't obvious from the code]
```

3. **Be concise.** The handoff should be scannable in 30 seconds. Cut anything that doesn't help the next agent continue.

4. **Save it.** Write the handoff to a file in the project root: `HANDOFF.md`

## When to Use This

- Switching from one agent to another (e.g., Claude Code → Cursor)
- Starting a new session after a long conversation
- The user needs to take a break and continue later
- Multiple agents will work on the same feature

## What Good Looks Like

```
# Handoff: User Authentication Flow

## Original Request
Implement JWT-based auth with refresh tokens

## What Was Done
- ✅ Created auth middleware
- ✅ Implemented login/register endpoints
- ✅ Added refresh token rotation
- ⏳ Working on rate limiting (started, not finished)

## Current State
Auth works end-to-end. Login returns access + refresh tokens.
Refresh rotation works. Rate limiter is started but has a bug
in the token bucket logic.

## Key Decisions
- Access token: 15min, Refresh: 7days (security vs UX tradeoff)
- Used Redis for token storage (scalability requirement)
- Rate limit: 100 req/min per IP (configurable)

## Files Modified
- `src/middleware/auth.ts` — JWT verification middleware
- `src/routes/auth.ts` — login, register, refresh endpoints
- `src/services/token.ts` — token generation and validation
- `src/services/rateLimit.ts` — WIP, has bug in bucket logic

## What's Next
- [ ] Fix rate limiter token bucket bug
- [ ] Add rate limit tests
- [ ] Update API documentation

## Context for Next Agent
The rate limiter bug is in `src/services/rateLimit.ts:47` —
the bucket refill logic doesn't account for elapsed time correctly.
Look at `getTokenRefill()` method.
```
