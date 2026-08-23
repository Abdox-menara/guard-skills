---
name: handoff
version: 2.0.0
author: Abdox
description: |
  ULTRA-ADVANCED Handoff skill with comprehensive context preservation,
  knowledge transfer, and intelligent documentation for seamless agent collaboration.
  Use when the user wants to: handoff work, save progress, switch agents,
  continue later, or any context preservation workflow.

  HANDOFF: Comprehensive context transfer system that preserves all knowledge,
  decisions, and progress for seamless agent collaboration.

  FEATURES:
  - Comprehensive context preservation
  - Decision rationale documentation
  - Knowledge graph construction
  - Risk and blocker tracking
  - Progress visualization
  - Next agent guidance
  - Session continuity
  - Collaboration history

  TRIGGER PHRASES: "handoff", "save progress", "switch agents", "continue later",
  "context transfer", "knowledge preservation", "seamless collaboration",
  "session continuity", "agent handoff".

  TRAINED ON: Knowledge management, context preservation, collaboration patterns,
  documentation standards, and agent coordination.

  ENVIRONMENT: Works with any agent, any project, any complexity.

  SECURITY: Enterprise-grade knowledge protection and access control.
---

# Handoff - ULTRA-ADVANCED v2.0

Compact the current conversation into a structured handoff document so another agent can continue the work without losing context.

## How to Execute

1. **Gather context.** Review the entire conversation and identify:
   - What was the original request?
   - What has been done so far?
   - What is the current state of the work?
   - What decisions were made and why?
   - What is blocked or pending?
   - What files were created or modified?
   - What knowledge was gained?
   - What risks were identified?
   - What dependencies exist?

2. **Structure the handoff.** Use this format:

```markdown
# Handoff: [Brief Description]

## Metadata
- **Session ID**: [Unique identifier]
- **Timestamp**: [ISO timestamp]
- **Agent**: [Current agent name]
- **Project**: [Project name]
- **Branch**: [Git branch if applicable]

## Original Request
[What the user asked for]

## What Was Done
- [Task 1] ✅ [Completion timestamp]
- [Task 2] ✅ [Completion timestamp]
- [Task 3] ⏳ [Progress percentage] (in progress)
- [Task 4] ❌ [Blocker reason] (blocked)

## Current State
[Where things stand right now — what's working, what's not]

### Working Features
- [Feature 1]: [Status and notes]
- [Feature 2]: [Status and notes]

### Known Issues
- [Issue 1]: [Description and workaround]
- [Issue 2]: [Description and workaround]

## Key Decisions
- [Decision 1]: [Why] (affects [what], alternatives considered: [alternatives])
- [Decision 2]: [Why] (affects [what], alternatives considered: [alternatives])

## Knowledge Gained
- [Insight 1]: [What was learned]
- [Insight 2]: [What was learned]

## Risk Assessment
- [Risk 1]: [Impact] [Mitigation strategy]
- [Risk 2]: [Impact] [Mitigation strategy]

## Dependencies
- [Dependency 1]: [Status] [Impact if unavailable]
- [Dependency 2]: [Status] [Impact if unavailable]

## Files Modified
- `path/to/file1.ts` — [what changed] [lines affected]
- `path/to/file2.ts` — [what changed] [lines affected]

## Architecture Notes
[Any architectural decisions or patterns that were established]

## Testing Status
- Unit Tests: [Coverage percentage] [Status]
- Integration Tests: [Coverage percentage] [Status]
- E2E Tests: [Coverage percentage] [Status]

## What's Next
- [ ] [Immediate next step] [Priority] [Estimated time]
- [ ] [Following step] [Priority] [Estimated time]
- [ ] [Blocker to resolve] [Priority] [Owner]

## Context for Next Agent
[Anything the next agent needs to know that isn't obvious from the code]

### Environment Setup
[How to set up the development environment]

### Running the Project
[How to run the project]

### Common Commands
[Useful commands for this project]

## Collaboration History
[Timeline of key events and decisions]

## Questions for Next Agent
[Questions the current agent wants the next agent to answer]

## Success Criteria
[How to know when the work is complete]
```

3. **Be concise.** The handoff should be scannable in 30 seconds. Cut anything that doesn't help the next agent continue.

4. **Save it.** Write the handoff to a file in the project root: `HANDOFF.md`

## When to Use This

- Switching from one agent to another (e.g., Claude Code → Cursor)
- Starting a new session after a long conversation
- The user needs to take a break and continue later
- Multiple agents will work on the same feature
- Long-running projects with multiple sessions
- Complex projects with many stakeholders

## Advanced Features

### Knowledge Graph Construction
```python
class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_id, node_type, attributes):
        """Add a node to the knowledge graph."""
        self.nodes[node_id] = {
            'type': node_type,
            'attributes': attributes,
            'created_at': datetime.now().isoformat()
        }

    def add_edge(self, from_node, to_node, relationship, attributes=None):
        """Add an edge to the knowledge graph."""
        if from_node not in self.edges:
            self.edges[from_node] = []

        self.edges[from_node].append({
            'to': to_node,
            'relationship': relationship,
            'attributes': attributes or {}
        })

    def get_node(self, node_id):
        """Get a node from the knowledge graph."""
        return self.nodes.get(node_id)

    def get_related_nodes(self, node_id, relationship=None):
        """Get nodes related to a specific node."""
        related = []

        if node_id in self.edges:
            for edge in self.edges[node_id]:
                if relationship is None or edge['relationship'] == relationship:
                    related.append({
                        'node': self.nodes.get(edge['to']),
                        'relationship': edge['relationship'],
                        'attributes': edge['attributes']
                    })

        return related

    def visualize(self):
        """Create a visualization of the knowledge graph."""
        visualization = {
            'nodes': [],
            'edges': []
        }

        for node_id, node in self.nodes.items():
            visualization['nodes'].append({
                'id': node_id,
                'label': f"{node['type']}: {node_id}",
                'type': node['type']
            })

        for from_node, edges in self.edges.items():
            for edge in edges:
                visualization['edges'].append({
                    'from': from_node,
                    'to': edge['to'],
                    'label': edge['relationship']
                })

        return visualization
```

### Decision Documentation
```python
class DecisionDocumentation:
    def __init__(self):
        self.decisions = []

    def document_decision(self, decision):
        """Document a key decision."""
        self.decisions.append({
            'id': f"decision_{len(self.decisions) + 1}",
            'timestamp': datetime.now().isoformat(),
            'decision': decision['decision'],
            'rationale': decision['rationale'],
            'alternatives': decision.get('alternatives', []),
            'impact': decision.get('impact', ''),
            'stakeholders': decision.get('stakeholders', [])
        })

    def get_decision_history(self):
        """Get the history of decisions."""
        return self.decisions

    def get_decision_by_id(self, decision_id):
        """Get a specific decision by ID."""
        for decision in self.decisions:
            if decision['id'] == decision_id:
                return decision
        return None

    def get_decisions_by_impact(self, impact_area):
        """Get decisions that affect a specific area."""
        return [
            d for d in self.decisions
            if impact_area.lower() in d['impact'].lower()
        ]
```

### Progress Tracker
```python
class ProgressTracker:
    def __init__(self):
        self.tasks = []
        self.milestones = []

    def add_task(self, task):
        """Add a task to track."""
        self.tasks.append({
            'id': f"task_{len(self.tasks) + 1}",
            'name': task['name'],
            'description': task.get('description', ''),
            'status': task.get('status', 'pending'),
            'priority': task.get('priority', 'medium'),
            'estimated_time': task.get('estimated_time', 0),
            'actual_time': task.get('actual_time', 0),
            'dependencies': task.get('dependencies', []),
            'blockers': task.get('blockers', [])
        })

    def update_task_status(self, task_id, status, notes=None):
        """Update the status of a task."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = status
                if notes:
                    task['notes'] = notes
                return True
        return False

    def get_progress_summary(self):
        """Get a summary of progress."""
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks if t['status'] == 'completed')
        in_progress_tasks = sum(1 for t in self.tasks if t['status'] == 'in_progress')
        blocked_tasks = sum(1 for t in self.tasks if t['status'] == 'blocked')

        return {
            'total_tasks': total_tasks,
            'completed': completed_tasks,
            'in_progress': in_progress_tasks,
            'blocked': blocked_tasks,
            'completion_percentage': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }

    def get_critical_path(self):
        """Get the critical path through tasks."""
        # Find tasks with no dependencies (starting points)
        starting_tasks = [
            t for t in self.tasks
            if not t['dependencies'] and t['status'] != 'completed'
        ]

        # Find longest path
        longest_path = []
        for start in starting_tasks:
            path = self._get_task_chain(start['id'])
            if len(path) > len(longest_path):
                longest_path = path

        return longest_path

    def _get_task_chain(self, task_id):
        """Get the chain of tasks dependent on a specific task."""
        chain = []
        visited = set()

        def dfs(task_id):
            if task_id in visited:
                return
            visited.add(task_id)

            for task in self.tasks:
                if task_id in task['dependencies']:
                    dfs(task['id'])
                    chain.append(task['id'])

        dfs(task_id)
        return chain
```

### Risk Tracker
```python
class RiskTracker:
    def __init__(self):
        self.risks = []

    def add_risk(self, risk):
        """Add a risk to track."""
        self.risks.append({
            'id': f"risk_{len(self.risks) + 1}",
            'description': risk['description'],
            'category': risk.get('category', 'technical'),
            'impact': risk.get('impact', 'medium'),
            'probability': risk.get('probability', 'medium'),
            'mitigation': risk.get('mitigation', ''),
            'status': risk.get('status', 'identified'),
            'owner': risk.get('owner', '')
        })

    def update_risk_status(self, risk_id, status):
        """Update the status of a risk."""
        for risk in self.risks:
            if risk['id'] == risk_id:
                risk['status'] = status
                return True
        return False

    def get_risks_by_category(self, category):
        """Get risks by category."""
        return [r for r in self.risks if r['category'] == category]

    def get_risks_by_impact(self, impact):
        """Get risks by impact level."""
        return [r for r in self.risks if r['impact'] == impact]

    def get_risk_summary(self):
        """Get a summary of risks."""
        total_risks = len(self.risks)
        high_impact_risks = sum(1 for r in self.risks if r['impact'] == 'high')
        mitigated_risks = sum(1 for r in self.risks if r['status'] == 'mitigated')

        return {
            'total_risks': total_risks,
            'high_impact': high_impact_risks,
            'mitigated': mitigated_risks,
            'unmitigated': total_risks - mitigated_risks
        }
```

## Handoff Quality Checklist

```markdown
# Handoff Quality Checklist

## Completeness
- [ ] Original request documented
- [ ] All tasks listed with status
- [ ] Current state described
- [ ] Key decisions documented with rationale
- [ ] Files modified listed
- [ ] Next steps identified
- [ ] Context for next agent provided

## Clarity
- [ ] Handoff is scannable in 30 seconds
- [ ] Technical terms explained
- [ ] Ambiguities resolved
- [ ] Critical information highlighted

## Accuracy
- [ ] All information verified
- [ ] Timestamps accurate
- [ ] File paths correct
- [ ] Dependencies identified

## Usefulness
- [ ] Next agent can continue without questions
- [ ] Blockers clearly identified
- [ ] Success criteria defined
- [ ] Environment setup documented
```

## What Good Looks Like

```markdown
# Handoff: User Authentication Flow

## Metadata
- **Session ID**: auth-session-001
- **Timestamp**: 2024-01-15T14:30:00Z
- **Agent**: Claude Code
- **Project**: E-commerce API
- **Branch**: feature/auth

## Original Request
Implement JWT-based auth with refresh tokens

## What Was Done
- ✅ Created auth middleware (2024-01-15 10:00)
- ✅ Implemented login/register endpoints (2024-01-15 11:30)
- ✅ Added refresh token rotation (2024-01-15 13:00)
- ⏳ Working on rate limiting (60% complete)

## Current State
Auth works end-to-end. Login returns access + refresh tokens.
Refresh rotation works. Rate limiter is started but has a bug
in the token bucket logic.

### Working Features
- JWT token generation and validation
- User registration and login
- Refresh token rotation
- Token revocation

### Known Issues
- Rate limiter bug in token bucket refill logic
- Need to add rate limit tests

## Key Decisions
- Access token: 15min, Refresh: 7days (security vs UX tradeoff)
- Used Redis for token storage (scalability requirement)
- Rate limit: 100 req/min per IP (configurable)

## Knowledge Gained
- Redis connection pooling is critical for performance
- Token rotation requires careful state management
- Rate limiting needs to account for distributed systems

## Risk Assessment
- **Security Risk**: High - JWT implementation must be secure
  - Mitigation: Use established libraries, security audits
- **Performance Risk**: Medium - Token validation overhead
  - Mitigation: Implement caching, use efficient algorithms

## Dependencies
- **Redis**: Available - Required for token storage
- **PostgreSQL**: Available - Required for user data

## Files Modified
- `src/middleware/auth.ts` — JWT verification middleware (lines 1-45)
- `src/routes/auth.ts` — login, register, refresh endpoints (lines 1-120)
- `src/services/token.ts` — token generation and validation (lines 1-80)
- `src/services/rateLimit.ts` — WIP, has bug in bucket logic (lines 1-60)

## Architecture Notes
- Using middleware pattern for auth
- Redis for token storage with connection pooling
- Rate limiter uses token bucket algorithm

## Testing Status
- Unit Tests: 85% coverage ✅
- Integration Tests: 70% coverage ⏳
- E2E Tests: 50% coverage ⏳

## What's Next
- [ ] Fix rate limiter token bucket bug (High priority, 2 hours)
- [ ] Add rate limit tests (Medium priority, 1 hour)
- [ ] Update API documentation (Low priority, 1 hour)

## Context for Next Agent
The rate limiter bug is in `src/services/rateLimit.ts:47` —
the bucket refill logic doesn't account for elapsed time correctly.
Look at `getTokenRefill()` method.

### Environment Setup
```bash
npm install
docker-compose up -d
npm run dev
```

### Running the Project
```bash
npm start
# or
docker-compose up
```

### Common Commands
```bash
npm test
npm run lint
npm run build
```

## Collaboration History
- 2024-01-15 10:00 - Started auth implementation
- 2024-01-15 11:30 - Completed login/register endpoints
- 2024-01-15 13:00 - Added refresh token rotation
- 2024-01-15 14:00 - Started rate limiting, found bug

## Questions for Next Agent
- Should we implement rate limiting per user or per IP?
- Should we add more detailed logging for security audits?
- Should we implement token blacklisting for logout?

## Success Criteria
- All auth endpoints working
- Rate limiting working correctly
- Tests passing with >80% coverage
- Security audit passed
```

## References

- [references/knowledge-management.md](references/knowledge-management.md) — knowledge preservation techniques
- [references/collaboration-patterns.md](references/collaboration-patterns.md) — agent collaboration patterns
- [references/documentation-standards.md](references/documentation-standards.md) — documentation best practices

---

**Version**: 2.0.0
**Status**: ULTRA-ADVANCED Handoff Ready
**Features**: Context Preservation, Knowledge Graph, Decision Documentation, Progress Tracking, Risk Assessment

---

**Remember**: A good handoff is a gift to the next agent. It should provide everything they need to continue the work without losing context. Document decisions, preserve knowledge, and make the transition seamless.
