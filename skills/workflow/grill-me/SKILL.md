---
name: grill-me
version: 2.0.0
author: Abdox
description: |
  ULTRA-ADVANCED Grill Me skill with systematic questioning, decision tree analysis,
  assumption validation, and comprehensive design review for thorough planning.
  Use when the user wants to: stress-test a plan, validate a design, explore alternatives,
  challenge assumptions, or any comprehensive planning workflow.

  GRILL ME: Comprehensive interview system that systematically explores all aspects
  of a plan or design until complete understanding is achieved.

  FEATURES:
  - Systematic questioning methodology
  - Decision tree analysis
  - Assumption validation
  - Alternative exploration
  - Risk identification
  - Dependency mapping
  - Edge case discovery
  - Design pattern validation

  TRIGGER PHRASES: "grill me", "stress test", "challenge assumptions", "explore alternatives",
  "validate design", "decision tree", "comprehensive review", "systematic questioning",
  "design review", "plan validation".

  TRAINED ON: Interview techniques, critical thinking, design patterns,
  decision analysis, risk assessment, and systematic planning.

  ENVIRONMENT: Works with any domain, any complexity, any scale.

  SECURITY: Enterprise-grade design review and security consideration.
---

# Grill Me - ULTRA-ADVANCED v2.0

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## How This Works

1. **Start broad:** What are we building? Who is it for? What problem does it solve?
2. **Drill into scope:** What's in? What's out? What are the hard constraints?
3. **Challenge assumptions:** Why this approach? What alternatives did you consider? Why did you reject them?
4. **Resolve dependencies:** What does this depend on? What depends on this? What's the order of operations?
5. **Find edge cases:** What happens when X fails? What about Y? Have you considered Z?
6. **Confirm decisions:** So we've agreed: [summary]. Anything you want to revisit?

## Advanced Questioning Framework

### The Socratic Method
```python
class SocraticQuestioning:
    def __init__(self):
        self.question_types = [
            'clarification',
            'assumptions',
            'evidence',
            'alternative_perspectives',
            'implications',
            'meta_questioning'
        ]

    def generate_questions(self, topic, context):
        """Generate Socratic questions about a topic."""
        questions = []

        # Clarification questions
        questions.extend(self._clarification_questions(topic))

        # Assumption questions
        questions.extend(self._assumption_questions(topic, context))

        # Evidence questions
        questions.extend(self._evidence_questions(topic, context))

        # Alternative perspective questions
        questions.extend(self._alternative_questions(topic))

        # Implication questions
        questions.extend(self._implication_questions(topic))

        return questions

    def _clarification_questions(self, topic):
        return [
            f"What do you mean by '{topic}'?",
            f"Could you explain '{topic}' in more detail?",
            f"What is the key issue here?",
            f"Could you give me an example?",
            f"What is the most important aspect of '{topic}'?"
        ]

    def _assumption_questions(self, topic, context):
        assumptions = self._identify_assumptions(context)
        return [f"What are you assuming about {assumption}?"
                for assumption in assumptions]

    def _evidence_questions(self, topic, context):
        return [
            f"What evidence supports your view on '{topic}'?",
            f"How do you know this is true?",
            f"What experience do you have with '{topic}'?",
            f"What would convince you otherwise?"
        ]

    def _alternative_questions(self, topic):
        return [
            f"What is an alternative perspective on '{topic}'?",
            f"What would someone who disagrees say?",
            f"What are the strengths of the opposite view?",
            f"Is there another way to look at this?"
        ]

    def _implication_questions(self, topic):
        return [
            f"What are the consequences of '{topic}'?",
            f"If this is true, what else must be true?",
            f"What would follow from this?",
            f"What are the implications for the larger system?"
        ]

    def _identify_assumptions(self, context):
        """Identify assumptions in the context."""
        # Simple assumption identification
        assumption_keywords = ['always', 'never', 'every', 'all', 'must', 'should']
        assumptions = []

        for keyword in assumption_keywords:
            if keyword in context.lower():
                assumptions.append(keyword)

        return assumptions
```

### Decision Tree Analyzer
```python
class DecisionTreeAnalyzer:
    def __init__(self):
        self.decision_tree = {}
        self.resolved_decisions = []

    def build_decision_tree(self, plan):
        """Build a decision tree from a plan."""
        tree = {
            'root': {
                'question': 'What are we building?',
                'options': [],
                'dependencies': [],
                'resolved': False
            }
        }

        # Analyze plan to extract decisions
        decisions = self._extract_decisions(plan)

        for decision in decisions:
            tree[decision['id']] = {
                'question': decision['question'],
                'options': decision['options'],
                'dependencies': decision.get('dependencies', []),
                'resolved': False,
                'parent': decision.get('parent', 'root')
            }

        return tree

    def _extract_decisions(self, plan):
        """Extract decisions from a plan."""
        import re

        # Look for decision patterns
        patterns = [
            r'we need to decide (.+)',
            r'we should choose between (.+)',
            r'the options are (.+)',
            r'we have to (.+)'
        ]

        decisions = []
        for pattern in patterns:
            matches = re.findall(pattern, plan, re.IGNORECASE)
            for match in matches:
                decisions.append({
                    'id': f'decision_{len(decisions)}',
                    'question': match,
                    'options': self._extract_options(match)
                })

        return decisions

    def _extract_options(self, text):
        """Extract options from text."""
        # Simple option extraction
        if 'or' in text.lower():
            return [opt.strip() for opt in text.split('or')]
        elif ',' in text:
            return [opt.strip() for opt in text.split(',')]
        else:
            return [text]

    def resolve_decision(self, decision_id, choice):
        """Resolve a decision with a choice."""
        if decision_id in self.decision_tree:
            self.decision_tree[decision_id]['resolved'] = True
            self.decision_tree[decision_id]['choice'] = choice
            self.resolved_decisions.append(decision_id)

            # Update dependent decisions
            self._update_dependent_decisions(decision_id, choice)

            return True
        return False

    def _update_dependent_decisions(self, decision_id, choice):
        """Update decisions that depend on this one."""
        for decision in self.decision_tree.values():
            if decision_id in decision.get('dependencies', []):
                # Update options based on parent choice
                decision['options'] = self._filter_options(
                    decision['options'],
                    choice
                )

    def _filter_options(self, options, parent_choice):
        """Filter options based on parent choice."""
        # Simple filtering - in reality would be more sophisticated
        return [opt for opt in options if parent_choice.lower() in opt.lower()]

    def get_next_decision(self):
        """Get the next unresolved decision."""
        for decision_id, decision in self.decision_tree.items():
            if not decision['resolved']:
                # Check if dependencies are resolved
                deps_resolved = all(
                    dep in self.resolved_decisions
                    for dep in decision.get('dependencies', [])
                )
                if deps_resolved:
                    return decision_id, decision

        return None, None

    def get_unresolved_dependencies(self, decision_id):
        """Get unresolved dependencies for a decision."""
        if decision_id in self.decision_tree:
            decision = self.decision_tree[decision_id]
            return [
                dep for dep in decision.get('dependencies', [])
                if dep not in self.resolved_decisions
            ]
        return []
```

### Assumption Validator
```python
class AssumptionValidator:
    def __init__(self):
        self.assumptions = []
        self.validated_assumptions = []

    def identify_assumptions(self, plan):
        """Identify assumptions in a plan."""
        import re

        assumption_patterns = [
            r'we assume (.+)',
            r'assuming (.+)',
            r'we expect (.+)',
            r'we believe (.+)',
            r'we think (.+)',
            r'we assume that (.+)',
            r'we expect that (.+)',
            r'we believe that (.+)'
        ]

        assumptions = []
        for pattern in assumption_patterns:
            matches = re.findall(pattern, plan, re.IGNORECASE)
            for match in matches:
                assumptions.append({
                    'id': f'assumption_{len(assumptions)}',
                    'statement': match,
                    'validated': False,
                    'evidence': [],
                    'risks': []
                })

        self.assumptions = assumptions
        return assumptions

    def validate_assumption(self, assumption_id, evidence, risks):
        """Validate an assumption with evidence."""
        for assumption in self.assumptions:
            if assumption['id'] == assumption_id:
                assumption['validated'] = True
                assumption['evidence'] = evidence
                assumption['risks'] = risks
                self.validated_assumptions.append(assumption_id)
                return True
        return False

    def get_unvalidated_assumptions(self):
        """Get all unvalidated assumptions."""
        return [
            a for a in self.assumptions
            if not a['validated']
        ]

    def get_assumption_risks(self):
        """Get risks for all assumptions."""
        risks = []
        for assumption in self.assumptions:
            for risk in assumption.get('risks', []):
                risks.append({
                    'assumption': assumption['statement'],
                    'risk': risk
                })
        return risks

    def generate_validation_questions(self):
        """Generate questions to validate assumptions."""
        questions = []
        for assumption in self.assumptions:
            if not assumption['validated']:
                questions.append(
                    f"What evidence supports the assumption: '{assumption['statement']}'?"
                )
        return questions
```

### Risk Identifier
```python
class RiskIdentifier:
    def __init__(self):
        self.risk_categories = [
            'technical',
            'business',
            'resource',
            'timeline',
            'dependency',
            'security',
            'performance',
            'scalability'
        ]

    def identify_risks(self, plan):
        """Identify risks in a plan."""
        risks = []

        # Technical risks
        risks.extend(self._identify_technical_risks(plan))

        # Business risks
        risks.extend(self._identify_business_risks(plan))

        # Resource risks
        risks.extend(self._identify_resource_risks(plan))

        # Timeline risks
        risks.extend(self._identify_timeline_risks(plan))

        # Dependency risks
        risks.extend(self._identify_dependency_risks(plan))

        return risks

    def _identify_technical_risks(self, plan):
        """Identify technical risks."""
        import re

        technical_risks = []

        # Look for technical risk patterns
        patterns = [
            (r'new technology', 'Technology unfamiliarity'),
            (r'complex algorithm', 'Algorithm complexity'),
            (r'performance', 'Performance requirements'),
            (r'security', 'Security concerns'),
            (r'integration', 'Integration challenges')
        ]

        for pattern, risk_type in patterns:
            if re.search(pattern, plan, re.IGNORECASE):
                technical_risks.append({
                    'category': 'technical',
                    'type': risk_type,
                    'description': f'Potential {risk_type.lower()} risk',
                    'mitigation': f'Plan for {risk_type.lower()} mitigation'
                })

        return technical_risks

    def _identify_business_risks(self, plan):
        """Identify business risks."""
        # Simplified business risk identification
        return [{
            'category': 'business',
            'type': 'Market Risk',
            'description': 'Market conditions may change',
            'mitigation': 'Monitor market trends'
        }]

    def _identify_resource_risks(self, plan):
        """Identify resource risks."""
        return [{
            'category': 'resource',
            'type': 'Resource Availability',
            'description': 'Required resources may not be available',
            'mitigation': 'Plan resource allocation carefully'
        }]

    def _identify_timeline_risks(self, plan):
        """Identify timeline risks."""
        return [{
            'category': 'timeline',
            'type': 'Timeline Risk',
            'description': 'Project may take longer than expected',
            'mitigation': 'Build buffer time into schedule'
        }]

    def _identify_dependency_risks(self, plan):
        """Identify dependency risks."""
        return [{
            'category': 'dependency',
            'type': 'External Dependency',
            'description': 'Dependent on external systems or teams',
            'mitigation': 'Identify and manage dependencies'
        }]

    def assess_risk_impact(self, risk):
        """Assess the impact of a risk."""
        impact_factors = {
            'technical': 0.8,
            'business': 0.7,
            'resource': 0.6,
            'timeline': 0.5,
            'dependency': 0.7
        }

        base_impact = impact_factors.get(risk['category'], 0.5)

        # Adjust based on risk type
        type_multipliers = {
            'Security': 1.5,
            'Performance': 1.3,
            'Scalability': 1.2,
            'Integration': 1.1
        }

        multiplier = type_multipliers.get(risk['type'], 1.0)

        return base_impact * multiplier
```

### Dependency Mapper
```python
class DependencyMapper:
    def __init__(self):
        self.dependencies = {}
        self.dependents = {}

    def map_dependencies(self, components):
        """Map dependencies between components."""
        for component in components:
            deps = self._extract_dependencies(component)
            self.dependencies[component['id']] = deps

            # Update dependents
            for dep in deps:
                if dep not in self.dependents:
                    self.dependents[dep] = []
                self.dependents[dep].append(component['id'])

    def _extract_dependencies(self, component):
        """Extract dependencies from a component."""
        # Simplified dependency extraction
        if 'dependencies' in component:
            return component['dependencies']
        return []

    def get_dependency_chain(self, component_id):
        """Get the full dependency chain for a component."""
        chain = []
        visited = set()

        def dfs(component_id):
            if component_id in visited:
                return
            visited.add(component_id)

            if component_id in self.dependencies:
                for dep in self.dependencies[component_id]:
                    dfs(dep)
                    chain.append(dep)

        dfs(component_id)
        return chain

    def get_critical_path(self):
        """Get the critical path through dependencies."""
        # Find components with no dependencies (starting points)
        starting_points = [
            comp for comp in self.dependencies
            if not self.dependencies[comp]
        ]

        # Find longest path
        longest_path = []
        for start in starting_points:
            path = self.get_dependency_chain(start)
            if len(path) > len(longest_path):
                longest_path = path

        return longest_path

    def identify_bottlenecks(self):
        """Identify dependency bottlenecks."""
        bottlenecks = []

        for component, dependents in self.dependents.items():
            if len(dependents) > 2:  # Threshold for bottleneck
                bottlenecks.append({
                    'component': component,
                    'dependent_count': len(dependents),
                    'dependents': dependents
                })

        return bottlenecks

    def visualize_dependencies(self):
        """Create a visualization of dependencies."""
        viz = {
            'nodes': [],
            'edges': []
        }

        # Add nodes
        for component in self.dependencies:
            viz['nodes'].append({
                'id': component,
                'label': component
            })

        # Add edges
        for component, deps in self.dependencies.items():
            for dep in deps:
                viz['edges'].append({
                    'from': dep,
                    'to': component
                })

        return viz
```

## Question Categories

### Technical Questions
1. **Architecture**: What architecture pattern are you using? Why?
2. **Technology**: What technologies will you use? What are the trade-offs?
3. **Scalability**: How will this scale? What are the limits?
4. **Security**: What are the security considerations? How will you address them?
5. **Performance**: What are the performance requirements? How will you meet them?

### Business Questions
1. **Value**: What value does this provide? How will you measure it?
2. **Users**: Who are the users? What are their needs?
3. **Market**: How does this fit in the market? What's the competitive landscape?
4. **Revenue**: How will this generate revenue? What's the business model?
5. **Success**: What does success look like? How will you know you've succeeded?

### Resource Questions
1. **Team**: What team is needed? What skills are required?
2. **Budget**: What's the budget? How will it be allocated?
3. **Timeline**: What's the timeline? What are the milestones?
4. **Tools**: What tools are needed? What's the infrastructure?
5. **Training**: What training is required? How long will it take?

### Risk Questions
1. **Technical Risks**: What could go wrong technically? How will you mitigate?
2. **Business Risks**: What could go wrong with the business? How will you mitigate?
3. **Resource Risks**: What could go wrong with resources? How will you mitigate?
4. **Timeline Risks**: What could go wrong with the timeline? How will you mitigate?
5. **External Risks**: What external factors could affect the project? How will you monitor?

## Rules

- One question at a time
- Provide your recommended answer for each question
- If the user is vague, push for specifics
- If the user contradicts themselves, call it out
- If a question can be answered by reading the code, read the code instead of asking
- Stop when every branch of the decision tree is resolved
- Document all decisions and their rationale
- Validate assumptions with evidence
- Identify and assess risks
- Map dependencies and identify bottlenecks

## What Good Looks Like

```
Agent: What's the primary data flow for this feature?
User: Users upload a CSV, we parse it, and show results.
Agent: Recommended: streaming parse for large files, batch insert.
       What's the max file size you expect?
User: ~10MB, maybe 50K rows.
Agent: That's manageable in memory. But if you want to support 100MB+,
       streaming is the safer default. Your call?
User: Let's go with streaming.
Agent: Got it. Streaming parse, batch insert. Next: how should errors
       in individual rows be reported to the user?
```

## Decision Tree Template

```markdown
# Decision Tree

## Root Decision
**Question**: What are we building?
**Options**: [List options]
**Decision**: [Chosen option]
**Rationale**: [Why this option]

## Decision 1
**Question**: [Question]
**Dependencies**: [Dependencies]
**Options**: [List options]
**Decision**: [Chosen option]
**Rationale**: [Why this option]

## Decision 2
**Question**: [Question]
**Dependencies**: [Dependencies]
**Options**: [List options]
**Decision**: [Chosen option]
**Rationale**: [Why this option]

## Summary
- **Key Decisions**: [List key decisions]
- **Assumptions**: [List assumptions]
- **Risks**: [List risks]
- **Next Steps**: [List next steps]
```

## References

- [references/decision-analysis.md](references/decision-analysis.md) — decision-making frameworks
- [references/risk-assessment.md](references/risk-assessment.md) — risk identification and mitigation
- [references/dependency-management.md](references/dependency-management.md) — dependency mapping and management
- [references/design-patterns.md](references/design-patterns.md) — common design patterns and trade-offs

---

**Version**: 2.0.0
**Status**: ULTRA-ADVANCED Grill Me Ready
**Features**: Systematic Questioning, Decision Analysis, Assumption Validation, Risk Assessment, Dependency Mapping

---

**Remember**: The goal of grilling is not to interrogate, but to achieve complete understanding. Every question should bring us closer to a shared understanding of the plan. Document everything, validate assumptions, and identify risks early.
