# SOLID Principles

Quick reference for the SOLID principles with detection smells.

## S — Single Responsibility Principle

> A class should have only one reason to change.

**Modern phrasing:** One actor per module. A class should be answerable to one stakeholder group (Accounting, Auth, Reporting).

**Smell:** If two unrelated subsystems both reach into the same class, split it.

## O — Open/Closed Principle

> Open for extension, closed for modification.

**Modern phrasing:** Extension via new code, not edits. If adding a new variant requires another type-tag branch in an existing function, refactor to a registry, strategy, or polymorphic dispatch first.

**Smell:** Adding a new case to a switch/if-else chain that grows with every feature.

## L — Liskov Substitution Principle

> Subtypes must be substitutable for their base types.

**Modern phrasing:** No subclass refuses its parent's contract. Never override a method to signal "not implemented" or "unsupported operation."

**Smell:** A subclass throws `NotImplementedError` or returns a dummy value.

## I — Interface Segregation Principle

> Many specific interfaces are better than one general-purpose interface.

**Modern phrasing:** Clients should not be forced to depend on methods they do not use.

**Smell:** A class implements an interface but throws errors for half the methods.

## D — Dependency Inversion Principle

> Depend on abstractions, not concretions.

**Modern phrasing:** Abstractions live with the client, not the implementation. When you introduce an interface, put it in the package that consumes it.

**Smell:** High-level modules directly import low-level modules.
