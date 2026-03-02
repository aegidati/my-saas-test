# Packages Architecture

---

## 1. Purpose

This document defines the architecture and governance of the `packages/` directory within the monorepo.

It specifies:

- The purpose of reusable backend packages
- What is allowed and not allowed inside packages
- Dependency rules
- Versioning strategy
- Integration with backend, frontend, and CI/CD
- Multi-tenant and security considerations

This document complements:

- ARCHITECTURE.md  
- backend-structure.md  
- database-abstraction.md  
- multi-tenancy.md  
- security-model.md  
- ci-cd.md  

In case of conflict, ADRs prevail.

---

## 2. Goals of the Packages Layer

The `packages/` directory exists to:

- Host reusable backend logic
- Avoid duplication across services or projects
- Provide standardized domain-independent utilities
- Encapsulate shared technical building blocks
- Enable modular architecture inside the monorepo

Packages must promote:

- Reusability
- Stability
- Clear dependency boundaries
- Framework independence (where possible)

---

## 3. Scope of Packages

Packages are:

- Backend-only
- Non-UI
- Framework-light or framework-agnostic where possible

Packages may contain:

- Shared domain utilities
- Generic services
- Cross-cutting libraries
- Validation utilities
- Shared abstractions
- Internal SDKs
- Policy engines
- Event utilities

Packages must not contain:

- Django views
- React components
- Mobile UI code
- Presentation logic

---

## 4. Directory Structure

Recommended monorepo structure:

packages/  
├── core-utils/  
├── domain-shared/  
├── validation/  
├── auth-core/  
├── multi-tenant-core/  
└── ...  

Each package should have:

- Its own dependency definition
- Clear public API surface
- Internal/private modules
- Dedicated tests

---

## 5. Package Design Principles

Packages must:

- Have a clearly defined responsibility
- Expose minimal public API
- Hide implementation details
- Avoid tight coupling to specific frameworks
- Avoid implicit global state
- Be independently testable

Packages should follow:

- Clean interfaces
- Explicit configuration injection
- Deterministic behavior

---

## 6. Dependency Rules

Allowed dependencies:

- Packages may depend on other packages.
- Backend may depend on packages.
- Frontend must not depend on backend-only packages unless explicitly designed (e.g., shared schema definitions).

Forbidden dependencies:

- Packages must not depend on `backend/interfaces/`.
- Packages must not depend on frontend code.
- Packages must not depend on environment-specific configuration directly.
- Circular dependencies between packages are forbidden.

Dependency graph must remain acyclic.

---

## 7. Multi-Tenancy Considerations

Packages must:

- Be tenant-agnostic by default.
- Accept Tenant Context explicitly when needed.
- Never rely on global mutable tenant state.
- Avoid embedding tenant-specific logic unless explicitly scoped.

If a package contains multi-tenant utilities:

- It must enforce tenant isolation consistently.
- It must not assume specific database implementations.

---

## 8. Security Considerations

Packages must:

- Follow rules defined in security-model.md.
- Avoid logging sensitive data.
- Avoid storing secrets.
- Avoid implicit security assumptions.

Security-sensitive packages (e.g., auth-core) must:

- Be carefully reviewed.
- Have high test coverage.
- Avoid leaking low-level cryptographic details outside public API.

---

## 9. Configuration Handling

Packages must:

- Not read environment variables directly.
- Receive configuration via explicit injection.
- Avoid static configuration initialization.
- Remain deterministic and testable.

Configuration binding must occur in backend infrastructure layer.

---

## 10. Testing Strategy for Packages

Each package must:

- Include its own unit tests.
- Avoid relying on external services.
- Be testable in isolation.

Integration tests may exist at backend level.

Test coverage expectations:

- High coverage for core utilities.
- Explicit tests for edge cases.
- Explicit tests for error conditions.

Packages must not rely on global state during tests.

---

## 11. Versioning Strategy

Even inside a monorepo, packages must:

- Follow semantic versioning internally.
- Avoid breaking public API without version bump.
- Clearly document breaking changes.

Versioning may be:

- Internal-only (monorepo controlled), or
- Publishable (if extracted to separate repositories in the future).

Breaking changes in shared packages must:

- Be reviewed carefully.
- Trigger dependent test runs.
- Be validated across all consumers.

---

## 12. CI/CD Integration

CI must:

- Detect changes in packages.
- Run package-specific tests.
- Run dependent backend tests when packages change.
- Prevent merge if breaking changes cause failures.

Optional:

- Enforce dependency graph validation.
- Enforce linting per package.

Packages must not bypass CI validation.

---

## 13. Public API Discipline

Each package must:

- Clearly define public entry points.
- Avoid exposing internal modules.
- Use explicit exports.

Internal modules must not be relied upon by external code.

Refactoring internal implementation must not break consumers.

---

## 14. Anti-Patterns

The following are forbidden:

- Dumping miscellaneous code into a "utils" package without structure.
- Allowing packages to grow without clear responsibility.
- Using packages as a shortcut to bypass architectural boundaries.
- Embedding Django-specific logic in generic packages.
- Embedding business domain logic that belongs in backend domain layer.
- Creating circular package dependencies.

Packages must not become a “god layer”.

---

## 15. Evolution Strategy

Packages architecture may evolve when:

- System modularity increases.
- New reusable components emerge.
- Microservice extraction is considered.
- Shared abstractions stabilize.

Changes affecting:

- Dependency rules
- Public API contracts
- Versioning strategy

Must be documented and, when significant, captured via ADR.

Packages represent long-term architectural assets and must be designed with stability and clarity in mind.