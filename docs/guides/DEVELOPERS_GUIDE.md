# Developer Onboarding Guide

---

## 1. Purpose

This document provides a structured onboarding guide for developers joining the project.

It explains:

- The architectural philosophy of the system
- How to navigate the documentation
- How to understand the monorepo structure
- How to work safely within architectural constraints
- How to use AI agents and Copilot responsibly
- How to contribute changes without breaking system integrity

This guide complements all documents inside `docs/architecture/` and must be read before contributing code.

---

## 2. High-Level System Overview

This project is a:

- Fullstack SaaS
- Multi-tenant
- Monorepo-based
- Backend: Python Django
- Web: React
- Mobile: React Native
- Shared reusable backend modules under `packages/`

The system follows strict layered architecture:

- Domain
- Application
- Infrastructure
- Interfaces (Presentation)

All contributors must respect this structure.

---

## 3. How to Navigate the Documentation

The documentation is organized into structured architecture documents.

### 3.1 Core Architecture

- `ARCHITECTURE.md` → System overview
- `backend-structure.md` → Backend layering rules
- `frontend-web.md` → React Web architecture
- `frontend-mobile.md` → React Native architecture
- `packages.md` → Reusable backend modules

---

### 3.2 Multi-Tenant and Data

- `multi-tenancy.md` → Tenant isolation model
- `database-abstraction.md` → Repository + DB abstraction rules

---

### 3.3 Security and Identity

- `authentication.md` → JWT + social login
- `authorization.md` → RBAC + policies
- `security-model.md` → Threat model + security rules

---

### 3.4 Operational Discipline

- `configuration.md` → Environment and secret management
- `testing-strategy.md` → Testing model
- `error-handling.md` → Error classification and API format
- `api-versioning.md` → API evolution strategy
- `logging.md` → Logging rules
- `observability.md` → Metrics + tracing
- `ci-cd.md` → CI/CD and deployment strategy

---

## 4. First Steps for New Developers

When joining the project:

1. Read `ARCHITECTURE.md`.
2. Read `backend-structure.md`.
3. Read `multi-tenancy.md`.
4. Read `authentication.md` and `authorization.md`.
5. Read `testing-strategy.md`.

Only after understanding these documents should you modify or add features.

---

## 5. Understanding the Monorepo

The repository contains:

- backend/
- frontend/web/
- frontend/mobile/
- packages/

Each directory has its own responsibility.

### Backend

- Strict layered architecture.
- Business rules in Domain.
- Use cases in Application.
- ORM and integrations in Infrastructure.
- HTTP layer in Interfaces.

### Frontend

- Presentation only.
- No business logic.
- No trust in client-side authorization.

### Packages

- Backend-only.
- Reusable modules.
- No UI.
- No environment coupling.

---

## 6. Architectural Discipline

Before writing code, ask:

- Which layer should this logic belong to?
- Does this violate separation of concerns?
- Is this multi-tenant safe?
- Does this respect authentication/authorization boundaries?
- Does this introduce cross-layer dependency?

If unsure, consult documentation before implementing.

---

## 7. How to Add a New Feature

Feature development follows this flow:

1. Create `FeatureXYZ.md` describing:
   - Functional objective
   - Expected API behavior
   - Tenant considerations
   - Security constraints
2. Plan changes in Application layer.
3. Implement domain logic (if needed).
4. Implement repository changes (if needed).
5. Add API endpoints.
6. Add frontend screens (if required).
7. Add tests (unit + integration + API).
8. Validate CI passes.

Never implement features directly in the Interface layer without application/domain alignment.

---

## 8. Working with AI (Copilot / Agents)

This project uses structured AI discipline.

AI must:

- Follow `copilot-instructions.md`.
- Respect documentation hierarchy.
- Never invent architecture.
- Never bypass layering rules.

Recommended workflow:

1. Provide a precise prompt with:
   - Target layer
   - Constraints
   - Reference to relevant docs
2. Review AI output critically.
3. Verify:
   - Layer correctness
   - Tenant safety
   - Security compliance
   - Test coverage

AI is an assistant, not the architect.

---

## 9. Multi-Tenant Awareness

Every developer must understand:

- Tenant Context is required for tenant-scoped operations.
- No cross-tenant queries are allowed.
- Repository operations must enforce tenant filtering.
- Tenant ID must never be trusted solely from frontend.

Multi-tenancy violations are critical bugs.

---

## 10. Security Awareness

Developers must:

- Never hardcode secrets.
- Never log tokens.
- Validate all external inputs.
- Follow secure coding guidelines.
- Respect token storage rules (Web vs Mobile).

Security mistakes are considered high severity.

---

## 11. Testing Discipline

Before merging:

- Add domain tests for business rules.
- Add application tests for use cases.
- Add integration tests for repository changes.
- Add API tests for new endpoints.
- Update frontend tests if UI changes.

Do not merge untested logic.

---

## 12. CI/CD Expectations

Before merging:

- All checks must pass.
- No skipped tests.
- No failing lint rules.
- No critical security scan warnings.

Production deployment must always be traceable to a commit.

---

## 13. Common Anti-Patterns to Avoid

Do not:

- Place business logic in React components.
- Access DB directly from Django views.
- Trust frontend authorization.
- Use global mutable state for tenant context.
- Introduce circular dependencies.
- Modify architecture without documentation.

If something feels convenient but bypasses rules, it is probably wrong.

---

## 14. When to Write an ADR

Write an ADR when:

- Changing multi-tenancy strategy.
- Changing database engine.
- Changing authentication method.
- Introducing a new major dependency.
- Modifying versioning model.
- Changing CI/CD flow significantly.

Architectural changes must be documented.

---

## 15. How to Ask for Help

If unsure:

- Reference the relevant architecture document.
- Explain which layer you think the change belongs to.
- Propose an approach aligned with documentation.
- Request review before large refactoring.

Clarity is preferred over speed.

---

## 16. Definition of Done

A feature is considered done when:

- Architecture respected.
- Multi-tenancy enforced.
- Authentication and authorization validated.
- Tests added and passing.
- CI pipeline green.
- Documentation updated (if needed).

---

## 17. Final Reminder

This system is:

- Multi-tenant
- Security-sensitive
- Architecturally structured
- Designed for long-term scalability

Discipline and consistency are more important than speed.

Every change must preserve:

- Tenant isolation
- Layer separation
- Security boundaries
- Testability
- Observability

Architecture is a shared responsibility.