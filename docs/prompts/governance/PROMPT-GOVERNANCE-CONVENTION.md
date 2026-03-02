# PROMPT GOVERNANCE CONVENTION

## 1. Purpose

This document defines the mandatory governance rules for:

- Writing operational prompts
- Using Planner / Implementer / Reviewer agents
- Performing structured handoffs
- Preventing architectural drift
- Ensuring compliance with ADRs and Definition of Done

This document is normative.

All operational prompts and agent executions MUST comply with this convention.

---

## 2. Prompt Categories

Prompts are divided into two categories:

### 2.1 Governance Prompts

Location:
docs/prompts/governance/

Purpose:
- Define rules for writing prompts
- Define workflow discipline
- Define authority hierarchy
- Define anti-drift mechanisms

These documents are normative and override operational prompts in case of conflict.

---

### 2.2 Operational Prompts

Location:
docs/prompts/operational/<step-or-feature>/

Purpose:
- Execute STEP-XX
- Execute STEP-FEAT-XX
- Guide Planner Agent behavior

Each operational prompt MUST:

- Reference its corresponding STEP document
- Reference all relevant ADRs
- Include constraints
- Include validation plan
- Include explicit Implementer handoff instructions

---

## 3. Agent Roles (Authoritative Definition)

### 3.1 Planner Agent

The Planner MUST:

- Read all required documents before planning
- Produce a structured plan
- Identify risks
- Confirm ADR compliance
- Define validation strategy
- Not implement code
- Not skip test planning

Planner output MUST include:

1. Current state assessment
2. Step-by-step execution plan
3. ADR compliance analysis
4. Risk assessment
5. Validation plan
6. Implementer handoff instructions

Planner cannot override ADR decisions.

---

### 3.2 Implementer Agent

The Implementer MUST:

- Follow the approved plan strictly
- Respect layering discipline
- Not introduce new features
- Not alter architecture outside the approved scope
- Explicitly declare compliance with:
  - ADRs
  - Definition of Done
  - Layering rules

Implementer MUST:

- Run mypy
- Run flake8
- Run pytest
- Add required tests

Implementer output MUST include:

1. Summary of changes
2. Files modified
3. Definition of Done self-evaluation
4. Static check results
5. Test results summary

---

### 3.3 Reviewer Agent

The Reviewer MUST validate against:

- STEP Definition of Done
- All referenced ADRs
- Prompt Governance Convention
- Layering discipline
- Security invariants
- Testing completeness

Reviewer MUST reject if:

- Tenant isolation is broken
- Layering is violated
- Secrets are hardcoded
- Cross-layer shortcuts are introduced
- Static checks are skipped
- Tests are missing

Reviewer output MUST include:

1. Executive summary
2. ADR compliance assessment
3. Security validation
4. Layering validation
5. Test coverage validation
6. Required fixes (if any)

Reviewer has authority to reject.

---

## 4. Mandatory Operational Prompt Structure

Every operational prompt MUST contain:

1. Purpose
2. Mandatory context to read
3. Objective
4. Required output structure
5. Constraints
6. Implementer handoff
7. Invocation pattern

No operational prompt may omit these sections.

---

## 5. Handoff Rules

Every handoff MUST explicitly state:

- Which agent receives control
- Which STEP is being reviewed or implemented
- Which Definition of Done applies
- Which ADRs are relevant
- That Prompt Governance Convention is binding

Example:

Handoff to @reviewer

Review according to:
- docs/operations/step-04/STEP-04-multi-tenant-infrastructure.md
- Definition of Done — STEP-04
- ADR-001, ADR-002, ADR-015
- Prompt Governance Convention

---

## 6. Anti-Drift Rules

The following are strictly forbidden:

- Hardcoded secrets
- Global tenant state
- Direct ORM access from presentation layer
- Cross-layer shortcuts
- Skipping tests
- Skipping static checks
- Introducing business logic in infrastructure
- Violating dependency direction

Any violation requires rejection and correction cycle.

---

## 7. Static Quality Enforcement

For every significant STEP:

The following MUST be executed:

- mypy
- flake8
- pytest

No STEP is considered DONE without these checks passing.

---

## 8. Authority Hierarchy

When conflict exists:

1. ADR documents override everything
2. Definition of Done overrides STEP description
3. Prompt Governance overrides operational prompt interpretation
4. Planner cannot override ADR
5. Implementer cannot override Planner
6. Reviewer cannot override ADR

---

This document is binding and normative.