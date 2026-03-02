# Copilot Instructions

---

## 1. Purpose

This document defines the behavioral, architectural, and quality constraints that GitHub Copilot (and any AI coding assistant) must follow within this project.

Copilot is an implementation assistant — not an architect.

All architectural authority is defined in project documentation.  
If a generated solution conflicts with documentation, documentation prevails.

---

## 2. Documentation Authority Hierarchy

Architecture and system structure are governed by the **Project Documentation Constitution**.

Authoritative sources, in descending order:

1. `/docs/adr/*.md` — Accepted Architecture Decision Records (highest authority)
2. `/docs/architecture/*.md` — Detailed architectural specifications
3. `/docs/architecture/ARCHITECTURE.md` — High-level system overview
4. `/docs/features/Features*.md` — Feature-level functional specifications

Rules:

- Architectural documents define **structure and constraints**.
- Feature documents define **functional behavior and scope**.
- Feature specifications must not override architectural constraints.
- In case of conflict, architectural documentation prevails.

Copilot must always respect this hierarchy.

---

## 3. Architectural Discipline

Before generating or modifying code, Copilot must internally determine:

- Which architectural document governs this part of the system?
- Which layer owns this responsibility?
- Whether the change respects defined boundaries and dependency rules.

Copilot must:

- Respect module boundaries.
- Respect layering rules.
- Respect dependency direction.
- Respect constraints defined in ADRs.
- Maintain separation of concerns.

Copilot must NOT:

- Introduce new architectural patterns autonomously.
- Collapse or bypass layers.
- Create circular dependencies.
- Move business logic into incorrect layers.
- Modify system structure without explicit instruction.

When uncertain, choose stricter separation.

---

## 4. Layer Responsibility Model

Unless explicitly stated otherwise:

### Domain Layer
- Business rules
- Core logic
- Invariants
- Pure domain models

### Application Layer
- Use cases
- Orchestration
- Coordination between domain and infrastructure

### Infrastructure Layer
- Persistence
- External APIs
- Framework integrations
- Technical implementations

### Presentation Layer
- Controllers
- UI components
- View models
- Transport-level logic

Strict prohibitions:

- No business logic in presentation.
- No direct database access from presentation.
- No bypassing domain rules from infrastructure.
- No leaking infrastructure concerns into domain.

---

## 5. Feature Implementation Rules

Functional requirements for individual features are defined in:

`/docs/features/Features*.md`

When working on a feature, Copilot must:

- Use the relevant `FeaturesXXX.md` as the functional source of truth.
- Avoid inventing new requirements.
- Avoid implicitly expanding scope.
- Surface ambiguities instead of guessing.
- Explicitly report conflicts with architecture documentation.

Feature specs define **what**.  
Architecture defines **how**.

Both must be respected.

---

## 6. Structured AI Development Phases

This project follows a structured AI-assisted workflow:

### 6.1 Planning Phase
- Produce a structured implementation plan.
- Identify impacted modules and layers.
- Respect architectural boundaries.
- List assumptions and open questions.
- Do NOT generate production code.

### 6.2 Implementation Phase
- Follow the approved plan.
- Respect ADRs and architecture constraints.
- Keep changes minimal and well-scoped.
- Preserve public interfaces unless explicitly instructed.
- Maintain backward compatibility unless instructed otherwise.
- Add or update appropriate tests.

### 6.3 Review Phase
- Validate adherence to:
  - Feature specification
  - ADRs
  - Architecture documentation
- Check security, performance, and maintainability.
- Surface violations clearly.
- Never silently approve architectural breaches.

If multiple phases are requested together, execute sequentially and clearly separate outputs.

---

## 7. Code Generation Principles

Copilot should:

- Prefer clarity over cleverness.
- Prefer explicit typing.
- Prefer small, composable units.
- Follow existing naming conventions.
- Maintain consistency with surrounding code.
- Generate testable logic.
- Preserve readability and maintainability.

Avoid:

- Monolithic functions.
- Hidden side effects.
- Implicit global state.
- Magic numbers.
- Over-engineered abstractions.
- Unnecessary complexity.

---

## 8. Change Safety Rules

When modifying existing code:

- Preserve public APIs unless explicitly instructed.
- Avoid breaking changes.
- Avoid silent behavioral changes.
- Prefer refactoring over patching structural problems.

If structural modification is required:

- Keep scope minimal.
- Do not cascade architectural changes.
- Do not introduce new dependencies without explicit approval.

---

## 9. Security Discipline

Copilot must:

- Validate all external inputs.
- Avoid insecure defaults.
- Respect authentication and authorization boundaries.
- Avoid leaking sensitive information in logs.
- Avoid unsafe serialization/deserialization.
- Follow `/docs/architecture/security-model.md` if present.

If uncertain, default to the secure option.

Security rules override convenience.

---

## 10. Database and Persistence Discipline

Copilot must:

- Follow data model definitions in `/docs/architecture/database*.md`.
- Respect repository or abstraction layers.
- Avoid N+1 query patterns.
- Avoid tightly coupling domain logic to persistence details.
- Keep persistence concerns outside the domain layer.

Database access must respect layering rules.

---

## 11. Performance and Scalability Awareness

Copilot must:

- Avoid inefficient loops and repeated queries.
- Avoid blocking operations in async contexts.
- Respect scalability constraints defined in architecture documents.
- Avoid unnecessary recomputation.

If an area is marked performance-sensitive in documentation, follow constraints strictly.

---

## 12. Testing Expectations

Copilot should:

- Suggest unit tests for domain logic.
- Prefer pure functions when possible.
- Follow existing testing frameworks and patterns.
- Avoid tightly coupled tests.
- Avoid superficial tests that depend on implementation details.

Testing must validate behavior, not structure.

---

## 13. Dependency Management

Copilot must NOT:

- Introduce new libraries without explicit instruction.
- Upgrade dependencies autonomously.
- Modify configuration files without request.
- Change project structure implicitly.

All dependency decisions require explicit confirmation.

---

## 14. Governance Reminder

This project follows structured engineering discipline:

1. Architecture is defined in documentation.
2. Decisions are recorded in ADRs.
3. Code must follow documented constraints.

Copilot assists implementation within these boundaries.

Architecture prevails over generated output.