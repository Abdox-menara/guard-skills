# Docs Guard — References

## Verification Procedure

### Step 1: Extract Claims

Read the documentation and list every factual claim:
- Function/method names
- Class names
- CLI commands and flags
- API endpoints
- Configuration keys
- Environment variables
- File paths
- Code samples
- Performance numbers
- Version compatibility claims

### Step 2: Verify Each Claim

For each claim, verify against the actual source:

| Claim Type | How to Verify |
|---|---|
| Function exists | Read the source file, check the function is defined |
| Signature matches | Compare params, return type, defaults |
| CLI flag exists | Run `--help` or read the CLI source |
| API endpoint exists | Check route definitions |
| Config key exists | Check config schema/defaults |
| Code sample runs | Run it in isolation (or verify imports + API) |
| Performance number | Find the benchmark or remove the claim |
| Version compatibility | Check the CI matrix or changelog |

### Step 3: Report Findings

For each violation:
- What the docs claim
- What the code actually has (with file:line)
- What to fix

## Code Sample Rules

### Runnability
- All imports resolve
- APIs exist with documented signatures
- No hardcoded local paths
- No real credentials
- No implicit prior state

### Realistic Data
- Use realistic example data, not "foo", "bar", "test123"
- Show the actual types the function expects
- Include edge cases in examples

### Error Paths
- Show what happens when things go wrong
- Document the error types raised
- Show the caller what to do about errors

### Secrets Hygiene
- Never use real API keys, even in examples
- Use placeholders: `YOUR_API_KEY`, `your-project-id`
- Warn when examples need credentials

## Docstring Rules

### When a Docstring Is Justified
- Public API functions (exported, documented)
- Non-obvious behavior (side effects, threading guarantees)
- Complex algorithms (explain the approach)
- Error conditions (what can go wrong)

### When a Docstring Is NOT Justified
- Private functions (the code is right there)
- Obvious getters/setters
- Functions whose name says everything
- Implementation that speaks for itself

### What a Docstring Must Contain
- Units of measurement (ms, bytes, count)
- Range constraints (0-100, positive only)
- Error conditions (throws on invalid input)
- Side effects (modifies DB, sends email)
- Threading guarantees (thread-safe, not thread-safe)

## Review Checklist

For review mode, walk through these checks:

1. **Accuracy** (must fix)
   - [ ] Every referenced symbol exists in the source
   - [ ] Every code sample runs on a clean machine
   - [ ] Documented behavior matches actual behavior
   - [ ] No unverifiable claims without sources

2. **Versioning** (should fix)
   - [ ] Features state their introduction version
   - [ ] Prerequisites are pinned or ranged
   - [ ] Deprecated items have replacements noted

3. **Substance** (should fix)
   - [ ] No filler or slop
   - [ ] No paraphrased upstream docs
   - [ ] Error paths documented

4. **Structure** (worth noting)
   - [ ] Headings match content
   - [ ] Internal links resolve
   - [ ] No TODO stubs in published docs

## Common Violation Patterns

| Pattern | Example | Fix |
|---|---|---|
| Hallucinated function | `auth.validate(token)` when method is `auth.verify(token)` | Check source, fix name |
| Wrong signature | `fetch(url, options)` when it's `fetch(url, init)` | Check source, fix params |
| Stale docs | Docs say "supports X" but X was removed | Grep for old references |
| Missing error docs | No mention that function throws on invalid input | Add error conditions |
| Marketing in docs | "blazingly fast" with no benchmark | Remove or add benchmark |
| Paraphrase of signature | "Gets user by ID" above `getUserById()` | Delete docstring |
