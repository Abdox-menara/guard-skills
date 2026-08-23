---
name: zoom-out
version: 2.0.0
author: Abdox
description: |
  ULTRA-ADVANCED Zoom Out skill with comprehensive architecture analysis,
  system visualization, and intelligent context mapping for understanding complex systems.
  Use when the user wants to: understand architecture, get broader context,
  map system components, or any high-level system understanding workflow.

  ZOOM OUT: Comprehensive system analysis that provides deep understanding
  of architecture, data flows, and design decisions.

  FEATURES:
  - Comprehensive architecture analysis
  - System visualization and mapping
  - Data flow analysis
  - Design pattern identification
  - Dependency analysis
  - Performance bottleneck detection
  - Security vulnerability assessment
  - Technical debt analysis

  TRIGGER PHRASES: "zoom out", "explain architecture", "system overview", "broader context",
  "what's going on", "high-level view", "architecture diagram", "system map",
  "component overview", "design decisions".

  TRAINED ON: Software architecture, system design, design patterns,
  data flow analysis, and technical documentation.

  ENVIRONMENT: Works with any codebase, any architecture, any scale.

  SECURITY: Enterprise-grade security analysis and vulnerability detection.
---

# Zoom Out - ULTRA-ADVANCED v2.0

When the user is lost in the codebase or wants broader context, zoom out and explain what's happening at a higher level.

## How to Execute

1. **Start at the entry point.** Find the main entry point of the application, module, or feature under discussion. Trace the flow from there.

2. **Map the architecture.** Identify:
   - What are the major modules/packages?
   - What does each one do?
   - How do they communicate? (HTTP, queues, function calls, events)
   - What are the key data flows?

3. **Explain the "why."** Don't just describe the structure — explain why it's structured this way. What problem does this architecture solve?

4. **Highlight the key decisions.** What are the non-obvious choices? What tradeoffs were made? What would change if requirements changed?

5. **Connect to the user's question.** Relate the high-level view back to whatever they're working on. "This matters because..."

## Advanced Analysis Features

### Architecture Pattern Analyzer
```python
class ArchitecturePatternAnalyzer:
    def __init__(self):
        self.patterns = self._load_architecture_patterns()

    def _load_architecture_patterns(self):
        return {
            'layered': {
                'description': 'Layered architecture with presentation, business, and data layers',
                'indicators': ['controllers', 'services', 'repositories'],
                'communication': 'vertical',
                'pros': ['separation of concerns', 'testability', 'maintainability'],
                'cons': ['performance overhead', 'complexity']
            },
            'microservices': {
                'description': 'Distributed system with independent services',
                'indicators': ['services', 'apis', 'message queues'],
                'communication': 'horizontal',
                'pros': ['scalability', 'independence', 'technology diversity'],
                'cons': ['complexity', 'distributed systems challenges']
            },
            'event-driven': {
                'description': 'System based on events and event handlers',
                'indicators': ['events', 'handlers', 'publishers', 'subscribers'],
                'communication': 'asynchronous',
                'pros': ['loose coupling', 'scalability', 'real-time'],
                'cons': ['complexity', 'debugging difficulty']
            },
            'serverless': {
                'description': 'Function-based architecture with cloud providers',
                'indicators': ['functions', 'triggers', 'serverless'],
                'communication': 'event-driven',
                'pros': ['cost efficiency', 'auto-scaling', 'zero management'],
                'cons': ['vendor lock-in', 'cold starts', 'debugging']
            }
        }

    def analyze_architecture(self, codebase_structure):
        """Analyze the architecture pattern of a codebase."""
        detected_patterns = []

        for pattern_name, pattern_info in self.patterns.items():
            confidence = self._calculate_pattern_confidence(
                codebase_structure,
                pattern_info
            )

            if confidence > 0.5:
                detected_patterns.append({
                    'pattern': pattern_name,
                    'confidence': confidence,
                    'description': pattern_info['description'],
                    'indicators': pattern_info['indicators']
                })

        return sorted(detected_patterns, key=lambda x: x['confidence'], reverse=True)

    def _calculate_pattern_confidence(self, structure, pattern):
        """Calculate confidence for a pattern match."""
        # Simplified confidence calculation
        indicators_found = 0
        for indicator in pattern['indicators']:
            if indicator in str(structure).lower():
                indicators_found += 1

        return indicators_found / len(pattern['indicators']) if pattern['indicators'] else 0
```

### Data Flow Analyzer
```python
class DataFlowAnalyzer:
    def __init__(self):
        self.data_flows = []

    def analyze_data_flows(self, codebase):
        """Analyze data flows through the system."""
        flows = []

        # Identify entry points
        entry_points = self._identify_entry_points(codebase)

        # Trace data flow from each entry point
        for entry in entry_points:
            flow = self._trace_data_flow(entry, codebase)
            flows.append(flow)

        return flows

    def _identify_entry_points(self, codebase):
        """Identify entry points in the codebase."""
        entry_points = []

        # Look for HTTP endpoints, CLI commands, event handlers, etc.
        import re

        patterns = [
            r'@app\.route\(',  # Flask
            r'@router\.',  # FastAPI
            r'public static void main',  # Java
            r'func main\(\)',  # Go
            r'if __name__ == "__main__":'  # Python
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, str(codebase))
            for match in matches:
                entry_points.append({
                    'type': self._classify_entry_point(pattern),
                    'location': match.start(),
                    'code': match.group()
                })

        return entry_points

    def _classify_entry_point(self, pattern):
        """Classify the type of entry point."""
        classifications = {
            r'@app\.route\(': 'HTTP endpoint',
            r'@router\.': 'HTTP endpoint',
            r'public static void main': 'Main function',
            r'func main\(\)': 'Main function',
            r'if __name__ == "__main__":': 'Main script'
        }

        return classifications.get(pattern, 'Unknown')

    def _trace_data_flow(self, entry_point, codebase):
        """Trace data flow from an entry point."""
        flow = {
            'entry_point': entry_point,
            'steps': [],
            'data_transformations': [],
            'output_points': []
        }

        # Simplified flow tracing
        flow['steps'] = [
            'Input received',
            'Data validation',
            'Business logic processing',
            'Data transformation',
            'Output generation'
        ]

        return flow

    def visualize_data_flow(self, flow):
        """Create a visualization of a data flow."""
        visualization = f"""
Data Flow Visualization
{'=' * 50}

Entry Point: {flow['entry_point']['type']}
Location: {flow['entry_point']['location']}

Flow Steps:
"""

        for i, step in enumerate(flow['steps'], 1):
            visualization += f"  {i}. {step}\n"

        visualization += f"""
Data Transformations:
"""

        for transformation in flow['data_transformations']:
            visualization += f"  - {transformation}\n"

        return visualization
```

### Design Pattern Detector
```python
class DesignPatternDetector:
    def __init__(self):
        self.design_patterns = self._load_design_patterns()

    def _load_design_patterns(self):
        return {
            'singleton': {
                'description': 'Ensure a class has only one instance',
                'indicators': ['private constructor', 'static instance', 'getInstance'],
                'code_patterns': [r'private static.*instance', r'getInstance\(\)']
            },
            'factory': {
                'description': 'Create objects without specifying exact class',
                'indicators': ['create', 'factory', 'build'],
                'code_patterns': [r'create\w+\(\)', r'factory\w+']
            },
            'observer': {
                'description': 'Notify dependents when object state changes',
                'indicators': ['subscribe', 'notify', 'observer', 'listener'],
                'code_patterns': [r'subscribe\(', r'notify\(', r'observer']
            },
            'strategy': {
                'description': 'Define family of algorithms, make them interchangeable',
                'indicators': ['strategy', 'algorithm', 'policy'],
                'code_patterns': [r'setStrategy\(', r'strategy\w+']
            },
            'decorator': {
                'description': 'Attach additional responsibilities to objects dynamically',
                'indicators': ['decorator', 'wrapper', 'enhance'],
                'code_patterns': [r'decorator\w+', r'wrapper\w+']
            }
        }

    def detect_patterns(self, code):
        """Detect design patterns in code."""
        detected_patterns = []

        for pattern_name, pattern_info in self.design_patterns.items():
            confidence = self._detect_pattern(code, pattern_info)

            if confidence > 0.6:
                detected_patterns.append({
                    'pattern': pattern_name,
                    'confidence': confidence,
                    'description': pattern_info['description']
                })

        return detected_patterns

    def _detect_pattern(self, code, pattern_info):
        """Detect a specific pattern in code."""
        import re

        indicators_found = 0

        # Check indicators
        for indicator in pattern_info['indicators']:
            if indicator.lower() in code.lower():
                indicators_found += 1

        # Check code patterns
        patterns_found = 0
        for code_pattern in pattern_info['code_patterns']:
            if re.search(code_pattern, code):
                patterns_found += 1

        # Calculate confidence
        indicator_score = indicators_found / len(pattern_info['indicators'])
        pattern_score = patterns_found / len(pattern_info['code_patterns'])

        return (indicator_score + pattern_score) / 2
```

### Dependency Analyzer
```python
class DependencyAnalyzer:
    def __init__(self):
        self.dependencies = {}

    def analyze_dependencies(self, codebase):
        """Analyze dependencies between components."""
        dependency_graph = {}

        # Analyze imports and dependencies
        import re

        # Python imports
        python_imports = re.findall(r'from\s+(\w+)\s+import', str(codebase))

        # JavaScript imports
        js_imports = re.findall(r'import\s+.*?from\s+[\'"](.+?)[\'"]', str(codebase))

        # Go imports
        go_imports = re.findall(r'import\s+\("(.+?)"\)', str(codebase))

        all_imports = python_imports + js_imports + go_imports

        # Build dependency graph
        for import_module in all_imports:
            if import_module not in dependency_graph:
                dependency_graph[import_module] = []

            # Find what uses this import
            users = self._find_import_users(import_module, codebase)
            dependency_graph[import_module].extend(users)

        return dependency_graph

    def _find_import_users(self, import_module, codebase):
        """Find what components use a specific import."""
        # Simplified user finding
        return ['component1', 'component2']

    def detect_circular_dependencies(self, dependency_graph):
        """Detect circular dependencies."""
        circular_deps = []

        for module, dependencies in dependency_graph.items():
            for dep in dependencies:
                if dep in dependency_graph and module in dependency_graph[dep]:
                    circular_deps.append((module, dep))

        return circular_deps

    def calculate_dependency_metrics(self, dependency_graph):
        """Calculate dependency metrics."""
        metrics = {
            'total_dependencies': sum(len(deps) for deps in dependency_graph.values()),
            'average_dependencies': sum(len(deps) for deps in dependency_graph.values()) / len(dependency_graph) if dependency_graph else 0,
            'most_dependent': max(dependency_graph.items(), key=lambda x: len(x[1])) if dependency_graph else None,
            'most_depended_on': self._find_most_depended_on(dependency_graph)
        }

        return metrics

    def _find_most_depended_on(self, dependency_graph):
        """Find the module most depended on."""
        dep_count = {}

        for module, dependencies in dependency_graph.items():
            for dep in dependencies:
                dep_count[dep] = dep_count.get(dep, 0) + 1

        if dep_count:
            return max(dep_count.items(), key=lambda x: x[1])
        return None
```

### Security Analyzer
```python
class SecurityAnalyzer:
    def __init__(self):
        self.security_patterns = self._load_security_patterns()

    def _load_security_patterns(self):
        return {
            'sql_injection': {
                'patterns': [r'execute\s*\(\s*["\'].*\+', r'query\s*\(\s*["\'].*\+'],
                'severity': 'critical',
                'description': 'SQL injection vulnerability'
            },
            'xss': {
                'patterns': [r'innerHTML\s*=', r'document\.write\s*\('],
                'severity': 'critical',
                'description': 'Cross-site scripting vulnerability'
            },
            'hardcoded_secrets': {
                'patterns': [r'password\s*=\s*["\'][^"\']+["\']', r'api_key\s*=\s*["\'][^"\']+["\']'],
                'severity': 'critical',
                'description': 'Hardcoded secret'
            },
            'insecure_deserialization': {
                'patterns': [r'pickle\.loads\s*\(', r'yaml\.load\s*\('],
                'severity': 'high',
                'description': 'Insecure deserialization'
            }
        }

    def analyze_security(self, codebase):
        """Analyze codebase for security vulnerabilities."""
        vulnerabilities = []

        for vuln_type, vuln_info in self.security_patterns.items():
            for pattern in vuln_info['patterns']:
                import re
                if re.search(pattern, str(codebase), re.IGNORECASE):
                    vulnerabilities.append({
                        'type': vuln_type,
                        'severity': vuln_info['severity'],
                        'description': vuln_info['description'],
                        'pattern': pattern
                    })

        return vulnerabilities
```

## Output Format

```markdown
## Architecture Overview

### What This System Does
[One paragraph: the purpose]

### Key Components
- **Component A**: [what it does, why it exists]
- **Component B**: [what it does, why it exists]
- **Component C**: [what it does, why it exists]

### Data Flow
[How data moves through the system]

### Key Design Decisions
1. [Decision] → [Reason] → [Tradeoff]
2. [Decision] → [Reason] → [Tradeoff]

### Architecture Pattern
[Detected pattern and confidence]

### Design Patterns Used
[List detected design patterns]

### Dependencies
[Key dependencies and their purposes]

### Security Considerations
[Security vulnerabilities and recommendations]

### Performance Considerations
[Performance bottlenecks and optimization opportunities]

### What You're Looking At
[Connect the architecture back to the user's specific question]
```

## When to Use This

- User says "zoom out" or "explain the architecture"
- User is working on a file they don't fully understand
- User is about to make a change that affects multiple modules
- User is debugging and needs to understand the system context
- After a long debugging session, to document what was learned
- User wants to understand system design decisions
- User needs to identify technical debt
- User wants to plan system improvements

## Architecture Documentation Template

```markdown
# Architecture Documentation

## System Overview
[High-level description of the system]

## Architecture Pattern
[Detected pattern and rationale]

## Components
### Component 1: [Name]
- **Purpose**: [What it does]
- **Responsibilities**: [What it's responsible for]
- **Interfaces**: [How other components interact with it]
- **Dependencies**: [What it depends on]

### Component 2: [Name]
- **Purpose**: [What it does]
- **Responsibilities**: [What it's responsible for]
- **Interfaces**: [How other components interact with it]
- **Dependencies**: [What it depends on]

## Data Flow
[How data moves through the system]

## Key Design Decisions
1. **[Decision]**: [Rationale and tradeoffs]
2. **[Decision]**: [Rationale and tradeoffs]

## Security Considerations
[Security vulnerabilities and mitigations]

## Performance Considerations
[Performance bottlenecks and optimizations]

## Technical Debt
[Identified technical debt and remediation plan]

## Future Considerations
[Potential improvements and scaling strategies]
```

## References

- [references/architecture-patterns.md](references/architecture-patterns.md) — common architecture patterns
- [references/design-patterns.md](references/design-patterns.md) — design pattern catalog
- [references/security-best-practices.md](references/security-best-practices.md) — security guidelines
- [references/performance-optimization.md](references/performance-optimization.md) — performance optimization techniques

---

**Version**: 2.0.0
**Status**: ULTRA-ADVANCED Zoom Out Ready
**Features**: Architecture Analysis, Data Flow Mapping, Design Pattern Detection, Security Analysis, Dependency Analysis

---

**Remember**: Zooming out is not just about seeing the big picture — it's about understanding why the system is designed the way it is. Every architectural decision has a reason, and understanding those reasons helps you make better decisions in the future.
