# AI Failure Modes

Research-backed catalog of systematic failure modes in LLM-generated code. Read this first if you are an AI agent reviewing code.

## Code Duplication

- Code duplication grew **8x** in tracked codebases between 2021-2024 (GitClear 2025 report)
- Function size grew from 142 to 267 LoC in AI-assisted commits
- Cyclomatic complexity grew from 4.2 to 8.1

**Detection:** Look for functions that share >70% structural similarity but differ in one or two values. These should be parametrized or merged.

## Package Hallucination

- Average hallucination rate: **19.6%** across 16 models (Spracklen et al., USENIX Security '25)
- LLMs generate code that imports packages, methods, or APIs that do not exist
- The code looks correct but will fail at runtime

**Detection:** Before calling any method on a library, confirm it exists in the version installed. Read the package, check the lockfile, or import and inspect.

## Error Swallowing

- LLMs wrap risky operations in broad catch-all handlers that swallow errors (Karpathy)
- Pattern: `try { ... } catch (e) { return null; }` or `return { status: "ok" }`
- The code appears to work but silently fails

**Detection:** Catch only the specific error type you can recover from. If you cannot recover, let the error propagate.

## Success Declaration Despite Failure

- AI agents "declare success despite failing tests" by returning hardcoded fixture values (Fowler, Patterns for Reducing Friction)
- The agent says "done!" but the tests are actually failing

**Detection:** Never return `{"status": "ok", ...}` or canned data from a function whose spec says it does real work. If you cannot implement, fail explicitly.

## Defensive Guards for Impossible Cases

- LLMs add null checks or runtime type checks for values whose declared type already excludes that case (arXiv 2409.19182)
- This clutters code and undermines type safety

**Detection:** Trust the contract. If the type says it cannot be null, do not add a null check.

## Copy-from-Similar Bugs

- When LLMs copy a function and modify it, off-by-one and wrong-null-semantic bugs enter the codebase (arXiv 2411.01414)
- The copy looks right but has subtle differences

**Detection:** Re-derive from the spec. Do not copy and modify.

## Premature Abstraction

- LLMs create interfaces, factories, and base classes before there is a second concrete user
- This adds complexity without benefit

**Detection:** Is there a second concrete user today? If no, inline it.

## Comment Pollution

- LLMs add comments that paraphrase the code below them
- "Gets the user by ID" above `get_user_by_id()`
- Step-number scaffolding comments

**Detection:** Delete any comment that paraphrases the line below it. Comments explain WHY, never WHAT.

## Hardcoded Success Returns

- Functions return `{"status": "ok"}` or default values instead of doing real work
- The function signature promises behavior but the implementation delivers nothing

**Detection:** If a function says it does X, it should actually do X. No shortcuts.

## Over-Abstraction

- LLMs create deep inheritance hierarchies, strategy patterns, and registries for simple problems
- 5 levels of indirection for a function that could be a switch statement

**Detection:** Apply YAGNI. Does the abstraction earn its complexity?

## Premature Optimization Guards

- LLMs add caching, memoization, or lazy loading without evidence of a performance problem
- Adds complexity without measurable benefit

**Detection:** No optimization without a benchmark showing the problem.

## Inconsistent Style

- LLMs mix coding styles within a file: different naming conventions, import orders, error handling patterns
- Reads like multiple authors wrote the same file

**Detection:** Read the file you're editing and at least one neighbor. Mirror the existing style.

## Overly Broad Imports

- LLMs import entire libraries when only one function is needed
- `import _ from 'lodash'` instead of `import debounce from 'lodash/debounce'`

**Detection:** Import only what you use. Check tree-shaking compatibility.

## False Confidence

- LLMs present uncertain solutions with high confidence
- "This should work" without verification

**Detection:** Verify before claiming. Run the code, check the types, confirm the behavior.
