# Test Guard — References

## Language-Specific Patterns

### Python (pytest)

**Parametrize:**
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```

**Fixtures (real objects, not mocks):**
```python
@pytest.fixture
def sample_user():
    return User(
        id=1,
        email="test@example.com",
        name="Test User"
    )

def test_user_display_name(sample_user):
    assert sample_user.display_name == "Test User (test@example.com)"
```

**Mock only at boundaries:**
```python
# GOOD: mocking external HTTP call
@patch('requests.get')
def test_fetch_weather(mock_get):
    mock_get.return_value.json.return_value = {"temp": 72}
    result = get_weather("NYC")
    assert result.temperature == 72

# BAD: mocking internal helper
@patch('myapp.utils._format_date')  # Never do this
def test_format_user(mock_format):
    ...
```

### JavaScript/TypeScript (Jest/Vitest)

**test.each:**
```typescript
test.each([
  ['hello', 'HELLO'],
  ['', ''],
  ['123', '123'],
])('converts %s to %s', (input, expected) => {
  expect(uppercase(input)).toBe(expected);
});
```

**MSW for API mocking (boundary only):**
```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/users/:id', () => {
    return HttpResponse.json({ id: 1, name: 'Test' });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

**Real objects, not mocks:**
```typescript
// GOOD: real object
const user = { id: 1, name: 'Test', email: 'test@example.com' };
expect(user.displayName).toBe('Test (test@example.com)');

// BAD: mock object
const mockUser = { displayName: jest.fn() }; // Hides field typos
```

### Go

**Table-driven tests:**
```go
func TestUppercase(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected string
    }{
        {"normal", "hello", "HELLO"},
        {"empty", "", ""},
        {"numbers", "123", "123"},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := uppercase(tt.input); got != tt.expected {
                t.Errorf("uppercase(%q) = %q, want %q", tt.input, got, tt.expected)
            }
        })
    }
}
```

**Real database for integration tests:**
```go
func TestCreateUser(t *testing.T) {
    db := setupTestDB(t) // real test database
    defer db.Close()

    user, err := CreateUser(db, "test@example.com")
    require.NoError(t, err)
    assert.NotZero(t, user.ID)
}
```

### PHP (PHPUnit/Pest)

**DataProvider:**
```php
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

**Real objects over mocks:**
```php
// GOOD: real entity
$user = new User();
$user->setEmail('test@example.com');
$this->assertSame('test@example.com', $user->getEmail());

// BAD: mock entity
$mockUser = $this->createMock(User::class); // Hides field typos
```

## When Separate Tests ARE Correct

| Scenario | Reason |
|----------|--------|
| Different setup | Each test needs different initial state |
| Different assertions | Testing different outcomes |
| Different mock configs | Boundary mocked differently |
| Genuinely different scenarios | Not just input variation |

## Common Anti-Patterns to Flag

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| `MagicMock()` for state objects | Hides field-name typos | Construct real instance |
| Duplicated test bodies | Maintenance drag | Parametrize |
| `assert_called_with()` on internals | Breaks on refactor | Assert return value |
| Testing framework defaults | Tests nothing | Delete or test custom logic |
| Log message assertions | Brittle, tests nothing | Assert behavior instead |
| Constructor setting attributes | Tests trivial code | Delete |
| `test_function_name()` naming | Doesn't describe scenario | `test_<scenario>_<expected>` |
