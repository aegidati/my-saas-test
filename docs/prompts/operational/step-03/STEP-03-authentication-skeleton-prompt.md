# STEP-03 — Authentication Skeleton
## Operational Prompt for Planner Agent

This document is a controlled operational prompt.

It MUST be used with the Planner Agent.

The Planner MUST:

- Respect all ADRs (001–020).
- Respect the Agentic Workflow Playbook.
- Respect Definition of Done — STEP-03.
- Avoid introducing business-specific authentication flows.
- Avoid modifying unrelated layers.

This STEP concerns authentication infrastructure only.

---

## 1. Mandatory Context to Read

Before generating the plan, you MUST read:

- docs/operations/step-03/STEP-03-authentication-skeleton.md
- docs/operations/step-02/STEP-02-infrastructure-baseline.md
- docs/operations/step-04/STEP-04-multi-tenant-infrastructure.md (for compatibility awareness)
- docs/adr/ (ADR-001 through ADR-020)
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md
- docs/operations/STEP-RESPONSIBILITY-MATRIX.md
- docs/governance/DEFINITION-OF-DONE-TEMPLATE.md

If any required file is missing, stop and report it.

---

## 2. Objective

Plan the execution of STEP-03.

Goals:

- Introduce JWT infrastructure using RS256 (ADR-003).
- Implement key loading compliant with ADR-014.
- Add authentication middleware.
- Introduce `/api/v1/auth/me/` endpoint.
- Ensure error handling follows ADR-015.
- Ensure compatibility with future tenant resolution (STEP-04).

This STEP MUST NOT:

- Implement full login/registration UX.
- Implement RBAC.
- Introduce tenant onboarding logic.
- Modify frontend/mobile layers.

---

## 3. Required Output Structure

Your output MUST include:

### 3.1 Current State Assessment

- Inspect user model situation.
- Inspect existing authentication logic (if any).
- Inspect settings for key configuration.

### 3.2 Authentication Infrastructure Plan

Provide a structured plan covering:

- User model confirmation or creation.
- JWT utility module:
  - Issuing tokens.
  - Validating tokens.
  - RS256 implementation.
  - `kid` header usage.
- Key management:
  - Environment-based loading.
  - Rotation-friendly structure.
- Middleware implementation:
  - Parsing Authorization header.
  - Attaching authenticated principal to request.
- `/api/v1/auth/me/` endpoint design.

### 3.3 ADR Compliance & Risk Analysis

Explicitly explain compliance with:

- ADR-003 (RS256, key rotation).
- ADR-014 (no hardcoded secrets).
- ADR-015 (error format).
- ADR-016 (testing requirements).
- ADR-019 (no secret logging).

Identify potential risks such as:

- Improper key loading.
- Logging sensitive data.
- Incorrect error responses.

### 3.4 Validation Plan

Explain how Definition of Done — STEP-03 will be validated:

- Unit tests.
- Integration tests.
- Static checks.
- Manual smoke test.

---

## 4. Constraints

- No business logic.
- No RBAC.
- No tenant resolution logic (only compatibility).
- No hardcoded keys.
- No logging of token contents.

---

## 5. Implementer Handoff (Mandatory)

Provide:

- Ordered implementation steps.
- Exact module/file placement suggestions.
- Clear separation of:
  - Domain
  - Application
  - Infrastructure
  - Interfaces
- Explicit reminder:
  - Run mypy.
  - Run flake8.
  - Add unit & integration tests.

---

## 6. Invocation Pattern

Invoke as:

@planner Plan docs/prompts/operational/step-03/STEP-03-authentication-skeleton-prompt.md