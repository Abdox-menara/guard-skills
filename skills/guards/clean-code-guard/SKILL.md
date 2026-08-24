---
name: clean-code-guard
version: 2.0.0
author: Abdox
description: |
  ULTRA-ADVANCED Clean Code Guard with automated code analysis, security scanning,
  performance profiling, and intelligent fix suggestions for enterprise code quality.
  Use when the user wants to: review code, enforce standards, detect anti-patterns,
  optimize performance, ensure security, or any code quality workflow.

  CLEAN CODE: Comprehensive code review system that enforces best practices,
  detects anti-patterns, and ensures production-ready code quality.

  FEATURES:
  - Automated code analysis with 50+ rules
  - Security vulnerability scanning
  - Performance bottleneck detection
  - Intelligent fix suggestions
  - Code metrics and complexity analysis
  - Architecture pattern validation
  - Dependency analysis
  - Documentation quality checks

  TRIGGER PHRASES: "clean code", "code review", "code quality", "enforce standards",
  "detect anti-patterns", "optimize performance", "security scan", "best practices",
  "SOLID", "DRY", "KISS", "YAGNI", "code guard".

  TRAINED ON: Clean Code principles, SOLID, DRY, KISS, YAGNI, security best practices,
  performance optimization, architecture patterns, and enterprise code quality.

  ENVIRONMENT: Works with any programming language, framework, or codebase.

  SECURITY: Enterprise-grade security scanning with vulnerability detection.
---

# Clean Code Guard - ULTRA-ADVANCED v2.0

You are reviewing generated or changed code before it ships. Apply the rules below as a guard pass after the first implementation pass.

## How to use this skill

**Guard-pass mode** (recommended): after code has been generated, edited, refactored, or fixed, check the diff or target files against the imperatives below. Fix violations before presenting, committing, or merging.

**Review mode** (triggered when the user asks you to review, audit, or rate code): walk the rules against the target file(s) and produce a structured findings report. Do not edit code in review mode unless asked.

**Security mode** (triggered when the user asks for security scan): perform comprehensive security analysis including vulnerability detection, injection prevention, and data protection checks.

**Performance mode** (triggered when the user asks for performance analysis): identify bottlenecks, optimize algorithms, and suggest performance improvements.

## Adapt to the project first

1. Read the project's agent instructions (CLAUDE.md, AGENTS.md) and coding conventions. Project-specific rules win when they conflict.
2. Identify the language and framework, then read the matching reference for language-specific patterns.
3. Read the file you're editing and at least one neighbor before writing. Mirror the existing style.
4. Check for existing linting and formatting configurations (ESLint, Prettier, Black, etc.)
5. Review project dependencies for known vulnerabilities and deprecated packages.

## The Imperatives

### Functions and Names

1. **Names reveal intent.** Never use `data`, `result`, `item`, `temp`, `value`, `obj`, `info`, `helper`, `manager`, `utils`, or `handle_*`/`process_*`/`do_*` without a qualifier. A name must answer why it exists and what it does.

2. **Functions stay small.** Target ≤20 lines, one level of abstraction, one thing. If you can extract a function with a name that doesn't restate the body, the parent was doing more than one thing.

3. **Four arguments is the hard ceiling.** At five, introduce a request/config object. Never use boolean flag arguments — split into two functions instead.

4. **No output arguments.** A function either returns a value (query) or has a side effect (command). Never both.

5. **Function naming consistency.** Use consistent naming patterns: `get_*` for queries, `set_*` for setters, `is_*`/`has_*` for booleans, `create_*`/`make_*` for factories.

### Comments and Structure

6. **Comments explain WHY, never WHAT.** Delete any comment that paraphrases the line below it. Delete step-number scaffolding comments. Delete commented-out code — version control exists.

7. **Match the file's existing style.** Mirror the casing, import order, error handling, logging, and HTTP/DB client choices. Do not introduce a second pattern.

8. **Documentation requirements.** Public APIs must have docstrings. Complex algorithms must have explanatory comments. Business logic must be documented.

### SOLID

9. **One actor per module.** A class should be answerable to one stakeholder group. If two unrelated subsystems both reach into the same class, split it.

10. **Extension via new code, not edits.** If adding a new variant requires another type-tag branch in an existing function, refactor to a registry, strategy, or polymorphic dispatch first.

11. **No subclass refuses its parent's contract.** Never override a method to signal "not implemented" or "unsupported operation."

12. **Abstractions live with the client, not the implementation.** Put interfaces in the package that consumes them, not next to the concrete class.

13. **Dependency inversion.** High-level modules should not depend on low-level modules. Both should depend on abstractions.

14. **Interface segregation.** Clients should not be forced to depend on interfaces they do not use.

### DRY, KISS, YAGNI

15. **Delete duplicated knowledge, not duplicated text.** Two functions that look alike but encode different rules are not a DRY violation.

16. **The wrong abstraction is worse than duplication.** If an abstraction has accumulated branches for each caller's special case, re-inline it.

17. **Complexity ceiling: cyclomatic ≤10, nesting depth ≤5.** Refactor before exceeding.

18. **No speculative anything.** No optional parameter, config flag, feature toggle, interface, factory, or base class without a present-day caller.

### Security Guardrails

19. **Input validation.** Validate all external inputs. Never trust user data, API responses, or file contents.

20. **Output encoding.** Encode all outputs to prevent injection attacks. Use parameterized queries for database operations.

21. **Authentication and authorization.** Implement proper authentication and authorization checks. Never rely on client-side security.

22. **Data protection.** Encrypt sensitive data at rest and in transit. Never log passwords, tokens, or PII.

23. **Dependency security.** Check for known vulnerabilities in dependencies. Use lock files and regular updates.

24. **Error handling security.** Never expose internal errors to users. Log detailed errors for debugging.

### Performance Guardrails

25. **Algorithm complexity.** Choose appropriate data structures and algorithms. Avoid O(n²) when O(n log n) is possible.

26. **Memory management.** Avoid memory leaks. Release resources properly. Use connection pooling for databases.

27. **Caching strategies.** Implement caching for expensive operations. Use appropriate cache invalidation.

28. **Async operations.** Use asynchronous operations for I/O-bound tasks. Avoid blocking the main thread.

29. **Database optimization.** Use indexes appropriately. Avoid N+1 query problems. Use batch operations.

30. **Resource limits.** Set appropriate timeouts, rate limits, and resource constraints.

### AI-Specific Guardrails

31. **Never swallow errors with broad catch-all handling.** Catch only the specific error type you can recover from. Returning null/none/empty success from a catch handler is forbidden unless documented.

32. **No defensive guards for impossible cases.** Do not add null checks for values whose declared type already excludes null.

33. **Verify every import and external call.** Before calling a method on a library, confirm it exists in the version installed. Do not generate code based on what the API "should" look like.

34. **No hardcoded "success" returns.** Never return `{"status": "ok"}` or canned data from a function whose spec says it does real work.

35. **Re-derive, do not copy from similar.** When tempted to copy a function and modify it, stop. Re-derive from the spec.

36. **Strip dead code before delivery.** Remove unused imports, unused symbols, unreachable branches, and "just in case" exports.

37. **No magic numbers or strings.** Extract constants with meaningful names. Use enums for fixed sets of values.

38. **Proper error propagation.** Don't swallow errors. Propagate them with context for debugging.

## Code Analysis Engine

### Static Analysis
```python
class CodeAnalyzer:
    def __init__(self):
        self.rules = self._load_rules()
        self.violations = []

    def _load_rules(self):
        return {
            'naming': [
                self._check_function_naming,
                self._check_variable_naming,
                self._check_class_naming,
                self._check_constant_naming
            ],
            'complexity': [
                self._check_cyclomatic_complexity,
                self._check_nesting_depth,
                self._check_function_length,
                self._check_parameter_count
            ],
            'security': [
                self._check_sql_injection,
                self._check_xss_vulnerabilities,
                self._check_hardcoded_secrets,
                self._check_insecure_dependencies
            ],
            'performance': [
                self._check_algorithm_complexity,
                self._check_memory_leaks,
                self._check_n_plus_one_queries,
                self._check_blocking_operations
            ],
            'maintainability': [
                self._check_code_duplication,
                self._check_long_methods,
                self._check_god_classes,
                self._check_dead_code
            ]
        }

    def analyze_file(self, file_path, language):
        with open(file_path, 'r') as f:
            code = f.read()

        violations = []
        for category, rules in self.rules.items():
            for rule in rules:
                result = rule(code, language)
                if result:
                    violations.extend(result)

        return violations

    def _check_function_naming(self, code, language):
        violations = []
        # Check for descriptive function names
        patterns = {
            'python': r'def\s+([a-z_][a-z0-9_]*)\s*\(',
            'javascript': r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(',
            'java': r'(public|private|protected|static)\s+\w+\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\('
        }

        if language in patterns:
            import re
            matches = re.findall(patterns[language], code)
            for match in matches:
                if len(match) < 3:
                    violations.append({
                        'rule': 'naming',
                        'severity': 'warning',
                        'message': f'Function name too short: {match}',
                        'suggestion': 'Use descriptive names that explain purpose'
                    })

        return violations

    def _check_cyclomatic_complexity(self, code, language):
        violations = []
        import re

        # Count decision points
        decision_points = len(re.findall(r'\b(if|else if|elif|while|for|case|catch|&&|\|\|)\b', code))

        if decision_points > 10:
            violations.append({
                'rule': 'complexity',
                'severity': 'error',
                'message': f'High cyclomatic complexity: {decision_points}',
                'suggestion': 'Break down into smaller functions'
            })

        return violations

    def _check_sql_injection(self, code, language):
        violations = []
        import re

        # Check for string concatenation in SQL queries
        sql_patterns = [
            r'execute\s*\(\s*["\'].*\+',
            r'query\s*\(\s*["\'].*\+',
            r'WHERE.*\+.*['\"]',
            r'SELECT.*\+.*['\"]'
        ]

        for pattern in sql_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                violations.append({
                    'rule': 'security',
                    'severity': 'critical',
                    'message': 'Potential SQL injection vulnerability',
                    'suggestion': 'Use parameterized queries or prepared statements'
                })
                break

        return violations

    def _check_xss_vulnerabilities(self, code, language):
        violations = []
        import re

        # Check for unsafe HTML rendering
        xss_patterns = [
            r'innerHTML\s*=',
            r'document\.write\s*\(',
            r'v-html\s*=',
            r'ng-bind-html\s*=',
            r'\.html\s*\('
        ]

        for pattern in xss_patterns:
            if re.search(pattern, code):
                violations.append({
                    'rule': 'security',
                    'severity': 'critical',
                    'message': 'Potential XSS vulnerability',
                    'suggestion': 'Sanitize input and use safe rendering methods'
                })
                break

        return violations

    def _check_hardcoded_secrets(self, code, language):
        violations = []
        import re

        # Check for hardcoded credentials
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'["\']sk-[a-zA-Z0-9]{20,}["\']'
        ]

        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                violations.append({
                    'rule': 'security',
                    'severity': 'critical',
                    'message': 'Hardcoded secret or credential detected',
                    'suggestion': 'Use environment variables or secret management'
                })
                break

        return violations
```

### Code Metrics Calculator
```python
class CodeMetrics:
    def __init__(self):
        self.metrics = {}

    def calculate_metrics(self, code, language):
        metrics = {
            'lines_of_code': self._count_lines(code),
            'cyclomatic_complexity': self._calculate_cyclomatic_complexity(code),
            'nesting_depth': self._calculate_nesting_depth(code),
            'function_count': self._count_functions(code, language),
            'class_count': self._count_classes(code, language),
            'comment_ratio': self._calculate_comment_ratio(code),
            'duplicate_lines': self._detect_duplicates(code),
            'maintainability_index': 0
        }

        # Calculate maintainability index
        metrics['maintainability_index'] = self._calculate_maintainability_index(metrics)

        return metrics

    def _count_lines(self, code):
        lines = code.split('\n')
        return {
            'total': len(lines),
            'blank': sum(1 for line in lines if line.strip() == ''),
            'comment': sum(1 for line in lines if line.strip().startswith('#') or line.strip().startswith('//')),
            'code': sum(1 for line in lines if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('//'))
        }

    def _calculate_cyclomatic_complexity(self, code):
        import re
        decision_points = len(re.findall(r'\b(if|else if|elif|while|for|case|catch|&&|\|\|)\b', code))
        return decision_points + 1

    def _calculate_nesting_depth(self, code):
        max_depth = 0
        current_depth = 0

        for char in code:
            if char in '{[(':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in '}])':
                current_depth -= 1

        return max_depth

    def _count_functions(self, code, language):
        import re
        patterns = {
            'python': r'def\s+\w+\s*\(',
            'javascript': r'function\s+\w+\s*\(',
            'java': r'(public|private|protected|static)\s+\w+\s+\w+\s*\('
        }

        if language in patterns:
            return len(re.findall(patterns[language], code))
        return 0

    def _count_classes(self, code, language):
        import re
        patterns = {
            'python': r'class\s+\w+',
            'javascript': r'class\s+\w+',
            'java': r'(public|private|protected)\s+class\s+\w+'
        }

        if language in patterns:
            return len(re.findall(patterns[language], code))
        return 0

    def _calculate_comment_ratio(self, code):
        lines = code.split('\n')
        total_lines = len(lines)
        comment_lines = sum(1 for line in lines if line.strip().startswith('#') or line.strip().startswith('//'))

        return comment_lines / total_lines if total_lines > 0 else 0

    def _detect_duplicates(self, code):
        lines = code.split('\n')
        seen_lines = set()
        duplicate_lines = 0

        for line in lines:
            stripped = line.strip()
            if stripped and len(stripped) > 10:  # Ignore short lines
                if stripped in seen_lines:
                    duplicate_lines += 1
                else:
                    seen_lines.add(stripped)

        return duplicate_lines

    def _calculate_maintainability_index(self, metrics):
        # Simplified maintainability index calculation
        loc = metrics['lines_of_code']['code']
        cc = metrics['cyclomatic_complexity']
        comment_ratio = metrics['comment_ratio']

        # Lower is better for complexity, higher is better for comments
        mi = 171 - 5.2 * (cc ** 0.5) - 0.23 * loc + 16.2 * (comment_ratio * 100)

        return max(0, min(100, mi))  # Clamp between 0 and 100
```

### Security Scanner
```python
class SecurityScanner:
    def __init__(self):
        self.vulnerability_patterns = self._load_vulnerability_patterns()

    def _load_vulnerability_patterns(self):
        return {
            'sql_injection': {
                'patterns': [
                    r'execute\s*\(\s*["\'].*\+',
                    r'query\s*\(\s*["\'].*\+',
                    r'WHERE.*\+.*['\"]',
                    r'SELECT.*\+.*['\"]'
                ],
                'severity': 'critical',
                'description': 'SQL injection vulnerability',
                'fix': 'Use parameterized queries or prepared statements'
            },
            'xss': {
                'patterns': [
                    r'innerHTML\s*=',
                    r'document\.write\s*\(',
                    r'v-html\s*=',
                    r'ng-bind-html\s*=',
                    r'\.html\s*\('
                ],
                'severity': 'critical',
                'description': 'Cross-site scripting (XSS) vulnerability',
                'fix': 'Sanitize input and use safe rendering methods'
            },
            'hardcoded_secrets': {
                'patterns': [
                    r'password\s*=\s*["\'][^"\']+["\']',
                    r'api_key\s*=\s*["\'][^"\']+["\']',
                    r'secret\s*=\s*["\'][^"\']+["\']',
                    r'token\s*=\s*["\'][^"\']+["\']',
                    r'["\']sk-[a-zA-Z0-9]{20,}["\']'
                ],
                'severity': 'critical',
                'description': 'Hardcoded secret or credential',
                'fix': 'Use environment variables or secret management'
            },
            'path_traversal': {
                'patterns': [
                    r'open\s*\(\s*["\'].*\.\./',
                    r'readFile\s*\(\s*.*\.\./',
                    r'include\s*\(\s*.*\.\./',
                    r'require\s*\(\s*.*\.\./'
                ],
                'severity': 'high',
                'description': 'Path traversal vulnerability',
                'fix': 'Validate and sanitize file paths'
            },
            'command_injection': {
                'patterns': [
                    r'exec\s*\(\s*.*\+',
                    r'system\s*\(\s*.*\+',
                    r'eval\s*\(\s*.*\+',
                    r'os\.system\s*\(\s*.*\+'
                ],
                'severity': 'critical',
                'description': 'Command injection vulnerability',
                'fix': 'Use parameterized commands and input validation'
            },
            'insecure_deserialization': {
                'patterns': [
                    r'pickle\.loads\s*\(',
                    r'yaml\.load\s*\(',
                    r'eval\s*\(',
                    r'exec\s*\('
                ],
                'severity': 'high',
                'description': 'Insecure deserialization',
                'fix': 'Use safe deserialization methods'
            }
        }

    def scan_code(self, code, language):
        vulnerabilities = []

        for vuln_type, vuln_info in self.vulnerability_patterns.items():
            for pattern in vuln_info['patterns']:
                import re
                if re.search(pattern, code, re.IGNORECASE):
                    vulnerabilities.append({
                        'type': vuln_type,
                        'severity': vuln_info['severity'],
                        'description': vuln_info['description'],
                        'fix': vuln_info['fix'],
                        'pattern': pattern
                    })
                    break

        return vulnerabilities

    def scan_dependencies(self, dependencies):
        vulnerabilities = []

        # Check for known vulnerable packages
        vulnerable_packages = {
            'lodash': {'versions': ['< 4.17.21'], 'vulnerability': 'Prototype Pollution'},
            'express': {'versions': ['< 4.18.2'], 'vulnerability': 'Open Redirect'},
            'axios': {'versions': ['< 0.21.1'], 'vulnerability': 'SSRF'}
        }

        for dep in dependencies:
            if dep['name'] in vulnerable_packages:
                vuln_info = vulnerable_packages[dep['name']]
                vulnerabilities.append({
                    'package': dep['name'],
                    'version': dep['version'],
                    'vulnerability': vuln_info['vulnerability'],
                    'fix': f"Update to latest version"
                })

        return vulnerabilities
```

### Performance Profiler
```python
class PerformanceProfiler:
    def __init__(self):
        self.bottleneck_patterns = self._load_bottleneck_patterns()

    def _load_bottleneck_patterns(self):
        return {
            'n_plus_one_queries': {
                'patterns': [
                    r'for.*in.*:.*\.query\(',
                    r'for.*in.*:.*\.find\(',
                    r'for.*in.*:.*\.select\('
                ],
                'description': 'N+1 query problem',
                'fix': 'Use eager loading or batch queries'
            },
            'blocking_io': {
                'patterns': [
                    r'time\.sleep\(',
                    r'\.wait\(',
                    r'\.join\(',
                    r'requests\.get\(',
                    r'urlopen\('
                ],
                'description': 'Blocking I/O operation',
                'fix': 'Use async/await or non-blocking operations'
            },
            'inefficient_loops': {
                'patterns': [
                    r'for.*in.*range\(len\(',
                    r'for.*in.*\.keys\(\)',
                    r'while.*True'
                ],
                'description': 'Inefficient loop pattern',
                'fix': 'Use enumerate(), .items(), or optimize loop logic'
            },
            'memory_leaks': {
                'patterns': [
                    r'global\s+\w+\s*=',
                    r'self\.\w+\s*=\s*\[\]',
                    r'append\(.*\)$'
                ],
                'description': 'Potential memory leak',
                'fix': 'Use proper cleanup and context managers'
            }
        }

    def profile_code(self, code, language):
        bottlenecks = []

        for bottleneck_type, bottleneck_info in self.bottleneck_patterns.items():
            for pattern in bottleneck_info['patterns']:
                import re
                if re.search(pattern, code, re.MULTILINE):
                    bottlenecks.append({
                        'type': bottleneck_type,
                        'description': bottleneck_info['description'],
                        'fix': bottleneck_info['fix'],
                        'pattern': pattern
                    })
                    break

        return bottlenecks

    def estimate_complexity(self, code):
        import re

        # Estimate time complexity
        complexity = 'O(1)'

        if re.search(r'for.*for', code):
            complexity = 'O(n²)'
        elif re.search(r'for.*while', code) or re.search(r'while.*for', code):
            complexity = 'O(n²)'
        elif re.search(r'for', code):
            complexity = 'O(n)'
        elif re.search(r'while', code):
            complexity = 'O(n)'

        return complexity
```

## Self-Check Before Delivery

1. Walk imperatives 1–38 against your diff. Fix every violation.
2. For new functions: lines ≤ 20? params ≤ 4? complexity ≤ 10? names reveal intent?
3. For new comments: does this explain WHY? If it explains WHAT, delete it.
4. For new error handling: is the caught error type specific? Does the handler do something other than silently return?
5. For new abstractions: is there a second concrete user today? If no, inline it.
6. Did you read the file you edited and at least one neighbor? Did your style match?
7. Is there any hardcoded "ok" return or fixture data? Replace with real implementation.
8. Run security scan: any SQL injection, XSS, hardcoded secrets, or command injection?
9. Run performance profiler: any N+1 queries, blocking I/O, or memory leaks?
10. Calculate metrics: cyclomatic complexity ≤ 10? Nesting depth ≤ 5? Maintainability index > 20?

## Reporting Format (Review Mode)

```
**Rule N violation** in `path/to/file.ext:line`
- What: <description>
- Fix: <what to do instead>
- Severity: <critical|high|medium|low>
- Category: <security|performance|maintainability|style>
```

Group violations by file. Lead with security findings (Rules 19-24), then performance (Rules 25-30), then AI-specific (Rules 31-38), then SOLID/DRY, then style.

## Severity Guide

- **Critical:** Security vulnerabilities (Rules 19-24) — immediate fix required
- **Must fix:** AI-specific guardrails (Rules 31-38) — these hide real bugs
- **Should fix:** Rules 1-18 — these cause maintenance drag
- **Worth noting:** Style inconsistencies and minor optimizations

## Code Quality Report Template

```markdown
# Code Quality Report

## Summary
- Total violations: X
- Critical: X
- High: X
- Medium: X
- Low: X

## Security Findings
[List security vulnerabilities]

## Performance Findings
[List performance bottlenecks]

## Maintainability Findings
[List maintainability issues]

## Metrics
- Cyclomatic Complexity: X
- Nesting Depth: X
- Maintainability Index: X/100
- Comment Ratio: X%

## Recommendations
[Prioritized list of improvements]
```

## References

- [references/ai-failure-modes.md](references/ai-failure-modes.md) — the systematic ways LLMs produce bad code
- [references/solid-principles.md](references/solid-principles.md) — SOLID with detection smells
- [references/testing-patterns.md](references/testing-patterns.md) — universal testing patterns
- [references/security-best-practices.md](references/security-best-practices.md) — security guidelines
- [references/performance-optimization.md](references/performance-optimization.md) — performance tips

---

**Version**: 2.0.0
**Status**: ULTRA-ADVANCED Clean Code Guard Ready
**Features**: Automated Analysis, Security Scanning, Performance Profiling, Code Metrics, Intelligent Fixes

---

**Remember**: Clean code is not just about following rules. It's about writing code that is readable, maintainable, secure, and performant. The goal is to deliver production-ready code that stands the test of time.

## See Also

- [clean-arch-guard](../clean-arch-guard/SKILL.md)
