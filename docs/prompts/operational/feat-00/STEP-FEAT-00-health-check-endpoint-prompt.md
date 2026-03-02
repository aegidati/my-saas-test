# STEP-FEAT-00 — Health Check Endpoint — Planner Prompt

## Role

You are the Planner Agent.

Your task is to design the execution plan for STEP-FEAT-00 — Health Check Endpoint in the generated project repository.

You must strictly follow ADR authority and governance rules.

---

## Mandatory Context

You MUST read and respect:

- docs/operations/feat-00/STEP-FEAT-00-health-check-endpoint.md
- docs/operations/step-01/STEP-01-monorepo-bootstrap.md
- docs/operations/step-06/STEP-06-testing-infrastructure.md
- docs/adr/ADR-001-multi-tenancy.md
- docs/adr/ADR-002-database-engine.md
- docs/adr/ADR-015-error-exception-handling-strategy.md
- docs/adr/ADR-016-testing-strategy.md
- docs/adr/ADR-019-observability-logging-contract.md
- docs/adr/ADR-020-code-style-governance.md
- docs/adr/ADR-INDEX.md
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md
- docs/prompts/governance/PROMPT-GOVERNANCE-CONVENTION.md

ADR documents are the primary authority.

---

## Goal

Produce a precise, implementable plan to introduce a minimal health check endpoint that:

- Respects layered architecture.
- Respects all ADR constraints.
- Fully satisfies the Definition of Done in the STEP document.

You must NOT modify files. You only produce the plan.

---

## Required Plan Structure

Your output MUST contain exactly these sections:

## 1. Context Summary
- Summary of STEP purpose.
- Relevant ADRs and why they matter.
- Constraints derived from existing backend structure.

## 2. Target Behavior
- Final endpoint URL.
- Allowed HTTP methods.
- JSON response structure.
- Authentication behavior (explicitly state unauthenticated).

## 3. File-Level Change Plan
For each file:
- Full relative path.
- Whether it is new or modified.
- Precise description of changes.
- Explanation of layering compliance.

## 4. Testing Plan
- Location of test files.
- Exact test scenarios.
- How tests align with ADR-016.

## 5. Static Checks & Quality Gates
- Commands to run:
  - pytest
  - mypy
  - flake8
- Any additional checks required by ADR-020.

## 6. Risk & Impact Assessment
- Potential risks (layering mistakes, logging issues).
- Why this STEP is low-risk.

## 7. Implementer Handoff Checklist
Provide a numbered checklist the Implementer must follow, including:
- Create/modify files.
- Add tests.
- Run static checks.
- Self-assess against Definition of Done.
- Confirm no ADR-level decision introduced.

---

## Constraints

- Do not invent new architecture rules.
- Do not assume components that do not exist.
- Adapt paths to the actual repository structure.
- Keep the plan minimal and precise.