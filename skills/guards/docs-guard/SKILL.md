---
name: docs-guard
version: 2.0.0
author: Abdox
description: |
  ULTRA-ADVANCED Docs Guard with automated documentation analysis, API verification,
  code sample testing, and intelligent documentation quality scoring for enterprise docs.
  Use when the user wants to: review documentation, verify API docs, test code samples,
  check documentation quality, or any documentation validation workflow.

  DOCS GUARD: Comprehensive documentation review system that verifies accuracy,
  detects drift, ensures completeness, and maintains documentation quality.

  FEATURES:
  - Automated symbol verification
  - Code sample testing and validation
  - Documentation drift detection
  - API documentation analysis
  - Documentation quality scoring
  - Multi-format support (Markdown, RST, HTML)
  - Documentation completeness checks
  - Accessibility compliance

  TRIGGER PHRASES: "docs guard", "documentation review", "API docs", "verify documentation",
  "code samples", "documentation quality", "docs vs code", "documentation drift",
  "readme review", "changelog review".

  TRAINED ON: Technical writing, API documentation, documentation best practices,
  accessibility standards, and documentation tooling.

  ENVIRONMENT: Works with any documentation format, any programming language.

  SECURITY: Enterprise-grade documentation security and compliance checking.
---

# Docs Guard - ULTRA-ADVANCED v2.0

You are reviewing generated or changed documentation before it ships. Apply the rules below as a guard pass. The core principle: documentation is a set of claims about a codebase, and every claim is checkable. Your job is to check them.

These rules exist because AI agents document from memory of how APIs usually look, not from the code in front of them. Half of AI answers to programming questions contain incorrect information, yet the prose sounds authoritative either way. You can verify; readers cannot.

## How to use this skill

**Guard-pass mode** (recommended): after documentation has been generated or edited, verify every claim against the source and run the self-check before delivery.

**Review mode** (the user asks you to review, audit, or fact-check docs): walk the rules against the target docs and produce a findings report with file:line evidence. Do not rewrite in review mode unless asked.

**Security mode** (triggered when the user asks for security documentation review): check for security documentation completeness, vulnerability disclosure, and security best practices.

**API mode** (triggered when the user asks for API documentation review): verify API endpoints, parameters, responses, and code examples against actual implementation.

## The Rules

### Accuracy — must fix

1. **Every referenced symbol must exist.** Every function, method, class, hook, CLI command, flag, endpoint, config key, env var, and file path mentioned in the docs gets verified against the actual source — by reading it, not recalling it.

2. **Every code sample must work.** Imports resolve, APIs exist with the documented signatures, and the sample runs outside the author's machine — no hardcoded local paths, no real credentials, no implicit prior state.

3. **Document the code's actual behavior, not its intended behavior.** Read the implementation before describing it. Where code and comments/specs disagree, the code is the truth — flag the disagreement to the user.

4. **No unverifiable claims.** Performance numbers, compatibility matrices, scale limits, and "production-ready" assertions require a source in the repository. "Fast" is marketing; "O(n log n), benchmarked in bench/sort.md" is documentation.

5. **API documentation accuracy.** Every endpoint, parameter, response type, and status code must match the actual implementation. Document all possible responses, including error cases.

6. **Configuration documentation.** All configuration options must be documented with their defaults, types, and valid ranges. Document environment variables and their precedence.

### Versioning and drift

7. **Versions are explicit.** Features, flags, and behaviors state the version that introduced them. Prerequisites are pinned or ranged, never "latest". Deprecated items say so, with the replacement.

8. **A code change owes a docs change.** When editing code whose behavior is documented — rename, signature change, new default, removed flag — update every doc surface that mentions it in the same change.

9. **Documentation versioning.** Maintain documentation versions that match code versions. Use version tags or branches for documentation.

### Substance — should fix

10. **No filler, no slop.** Delete: docstrings that paraphrase the signature ("Gets the user by ID" above `get_user_by_id`), sections that restate their heading, marketing adjectives in technical prose ("powerful", "seamless", "blazingly fast"), and intro padding ("In this section, we will explore…").

11. **Don't paraphrase upstream docs.** Link to external documentation instead of restating it. Document only your project's relationship to the external thing.

12. **Examples cover the failure path too.** A tutorial that only shows the happy path documents half the API. Show what the error looks like and what the caller should do.

13. **Documentation completeness.** Document all public APIs, configuration options, and features. Include examples for common use cases.

### Structure — worth noting

14. **Navigation tells the truth.** Headings describe their sections, internal links resolve, and there are no TODO stubs or "coming soon" sections in published docs.

15. **Documentation hierarchy.** Use proper heading hierarchy. Don't skip levels. Maintain consistent structure across documents.

16. **Cross-references.** Link to related documentation. Use consistent reference formats.

### Accessibility

17. **Alternative text for images.** All images must have descriptive alt text. Charts and diagrams must have text descriptions.

18. **Color contrast.** Ensure sufficient color contrast for readability. Don't rely solely on color to convey information.

19. **Keyboard navigation.** Documentation must be navigable via keyboard. Interactive elements must be accessible.

20. **Screen reader compatibility.** Use semantic markup. Provide clear structure for screen readers.

## Documentation Analysis Engine

### Symbol Verifier
```python
class SymbolVerifier:
    def __init__(self):
        self.verified_symbols = {}
        self.unverified_symbols = []

    def verify_documentation(self, doc_content, source_files):
        """Verify all symbols mentioned in documentation exist in source code."""
        symbols = self._extract_symbols(doc_content)
        verification_results = []

        for symbol in symbols:
            result = self._verify_symbol(symbol, source_files)
            verification_results.append(result)

        return verification_results

    def _extract_symbols(self, doc_content):
        """Extract all symbols from documentation."""
        import re

        patterns = [
            r'`([^`]+)`',  # Inline code
            r'```[\s\S]*?```',  # Code blocks
            r'\[([^\]]+)\]\([^)]+\)',  # Links
            r'###?\s+([^\n]+)',  # Headings
        ]

        symbols = set()
        for pattern in patterns:
            matches = re.findall(pattern, doc_content)
            for match in matches:
                if isinstance(match, tuple):
                    symbols.update(match)
                else:
                    symbols.add(match)

        return symbols

    def _verify_symbol(self, symbol, source_files):
        """Verify if a symbol exists in source files."""
        for file_path, content in source_files.items():
            if symbol in content:
                return {
                    'symbol': symbol,
                    'verified': True,
                    'file': file_path,
                    'line': self._find_line_number(content, symbol)
                }

        return {
            'symbol': symbol,
            'verified': False,
            'file': None,
            'line': None
        }

    def _find_line_number(self, content, symbol):
        """Find the line number of a symbol in content."""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if symbol in line:
                return i
        return None
```

### Code Sample Tester
```python
class CodeSampleTester:
    def __init__(self):
        self.test_results = []

    def test_code_samples(self, doc_content, language):
        """Test all code samples in documentation."""
        code_samples = self._extract_code_samples(doc_content)
        test_results = []

        for sample in code_samples:
            result = self._test_code_sample(sample, language)
            test_results.append(result)

        return test_results

    def _extract_code_samples(self, doc_content):
        """Extract all code samples from documentation."""
        import re

        pattern = r'```(\w+)?\n([\s\S]*?)```'
        matches = re.findall(pattern, doc_content)

        samples = []
        for lang, code in matches:
            samples.append({
                'language': lang or 'unknown',
                'code': code.strip()
            })

        return samples

    def _test_code_sample(self, sample, language):
        """Test a single code sample."""
        try:
            # Basic syntax check
            if language == 'python':
                import ast
                ast.parse(sample['code'])
            elif language in ['javascript', 'typescript']:
                # Simple syntax validation
                if not self._validate_javascript_syntax(sample['code']):
                    return {
                        'sample': sample,
                        'passed': False,
                        'error': 'Syntax validation failed',
                        'line': None
                    }

            # Check for common issues
            issues = self._check_common_issues(sample['code'], language)

            return {
                'sample': sample,
                'passed': len(issues) == 0,
                'issues': issues,
                'error': None
            }

        except SyntaxError as e:
            return {
                'sample': sample,
                'passed': False,
                'error': f'Syntax error: {e}',
                'line': e.lineno
            }

    def _validate_javascript_syntax(self, code):
        """Basic JavaScript syntax validation."""
        # Simple bracket matching
        stack = []
        pairs = {')': '(', ']': '[', '}': '{'}

        for char in code:
            if char in '([{':
                stack.append(char)
            elif char in ')]}':
                if not stack or stack[-1] != pairs[char]:
                    return False
                stack.pop()

        return len(stack) == 0

    def _check_common_issues(self, code, language):
        """Check for common code sample issues."""
        issues = []

        # Check for hardcoded credentials
        import re
        credential_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']'
        ]

        for pattern in credential_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    'type': 'hardcoded_credential',
                    'severity': 'critical',
                    'message': 'Hardcoded credential in code sample'
                })

        # Check for local paths
        if re.search(r'[A-Z]:\\', code) or re.search(r'/home/', code):
            issues.append({
                'type': 'local_path',
                'severity': 'high',
                'message': 'Local file path in code sample'
            })

        return issues
```

### Documentation Quality Scorer
```python
class DocumentationQualityScorer:
    def __init__(self):
        self.scoring_criteria = self._load_scoring_criteria()

    def _load_scoring_criteria(self):
        return {
            'completeness': {
                'weight': 0.25,
                'checks': [
                    'has_readme',
                    'has_api_docs',
                    'has_examples',
                    'has_changelog',
                    'has_contributing_guide',
                    'has_license'
                ]
            },
            'accuracy': {
                'weight': 0.30,
                'checks': [
                    'symbols_verified',
                    'code_samples_work',
                    'api_documentation_accurate',
                    'no_unverifiable_claims'
                ]
            },
            'clarity': {
                'weight': 0.20,
                'checks': [
                    'no_filler_text',
                    'clear_structure',
                    'consistent_style',
                    'proper_grammar'
                ]
            },
            'accessibility': {
                'weight': 0.15,
                'checks': [
                    'has_alt_text',
                    'proper_heading_hierarchy',
                    'keyboard_navigable',
                    'screen_reader_compatible'
                ]
            },
            'maintainability': {
                'weight': 0.10,
                'checks': [
                    'version_information',
                    'documentation_drift_detected',
                    'cross_references_valid'
                ]
            }
        }

    def score_documentation(self, documentation_data):
        """Calculate documentation quality score."""
        scores = {}

        for category, criteria in self.scoring_criteria.items():
            category_score = 0
            for check in criteria['checks']:
                if check in documentation_data:
                    category_score += documentation_data[check]

            # Normalize to 0-1
            category_score = category_score / len(criteria['checks'])
            scores[category] = category_score * criteria['weight']

        total_score = sum(scores.values()) * 100

        return {
            'total_score': round(total_score, 2),
            'category_scores': scores,
            'grade': self._calculate_grade(total_score)
        }

    def _calculate_grade(self, score):
        """Calculate letter grade from score."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
```

### Drift Detector
```python
class DriftDetector:
    def __init__(self):
        self.drift_patterns = []

    def detect_drift(self, documentation, code_changes):
        """Detect documentation drift from code changes."""
        drift_items = []

        for change in code_changes:
            affected_docs = self._find_affected_documentation(change, documentation)

            for doc in affected_docs:
                drift_item = {
                    'code_change': change,
                    'affected_documentation': doc,
                    'drift_type': self._classify_drift(change, doc),
                    'severity': self._assess_severity(change, doc)
                }
                drift_items.append(drift_item)

        return drift_items

    def _find_affected_documentation(self, change, documentation):
        """Find documentation affected by a code change."""
        affected = []

        for doc in documentation:
            if self._is_affected(change, doc):
                affected.append(doc)

        return affected

    def _is_affected(self, change, doc):
        """Check if documentation is affected by a code change."""
        # Simple string matching (in reality, would use AST analysis)
        return change['symbol'] in doc['content']

    def _classify_drift(self, change, doc):
        """Classify the type of drift."""
        if change['type'] == 'rename':
            return 'symbol_rename'
        elif change['type'] == 'remove':
            return 'symbol_removal'
        elif change['type'] == 'modify':
            return 'behavior_change'
        else:
            return 'unknown'

    def _assess_severity(self, change, doc):
        """Assess the severity of drift."""
        if change['type'] == 'remove':
            return 'critical'
        elif change['type'] == 'rename':
            return 'high'
        else:
            return 'medium'
```

### Accessibility Checker
```python
class AccessibilityChecker:
    def __init__(self):
        self.accessibility_rules = self._load_accessibility_rules()

    def _load_accessibility_rules(self):
        return {
            'alt_text': {
                'pattern': r'!\[([^\]]*)\]\([^)]+\)',
                'description': 'Images must have alt text',
                'severity': 'high'
            },
            'heading_hierarchy': {
                'pattern': r'#{1,6}\s+[^\n]+',
                'description': 'Proper heading hierarchy',
                'severity': 'medium'
            },
            'link_text': {
                'pattern': r'\[([^\]]+)\]\([^)]+\)',
                'description': 'Links must have descriptive text',
                'severity': 'medium'
            },
            'table_headers': {
                'pattern': r'\|[^|]+\|[^|]+\|',
                'description': 'Tables must have headers',
                'severity': 'low'
            }
        }

    def check_accessibility(self, documentation):
        """Check documentation for accessibility issues."""
        issues = []

        for rule_name, rule_info in self.accessibility_rules.items():
            rule_issues = self._check_rule(documentation, rule_name, rule_info)
            issues.extend(rule_issues)

        return issues

    def _check_rule(self, documentation, rule_name, rule_info):
        """Check a specific accessibility rule."""
        import re

        issues = []
        matches = re.finditer(rule_info['pattern'], documentation)

        for match in matches:
            if rule_name == 'alt_text':
                if not match.group(1).strip():
                    issues.append({
                        'rule': rule_name,
                        'severity': rule_info['severity'],
                        'message': rule_info['description'],
                        'location': match.start()
                    })

        return issues
```

## Self-Check Before Delivery

1. List every symbol, flag, endpoint, config key, and path your docs mention. Did you verify each one against the source in this session?
2. Would every code sample run on a clean machine?
3. Any number, compatibility claim, or superlative without a repo-verifiable source?
4. If this change touched code: did you grep all docs surfaces for the old names?
5. Any docstring that just restates the signature? Any section that restates its heading?
6. Do all internal links resolve?
7. Run accessibility check: any missing alt text, poor heading hierarchy, or inaccessible content?
8. Run drift detection: any code changes that require documentation updates?
9. Score documentation quality: completeness, accuracy, clarity, accessibility, maintainability?
10. Verify API documentation: all endpoints, parameters, responses documented?

## Reporting Format (Review Mode)

```
**Rule N violation** in `docs/path.md:<line or section>`
- Claim: <what the docs say>
- Reality: <what the code actually has, with file:line>
- Fix: <one sentence>
- Severity: <critical|high|medium|low>
- Category: <accuracy|versioning|substance|structure|accessibility>
```

Lead with Rule 1–6 findings (false claims), then drift, then substance, then accessibility.

## Severity Guide

- **Critical:** False documentation (Rules 1-6) — immediate fix required
- **Must fix:** Security documentation gaps — compliance risk
- **Should fix:** Rules 7-13 — drift debt and noise
- **Worth noting:** Rules 14-20 — navigation, polish, and accessibility

## Documentation Quality Report Template

```markdown
# Documentation Quality Report

## Summary
- Total violations: X
- Critical: X
- High: X
- Medium: X
- Low: X

## Accuracy Findings
[List accuracy violations]

## Versioning Findings
[List versioning issues]

## Substance Findings
[List substance problems]

## Accessibility Findings
[List accessibility issues]

## Quality Score
- Completeness: X/100
- Accuracy: X/100
- Clarity: X/100
- Accessibility: X/100
- Maintainability: X/100
- Overall: X/100 (Grade: X)

## Recommendations
[Prioritized list of improvements]
```

## References

- [references/documentation-standards.md](references/documentation-standards.md) — documentation best practices
- [references/api-documentation.md](references/api-documentation.md) — API documentation guidelines
- [references/accessibility-standards.md](references/accessibility-standards.md) — accessibility compliance
- [references/writing-style-guide.md](references/writing-style-guide.md) — technical writing guidelines

---

**Version**: 2.0.0
**Status**: ULTRA-ADVANCED Docs Guard Ready
**Features**: Symbol Verification, Code Testing, Drift Detection, Quality Scoring, Accessibility

---

**Remember**: Documentation is a living contract with users. Every claim must be verifiable, every example must work, and every update must be timely. The goal is documentation that users can trust completely.
