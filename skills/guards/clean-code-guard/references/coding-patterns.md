# Clean Code Guard — References

## Naming and Functions

### Names Reveal Intent

| Bad Name | Good Name |
|----------|-----------|
| `data` | `userProfile` |
| `result` | `sortedTransactions` |
| `temp` | `temporaryBuffer` |
| `process()` | `validateAndSaveOrder()` |
| `handle()` | `authenticateRequest()` |
| `utils` | `dateFormatters` |
| `manager` | `connectionPool` |

### Function Size

- Target: ≤20 lines per function
- One level of abstraction per function
- One thing per function
- If you can extract a function with a name that doesn't restate the body, the parent was doing more than one thing

### Parameters

- Maximum: 4 arguments
- At 5+: introduce a request/config object (record, struct, DTO)
- Never use boolean flag arguments — split into two functions
- No output parameters — functions either return a value or have a side effect

## Comments and Formatting

### When to Comment
- WHY the code exists (business context, non-obvious decision)
- TODO with a clear action and owner
- Warning about non-obvious side effects
- Public API contracts (units, ranges, error conditions)

### When to Delete
- Comments that paraphrase the line below
- Step-number scaffolding ("Step 1:", "Step 2:")
- Commented-out code (version control exists)
- "Author: ..." metadata (git blame exists)
- Obvious comments ("// constructor")

### Match Existing Style
- Read the file you're editing and at least one neighbor
- Mirror: casing, import order, error handling, logging, HTTP/DB client choices
- Do not introduce a second pattern

## SOLID Detection Smells

### SRP Violation
- Class has methods that modify data AND methods that format/report on it
- Class is imported by unrelated subsystems
- Changes to one feature break another feature's tests

### OCP Violation
- Adding a new case to a switch/if-else chain
- "if type == X then ... else if type == Y then ..."
- Adding a new variant requires editing existing code

### LSP Violation
- Subclass throws `NotImplementedError`
- Subclass overrides a method to do nothing
- Subclass strengthens preconditions (more restrictive inputs)

### ISP Violation
- Class implements interface but throws for half the methods
- Client depends on methods it never calls

### DIP Violation
- High-level module directly imports low-level module
- Business logic depends on database library directly

## DRY/KISS/YAGNI Detection

### DRY Violations
- Two functions that encode the same rule in different places
- One rule expressed in code + docs + schema
- Similar error messages/handling in multiple places

### KISS Violations
- Indirection that doesn't earn its complexity
- Abstract base classes with one implementation
- Factory patterns for objects with no variants

### YAGNI Violations
- `enable_*` or `use_*_v2` config flags
- Interface with one implementation
- Base class with one subclass
- Feature toggles without a removal date

## Complexity Limits

| Metric | Limit | Action |
|--------|-------|--------|
| Cyclomatic complexity | ≤10 | Refactor into smaller functions |
| Nesting depth | ≤5 | Extract early returns, use guard clauses |
| Function length | ≤20 lines | Extract helper functions |
| Parameter count | ≤4 | Use config object |
