# Operational Prompt Execution Sequence

## 1. Purpose

This document defines the official execution sequence
for all operational STEPs in this repository.

It standardizes:

- Planner invocation
- Implementer execution
- Reviewer validation
- Handoff behavior
- Governance compliance

This document MUST be followed for every STEP.

---

## 2. Universal Execution Pattern

Every STEP must follow this sequence:

1. Planner
2. Implementer
3. Manual Execution (if required)
4. Reviewer
5. Approval or Rework

Skipping any phase is a governance violation.

---

## 3. STEP-00 — Development Environment

### Planner

Invoke:

@planner Plan docs/prompts/operational/step-00/STEP-00-dev-environment-prompt.md

Expected Output:
- Structured execution plan
- Ordered checklist
- Tool validation instructions
- DoD alignment

---

### Implementer

Invoke:

@implementer Execute the approved plan for STEP-00.

Expected Output:
- Execution checklist
- Dependency verification
- Tooling validation confirmation
- DoD self-assessment

Manual execution may be required for:
- Virtual environment creation
- pip installations

---

### Reviewer

Invoke:

Handoff to @reviewer

Review the execution of STEP-00 according to:
- docs/operations/step-00/STEP-00-dev-environment.md
- Definition of Done — STEP-00
- Prompt Governance Convention

Validate only STEP-00 responsibilities.
Ignore repository structure validation.

Expected Output:
- Executive Summary
- DoD compliance check
- Risk classification
- Final verdict

---

## 4. STEP-01 — Monorepo Bootstrap

### Planner

Invoke:

@planner Plan docs/prompts/operational/step-01/STEP-01-bootstrap-prompt.md

Expected Output:
- Repository structure plan
- Layering enforcement strategy
- ADR alignment mapping
- Validation plan

---

### Implementer

Invoke:

@implementer Execute the approved plan for STEP-01.

Expected Output:
- Created directory structure
- Django project bootstrap
- Layer separation confirmation
- Static analysis results
- DoD self-assessment

---

### Reviewer

Invoke:

Handoff to @reviewer

Review the execution of STEP-01 according to:
- docs/operations/step-01/STEP-01-monorepo-bootstrap.md
- Definition of Done — STEP-01
- ADR-001
- ADR-002
- ADR-009
- ADR-014

Expected Output:
- Executive Summary
- ADR Compliance Check
- Layering Validation
- Static Analysis Validation
- DoD Compliance
- Risk Classification
- Final Verdict

---

## 5. Generic Template for Any STEP-XX

For any new STEP:

### Planner

@planner Plan <path-to-operational-prompt.md>

---

### Implementer

@implementer Execute the approved plan for STEP-XX.

---

### Reviewer

Handoff to @reviewer

Review the execution of STEP-XX according to:
- <path-to-step-document.md>
- Definition of Done — STEP-XX
- Relevant ADRs
- Prompt Governance Convention

Produce structured review output.

---

## 6. Mandatory Rules

1. Every STEP must have:
   - An operational document
   - A prompt document
   - A Definition of Done section
   - A matrix registration entry

2. Planner never writes production code.

3. Implementer must always include:
   - DoD self-assessment section

4. Reviewer must always produce:
   - Executive Summary
   - ADR compliance check
   - DoD compliance check
   - Risk classification (P1 / P2)
   - Final approval status

5. If a STEP lacks a Definition of Done,
   the Reviewer must reject it immediately.

---

## 7. Risk Classification

P1 — Blocking Issue  
- Architectural violation  
- ADR violation  
- DoD failure  

P2 — Non-blocking Improvement  
- Tooling optimization  
- Documentation refinement  
- Optional enhancement  

---

## 8. Evolution Rule

When introducing a new STEP:

- Add it to STEP-RESPONSIBILITY-MATRIX.md
- Create its operational document
- Create its prompt document
- Define its Definition of Done
- Register it in this sequence document

A STEP not listed here is unofficial.