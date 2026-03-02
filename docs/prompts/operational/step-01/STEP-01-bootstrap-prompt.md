# STEP-01 — Monorepo Bootstrap (Operational Prompt)

## Agent: Planner

This document is a self-contained operational manifest.

When invoked by the Planner Agent, you MUST:

1. Read all required context files listed below.
2. Produce a structured execution plan.
3. NOT generate implementation code.
4. Respect all architectural invariants and ADRs.
5. Prepare a Reviewer checklist.
6. Prepare for structured handoff to Implementer.

---

# 1. Required Context (MANDATORY READ)

Before generating the plan, you MUST read:

- docs/operations/step-01/STEP-01-monorepo-bootstrap.md
- docs/prompts/governance/PROMPT-GOVERNANCE-CONVENTION.md
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md
- docs/adr/ADR-001-multi-tenancy.md
- docs/adr/ADR-002-database-engine.md
- docs/adr/ADR-009-horizontal-scaling-and-load-balancing-strategy.md

If any of these files are missing, explicitly state it.

Do NOT proceed without loading context.

---

# 2. Objective

Initialize the structural foundation of the monorepo:

- Django backend bootstrap
- Strict layered structure
- Multi-tenant ready foundation
- Stateless-ready architecture
- Governance-compliant structure

This step establishes structure only.

No business logic.
No infrastructure integrations.
No authentication.
No background jobs.

---

# 3. Architectural Invariants (NON-NEGOTIABLE)

You MUST enforce:

## Layering

- backend/domain MUST NOT import Django, ORM, infrastructure, or interfaces.
- backend/infrastructure MAY depend on domain.
- backend/interfaces MUST NOT contain business logic.
- backend/application orchestrates use cases only.
- No circular dependencies.

## Multi-Tenancy (ADR-001)

- Structure must allow future tenant-aware repositories.
- No global mutable state.
- No cross-tenant assumptions.

## Database Strategy (ADR-002)

- PostgreSQL is production engine.
- Django ORM is abstraction.
- For bootstrap, default SQLite is acceptable.
- SQLite usage in this step is a temporary bootstrap exception and not production compliant with ADR-002.
- No engine-specific logic outside infrastructure.

## Horizontal Scaling (ADR-009)

- Stateless web discipline.
- No in-memory session reliance.
- No process-level business state.

## Secrets (ADR-014)

- No secrets.
- No API keys.
- No hardcoded credentials.
- No JWT keys.
- In development, SECRET_KEY may be generated at runtime for convenience.
- Production always requires explicit environment configuration.

Authority follows the documented hierarchy: ADR > Definition of Done > Prompt Governance Convention > Operations > Architecture > Operational prompts > Snapshots.

---

# 4. Expected Output Structure (MANDATORY FORMAT)

You MUST produce the plan using this exact structure:

## 1. Architectural Overview

Explain how STEP-01 fits into the architecture and ADRs.

## 2. Execution Steps

Numbered, ordered list of implementation actions.

## 3. Layer Impact Analysis

Describe impact on:

- Domain
- Application
- Infrastructure
- Interfaces
- Settings

## 4. Risks & Mitigations

Identify architectural risks and mitigation strategies.

## 5. Non-Goals

Explicitly list what will NOT be implemented in STEP-01.

## 6. Reviewer Checklist

Produce a strict checklist covering:

- Layer violations
- Tenant isolation
- Secret exposure
- Stateless discipline
- Circular dependencies

---

# 5. Handoff Preparation

At the end of the plan, include:

## Implementer Handoff Block

Summarize:

- Active ADR constraints
- Non-goals
- Validation commands to run
- Scope boundaries

Do NOT implement anything.

The next step must be:
Planner → Implementer (via structured handoff).

---

# 6. Invocation Pattern

This prompt is designed to be invoked as:

@planner Plan docs/prompts/operational/step-01/STEP-01-bootstrap-prompt.md

It must work without additional instructions.

---

# 7. Enforcement Clause

If the requested action conflicts with:

- Any ADR
- Prompt Governance Convention
- Agentic Workflow Playbook

You MUST:

1. Explicitly highlight the conflict.
2. Refuse unsafe planning.
3. Propose an ADR-compliant alternative.

---

# End of STEP-01 Operational Prompt