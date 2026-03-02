# WORKFLOW CONTEXT SNAPSHOT

## 1. Purpose

This document tracks the operational state of a project generated from the AgenticDev template.

It must be updated in the generated repository to reflect:
- Completed STEPs
- Completed Feature STEPs
- Governance validation state
- Current implementation focus

This file is intentionally initialized in a neutral state inside the template.

---

## 2. Repository Context

### Template Source
AgenticDev Template

### Generated Project
[Project name to be inserted]

---

## 3. Architectural Governance Status

### ADR Inventory
- ADR-001 … ADR-021 present in template.

### Authority Hierarchy

1. ADR documents (source of truth)
2. Definition of Done
3. Prompt Governance Convention
4. STEP operational documents and operations playbooks
5. Architecture documents
6. Operational prompts
7. Snapshots

No document may override an ADR.

Governance status:
- Initial state (to be validated in generated project).

---

## 4. Operational STEPs Status

Validation Step:
- STEP-FEAT-00 — Mandatory technical validation (ADR-021) ⬜ Not executed

### Environment & Bootstrap

- STEP-00 — Dev Environment Setup ⬜ Not executed
- STEP-01 — Monorepo Bootstrap ⬜ Not executed
- STEP-01A — Documentation Alignment ⬜ Not executed
- STEP-02 — Infrastructure Baseline ⬜ Not executed
- STEP-03 — Authentication Skeleton ⬜ Not executed
- STEP-04 — Multi-Tenant Infrastructure ⬜ Not executed
- STEP-05 — Repository & Service Foundation ⬜ Not executed
- STEP-06 — Testing Infrastructure ⬜ Not executed

---

## 5. Feature STEPs

None defined yet.

---

## 6. Current Focus

Initial state.

Next action:
- Execute STEP-00 and STEP-01 in generated project.

---

## 7. Quality & Tooling

Static analysis tools defined in template:
- mypy
- flake8

Testing framework defined in template:
- pytest

To be activated in generated project.

---

## 8. Update Instructions

When using this template to create a new repository:

1. Rename or keep this file as WORKFLOW-CONTEXT-SNAPSHOT.md.
2. Insert project name.
3. Update STEP execution status after each completed STEP.
4. Record governance validation state.
5. Track feature evolution.

---

## 9. Governance

ADR-021 enforces mandatory validation (STEP-FEAT-00) before business feature work.

---

Last updated:
Template baseline version