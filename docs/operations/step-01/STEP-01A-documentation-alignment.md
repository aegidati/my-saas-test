# STEP-01A — Documentation Alignment (Architecture ↔ ADR, SAFE MODE)

## 1. Purpose

This STEP ensures a **safe** and **incremental** alignment between:

- docs/adr/
- docs/architecture/

The objective is to:

- Gradually eliminate duplication between ADRs and architecture documents.
- Ensure that architectural decisions live in ADRs.
- Ensure that architecture documents focus on implementation guidance only.
- Do this **without any risk to source code** or non-documentation assets.

This STEP is designed to be **SAFE MODE**:

- It MUST NOT touch anything outside `docs/`.
- It SHOULD be executed **file-by-file**, not as a global bulk refactor.
- It assumes that the human developer keeps control of the actual edits.

---

## 2. Scope

### 2.1 In Scope

- Only files under:

  - `docs/architecture/`
  - `docs/adr/` (read-only, for reference)

- Activities:

  - Adding “Related ADRs” sections to architecture docs.
  - Rewriting duplicated normative sentences in architecture docs to reference ADRs instead.
  - Clarifying that ADRs are the single source of truth for decisions.

### 2.2 Out of Scope (SAFE MODE HARD LIMIT)

This STEP MUST NOT:

- Modify any file outside `docs/`.
- Modify or delete any ADR file content.
- Rename, move or delete any file under `docs/`.
- Change repository structure.
- Change any runtime behavior (backend, frontend, packages, tools, .github).

If any plan or suggestion conflicts with these constraints, it MUST be rejected.

---

## 3. SAFE MODE Execution Model

This STEP is intentionally designed to be executed in a **controlled, manual** way.

### 3.1 Planner Agent Role

The Planner Agent MUST:

1. Work at the level of **documentation analysis only**.
2. Produce:
   - A list of files under `docs/architecture/`.
   - For each file:
     - The **probable Related ADRs**.
     - A list of **normative statements** that look like decisions (MUST / MUST NOT / ALWAYS / NEVER).
3. Propose **per-file edits**, not a global repo-wide refactor.
4. Explicitly state:
   - “These changes MUST be applied manually by the developer.”
   - “The Implementer MUST NOT be allowed to apply bulk changes across the repo.”

The Planner MUST NOT suggest:

- Editing `backend/`, `frontend/`, `packages/`, `tools/`, `.github/`.
- Deleting or renaming files.
- Changing ADR texts.

---

### 3.2 Implementer Agent Role (SAFE MODE)

The Implementer Agent is **optional** for this STEP.

If used, it MUST follow these rules:

- It can be invoked **only on a single file at a time**, with an explicit path, for example:

  > “@implementer Refactor `docs/architecture/authentication.md` according to the approved STEP-01A plan, but only this file.”

- It MUST:

  - Limit suggestions to the specified file.
  - Only adjust text (no deletes/moves of files).
  - Preserve all content that is not explicitly part of the alignment.

- It MUST NOT:

  - Touch any file outside `docs/architecture/`.
  - Modify ADRs.
  - Propose repository-wide refactors.

**Recommended usage:**  
For this STEP, the developer SHOULD primarily:

- Use the Planner to obtain a checklist and suggestions.
- Apply modifications manually in the editor.
- Use the Implementer only for small, clearly scoped refactors in a single open file.

---

### 3.3 Reviewer Agent Role

The Reviewer Agent MUST:

- Validate only documentation-related changes.
- Verify that:

  - No files outside `docs/` were modified.
  - ADR contents are unchanged.
  - Each modified architecture file:
    - Has a “Related ADRs” section.
    - No longer redefines decisions that already live in ADRs.
    - Still provides useful implementation guidance.

- Explicitly check for scope violations:
  - Any touched file outside `docs/` is a **FAIL** for STEP-01A SAFE MODE.

---

## 4. Alignment Rules (Simplified for SAFE MODE)

### Rule 1 — Decisions Stay in ADRs

- Any sentence in `docs/architecture/` that defines a hard rule (MUST / MUST NOT / ALWAYS / NEVER) SHOULD be checked:
  - If an ADR already defines that rule → the architecture doc SHOULD refer to that ADR instead of restating the rule as a new decision.
  - If no ADR exists → flag this in a note, but DO NOT create or modify ADRs in this STEP.

### Rule 2 — Architecture Docs Explain “How”

- `docs/architecture/` SHOULD focus on:
  - Folder structures.
  - Examples and patterns.
  - Code/config snippets.
  - Practical application of ADR rules.

### Rule 3 — Related ADRs Section

- Each architecture file SHOULD have a heading near the top:

  ```md
  Related ADRs:
  - ADR-0xx — ...
  - ADR-0yy — ...