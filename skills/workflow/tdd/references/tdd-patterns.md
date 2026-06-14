# TDD — References

## Deep Modules

> "The best modules are deep. They allow a lot of functionality to be accessed through a simple interface."
> — John Ousterhout, *A Philosophy of Software Design*

A deep module has:
- **Simple interface**: few methods, easy to understand
- **Deep implementation**: significant functionality hidden behind the interface

Example: A `Database` class with a simple `query(sql)` interface that handles connection pooling, retries, transaction management, and caching internally.

### Why This Matters for TDD

Deep modules are easier to test because:
- Fewer public methods = fewer test surfaces
- More functionality per method = more meaningful assertions
- Internal complexity is hidden = tests focus on behavior

## Interface Design for Testability

### Good Interfaces (Easy to Test)
```python
# Pure function — trivial to test
def calculate_total(items: list[Item]) -> Decimal:
    ...

# Single responsibility — one thing to test
def send_notification(user: User, message: str) -> None:
    ...
```

### Bad Interfaces (Hard to Test)
```python
# Too many responsibilities — what do you even test?
def process_order(order, user, inventory, notification_service, logger):
    ...

# Side effects everywhere — test setup is complex
def create_and_save_and_send_and_log(data):
    ...
```

## Refactoring Checklist

After all tests pass, look for:

- [ ] **Extract duplication** — same code in multiple places
- [ ] **Deepen modules** — move complexity behind simple interfaces
- [ ] **SOLID principles** — where natural, not forced
- [ ] **Rename for clarity** — names should reveal intent
- [ ] **Remove dead code** — if nothing calls it, delete it
- [ ] **Simplify conditionals** — guard clauses, early returns

**Never refactor while RED.** Get to GREEN first.

## Common TDD Mistakes

| Mistake | Why It's Bad | Fix |
|---|---|---|
| Writing all tests first | Tests imagined, not actual behavior | One test at a time |
| Testing implementation details | Tests break on refactor | Test public interface only |
| Mocking everything | Tests verify mocks, not code | Mock only boundaries |
| Skipping the refactor phase | Code stays messy | Always refactor after GREEN |
| Testing framework behavior | Tests nothing useful | Test YOUR logic |
