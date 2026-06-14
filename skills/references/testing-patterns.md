# Testing Patterns

Universal testing patterns and anti-patterns for AI-generated tests.

## Core Principle

Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

## Good Tests

- Exercise real code paths through public APIs
- Describe WHAT the system does, not HOW it does it
- Read like a specification: "user can checkout with valid cart"
- Survive refactors because they don't care about internal structure
- One scenario per test, data-driven for variants

## Bad Tests

- Mock internal collaborators
- Test private methods
- Verify through external means (querying DB directly instead of using the interface)
- Break when you refactor, but behavior hasn't changed
- Share identical setup and differ only in input/output values (should be parametrized)

## The Nine Rules

### 1. Test behavior, not implementation
Assert return values and observable side effects. Never assert that an internal helper was called with specific arguments.

### 2. Every mock must be justified
Mock only at system boundaries: network, databases, filesystem I/O, clock, third-party SDKs. Never mock internal classes.

### 3. One scenario per test, data-driven for variants
If two tests share setup and differ only in values, merge into one data-driven test (`@pytest.mark.parametrize`, `test.each`, `#[DataProvider]`).

### 4. Every test must justify its existence
Ask: "What bug does this catch that no other test catches?" Delete tests that only catch typos or verify trivial defaults.

### 5. Name tests for the scenario
Pattern: `test_<scenario>_<expected_outcome>`. The name should read like a requirement.

### 6. Production regression tests are sacred
Tests that reproduce a real production bug are always justified. Reference the incident in the name or comment. Never delete them.

### 7. No tests for framework guarantees
Don't test that the validation library validates, the ORM commits, or the router returns 404. Test YOUR logic.

### 8. State and value objects are real, never mocked
Never mock a data model, DTO, or entity. Construct a real instance. Mocking state hides field-name typos.

### 9. Infrastructure under test gets real infrastructure
When database queries ARE the subject of the test, run against a real test database with real migrations.

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
describe('uppercase', () => {
  test.each([
    ['hello', 'HELLO'],
    ['', ''],
    ['123', '123'],
  ])('converts %s to %s', (input, expected) => {
    expect(uppercase(input)).toBe(expected);
  });
});
```

```php
// PHPUnit with DataProvider
/**
 * @dataProvider uppercaseProvider
 */
public function testUppercase(string $input, string $expected): void
{
    $this->assertSame($expected, uppercase($input));
}

public static function uppercaseProvider(): array
{
    return [
        'normal' => ['hello', 'HELLO'],
        'empty' => ['', ''],
        'numbers' => ['123', '123'],
    ];
}
```
