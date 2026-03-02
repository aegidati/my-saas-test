# ADR-021 — Project Initialization & Validation Policy

## Status
Accepted

## Context

The AgenticDev template defines a complete ADR-driven architectural and governance model.

When a new project repository is generated from the template, there is a critical need to:

- Validate that the architectural structure is operational.
- Confirm that the backend wiring works correctly.
- Verify that testing and static analysis infrastructure are functional.
- Ensure that the Planner → Implementer → Reviewer workflow is executable end-to-end.
- Prevent business feature development from starting on an unvalidated structural base.

Without a formal validation step, projects risk introducing business complexity before confirming architectural integrity.

---

## Decision

Every project generated from the AgenticDev template MUST execute a minimal technical validation feature before starting business features.

This validation is defined as:

STEP-FEAT-00 — Health Check Endpoint

The purpose of STEP-FEAT-00 is to validate:

- Interface layer routing
- Layer isolation (no domain leakage)
- Testing infrastructure (pytest)
- Static analysis (mypy, flake8)
- ADR compliance enforcement
- Agentic workflow reliability

No business logic is introduced in STEP-FEAT-00.

Business feature development (FEAT-01+) MUST NOT begin until:

1. STEP-00 (environment) is completed.
2. STEP-01 (monorepo bootstrap) is completed.
3. STEP-FEAT-00 is successfully implemented and reviewed.
4. Definition of Done is satisfied.
5. No P1 governance issues remain.

---

## Scope

This ADR applies to:

- All repositories generated from the AgenticDev template.
- All production or real development projects derived from the template.

This ADR does NOT apply to:

- Template-only structural validation.
- Documentation-only test repositories.

---

## Consequences

### Positive

- Architectural integrity is validated early.
- Reduces risk of hidden infrastructure defects.
- Standardizes project initialization.
- Improves auditability and governance clarity.
- Enforces discipline before feature complexity increases.

### Negative

- Adds one mandatory step before business feature work.
- Slightly increases initial setup time.

---

## Enforcement

The Agentic Workflow Playbook and Definition of Done must reference this ADR.

Reviewer Agents must verify compliance with ADR-021 before approving the first business feature.

Failure to implement STEP-FEAT-00 before business features constitutes a governance violation.

---

## Related ADRs

- ADR-001 — Multi-Tenancy Isolation Strategy
- ADR-002 — Database Engine Strategy
- ADR-016 — Testing Strategy
- ADR-019 — Observability & Logging Contract
- ADR-020 — Code Style & Formatting Governance

---

## Notes

STEP-FEAT-00 is a technical validation mechanism, not a business feature.

Future revisions may define alternative validation features, but a validation step will always remain mandatory.