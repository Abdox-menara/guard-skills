# Diagnose — References

## Feedback Loop Patterns

### 1. Failing Test (Best)
```python
def test_user_login_with_wrong_password():
    with pytest.raises(AuthenticationError):
        login("user@example.com", "wrongpassword")
```

### 2. Curl / HTTP Script
```bash
#!/bin/bash
# Reproduce the bug
curl -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"wrong"}' \
  | jq '.error' | grep -q "Invalid credentials"
```

### 3. CLI Invocation
```bash
#!/bin/bash
# Run with known input, diff against expected
python -m myapp.process input.json > actual.json
diff expected.json actual.json
```

### 4. Headless Browser
```typescript
import { test, expect } from '@playwright/test';

test('login form shows error on bad credentials', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'wrong');
  await page.click('#submit');
  await expect(page.locator('.error')).toBeVisible();
});
```

### 5. Property / Fuzz Loop
```python
import hypothesis
from hypothesis import given, strategies as st

@given(st.text(min_size=1))
def test_parse_never_crashes(input_string):
    # Should never raise, only return error or valid result
    result = parse(input_string)
    assert result is not None or result is None  # No crash
```

### 6. Differential Loop
```python
def test_regression():
    input_data = load_fixture("input.json")
    
    old_result = run_old_version(input_data)
    new_result = run_new_version(input_data)
    
    assert old_result == new_result, f"Regression: outputs differ"
```

## Hypothesis Format

Each hypothesis must be falsifiable:

```
If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse.
```

Examples:
- "If the bug is a race condition, then adding a sleep(1) before the assertion will make it disappear."
- "If the bug is in the parser, then using a different input format will not trigger it."
- "If the bug is a null reference, then adding a null check will make it disappear."

## Instrumentation Tags

Use unique prefixes for debug logs:
```
[DEBUG-a4f2] user_id=123, status=pending
[DEBUG-a4f2] calling payment_service.charge()
[DEBUG-a4f2] payment_service returned: success
```

Cleanup: `grep -r "\[DEBUG-a4f2\]"` → remove all matches.

## Performance Baseline

```python
import time

def benchmark(func, iterations=1000):
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    return elapsed / iterations
```

Measure before and after. Never optimize without a baseline.
