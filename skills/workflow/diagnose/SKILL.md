---
name: diagnose
version: 2.0.0
author: Abdox
description: |
  ULTRA-ADVANCED Diagnose skill with systematic debugging, root cause analysis,
  performance profiling, and intelligent bug detection for complex issues.
  Use when the user wants to: debug issues, diagnose problems, find root causes,
  fix performance regressions, or any systematic debugging workflow.

  DIAGNOSE: Comprehensive debugging system that systematically identifies,
  analyzes, and resolves complex software issues.

  FEATURES:
  - Systematic debugging methodology
  - Root cause analysis (5 Whys, Fishbone, Pareto)
  - Performance profiling and optimization
  - Memory leak detection
  - Concurrency issue analysis
  - Security vulnerability debugging
  - Automated bug detection
  - Knowledge base building

  TRIGGER PHRASES: "diagnose", "debug", "troubleshoot", "root cause", "fix bug",
  "performance issue", "memory leak", "concurrency problem", "security vulnerability",
  "systematic debugging".

  TRAINED ON: Debugging methodologies, root cause analysis, performance profiling,
  memory analysis, concurrency patterns, and security debugging.

  ENVIRONMENT: Works with any programming language, any platform, any complexity.

  SECURITY: Enterprise-grade security debugging and vulnerability detection.
---

# Diagnose - ULTRA-ADVANCED v2.0

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
10. **A/B testing harness** — compare behavior between two versions or configurations.
11. **Chaos engineering** — introduce controlled failures to test resilience.
12. **Load testing harness** — simulate high load to trigger performance issues.

Build the right feedback loop, and the bug is 90% fixed.

### Iterate on the Loop Itself

Treat the loop as a product:
- Can I make it faster?
- Can I make the signal sharper?
- Can I make it more deterministic?
- Can I make it more automated?
- Can I make it more reusable?

A 2-second deterministic loop is a debugging superpower.

### Non-Deterministic Bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100x, parallelise, add stress, narrow timing windows. A 50%-flake bug is debuggable; 1% is not — keep raising the rate.

### When You Genuinely Cannot Build a Loop

Stop and say so explicitly. List what you tried. Ask the user for:
- Access to whatever environment reproduces it
- A captured artifact (HAR file, log dump, screen recording)
- Permission to add temporary production instrumentation
- Access to monitoring and logging systems
- Permission to run diagnostic tools

Do not proceed to Phase 2 without a loop.

## Phase 2 — Reproduce

Run the loop. Watch the bug appear.

Confirm:
- The loop produces the failure mode the **user** described — not a different failure nearby
- The failure is reproducible across multiple runs
- You have captured the exact symptom (error message, wrong output, slow timing)
- You have captured the environment (OS, versions, configuration)
- You have captured the input data

Do not proceed until you reproduce the bug.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear."

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly.

### Root Cause Analysis Methods

#### 5 Whys Analysis
```python
def five_whys(problem, get_cause):
    """Perform 5 Whys root cause analysis."""
    whys = []
    current_problem = problem

    for i in range(5):
        cause = get_cause(current_problem)
        whys.append({
            'level': i + 1,
            'problem': current_problem,
            'cause': cause
        })
        current_problem = cause

    return whys
```

#### Fishbone (Ishikawa) Diagram
```python
def fishbone_diagram(problem, categories):
    """Create a fishbone diagram for root cause analysis."""
    diagram = {
        'problem': problem,
        'categories': {}
    }

    for category, causes in categories.items():
        diagram['categories'][category] = {
            'causes': causes,
            'sub-causes': {}
        }

    return diagram
```

#### Pareto Analysis
```python
def pareto_analysis(issues):
    """Perform Pareto analysis (80/20 rule)."""
    # Sort issues by frequency
    sorted_issues = sorted(issues.items(), key=lambda x: x[1], reverse=True)

    total = sum(count for _, count in sorted_issues)
    cumulative = 0

    pareto_items = []
    for issue, count in sorted_issues:
        cumulative += count
        percentage = (count / total) * 100
        cumulative_percentage = (cumulative / total) * 100

        pareto_items.append({
            'issue': issue,
            'count': count,
            'percentage': percentage,
            'cumulative_percentage': cumulative_percentage,
            'is_vital_few': cumulative_percentage <= 80
        })

    return pareto_items
```

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:
1. **Debugger / REPL inspection** — one breakpoint beats ten logs
2. **Targeted logs** at the boundaries that distinguish hypotheses
3. Never "log everything and grep"

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup becomes a single grep.

**Perf branch.** For performance regressions: establish a baseline measurement, then bisect. Measure first, fix second.

### Debugging Tools

#### Performance Profiler
```python
import time
import functools

def profile(func):
    """Decorator to profile function execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        start_memory = get_memory_usage()

        result = func(*args, **kwargs)

        end = time.time()
        end_memory = get_memory_usage()

        print(f"[PROFILE] {func.__name__}:")
        print(f"  Time: {end - start:.4f}s")
        print(f"  Memory: {end_memory - start_memory:.2f}MB")

        return result
    return wrapper

def get_memory_usage():
    """Get current memory usage."""
    import psutil
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024
```

#### Memory Leak Detector
```python
import gc
import objgraph

def detect_memory_leaks():
    """Detect memory leaks in Python code."""
    gc.collect()

    # Get object counts
    object_counts = objgraph.show_most_common_types(limit=10)

    # Look for growing object counts
    return object_counts

def track_memory_allocation(func):
    """Track memory allocation in a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        gc.collect()
        before = objgraph.show_most_common_types()

        result = func(*args, **kwargs)

        gc.collect()
        after = objgraph.show_most_common_types()

        # Compare before and after
        for obj_type in after:
            if after[obj_type] > before.get(obj_type, 0):
                print(f"[MEMORY] {obj_type} increased by {after[obj_type] - before.get(obj_type, 0)}")

        return result
    return wrapper
```

#### Concurrency Debugger
```python
import threading
import traceback

def debug_concurrency():
    """Debug concurrency issues."""
    # Get all threads
    for thread_id, frame in sys._current_frames().items():
        print(f"\nThread {thread_id}:")
        traceback.print_stack(frame)
```

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

### Fix Strategies

#### Defensive Programming
```python
def defensive_fix(original_code, vulnerability):
    """Apply defensive programming fix."""
    fixes = {
        'null_check': lambda code: f"if {code} is None: raise ValueError('Input cannot be None')\n{code}",
        'type_check': lambda code: f"if not isinstance({code}, expected_type): raise TypeError(f'Expected {{expected_type}}, got {{type({code})}}')\n{code}",
        'bounds_check': lambda code: f"if {code} < 0 or {code} >= len(array): raise IndexError(f'Index {code} out of bounds')\n{code}"
    }

    return fixes.get(vulnerability, lambda code: code)(original_code)
```

#### Algorithm Optimization
```python
def optimize_algorithm(code, performance_issue):
    """Optimize algorithm based on performance issue."""
    optimizations = {
        'nested_loops': 'Use hash maps or sets for O(1) lookups',
        'recursive': 'Add memoization or convert to iterative',
        'string_concatenation': 'Use string builder or join',
        'list_appending': 'Use list comprehension or generator'
    }

    return optimizations.get(performance_issue, 'Review algorithm complexity')
```

## Phase 6 — Cleanup + Post-Mortem

Required before declaring done:
- [ ] Original repro no longer reproduces
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed
- [ ] Throwaway prototypes deleted
- [ ] The hypothesis that turned out correct is stated in the commit/PR message
- [ ] Documentation updated if necessary
- [ ] Knowledge base updated with lessons learned

**Then ask: what would have prevented this bug?** If the answer involves architectural change, hand off to architecture improvement skills with the specifics.

### Post-Mortem Template

```markdown
# Bug Post-Mortem

## Summary
- **Bug**: [Brief description]
- **Root Cause**: [What actually caused it]
- **Impact**: [What was affected]
- **Duration**: [How long it existed]

## Timeline
- [Time] Bug reported
- [Time] Reproduction confirmed
- [Time] Root cause identified
- [Time] Fix implemented
- [Time] Fix verified

## Root Cause Analysis
### 5 Whys
1. Why did the bug occur? [Answer]
2. Why did [answer to 1]? [Answer]
3. Why did [answer to 2]? [Answer]
4. Why did [answer to 3]? [Answer]
5. Why did [answer to 4]? [Answer]

### Contributing Factors
- [Factor 1]
- [Factor 2]

## What Went Well
- [Thing 1]
- [Thing 2]

## What Could Be Improved
- [Improvement 1]
- [Improvement 2]

## Action Items
- [ ] [Action 1] - [Owner] - [Due Date]
- [ ] [Action 2] - [Owner] - [Due Date]

## Lessons Learned
- [Lesson 1]
- [Lesson 2]
```

## Debugging Knowledge Base

### Bug Patterns
```python
class BugPatterns:
    def __init__(self):
        self.patterns = {}

    def add_pattern(self, pattern):
        """Add a bug pattern to the knowledge base."""
        self.patterns[pattern['name']] = pattern

    def find_similar_patterns(self, current_bug):
        """Find similar patterns to current bug."""
        similar = []

        for name, pattern in self.patterns.items():
            similarity = self._calculate_similarity(current_bug, pattern)
            if similarity > 0.7:  # 70% similarity threshold
                similar.append({
                    'pattern': pattern,
                    'similarity': similarity
                })

        return sorted(similar, key=lambda x: x['similarity'], reverse=True)

    def _calculate_similarity(self, bug1, bug2):
        """Calculate similarity between two bugs."""
        # Simple similarity based on symptoms and causes
        symptoms_similarity = self._compare_symptoms(bug1['symptoms'], bug2['symptoms'])
        causes_similarity = self._compare_causes(bug1.get('causes', []), bug2.get('causes', []))

        return (symptoms_similarity + causes_similarity) / 2
```

### Solution Database
```python
class SolutionDatabase:
    def __init__(self):
        self.solutions = {}

    def add_solution(self, solution):
        """Add a solution to the database."""
        self.solutions[solution['id']] = solution

    def find_solutions_for_pattern(self, pattern_id):
        """Find solutions for a specific bug pattern."""
        return [s for s in self.solutions.values() if pattern_id in s['patterns']]

    def get_effective_solutions(self):
        """Get solutions sorted by effectiveness."""
        return sorted(self.solutions.values(),
                     key=lambda x: x['success_rate'],
                     reverse=True)
```

## Debugging Checklist

```markdown
# Debugging Checklist

## Before Starting
- [ ] Understand the problem completely
- [ ] Gather all available information
- [ ] Set up debugging environment
- [ ] Prepare tools and instrumentation

## Phase 1: Build Feedback Loop
- [ ] Choose appropriate debugging method
- [ ] Create reproducible test case
- [ ] Verify loop works consistently
- [ ] Document reproduction steps

## Phase 2: Reproduce
- [ ] Run the feedback loop
- [ ] Confirm bug matches description
- [ ] Capture exact symptoms
- [ ] Document environment details

## Phase 3: Hypothesise
- [ ] Generate 3-5 hypotheses
- [ ] Rank hypotheses by likelihood
- [ ] Get user input on rankings
- [ ] Plan hypothesis testing

## Phase 4: Instrument
- [ ] Add targeted logging
- [ ] Set breakpoints strategically
- [ ] Monitor key variables
- [ ] Track execution flow

## Phase 5: Fix + Test
- [ ] Write regression test first
- [ ] Verify test fails
- [ ] Implement fix
- [ ] Verify test passes
- [ ] Run full test suite

## Phase 6: Cleanup
- [ ] Remove debug instrumentation
- [ ] Update documentation
- [ ] Write post-mortem
- [ ] Share lessons learned
```

## References

- [references/testing-patterns.md](references/testing-patterns.md) — for writing regression tests
- [references/performance-profiling.md](references/performance-profiling.md) — performance analysis techniques
- [references/memory-debugging.md](references/memory-debugging.md) — memory leak detection
- [references/concurrency-debugging.md](references/concurrency-debugging.md) — threading and async issues
- [references/security-debugging.md](references/security-debugging.md) — security vulnerability debugging

---

**Version**: 2.0.0
**Status**: ULTRA-ADVANCED Diagnose Ready
**Features**: Systematic Debugging, Root Cause Analysis, Performance Profiling, Memory Detection, Knowledge Base

---

**Remember**: Debugging is a systematic process, not random guessing. Follow the methodology, build good feedback loops, and document everything you learn. The goal is not just to fix the bug, but to prevent similar bugs in the future.
