# STEP-05 — Repository & Service Pattern Foundation
## Operational Prompt for Planner Agent

This document is a controlled operational prompt.

It MUST be used with the Planner Agent.

The Planner MUST:

- Respect all ADRs (001–020).
- Respect the Agentic Workflow Playbook.
- Respect Definition of Done — STEP-05.
- Preserve strict layering discipline.
- Avoid introducing business feature logic.

This STEP formalizes repository abstractions and the application service layer.

---

## 1. Mandatory Context to Read

Before generating the plan, you MUST read:

- docs/operations/step-05/STEP-05-repository-service-foundation.md
- docs/operations/step-04/STEP-04-multi-tenant-infrastructure.md
- docs/operations/step-03/STEP-03-authentication-skeleton.md
- docs/operations/step-02/STEP-02-infrastructure-baseline.md
- docs/adr/ (ADR-001 through ADR-020)
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md
- docs/operations/STEP-RESPONSIBILITY-MATRIX.md
- docs/governance/DEFINITION-OF-DONE-TEMPLATE.md

If any required file is missing, stop and report it.

---

## 2. Objective

Plan the execution of STEP-05.

Goals:

- Define repository interfaces outside infrastructure.
- Implement repository concrete classes inside infrastructure.
- Introduce Application Service layer (use-case layer).
- Enforce dependency direction:
  domain ← application ← infrastructure ← interfaces.
- Remove direct ORM access from interfaces or application layers.
- Provide at least one clean vertical slice example.

This STEP MUST NOT:

- Introduce new business features.
- Modify tenant logic beyond enforcement usage.
- Introduce RBAC or advanced authorization.
- Modify frontend/mobile.

---

## 3. Required Output Structure

Your output MUST include:

### 3.1 Current State Assessment

- Inspect domain, application, infrastructure, interfaces folders.
- Identify any direct ORM usage outside infrastructure.
- Identify missing repository abstractions.
- Identify current service layer (if any).

### 3.2 Repository Architecture Plan

Provide a structured plan covering:

- Repository interface placement:
  - Suggested folder.
  - Naming conventions.
- Repository interface definitions:
  - UserRepository.
  - TenantRepository.
  - TenantScopedRepository (integration with STEP-04).
- Concrete implementations:
  - File placement in infrastructure.
  - ORM model integration.
- Guardrails against cross-layer ORM imports.

### 3.3 Application Service Layer Plan

Define:

- Application service folder structure.
- Example service (vertical slice):
  - Interfaces → Application Service → Repository → ORM.
- Clear separation of:
  - Business orchestration.
  - Data access.
  - Presentation logic.

### 3.4 ADR Compliance & Risk Analysis

Explicitly explain compliance with:

- ADR-001 (tenant enforcement).
- ADR-002 (DB abstraction).
- ADR-015 (error handling at service boundary).
- ADR-016 (testability of services).
- ADR-017 (dependency direction).
- ADR-020 (style & static checks).

Identify risks such as:

- Circular dependencies.
- Leakage of ORM into application.
- Hidden coupling.

### 3.5 Validation Plan

Explain how Definition of Done — STEP-05 will be validated:

- Structural review of dependency direction.
- Static analysis (mypy).
- Lint check (flake8).
- Refactoring confirmation that interfaces no longer access ORM directly.

---

## 4. Constraints

- No circular imports allowed.
- No ORM imports in domain/application.
- No business feature introduction.
- No breaking of tenant enforcement.
- No cross-layer shortcuts.

---

## 5. Implementer Handoff (Mandatory)

Provide:

- Ordered implementation steps.
- File-by-file refactoring strategy.
- Explicit repository interface signatures.
- Clear layering boundary explanation.
- Reminder to:
  - Refactor `/auth/me` to use Application Service.
  - Run mypy.
  - Run flake8.
  - Run pytest.

---

## 6. Invocation Pattern

Invoke as:

@planner Plan docs/prompts/operational/step-05/STEP-05-repository-service-foundation-prompt.md