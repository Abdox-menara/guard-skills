---
name: test-guard
description: Review generated or changed test code against universal testing rules before it ships. Best used reactively after an agent writes, edits, generates, or refactors tests, before presenting, committing, or merging them.
---

# Test Guard

You are reviewing generated or changed test code before it ships. Enforce the rules below after the first test-writing pass and before the tests are presented, committed, or merged.

These rules exist because coding agents over-generate tests. The common failure modes: mock-heavy unit tests that assert implementation details, near-duplicate test bodies that differ by one value, and tests that re-verify the framework instead of the project's logic.

## When this skill activates

- A coding agent has just written new test functions or test files
- You are editing existing tests
- You are reviewing a diff that contains test changes
- The user asks you to write, add, or review tests

## Adapt to the project first

1. Check the project's own agent instructions and testing docs. Project-specific testing rules win.
2. Identify the test stack and apply the appropriate patterns:
   - Python / pytest → parametrize, fixtures, real instances
   - JavaScript / Jest / Vitest → test.each, module mocks, msw
   - PHP / PHPUnit / Pest → DataProvider, prophecy
   - Go → table-driven tests, subtests
3. Map the project's system boundaries: network, databases, filesystem, clock, third-party SDKs.

## The Nine Rules

### Rule 1: Test behavior, not implementation
Test what code does from the caller's perspective. Assert return values and observable side effects. Never assert that an internal helper was called with specific arguments — that test breaks on every refactor while catching nothing.

**Violation pattern:** asserting a mock of an internal function was called, where that function is not a system boundary.
**Fix:** assert the return value or the state change the caller observes.

### Rule 2: Every mock must be justified
Mock only at system boundaries: network/HTTP calls, databases, filesystem I/O on external files, clock and randomness, third-party SDKs. Never mock internal classes or helper functions.

When you mock a boundary, assert what the caller does with the response, not that the mock received specific arguments.

### Rule 3: One scenario per test, data-driven for variants
If two or more tests share identical setup and differ only in input/output values, merge them into one data-driven test.

**When separate tests ARE correct:** different setup, different assertions, different mock configurations, or genuinely different scenarios.

### Rule 4: Every test must justify its existence
Ask: "What bug does this catch that no other test catches?" Delete tests that only catch typos, verify default values of data classes, or test trivial pass-through logic.

### Rule 5: Name tests for the scenario
Pattern: `test_<scenario>_<expected_outcome>`. The name should read like a requirement, not echo the function signature.

| Bad | Good |
|-----|------|
| `test_parse_response_missing_field` | `test_malformed_response_falls_back_to_default` |
| `test_get_language_no_class` | `test_element_without_class_returns_empty_language` |

### Rule 6: Production regression tests are sacred
Tests that reproduce a real production bug are always justified. Reference the incident (date, issue ID, or short description) in the name or a comment, and never delete them. They are exempt from Rule 4.

### Rule 7: No tests for framework guarantees
Don't test that the validation library validates, the ORM commits, the router returns 404, or the test framework's fixtures work. Test YOUR logic that sits on top of the framework.

**Violation pattern:** a test that would still pass if you deleted all the project's custom code and kept only framework defaults.

### Rule 8: State and value objects are real, never mocked
Never mock a data model, DTO, entity, or state object. Construct a real instance. Mocking state hides field-name typos and validation errors — exactly the bugs worth catching.

### Rule 9: Infrastructure under test gets real infrastructure
When database queries, schema behavior, or persistence logic IS the subject of the test, run against a real test database with real migrations applied via fixtures. Mocking the session there tests nothing.

## Parametrized Test Examples

```python
# Python/pytest
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```

```javascript
// Jest/Vitest
test.each([
  ['hello', 'HELLO'],
  ['', ''],
  ['123', '123'],
])('converts %s to %s', (input, expected) => {
  expect(uppercase(input)).toBe(expected);
});
```

```go
// Go table-driven
func TestUppercase(t *testing.T) {
    tests := []struct {
        input    string
        expected string
    }{
        {"hello", "HELLO"},
        {"", ""},
        {"123", "123"},
    }
    for _, tt := range tests {
        t.Run(tt.input, func(t *testing.T) {
            if got := uppercase(tt.input); got != tt.expected {
                t.Errorf("uppercase(%q) = %q, want %q", tt.input, got, tt.expected)
            }
        })
    }
}
```

## Reporting Format

```
**Rule N violation** in `tests/path/file.ext::<test_name>`
- What: <one sentence describing the violation>
- Fix: <one sentence describing what to do instead>
```

Group violations by file. If a file has no violations, don't mention it.

## Severity Guide

- **Must fix:** Rules 1, 2, 8 — these hide real bugs or make tests brittle
- **Should fix:** Rules 3, 4, 5, 7 — these cause bloat and maintenance drag
- **Sacred:** Rule 6 — never delete, always allow
- **Worth noting:** Rule 9 — test architecture; flag it, but don't block small changes

## References

- [references/testing-patterns.md](references/testing-patterns.md) — universal testing patterns and examples
