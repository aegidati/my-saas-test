# STEP-01A — Documentation Alignment (Architecture ↔ ADR)
## Operational Prompt for Planner Agent

This document is a self-contained operational prompt.

It MUST be used with the Planner Agent.

The Planner MUST:

- Produce a structured execution plan.
- Respect all ADRs (001–020).
- Respect the Agentic Workflow Playbook.
- Respect the Definition of Done defined in STEP-01A.
- Avoid modifying runtime code.
- Avoid introducing new architectural decisions.

This STEP is documentation-only.

---

## 1. Mandatory Context to Read

Before generating the plan, you MUST read:

- docs/operations/step-01/STEP-01A-documentation-alignment.md
- docs/adr/ (all ADR-001 through ADR-020)
- docs/architecture/ (all files)
- docs/governance/DEFINITION-OF-DONE-TEMPLATE.md
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md
- docs/operations/STEP-RESPONSIBILITY-MATRIX.md

If any required file is missing, stop and report it.

---

## 2. Objective

Plan the execution of STEP-01A.

Goal:

- Align docs/architecture/ with docs/adr/.
- Remove duplicated normative statements.
- Ensure that all decisions live exclusively in ADRs.
- Ensure that architecture docs focus on implementation guidance only.
- Add “Related ADRs” section to every architecture file.

This STEP MUST NOT:

- Modify backend/ frontend/ packages/
- Change runtime behavior
- Alter ADR decisions
- Introduce new policy-level rules

---

## 3. Required Output Structure

Your output MUST follow this structure.

### 3.1 Current State Assessment

- List all files under docs/architecture/.
- Identify:
  - Normative statements.
  - Potential duplicated policy content.
  - Missing "Related ADRs" sections.

### 3.2 Refactoring Plan

Provide a file-by-file plan:

For each architecture file:

- ADRs to reference.
- Normative statements to remove or rewrite.
- References to add.
- Sections to restructure (if needed).

The plan MUST:

- Preserve semantic meaning.
- Not weaken ADR authority.
- Avoid introducing new decisions.

### 3.3 Risk Analysis

- Identify any hidden architectural decisions not covered by ADRs.
- Flag potential conflicts between architecture docs and ADRs.
- Highlight ambiguous terminology.

### 3.4 Validation Plan

Describe how compliance with STEP-01A Definition of Done will be verified.

Explicitly reference:

- No duplicated normative rules.
- ADR authority preserved.
- No runtime code modified.
- Scope integrity maintained.

---

## 4. Constraints

You MUST:

- Keep all changes strictly within docs/.
- Preserve ADR wording.
- Avoid semantic drift.
- Avoid restructuring unrelated documentation.
- Not modify Agent definitions.

If you discover a true missing decision:

- Flag it explicitly.
- Do NOT create a new ADR in this STEP.
- Propose it as a follow-up action.

---

## 5. Implementer Handoff Section (Mandatory)

At the end of your output, include a clear:

### Implementer Handoff

Provide:

- Summary of changes to apply.
- Ordered list of documentation edits.
- Explicit confirmation that runtime code is untouched.
- Reminder to verify Definition of Done — STEP-01A.

---

## 6. Invocation Pattern

This prompt MUST be invoked as:

@planner Plan docs/prompts/operational/step-01/STEP-01A-documentation-alignment-prompt.md

No additional instructions are required.