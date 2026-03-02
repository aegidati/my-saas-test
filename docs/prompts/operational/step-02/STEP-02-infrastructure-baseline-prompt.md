# STEP-02 — Infrastructure Baseline
## Operational Prompt for Planner Agent

This document is a controlled operational prompt.

It MUST be used with the Planner Agent.

The Planner MUST:

- Respect all ADRs (001–020).
- Respect the Agentic Workflow Playbook.
- Respect Definition of Done — STEP-02.
- Avoid introducing business logic.
- Avoid modifying unrelated layers.

This STEP concerns backend runtime infrastructure only.

---

## 1. Mandatory Context to Read

Before generating the plan, you MUST read:

- docs/operations/step-02/STEP-02-infrastructure-baseline.md
- docs/adr/ (ADR-001 through ADR-020)
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md
- docs/operations/STEP-RESPONSIBILITY-MATRIX.md
- docs/governance/DEFINITION-OF-DONE-TEMPLATE.md

If any required file is missing, stop and report it.

---

## 2. Objective

Plan the execution of STEP-02.

Goals:

- Establish clean settings separation (base/dev/prod).
- Configure PostgreSQL for production (ADR-002).
- Ensure secrets are environment-based (ADR-014).
- Introduce minimal logging baseline.
- Introduce `/health/` endpoint.
- Prepare backend runtime for STEP-03 and STEP-04.

This STEP MUST NOT:

- Introduce domain logic.
- Introduce business features.
- Implement authentication flows.
- Modify frontend.

---

## 3. Required Output Structure

Your output MUST include:

### 3.1 Current State Assessment

- Inspect backend structure.
- Inspect current settings.
- Identify missing infrastructure components.

### 3.2 Infrastructure Plan

Provide a step-by-step implementation plan:

- Settings structure.
- Database configuration.
- Secret management.
- Logging baseline.
- Health endpoint wiring.

### 3.3 Risk & ADR Compliance

- Explain how plan complies with:
  - ADR-002
  - ADR-014
  - ADR-019
  - ADR-016

- Identify potential misconfiguration risks.

### 3.4 Validation Plan

Explain how Definition of Done — STEP-02 will be validated.

---

## 4. Constraints

- Changes limited to backend infrastructure.
- No business/domain logic.
- No cross-layer violations.
- No hardcoded secrets.

---

## 5. Implementer Handoff (Mandatory)

Provide:

- Ordered implementation steps.
- Clear file-level targets.
- Confirmation that no feature logic is introduced.
- Reminder to validate mypy, flake8, and test run.

---

## 6. Invocation Pattern

Invoke as:

@planner Plan docs/prompts/operational/step-02/STEP-02-infrastructure-baseline-prompt.md