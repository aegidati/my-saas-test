# STEP-04 — Multi-Tenant Infrastructure Layer
## Operational Prompt for Planner Agent

This document is a controlled operational prompt.

It MUST be used with the Planner Agent.

The Planner MUST:

- Respect all ADRs (001–020).
- Respect the Agentic Workflow Playbook.
- Respect Definition of Done — STEP-04.
- Preserve strict tenant isolation.
- Avoid introducing business-specific tenant features.

This STEP concerns multi-tenant infrastructure only.

---

## 1. Mandatory Context to Read

Before generating the plan, you MUST read:

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

Plan the execution of STEP-04.

Goals:

- Introduce canonical `Tenant` model.
- Implement tenant resolution middleware.
- Introduce explicit TenantContext propagation.
- Implement tenant-aware repository base class.
- Enforce row-level isolation (ADR-001).
- Prevent cross-tenant data access.

This STEP MUST NOT:

- Implement tenant onboarding flows.
- Implement billing, quotas, invitations.
- Introduce RBAC logic.
- Modify frontend/mobile.
- Introduce global tenant state.

---

## 3. Required Output Structure

Your output MUST include:

### 3.1 Current State Assessment

- Inspect existing models.
- Inspect repository structure (from STEP-05 preparation).
- Inspect authentication context compatibility.
- Identify any existing tenant-related assumptions.

### 3.2 Multi-Tenant Infrastructure Plan

Provide a structured plan covering:

- Tenant model design:
  - Fields.
  - Indexing.
  - Uniqueness constraints.
- Tenant resolution strategy:
  - Source of tenant identifier (header, subdomain, path, etc.).
  - Error behavior for missing/invalid tenant.
- Middleware:
  - Order in middleware stack.
  - Attaching tenant to request context.
- TenantContext object definition.
- TenantScopedRepository base class:
  - Required methods.
  - Enforcement patterns.
  - Guardrails against cross-tenant queries.

### 3.3 ADR Compliance & Risk Analysis

Explicitly explain compliance with:

- ADR-001 (strict tenant isolation).
- ADR-002 (PostgreSQL compatibility).
- ADR-015 (error format for invalid tenant).
- ADR-016 (testability).
- ADR-019 (tenant_id logging discipline).

Identify potential risks such as:

- Accidental cross-tenant queries.
- Hidden global state.
- Incorrect middleware ordering.

### 3.4 Validation Plan

Explain how Definition of Done — STEP-04 will be validated:

- Unit tests for tenant resolution.
- Integration tests for tenant isolation.
- Repository enforcement tests.
- Static checks (mypy, flake8).

---

## 4. Constraints

- No global tenant variable.
- TenantContext must be explicit.
- All tenant-scoped queries must require tenant_id.
- No business tenant features.
- No cross-layer violations.

---

## 5. Implementer Handoff (Mandatory)

Provide:

- Ordered implementation steps.
- Exact module/file placement guidance.
- Explicit repository enforcement strategy.
- Clear layering boundaries.
- Reminder to:
  - Add isolation tests.
  - Run mypy.
  - Run flake8.
  - Run pytest.

---

## 6. Invocation Pattern

Invoke as:

@planner Plan docs/prompts/operational/step-04/STEP-04-multi-tenant-infrastructure-prompt.md