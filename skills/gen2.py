import os, json
BASE = r"C:\opencodes\guard skills\skills"
SKILLS = {}
SKILLS["guards"] = [
    ("ddd-guard", "Domain-driven design validation - aggregates, entities, bounded contexts", "ddd check, domain driven design", [
        ("Aggregate Root violation", "Logic outside aggregate roots", "critical"),
        ("Ubiquitous language drift", "Domain terms not in code", "high"),
        ("Bounded context leak", "Cross-context coupling", "critical"),
        ("Repository pattern violation", "Direct data access in domain", "high"),
        ("Entity vs Value Object misuse", "Wrong type semantics", "medium"),
    ]),
    ("hexagonal-guard", "Hexagonal/ports-and-adapters architecture validation", "hexagonal architecture, ports and adapters", [
        ("Port interface violation", "Domain depends on infrastructure", "critical"),
        ("Adapter layer leak", "Infrastructure detail in application", "high"),
        ("Hexagonal layer violation", "Wrong import direction", "critical"),
        ("Input port missing", "No inbound boundary interface", "medium"),
        ("Output port missing", "No outbound boundary interface", "medium"),
    ]),
    ("clean-arch-guard", "Clean architecture layer dependency validation", "clean architecture, dependency rule", [
        ("Dependency rule violation", "Inner layer imports outer", "critical"),
        ("Entity leak", "Entities referenced outside domain", "high"),
        ("Use case bypass", "Controller directly accesses repository", "high"),
        ("Framework coupling in core", "Framework dependency in domain", "critical"),
        ("Gateway violation", "Gateway called from use case directly", "medium"),
    ]),
    ("cqrs-guard", "CQRS pattern validation - command/query separation", "cqrs, command query segregation", [
        ("Command returning data", "Command returns query results", "critical"),
        ("Read model stale", "No refresh strategy for read model", "high"),
        ("Command validation leak", "Validation mixed with handler", "medium"),
        ("Query affecting state", "Query has side effects", "critical"),
        ("Shared model violation", "Read/write share same model", "high"),
    ]),
    ("event-sourcing-guard", "Event sourcing pattern validation", "event sourcing, event store", [
        ("Event mutation", "Events modified after append", "critical"),
        ("Missing event type", "Event without type discriminator", "high"),
        ("Event version missing", "No versioning on events", "high"),
        ("Snapshot strategy missing", "No snapshot for long streams", "medium"),
        ("Event replay safety", "Side effects during replay", "high"),
    ]),
    ("saga-guard", "Saga/choreography pattern validation", "saga pattern, compensating transactions", [
        ("Missing compensating action", "Saga step without rollback", "critical"),
        ("Step order wrong", "Wrong execution sequence", "high"),
        ("Compensating not idempotent", "Compensation not idempotent", "critical"),
        ("Timeout missing on step", "No timeout for saga step", "high"),
        ("Orchestrator bottleneck", "Central orchestrator coupling", "medium"),
    ]),
    ("api-contract-guard", "API contract compliance validation", "api contract, contract testing", [
        ("Contract breaking change", "Breaking change in API contract", "critical"),
        ("Missing endpoint", "Endpoints in contract not implemented", "high"),
        ("Parameter mismatch", "Request params differ from contract", "high"),
        ("Response mismatch", "Response structure differs", "high"),
        ("Content type mismatch", "Wrong media type used", "medium"),
    ]),
    ("cors-guard", "CORS configuration validation and security", "cors check, cross origin", [
        ("Wildcard CORS origin", "Access-Control-Allow-Origin: *", "critical"),
        ("Credentials with wildcard", "Credentials + wildcard origin", "critical"),
        ("Exposed headers too permissive", "Too many exposed headers", "high"),
        ("Allow methods too broad", "Allow-Methods: * wildcard", "high"),
        ("Preflight cache too long", "Max-Age > 86400", "medium"),
    ]),
    ("jwt-guard", "JWT implementation validation and security", "jwt check, token validation", [
        ("Hardcoded JWT secret", "Secret in source code", "critical"),
        ("No signature verification", "JWT without verification", "critical"),
        ("Weak algorithm", "alg: none or HS256 with RSA key", "critical"),
        ("Missing expiry check", "No exp validation", "high"),
        ("Sensitive data in payload", "PII in JWT payload", "high"),
    ]),
    ("csrf-guard", "CSRF protection validation", "csrf check, cross site request forgery", [
        ("Missing CSRF token", "Forms without CSRF protection", "critical"),
        ("Weak CSRF token generation", "Predictable or weak token", "high"),
        ("CSRF token reuse", "Same token across requests", "high"),
        ("Double submit cookie validation", "Cookie not validated", "medium"),
        ("AJAX CSRF check missing", "AJAX endpoints without CSRF", "high"),
    ]),
